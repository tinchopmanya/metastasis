#!/usr/bin/env python3
"""External CRLM validation screen using GSE234804 H5Seurat files.

GSE234804 provides moderate-sized H5Seurat files for CRC primary samples and
liver metastases (LM). This script downloads only the CRC and LM sample files,
extracts the active hypothesis genes from `/assays/RNA/data`, computes sample
level expression/signature summaries, and compares LM vs CRC.

This is not a spatial or cell-type-resolved validation because these H5Seurat
files do not expose rich cell annotations in `meta.data`. It is an external
sample-level CRLM plausibility screen.

Requires: h5py and numpy.
"""

from __future__ import annotations

import argparse
import csv
import math
import ssl
import time
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

try:
    import h5py
    import numpy as np
except ImportError as exc:  # pragma: no cover - runtime dependency message
    raise SystemExit("This script requires h5py and numpy. Install with: python -m pip install h5py") from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"
DEFAULT_RAW_DIR = DEFAULT_OUT_DIR / "gse234804_raw"
DEFAULT_FILELIST = DEFAULT_OUT_DIR / "geo_external_filelist.tsv"

TARGET_GENES = [
    "HGF",
    "MET",
    "MYC",
    "SLC2A1",
    "HK2",
    "PGK1",
    "TPI1",
    "LDHA",
    "ENO1",
    "MCAM",
    "COL1A1",
    "COL1A2",
    "FAP",
    "ACTA2",
    "POSTN",
    "PDGFRA",
    "PDGFRB",
    "EPCAM",
    "KRT20",
]

SIGNATURES = {
    "caf_core": ["COL1A1", "COL1A2", "ACTA2", "FAP", "POSTN", "PDGFRA", "PDGFRB"],
    "mcam_caf": ["MCAM", "COL1A1", "COL1A2", "ACTA2"],
    "hgf_met_axis": ["HGF", "MET"],
    "myc_glycolysis_core": ["MYC", "SLC2A1", "HK2", "PGK1", "TPI1", "LDHA", "ENO1"],
    "tumor_epithelial": ["EPCAM", "KRT20"],
}


