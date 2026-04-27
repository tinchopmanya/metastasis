#!/usr/bin/env python3
"""External paired scRNA validation using GSE245552.

GSE245552 contains matched primary CRC and liver metastasis samples from
multiple patients. This script downloads split 10x files, extracts only genes
needed for the CRLM layered-niche model, and computes lightweight sample-level
and compartment-proxy summaries.

This is not spatial validation. It is a paired single-cell pressure test:
does the SPP1/CXCL12-lite and tumor metabolic arm appear stronger in liver
metastasis than in matched primary tumor, and in which coarse cell proxies?
"""

from __future__ import annotations

import argparse
import csv
import gzip
import math
import re
import ssl
import time
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"
DEFAULT_RAW_DIR = DEFAULT_OUT_DIR / "gse245552_raw"
DEFAULT_SIGNATURES = DEFAULT_OUT_DIR / "signatures_normalized.tsv"
GSE = "GSE245552"
SERIES_PREFIX = "GSE245nnn"
FILELIST_URL = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{SERIES_PREFIX}/{GSE}/suppl/filelist.txt"
SOFT_URL = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{SERIES_PREFIX}/{GSE}/soft/{GSE}_family.soft.gz"
SAMPLE_BASE_URL = "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM7844nnn"


SELECTED_SIGNATURES = [
    "caf_core",
    "caf_core_desoverlap_2026",
    "mcam_caf",
    "spp1_cxcl12_caf_myeloid_axis",
    "spp1_cxcl12_axis_desoverlap_2026",
    "hla_drb5_macrophage_axis",
    "hla_drb5_macrophage_axis_desoverlap_2026",
    "myc_glycolysis_core",
    "myc_glycolysis_desoverlap_2026",
    "glut1_invasive_margin_axis",
    "crlm_metabolic_vulnerabilities_2026",
]

MARKER_SETS = {
    "tumor_epithelial_proxy": ["EPCAM", "KRT8", "KRT18", "KRT19", "KRT20", "CEACAM5"],
    "caf_proxy": ["COL1A1", "COL1A2", "ACTA2", "FAP", "POSTN", "PDGFRA"],
    "myeloid_proxy": ["PTPRC", "LYZ", "LST1", "CD68", "CD14", "FCGR3A", "MS4A7", "AIF1"],
    "tcell_proxy": ["CD3D", "CD3E", "CD4", "CD8A", "CD8B", "CXCL13", "TOX"],
}

CORE_GENES = [
    "HGF",
    "MET",
    "MYC",
    "SPP1",
    "CXCL12",
    "CD44",
    "MIF",
    "FN1",
    "HLA-DRB5",
    "CD74",
    "CXCR4",
    "LGALS9",
    "PTPRC",
    "CD8A",
    "TOX",
    "GZMB",
    "PRF1",
    "SLC2A1",
    "SHMT1",
    "NDRG1",
    "MORF4L1",
    "MARCO",
    "EPCAM",
    "KRT8",
    "KRT18",
    "KRT19",
    "KRT20",
    "CEACAM5",
    "LYZ",
    "LST1",
    "CD68",
    "CD14",
    "FCGR3A",
    "MS4A7",
    "AIF1",
    "COL1A1",
    "COL1A2",
    "ACTA2",
    "FAP",
    "POSTN",
    "PDGFRA",
    "MCAM",
]


def get_url(url: str, attempts: int = 4) -> bytes:
    ctx = ssl.create_default_context()
    request = urllib.request.Request(url, headers={"User-Agent": "metastasis-research/0.1"})
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=900, context=ctx) as response:
                return response.read()
        except Exception as exc:  # noqa: BLE001 - keep script dependency-free.
            last_error = exc
            time.sleep(3 * attempt)
    raise RuntimeError(f"Failed to fetch {url}") from last_error


def download_file(url: str, out_path: Path) -> None:
    if out_path.exists() and out_path.stat().st_size > 1024:
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp_path.write_bytes(get_url(url))
    if tmp_path.stat().st_size <= 1024:
        tmp_path.unlink(missing_ok=True)
        raise OSError(f"Downloaded file is unexpectedly small: {out_path}")
    tmp_path.replace(out_path)


def parse_filelist(text: str) -> dict[str, dict[str, str]]:
    files: dict[str, dict[str, str]] = {}
    reader = csv.DictReader(text.splitlines(), delimiter="\t")
    for row in reader:
        if row.get("#Archive/File") != "File":
            continue
        name = row["Name"]
        if "_barcodes.tsv.gz" not in name and "_features.tsv.gz" not in name and "_matrix.mtx.gz" not in name:
            continue
        prefix = name.rsplit("_", 1)[0]
        kind = name.rsplit("_", 1)[1].replace(".tsv.gz", "").replace(".mtx.gz", "")
        files.setdefault(prefix, {})[kind] = f"{SAMPLE_BASE_URL}/{prefix.split('_', 1)[0]}/suppl/{name}"
    return files


def parse_soft(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for block in text.split("\n^SAMPLE = ")[1:]:
        gsm = block.split("\n", 1)[0].strip()
        title = re.search(r"!Sample_title = (.*)", block)
        source = re.search(r"!Sample_source_name_ch1 = (.*)", block)
        tissue = re.search(r"!Sample_characteristics_ch1 = tissue: (.*)", block)
        if not title or not source or not tissue:
            continue
        sample_code = title.group(1).split(",", 1)[0]
        patient = sample_code.split("_", 1)[0]
        rows.append({
            "gsm": gsm,
            "sample_code": sample_code,
            "patient": patient,
            "source": source.group(1),
            "tissue": tissue.group(1),
            "file_prefix": f"{gsm}_{sample_code}",
        })
    return rows


def read_signatures(path: Path) -> dict[str, list[str]]:
    signatures: dict[str, list[str]] = defaultdict(list)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            signature = row["signature_id"]
            if signature in SELECTED_SIGNATURES:
                signatures[signature].append(row["gene_symbol"].upper())
    for name, genes in MARKER_SETS.items():
        signatures[name] = [gene.upper() for gene in genes]
    return dict(signatures)


def read_barcodes(path: Path) -> list[str]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def read_features(path: Path, target_genes: set[str]) -> dict[int, str]:
    row_to_gene: dict[int, str] = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for idx, line in enumerate(handle, start=1):
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            symbol = parts[1].upper()
            if symbol in target_genes:
                row_to_gene[idx] = symbol
    return row_to_gene


def extract_counts(matrix_path: Path, n_cells: int, row_to_gene: dict[int, str]) -> dict[str, list[float]]:
    values: dict[str, list[float]] = {gene: [0.0] * n_cells for gene in set(row_to_gene.values())}
    with gzip.open(matrix_path, "rt", encoding="utf-8") as handle:
        dims_seen = False
        for line in handle:
            if line.startswith("%"):
                continue
            if not dims_seen:
                dims_seen = True
                continue
            row_idx, col_idx, raw_value = line.strip().split()
            row = int(row_idx)
            if row not in row_to_gene:
                continue
            col = int(col_idx) - 1
            values[row_to_gene[row]][col] += float(raw_value)
    return values


def mean(values: list[float]) -> float:
    valid = [value for value in values if not math.isnan(value)]
    return sum(valid) / len(valid) if valid else float("nan")


def score_cells(log_values: dict[str, list[float]], genes: list[str], n_cells: int) -> list[float]:
    present = [gene for gene in genes if gene in log_values]
    if not present:
        return [float("nan")] * n_cells
    return [mean([log_values[gene][idx] for gene in present]) for idx in range(n_cells)]


def normal_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def mann_whitney(group_a: list[float], group_b: list[float]) -> tuple[float, float]:
    a = [v for v in group_a if not math.isnan(v)]
    b = [v for v in group_b if not math.isnan(v)]
    n1, n2 = len(a), len(b)
    if n1 == 0 or n2 == 0:
        return float("nan"), float("nan")
    combined = [(v, 0) for v in a] + [(v, 1) for v in b]
    combined.sort(key=lambda item: item[0])
    ranks = [0.0] * len(combined)
    i = 0
    while i < len(combined):
        j = i + 1
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        rank = (i + 1 + j) / 2
        for k in range(i, j):
            ranks[k] = rank
        i = j
    rank_sum_a = sum(rank for rank, (_, group) in zip(ranks, combined) if group == 0)
    u1 = rank_sum_a - n1 * (n1 + 1) / 2
    mean_u = n1 * n2 / 2
    sd_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if sd_u == 0:
        return float("nan"), float("nan")
    z = (u1 - mean_u) / sd_u
    p = 2 * (1 - normal_cdf(abs(z)))
    delta = (2 * u1 / (n1 * n2)) - 1
    return max(p, 1e-300), delta


def sign_test_p(positive: int, total: int) -> float:
    if total == 0:
        return float("nan")
    k = min(positive, total - positive)
    prob = sum(math.comb(total, i) for i in range(0, k + 1)) / (2 ** total)
    return min(1.0, 2 * prob)


def summarize_sample(
    meta: dict[str, str],
    paths: dict[str, Path],
    signatures: dict[str, list[str]],
    target_genes: set[str],
) -> dict[str, str | int | float]:
    barcodes = read_barcodes(paths["barcodes"])
    n_cells = len(barcodes)
    row_to_gene = read_features(paths["features"], target_genes)
    counts = extract_counts(paths["matrix"], n_cells, row_to_gene)
    log_values = {
        gene: [math.log1p(value) for value in cell_values]
        for gene, cell_values in counts.items()
    }

    scores = {
        signature: score_cells(log_values, genes, n_cells)
        for signature, genes in signatures.items()
    }
    compartment_names = ["tumor_epithelial_proxy", "caf_proxy", "myeloid_proxy", "tcell_proxy"]
    compartments: dict[str, list[int]] = {name: [] for name in compartment_names}
    for idx in range(n_cells):
        marker_values = {name: scores[name][idx] for name in compartment_names}
        best_name, best_value = max(marker_values.items(), key=lambda item: -1 if math.isnan(item[1]) else item[1])
        if not math.isnan(best_value) and best_value > 0:
            compartments[best_name].append(idx)

    row: dict[str, str | int | float] = {
        "sample": meta["sample_code"],
        "gsm": meta["gsm"],
        "patient": meta["patient"],
        "tissue": meta["tissue"],
        "n_cells": n_cells,
        "n_target_genes_present": len(row_to_gene),
    }
    for gene in sorted(target_genes):
        if gene in log_values:
            row[f"gene_{gene}"] = mean(log_values[gene])
            row[f"pct_{gene}"] = sum(1 for value in log_values[gene] if value > 0) / n_cells
        else:
            row[f"gene_{gene}"] = float("nan")
            row[f"pct_{gene}"] = float("nan")

    for signature, cell_scores in scores.items():
        row[f"score_{signature}"] = mean(cell_scores)
        present = [gene for gene in signatures[signature] if gene in log_values]
        row[f"n_{signature}_genes"] = len(present)

    for compartment, indices in compartments.items():
        row[f"fraction_{compartment}"] = len(indices) / n_cells if n_cells else float("nan")

    compartment_metrics = {
        "tumor_epithelial_proxy": [
            "myc_glycolysis_desoverlap_2026",
            "myc_glycolysis_core",
            "glut1_invasive_margin_axis",
        ],
        "caf_proxy": [
            "spp1_cxcl12_axis_desoverlap_2026",
            "spp1_cxcl12_caf_myeloid_axis",
        ],
        "myeloid_proxy": [
            "hla_drb5_macrophage_axis_desoverlap_2026",
            "hla_drb5_macrophage_axis",
            "spp1_cxcl12_axis_desoverlap_2026",
        ],
        "tcell_proxy": [
            "tcell_proxy",
            "glut1_invasive_margin_axis",
        ],
    }
    for compartment, metric_names in compartment_metrics.items():
        indices = compartments[compartment]
        for metric in metric_names:
            values = scores[metric]
            selected = [values[idx] for idx in indices]
            row[f"{compartment}__score_{metric}"] = mean(selected)

    return row


def tissue_comparisons(rows: list[dict[str, str | int | float]]) -> list[dict[str, str | int | float]]:
    metrics = [key for key in rows[0] if key.startswith("score_") or key.startswith("fraction_") or "__score_" in key]
    results: list[dict[str, str | int | float]] = []
    for metric in sorted(metrics):
        lm = [float(row[metric]) for row in rows if row["tissue"] == "liver metastasis"]
        primary = [float(row[metric]) for row in rows if row["tissue"] == "primary tumor"]
        adjacent = [float(row[metric]) for row in rows if "adjacent" in str(row["tissue"])]
        p, delta = mann_whitney(lm, primary)
        lm_mean = mean(lm)
        primary_mean = mean(primary)
        results.append({
            "metric": metric,
            "n_lm": len(lm),
            "n_primary": len(primary),
            "n_adjacent": len(adjacent),
            "mean_lm": lm_mean,
            "mean_primary": primary_mean,
            "mean_adjacent": mean(adjacent),
            "lm_minus_primary": lm_mean - primary_mean,
            "lm_over_primary": lm_mean / primary_mean if primary_mean and not math.isnan(primary_mean) else float("nan"),
            "mann_whitney_p_lm_vs_primary": p,
            "rank_delta_lm_vs_primary": delta,
        })
    return results


def paired_deltas(rows: list[dict[str, str | int | float]]) -> list[dict[str, str | int | float]]:
    metrics = [key for key in rows[0] if key.startswith("score_") or key.startswith("fraction_") or "__score_" in key]
    by_patient_tissue: dict[tuple[str, str], list[dict[str, str | int | float]]] = defaultdict(list)
    for row in rows:
        if row["tissue"] in {"primary tumor", "liver metastasis"}:
            by_patient_tissue[(str(row["patient"]), str(row["tissue"]))].append(row)

    patient_means: dict[tuple[str, str], dict[str, float]] = {}
    for key, sample_rows in by_patient_tissue.items():
        patient_means[key] = {
            metric: mean([float(row[metric]) for row in sample_rows])
            for metric in metrics
        }

    results: list[dict[str, str | int | float]] = []
    patients = sorted({patient for patient, _ in patient_means})
    for metric in sorted(metrics):
        deltas: list[float] = []
        used_patients: list[str] = []
        for patient in patients:
            primary = patient_means.get((patient, "primary tumor"))
            lm = patient_means.get((patient, "liver metastasis"))
            if not primary or not lm:
                continue
            delta = lm[metric] - primary[metric]
            if math.isnan(delta):
                continue
            deltas.append(delta)
            used_patients.append(patient)
        positive = sum(1 for delta in deltas if delta > 0)
        results.append({
            "metric": metric,
            "n_pairs": len(deltas),
            "mean_lm_minus_primary": mean(deltas),
            "positive_pairs": positive,
            "negative_pairs": sum(1 for delta in deltas if delta < 0),
            "zero_pairs": sum(1 for delta in deltas if delta == 0),
            "sign_test_p": sign_test_p(positive, len(deltas)),
            "patients": ",".join(used_patients),
        })
    return results


def write_tsv(rows: list[dict[str, str | int | float]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: object, digits: int = 3) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return "NA"
        return f"{value:.{digits}f}"
    return str(value)


def write_report(
    manifest: list[dict[str, str]],
    rows: list[dict[str, str | int | float]],
    comparisons: list[dict[str, str | int | float]],
    deltas: list[dict[str, str | int | float]],
    out_path: Path,
) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    comp = {str(row["metric"]): row for row in comparisons}
    paired = {str(row["metric"]): row for row in deltas}
    priority = [
        "score_spp1_cxcl12_axis_desoverlap_2026",
        "score_spp1_cxcl12_caf_myeloid_axis",
        "score_myc_glycolysis_desoverlap_2026",
        "score_hla_drb5_macrophage_axis_desoverlap_2026",
        "score_caf_core_desoverlap_2026",
        "fraction_caf_proxy",
        "fraction_myeloid_proxy",
        "fraction_tumor_epithelial_proxy",
        "caf_proxy__score_spp1_cxcl12_axis_desoverlap_2026",
        "myeloid_proxy__score_spp1_cxcl12_axis_desoverlap_2026",
        "tumor_epithelial_proxy__score_myc_glycolysis_desoverlap_2026",
        "myeloid_proxy__score_hla_drb5_macrophage_axis_desoverlap_2026",
    ]
    lines = [
        "# GSE245552 paired scRNA external validation",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "",
        "Pressure-test whether the 2026 `CAF/SPP1-CXCL12/metabolic` macro-niche has support in an independent paired primary CRC/liver-metastasis scRNA cohort.",
        "",
        "## Dataset",
        "",
        f"- Samples in GEO metadata: {len(manifest)}.",
        f"- Processed samples: {len(rows)}.",
        "- Tissues include primary tumor, liver metastasis, colon adjacent tissue, and liver adjacent tissue.",
        "- This is not spatial; it is a paired single-cell sample/compartment-proxy validation.",
        "",
        "## Key LM vs Primary Comparisons",
        "",
        "| Metric | LM mean | Primary mean | LM-primary | LM/primary | p | Rank delta | Paired mean delta | Positive pairs | Sign p |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for metric in priority:
        if metric not in comp:
            continue
        row = comp[metric]
        paired_row = paired.get(metric, {})
        lines.append(
            f"| `{metric}` | {fmt(row['mean_lm'])} | {fmt(row['mean_primary'])} | "
            f"{fmt(row['lm_minus_primary'])} | {fmt(row['lm_over_primary'])} | "
            f"{float(row['mann_whitney_p_lm_vs_primary']):.2e} | {fmt(row['rank_delta_lm_vs_primary'])} | "
            f"{fmt(paired_row.get('mean_lm_minus_primary', float('nan')))} | "
            f"{paired_row.get('positive_pairs', 'NA')}/{paired_row.get('n_pairs', 'NA')} | "
            f"{fmt(paired_row.get('sign_test_p', float('nan')))} |"
        )

    spp1_lite = comp.get("score_spp1_cxcl12_axis_desoverlap_2026", {})
    tumor_lite = comp.get("score_myc_glycolysis_desoverlap_2026", {})
    hla_lite = comp.get("score_hla_drb5_macrophage_axis_desoverlap_2026", {})
    caf_proxy = comp.get("caf_proxy__score_spp1_cxcl12_axis_desoverlap_2026", {})
    myeloid_spp1_proxy = comp.get("myeloid_proxy__score_spp1_cxcl12_axis_desoverlap_2026", {})
    tumor_proxy = comp.get("tumor_epithelial_proxy__score_myc_glycolysis_desoverlap_2026", {})
    myeloid_proxy = comp.get("myeloid_proxy__score_hla_drb5_macrophage_axis_desoverlap_2026", {})

    lines.extend([
        "",
        "## Interpretation",
        "",
        f"- Whole-sample `SPP1/CXCL12-lite` LM/primary ratio: {fmt(spp1_lite.get('lm_over_primary', float('nan')))}.",
        f"- Whole-sample `MYC/glycolysis-lite` LM/primary ratio: {fmt(tumor_lite.get('lm_over_primary', float('nan')))}.",
        f"- Whole-sample `HLA-DRB5-lite` LM/primary ratio: {fmt(hla_lite.get('lm_over_primary', float('nan')))}.",
        f"- CAF-proxy `SPP1/CXCL12-lite` LM/primary ratio: {fmt(caf_proxy.get('lm_over_primary', float('nan')))}.",
        f"- Myeloid-proxy `SPP1/CXCL12-lite` LM/primary ratio: {fmt(myeloid_spp1_proxy.get('lm_over_primary', float('nan')))}.",
        f"- Tumor-proxy `MYC/glycolysis-lite` LM/primary ratio: {fmt(tumor_proxy.get('lm_over_primary', float('nan')))}.",
        f"- Myeloid-proxy `HLA-DRB5-lite` LM/primary ratio: {fmt(myeloid_proxy.get('lm_over_primary', float('nan')))}.",
        "",
        "## Caveats",
        "",
        "- Coarse cell proxies are marker-based, not curated annotations.",
        "- Expression is computed from raw 10x counts with log1p summaries, not full scRNA normalization/integration.",
        "- This validates sample/cell-state pressure, not spatial adjacency.",
        "- Strong positive results here would motivate a paper-grade integrated analysis; weak results would push the claim back toward spatial specificity.",
        "",
    ])
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--signatures", type=Path, default=DEFAULT_SIGNATURES)
    parser.add_argument("--limit-samples", type=int, default=0)
    args = parser.parse_args()

    filelist_text = get_url(FILELIST_URL).decode("utf-8", errors="replace")
    soft_text = gzip.decompress(get_url(SOFT_URL)).decode("utf-8", errors="replace")
    files = parse_filelist(filelist_text)
    manifest = parse_soft(soft_text)
    if args.limit_samples:
        manifest = manifest[:args.limit_samples]

    signatures = read_signatures(args.signatures)
    target_genes = set(CORE_GENES)
    for genes in signatures.values():
        target_genes.update(genes)

    sample_rows: list[dict[str, str | int | float]] = []
    for meta in manifest:
        prefix = meta["file_prefix"]
        if prefix not in files:
            print(f"[{meta['sample_code']}] missing split 10x files, skipping", flush=True)
            continue
        paths = {
            "barcodes": args.raw_dir / f"{prefix}_barcodes.tsv.gz",
            "features": args.raw_dir / f"{prefix}_features.tsv.gz",
            "matrix": args.raw_dir / f"{prefix}_matrix.mtx.gz",
        }
        print(f"[{meta['sample_code']}] downloading/reading {meta['tissue']}...", flush=True)
        for kind, path in paths.items():
            download_file(files[prefix][kind], path)
        row = summarize_sample(meta, paths, signatures, target_genes)
        sample_rows.append(row)
        print(f"  cells: {row['n_cells']}; target genes present: {row['n_target_genes_present']}", flush=True)

    comparisons = tissue_comparisons(sample_rows)
    deltas = paired_deltas(sample_rows)
    write_tsv(manifest, args.out_dir / "gse245552_sample_manifest.tsv")
    write_tsv(sample_rows, args.out_dir / "gse245552_sample_signature_scores.tsv")
    write_tsv(comparisons, args.out_dir / "gse245552_lm_vs_primary_comparisons.tsv")
    write_tsv(deltas, args.out_dir / "gse245552_paired_deltas.tsv")
    write_report(manifest, sample_rows, comparisons, deltas, args.out_dir / "gse245552_external_validation_report.md")

    print(f"Samples processed: {len(sample_rows)}")
    print("Report: gse245552_external_validation_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