def read_geo_filelist(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def selected_gse234804_files(filelist: list[dict[str, str]]) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for row in filelist:
        if row.get("accession") != "GSE234804":
            continue
        name = row.get("name", "")
        if not name.endswith(".h5seurat"):
            continue
        sample = name.split("_", 1)[1].replace("_new.h5seurat", "")
        if sample.startswith("CRC"):
            tissue = "CRC"
        elif sample.startswith("LM"):
            tissue = "LM"
        else:
            continue
        selected.append({
            "name": name,
            "sample": sample,
            "tissue": tissue,
            "url": row["url"],
            "size_bytes": row["size_bytes"],
        })
    return selected


def download_file(url: str, out_path: Path) -> None:
    if out_path.exists() and out_path.stat().st_size > 1024:
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context()
    request = urllib.request.Request(url, headers={"User-Agent": "metastasis-research/0.1"})
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    last_error: Exception | None = None
    for attempt in range(1, 5):
        try:
            with urllib.request.urlopen(request, timeout=900, context=ctx) as response:
                tmp_path.write_bytes(response.read())
            if tmp_path.stat().st_size <= 1024:
                raise OSError(f"Downloaded file is unexpectedly small: {tmp_path.stat().st_size} bytes")
            tmp_path.replace(out_path)
            return
        except Exception as exc:
            last_error = exc
            if tmp_path.exists():
                tmp_path.unlink()
            time.sleep(5 * attempt)
    raise RuntimeError(f"Failed to download {url}: {last_error}")


def decode_array(values) -> list[str]:
    decoded: list[str] = []
    for value in values:
        if isinstance(value, bytes):
            decoded.append(value.decode("utf-8", errors="replace"))
        else:
            decoded.append(str(value))
    return decoded


def mean(values: list[float]) -> float:
    valid = [v for v in values if not math.isnan(v)]
    return sum(valid) / len(valid) if valid else float("nan")


def std(values: list[float]) -> float:
    valid = [v for v in values if not math.isnan(v)]
    if len(valid) < 2:
        return float("nan")
    m = mean(valid)
    return math.sqrt(sum((v - m) ** 2 for v in valid) / (len(valid) - 1))


def normal_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def mann_whitney(group_a: list[float], group_b: list[float]) -> tuple[float, float]:
    """Return two-sided normal-approx p-value and rank delta for group_a vs group_b."""
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


def extract_sample(path: Path, sample: str, tissue: str) -> dict[str, str | float | int]:
    with h5py.File(path, "r") as handle:
        features = decode_array(handle["assays/RNA/features"][:])
        feature_to_idx = {gene.upper(): idx for idx, gene in enumerate(features)}
        data = handle["assays/RNA/data"]
        n_cells, n_genes = data.shape
        row: dict[str, str | float | int] = {
            "sample": sample,
            "tissue": tissue,
            "n_cells": int(n_cells),
            "n_genes": int(n_genes),
        }

        for gene in TARGET_GENES:
            idx = feature_to_idx.get(gene)
            if idx is None:
                row[gene] = float("nan")
                row[f"{gene}_pct_expr"] = float("nan")
                continue
            values = np.asarray(data[:, idx])
            row[gene] = float(np.mean(values))
            row[f"{gene}_pct_expr"] = float(np.mean(values > 0))

        for sig, genes in SIGNATURES.items():
            present = [float(row[gene]) for gene in genes if not math.isnan(float(row.get(gene, float("nan"))))]
            row[f"score_{sig}"] = mean(present)
            row[f"n_{sig}_genes"] = len(present)

        row["score_caf_met_myc_glycolysis_composite"] = mean([
            float(row["score_caf_core"]),
            float(row["score_mcam_caf"]),
            float(row["score_hgf_met_axis"]),
            float(row["score_myc_glycolysis_core"]),
        ])
        return row


def compare_lm_crc(sample_rows: list[dict[str, str | float | int]]) -> list[dict[str, str | float | int]]:
    metrics = [
        *TARGET_GENES,
        *[f"score_{name}" for name in SIGNATURES],
        "score_caf_met_myc_glycolysis_composite",
    ]
    results: list[dict[str, str | float | int]] = []
    for metric in metrics:
        lm = [float(row[metric]) for row in sample_rows if row["tissue"] == "LM"]
        crc = [float(row[metric]) for row in sample_rows if row["tissue"] == "CRC"]
        lm_mean = mean(lm)
        crc_mean = mean(crc)
        p, delta = mann_whitney(lm, crc)
        results.append({
            "metric": metric,
            "n_lm": len(lm),
            "n_crc": len(crc),
            "mean_lm": lm_mean,
            "mean_crc": crc_mean,
            "lm_minus_crc": lm_mean - crc_mean,
            "lm_over_crc": (lm_mean / crc_mean) if crc_mean and not math.isnan(crc_mean) else float("nan"),
            "mann_whitney_p": p,
            "rank_delta_lm_vs_crc": delta,
        })
    return results


def write_tsv(rows: list[dict[str, str | float | int]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: object, digits: int = 3) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return "NA"
        return f"{value:.{digits}f}"
    return str(value)


def write_report(
    sample_rows: list[dict[str, str | float | int]],
    comparisons: list[dict[str, str | float | int]],
    out_path: Path,
) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    priority = [
        "score_mcam_caf",
        "score_caf_core",
        "score_hgf_met_axis",
        "score_myc_glycolysis_core",
        "score_caf_met_myc_glycolysis_composite",
        "HGF",
        "MET",
        "MYC",
        "MCAM",
        "COL1A1",
        "PGK1",
        "TPI1",
    ]
    comp_by_metric = {str(row["metric"]): row for row in comparisons}
    caf_row = comp_by_metric["score_mcam_caf"]
    gly_row = comp_by_metric["score_myc_glycolysis_core"]
    met_row = comp_by_metric["MET"]
    hgf_row = comp_by_metric["HGF"]
    caf_direction = "higher" if float(caf_row["lm_minus_crc"]) > 0 else "lower"
    gly_direction = "higher" if float(gly_row["lm_minus_crc"]) > 0 else "lower"
    lines = [
        "# GSE234804 H5Seurat external validation screen",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "",
        "Test whether CRC liver metastasis samples in GSE234804 show sample-level enrichment of the active CAF/MCAM and MET-MYC-glycolysis signals compared with primary CRC samples.",
        "",
        "## Scope",
        "",
        "- Downloaded only individual `CRC*` and `LM*` H5Seurat files.",
        "- Excluded `PC*` samples from the first pass.",
        "- Used `/assays/RNA/data` mean expression per sample.",
        "- No cell-type labels were available in `meta.data`, so this is sample-level, not cell-type-resolved.",
        "",
        "## Samples",
        "",
        "| Sample | Tissue | Cells | Genes | CAF score | MCAM CAF | HGF-MET | MYC-glycolysis |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in sample_rows:
        lines.append(
            f"| {row['sample']} | {row['tissue']} | {row['n_cells']} | {row['n_genes']} | "
            f"{fmt(row['score_caf_core'])} | {fmt(row['score_mcam_caf'])} | "
            f"{fmt(row['score_hgf_met_axis'])} | {fmt(row['score_myc_glycolysis_core'])} |"
        )

    lines.extend([
        "",
        "## LM vs CRC Comparisons",
        "",
        "| Metric | LM mean | CRC mean | LM-CRC | LM/CRC | p | Rank delta |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for metric in priority:
        row = comp_by_metric[metric]
        lines.append(
            f"| `{metric}` | {fmt(row['mean_lm'])} | {fmt(row['mean_crc'])} | "
            f"{fmt(row['lm_minus_crc'])} | {fmt(row['lm_over_crc'])} | "
            f"{float(row['mann_whitney_p']):.2e} | {fmt(row['rank_delta_lm_vs_crc'])} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        f"- `score_mcam_caf` is {caf_direction} in LM than CRC at sample level (LM mean {fmt(caf_row['mean_lm'])}, CRC mean {fmt(caf_row['mean_crc'])}).",
        f"- `score_myc_glycolysis_core` is {gly_direction} in LM than CRC at sample level (LM mean {fmt(gly_row['mean_lm'])}, CRC mean {fmt(gly_row['mean_crc'])}).",
        f"- `MET` is modestly higher in LM (LM/CRC {fmt(met_row['lm_over_crc'])}), while `HGF` is nearly unchanged/very low (LM/CRC {fmt(hgf_row['lm_over_crc'])}).",
        "- This does not externally replicate the full `CAF-high -> MET/MYC/glycolysis` model as a simple sample-level LM-vs-CRC signature.",
        "- The negative result is still informative: it supports treating the hypothesis as spatial/cell-state-specific rather than as a universal bulk-like liver-metastasis signature.",
        "- Sample count is small and no cell-type labels were available, so this is a falsification pressure test, not a final rejection.",
        "",
    ])
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--filelist", type=Path, default=DEFAULT_FILELIST)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    filelist = read_geo_filelist(args.filelist)
    selected = selected_gse234804_files(filelist)
    if not selected:
        raise ValueError("No GSE234804 CRC/LM H5Seurat files found. Run triage_geo_external_validation.py first.")

    sample_rows: list[dict[str, str | float | int]] = []
    for item in selected:
        out_path = args.raw_dir / item["name"]
        print(f"[{item['sample']}] downloading/reading {item['name']}...", flush=True)
        download_file(item["url"], out_path)
        row = extract_sample(out_path, item["sample"], item["tissue"])
        sample_rows.append(row)
        print(f"  cells: {row['n_cells']}, genes: {row['n_genes']}", flush=True)

    comparisons = compare_lm_crc(sample_rows)
    write_tsv(sample_rows, args.out_dir / "gse234804_sample_signature_scores.tsv")
    write_tsv(comparisons, args.out_dir / "gse234804_lm_vs_crc_comparisons.tsv")
    write_report(sample_rows, comparisons, args.out_dir / "gse234804_external_validation_report.md")

    print(f"Samples: {len(sample_rows)}")
    print("Report: gse234804_external_validation_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
