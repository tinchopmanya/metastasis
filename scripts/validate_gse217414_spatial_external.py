#!/usr/bin/env python3
"""External spatial validation using GSE217414 CRLM Visium samples.

GSE217414 contains four 10x Visium sections from colorectal cancer liver
metastases. This script downloads only the filtered feature H5 matrices and
spatial coordinates, scores the 2026 layered-niche signatures, and tests
whether high-source spots have neighboring target programs above an in-sample
permutation null.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import math
import random
import ssl
import tarfile
import time
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import h5py


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"
DEFAULT_RAW_DIR = DEFAULT_OUT_DIR / "gse217414_spatial_raw"
DEFAULT_SIGNATURES = DEFAULT_OUT_DIR / "signatures_normalized.tsv"
GSE = "GSE217414"
SERIES_PREFIX = "GSE217nnn"
SAMPLE_BASE_URL = "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM6716nnn"
FILELIST_URL = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{SERIES_PREFIX}/{GSE}/suppl/filelist.txt"
SOFT_URL = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{SERIES_PREFIX}/{GSE}/soft/{GSE}_family.soft.gz"

SAMPLES = {
    "GSM6716963_19G081": {"patient": "Patient1", "sample": "19G081", "tissue": "CRLM"},
    "GSM6716964_19G0619": {"patient": "Patient2", "sample": "19G0619", "tissue": "CRLM"},
    "GSM6716965_19G0635": {"patient": "Patient3", "sample": "19G0635", "tissue": "CRLM"},
    "GSM6716966_19G02977": {"patient": "Patient4", "sample": "19G02977", "tissue": "CRLM"},
}

SELECTED_SIGNATURES = [
    "caf_core",
    "mcam_caf",
    "spp1_cxcl12_caf_myeloid_axis",
    "spp1_cxcl12_axis_desoverlap_2026",
    "hla_drb5_macrophage_axis",
    "hla_drb5_macrophage_axis_desoverlap_2026",
    "myc_glycolysis_core",
    "myc_glycolysis_desoverlap_2026",
    "glut1_invasive_margin_axis",
    "cxcl13_t_cells",
    "crlm_metabolic_vulnerabilities_2026",
]

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
    "SLC2A1",
    "SHMT1",
    "NDRG1",
    "MORF4L1",
    "MARCO",
]

HEX_NEIGHBOR_OFFSETS = [
    (0, 2),
    (0, -2),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]


def score_col(signature_id: str) -> str:
    return f"score_{signature_id}"


def get_url(url: str, attempts: int = 4) -> bytes:
    ctx = ssl.create_default_context()
    request = urllib.request.Request(url, headers={"User-Agent": "metastasis-research/0.1"})
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=900, context=ctx) as response:
                return response.read()
        except Exception as exc:  # noqa: BLE001 - dependency-free retry loop.
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
        if name.endswith("_filtered_feature_bc_matrix.h5"):
            prefix = name.replace("_filtered_feature_bc_matrix.h5", "")
            kind = "h5"
        elif name.endswith("_spatial.tar.gz"):
            prefix = name.replace("_spatial.tar.gz", "")
            kind = "spatial"
        else:
            continue
        gsm = prefix.split("_", 1)[0]
        files.setdefault(prefix, {})[kind] = f"{SAMPLE_BASE_URL}/{gsm}/suppl/{name}"
    return files


def read_signatures(path: Path) -> dict[str, list[str]]:
    signatures: dict[str, list[str]] = {signature_id: [] for signature_id in SELECTED_SIGNATURES}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            signature_id = row["signature_id"]
            if signature_id in signatures:
                signatures[signature_id].append(row["gene_symbol"].upper())
    return {key: genes for key, genes in signatures.items() if genes}


def decode(value: bytes | str) -> str:
    return value.decode("utf-8") if isinstance(value, bytes) else str(value)


def read_h5_log_values(path: Path, target_genes: set[str]) -> tuple[list[str], dict[str, list[float]], set[str]]:
    with h5py.File(path, "r") as handle:
        matrix = handle["matrix"]
        barcodes = [decode(value) for value in matrix["barcodes"][:]]
        feature_names = [decode(value).upper() for value in matrix["features"]["name"][:]]
        target_rows = {
            idx: gene
            for idx, gene in enumerate(feature_names)
            if gene in target_genes
        }
        values: dict[str, list[float]] = {
            gene: [0.0] * len(barcodes)
            for gene in set(target_rows.values())
        }
        data = matrix["data"][:]
        indices = matrix["indices"][:]
        indptr = matrix["indptr"][:]
        for col_idx in range(len(barcodes)):
            start = int(indptr[col_idx])
            end = int(indptr[col_idx + 1])
            for row_idx, raw_value in zip(indices[start:end], data[start:end]):
                gene = target_rows.get(int(row_idx))
                if gene:
                    values[gene][col_idx] += float(raw_value)
    log_values = {
        gene: [math.log1p(value) for value in cell_values]
        for gene, cell_values in values.items()
    }
    return barcodes, log_values, set(values)


def read_positions_from_tar(path: Path) -> dict[str, dict[str, str]]:
    with tarfile.open(path, "r:gz") as archive:
        members = [
            member for member in archive.getmembers()
            if member.name.endswith("tissue_positions_list.csv") or member.name.endswith("tissue_positions.csv")
        ]
        if not members:
            raise FileNotFoundError(f"No tissue positions file found in {path}")
        extracted = archive.extractfile(members[0])
        if extracted is None:
            raise FileNotFoundError(f"Could not extract positions from {path}")
        text = extracted.read().decode("utf-8")

    rows = list(csv.reader(text.splitlines()))
    if not rows:
        return {}
    has_header = rows[0] and rows[0][0].lower() in {"barcode", "barcodes"}
    data_rows = rows[1:] if has_header else rows
    positions: dict[str, dict[str, str]] = {}
    for row in data_rows:
        if len(row) < 4:
            continue
        positions[row[0]] = {
            "barcode": row[0],
            "in_tissue": row[1],
            "array_row": row[2],
            "array_col": row[3],
        }
    return positions


def valid_mean(values: list[float]) -> float:
    valid = [value for value in values if not math.isnan(value)]
    return sum(valid) / len(valid) if valid else float("nan")


def percentile(values: list[float], pct: float) -> float:
    valid = sorted(value for value in values if not math.isnan(value))
    if not valid:
        return float("nan")
    idx = int(round((len(valid) - 1) * pct))
    return valid[max(0, min(idx, len(valid) - 1))]


def pearson(xs: list[float], ys: list[float]) -> tuple[float, int]:
    pairs = [(x, y) for x, y in zip(xs, ys) if not math.isnan(x) and not math.isnan(y)]
    n = len(pairs)
    if n < 3:
        return float("nan"), n
    mx = sum(x for x, _ in pairs) / n
    my = sum(y for _, y in pairs) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x, _ in pairs))
    sy = math.sqrt(sum((y - my) ** 2 for _, y in pairs))
    if sx == 0 or sy == 0:
        return float("nan"), n
    cov = sum((x - mx) * (y - my) for x, y in pairs)
    return cov / (sx * sy), n


def ratio_for_indices(values: list[float], neighbor_idxs: set[int], background_idxs: set[int]) -> tuple[float, float, float]:
    neighbor_mean = valid_mean([values[idx] for idx in neighbor_idxs])
    background_mean = valid_mean([values[idx] for idx in background_idxs])
    ratio = (
        neighbor_mean / background_mean
        if background_mean and not math.isnan(background_mean)
        else float("nan")
    )
    return neighbor_mean, background_mean, ratio


def stable_seed(seed: int, label: str) -> int:
    value = seed
    for idx, char in enumerate(label, start=1):
        value += idx * ord(char)
    return value


def fmt(value: object, digits: int = 3) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return "NA"
        return f"{value:.{digits}f}"
    return str(value)


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


def build_spot_rows(
    sample_id: str,
    paths: dict[str, Path],
    target_genes: set[str],
    signatures: dict[str, list[str]],
) -> tuple[list[dict[str, str | float]], dict[str, list[str]]]:
    barcodes, log_values, present_genes = read_h5_log_values(paths["h5"], target_genes)
    barcode_to_idx = {barcode: idx for idx, barcode in enumerate(barcodes)}
    positions = read_positions_from_tar(paths["spatial"])
    usable_signature_genes = {
        signature_id: [gene for gene in genes if gene in present_genes]
        for signature_id, genes in signatures.items()
    }
    info = SAMPLES[sample_id]

    rows: list[dict[str, str | float]] = []
    for barcode in barcodes:
        pos = positions.get(barcode)
        if not pos or pos["in_tissue"] != "1":
            continue
        idx = barcode_to_idx[barcode]
        row: dict[str, str | float] = {
            "sample_id": sample_id,
            "sample": info["sample"],
            "patient": info["patient"],
            "tissue": info["tissue"],
            "barcode": barcode,
            "array_row": pos["array_row"],
            "array_col": pos["array_col"],
        }
        for gene in sorted(target_genes):
            row[gene] = log_values[gene][idx] if gene in log_values else float("nan")
        for signature_id, genes in usable_signature_genes.items():
            row[score_col(signature_id)] = valid_mean([float(row[gene]) for gene in genes])
        rows.append(row)
    return rows, usable_signature_genes


def adjacency_regions(
    sample_rows: list[dict[str, str | float]],
    source: str,
) -> tuple[float, set[int], set[int], set[int]]:
    coord_to_idx: dict[tuple[int, int], int] = {}
    for idx, row in enumerate(sample_rows):
        coord_to_idx[(int(row["array_row"]), int(row["array_col"]))] = idx

    source_values = [float(row[source]) for row in sample_rows]
    threshold = percentile(source_values, 0.75)
    high_idxs = {
        idx for idx, row in enumerate(sample_rows)
        if not math.isnan(float(row[source])) and float(row[source]) >= threshold and float(row[source]) > 0
    }
    neighbor_idxs: set[int] = set()
    for idx in high_idxs:
        row = sample_rows[idx]
        coord = (int(row["array_row"]), int(row["array_col"]))
        for dr, dc in HEX_NEIGHBOR_OFFSETS:
            neighbor = coord_to_idx.get((coord[0] + dr, coord[1] + dc))
            if neighbor is not None and neighbor not in high_idxs:
                neighbor_idxs.add(neighbor)
    background_idxs = {
        idx for idx in range(len(sample_rows))
        if idx not in high_idxs and idx not in neighbor_idxs
    }
    return threshold, high_idxs, neighbor_idxs, background_idxs


def compute_correlations(
    rows: list[dict[str, str | float]],
    pairs: list[tuple[str, str]],
) -> list[dict[str, str | float]]:
    results: list[dict[str, str | float]] = []
    by_sample: dict[str, list[dict[str, str | float]]] = defaultdict(list)
    for row in rows:
        by_sample[str(row["sample_id"])].append(row)
    for sample_id, sample_rows in sorted(by_sample.items()):
        for x_name, y_name in pairs:
            xs = [float(row[x_name]) for row in sample_rows]
            ys = [float(row[y_name]) for row in sample_rows]
            r, n = pearson(xs, ys)
            results.append({
                "sample_id": sample_id,
                "sample": str(sample_rows[0]["sample"]),
                "x": x_name,
                "y": y_name,
                "pearson_r": r,
                "n_spots": n,
            })
    return results


def compute_adjacency_permutations(
    rows: list[dict[str, str | float]],
    sources: list[str],
    targets: list[str],
    permutations: int,
    seed: int,
) -> list[dict[str, str | float]]:
    results: list[dict[str, str | float]] = []
    by_sample: dict[str, list[dict[str, str | float]]] = defaultdict(list)
    for row in rows:
        by_sample[str(row["sample_id"])].append(row)

    for sample_id, sample_rows in sorted(by_sample.items()):
        for source in sources:
            threshold, high_idxs, neighbor_idxs, background_idxs = adjacency_regions(sample_rows, source)
            for target in targets:
                if source == target:
                    continue
                target_values = [float(row[target]) for row in sample_rows]
                observed_neighbor_mean, observed_background_mean, observed_ratio = ratio_for_indices(
                    target_values,
                    neighbor_idxs,
                    background_idxs,
                )
                rng = random.Random(stable_seed(seed, f"{sample_id}:{source}:{target}"))
                null_ratios: list[float] = []
                shuffled = target_values[:]
                for _ in range(permutations):
                    rng.shuffle(shuffled)
                    _, _, null_ratio = ratio_for_indices(shuffled, neighbor_idxs, background_idxs)
                    if not math.isnan(null_ratio):
                        null_ratios.append(null_ratio)
                null_mean = valid_mean(null_ratios)
                null_sd = (
                    math.sqrt(sum((value - null_mean) ** 2 for value in null_ratios) / (len(null_ratios) - 1))
                    if len(null_ratios) > 1 and not math.isnan(null_mean)
                    else float("nan")
                )
                z_score = (
                    (observed_ratio - null_mean) / null_sd
                    if null_sd and not math.isnan(observed_ratio) and not math.isnan(null_mean)
                    else float("nan")
                )
                empirical_p = (
                    (1 + sum(value >= observed_ratio for value in null_ratios)) / (len(null_ratios) + 1)
                    if null_ratios and not math.isnan(observed_ratio)
                    else float("nan")
                )
                results.append({
                    "sample_id": sample_id,
                    "sample": str(sample_rows[0]["sample"]),
                    "source": source,
                    "target": target,
                    "source_threshold": threshold,
                    "high_source_spots": len(high_idxs),
                    "neighbor_spots": len(neighbor_idxs),
                    "background_spots": len(background_idxs),
                    "observed_neighbor_mean": observed_neighbor_mean,
                    "observed_background_mean": observed_background_mean,
                    "observed_neighbor_vs_background_ratio": observed_ratio,
                    "null_permutations": len(null_ratios),
                    "null_ratio_mean": null_mean,
                    "null_ratio_sd": null_sd,
                    "z_score": z_score,
                    "empirical_p_ge_observed": empirical_p,
                })
    return results


def summarize_availability(
    signatures: dict[str, list[str]],
    usable_by_sample: dict[str, dict[str, list[str]]],
) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for sample_id, usable in sorted(usable_by_sample.items()):
        for signature_id, genes in signatures.items():
            present = usable.get(signature_id, [])
            rows.append({
                "sample_id": sample_id,
                "sample": SAMPLES[sample_id]["sample"],
                "signature_id": signature_id,
                "expected_genes": len(genes),
                "usable_genes": len(present),
                "usable_gene_symbols": ",".join(present),
            })
    return rows


def write_report(
    availability: list[dict[str, str | int]],
    correlations: list[dict[str, str | float]],
    adjacency: list[dict[str, str | float]],
    out_path: Path,
) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    key_adjacency = [
        (score_col("caf_core"), score_col("spp1_cxcl12_axis_desoverlap_2026")),
        (score_col("caf_core"), score_col("hla_drb5_macrophage_axis_desoverlap_2026")),
        (score_col("spp1_cxcl12_axis_desoverlap_2026"), score_col("myc_glycolysis_desoverlap_2026")),
        (score_col("hla_drb5_macrophage_axis_desoverlap_2026"), score_col("myc_glycolysis_desoverlap_2026")),
        (score_col("spp1_cxcl12_axis_desoverlap_2026"), "MYC"),
        (score_col("hla_drb5_macrophage_axis_desoverlap_2026"), "MYC"),
        (score_col("caf_core"), "MET"),
    ]

    def vals(source: str, target: str, field: str) -> list[float]:
        return [
            float(row[field]) for row in adjacency
            if row["source"] == source and row["target"] == target and not math.isnan(float(row[field]))
        ]

    lines = [
        "# GSE217414 external spatial CRLM validation",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "",
        "Validate whether the CRLM layered-niche signal is visible in an independent four-patient Visium dataset, using the same CAF/SPP1-CXCL12/HLA-DRB5/MYC-glycolysis signature logic.",
        "",
        "## Dataset",
        "",
        "- GEO: GSE217414.",
        "- Four colorectal cancer liver metastasis Visium sections.",
        "- Raw processed GEO package is small enough for reproducible validation: H5 matrices plus spatial coordinates.",
        "",
        "## Signature Availability",
        "",
        "| Sample | Signature | Usable / Expected | Usable genes |",
        "| --- | --- | --- | --- |",
    ]
    for row in availability:
        lines.append(
            f"| {row['sample']} | `{row['signature_id']}` | {row['usable_genes']} / {row['expected_genes']} | `{row['usable_gene_symbols']}` |"
        )

    lines.extend([
        "",
        "## Key Spatial Adjacency Tests",
        "",
        "| Sample | Source | Target | Observed ratio | Null mean | z | Empirical p >= observed |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in adjacency:
        if (row["source"], row["target"]) not in key_adjacency:
            continue
        lines.append(
            f"| {row['sample']} | `{row['source']}` | `{row['target']}` | "
            f"{fmt(float(row['observed_neighbor_vs_background_ratio']))} | "
            f"{fmt(float(row['null_ratio_mean']))} | "
            f"{fmt(float(row['z_score']))} | "
            f"{fmt(float(row['empirical_p_ge_observed']))} |"
        )

    lines.extend([
        "",
        "## Mean External Spatial Effects",
        "",
        f"- `CAF -> SPP1/CXCL12-lite`: mean neighbor/background ratio {fmt(valid_mean(vals(score_col('caf_core'), score_col('spp1_cxcl12_axis_desoverlap_2026'), 'observed_neighbor_vs_background_ratio')))}.",
        f"- `CAF -> HLA-DRB5-lite`: mean neighbor/background ratio {fmt(valid_mean(vals(score_col('caf_core'), score_col('hla_drb5_macrophage_axis_desoverlap_2026'), 'observed_neighbor_vs_background_ratio')))}.",
        f"- `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: mean neighbor/background ratio {fmt(valid_mean(vals(score_col('spp1_cxcl12_axis_desoverlap_2026'), score_col('myc_glycolysis_desoverlap_2026'), 'observed_neighbor_vs_background_ratio')))}.",
        f"- `HLA-DRB5-lite -> MYC/glycolysis-lite`: mean neighbor/background ratio {fmt(valid_mean(vals(score_col('hla_drb5_macrophage_axis_desoverlap_2026'), score_col('myc_glycolysis_desoverlap_2026'), 'observed_neighbor_vs_background_ratio')))}.",
        "",
        "## Interpretation Guardrails",
        "",
        "- This is independent spatial validation, but still Visium-level and exploratory.",
        "- Ratios above 1 with low empirical p suggest local coupling beyond random in-sample placement.",
        "- Heterogeneous samples matter: a paper-grade claim should model patient/section variability, not just pooled averages.",
        "- Positive GSE217414 plus positive GSE225857 would justify a manuscript-style storyline; discordance would sharpen the niche-specific boundary.",
        "",
    ])
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--signatures", type=Path, default=DEFAULT_SIGNATURES)
    parser.add_argument("--permutations", type=int, default=500)
    parser.add_argument("--seed", type=int, default=37)
    args = parser.parse_args()

    filelist_text = get_url(FILELIST_URL).decode("utf-8", errors="replace")
    files = parse_filelist(filelist_text)
    signatures = read_signatures(args.signatures)
    target_genes = set(CORE_GENES)
    for genes in signatures.values():
        target_genes.update(genes)

    all_rows: list[dict[str, str | float]] = []
    usable_by_sample: dict[str, dict[str, list[str]]] = {}
    for sample_id in SAMPLES:
        if sample_id not in files:
            print(f"[{sample_id}] missing GEO files, skipping", flush=True)
            continue
        paths = {
            "h5": args.raw_dir / f"{sample_id}_filtered_feature_bc_matrix.h5",
            "spatial": args.raw_dir / f"{sample_id}_spatial.tar.gz",
        }
        print(f"[{sample_id}] downloading/scoring Visium sample...", flush=True)
        download_file(files[sample_id]["h5"], paths["h5"])
        download_file(files[sample_id]["spatial"], paths["spatial"])
        sample_rows, usable_signature_genes = build_spot_rows(sample_id, paths, target_genes, signatures)
        all_rows.extend(sample_rows)
        usable_by_sample[sample_id] = usable_signature_genes
        print(f"  in-tissue spots: {len(sample_rows)}", flush=True)

    correlation_pairs = [
        (score_col("caf_core"), score_col("spp1_cxcl12_axis_desoverlap_2026")),
        (score_col("caf_core"), score_col("hla_drb5_macrophage_axis_desoverlap_2026")),
        (score_col("spp1_cxcl12_axis_desoverlap_2026"), score_col("myc_glycolysis_desoverlap_2026")),
        (score_col("hla_drb5_macrophage_axis_desoverlap_2026"), score_col("myc_glycolysis_desoverlap_2026")),
        ("SPP1", "CXCL12"),
        ("SPP1", "CD44"),
        ("MIF", "CXCR4"),
        ("MET", "MYC"),
        ("MYC", score_col("myc_glycolysis_desoverlap_2026")),
    ]
    adjacency_sources = [
        score_col("caf_core"),
        score_col("mcam_caf"),
        score_col("spp1_cxcl12_axis_desoverlap_2026"),
        score_col("hla_drb5_macrophage_axis_desoverlap_2026"),
    ]
    adjacency_targets = [
        "MET",
        "MYC",
        score_col("spp1_cxcl12_axis_desoverlap_2026"),
        score_col("hla_drb5_macrophage_axis_desoverlap_2026"),
        score_col("myc_glycolysis_desoverlap_2026"),
        score_col("glut1_invasive_margin_axis"),
        score_col("crlm_metabolic_vulnerabilities_2026"),
    ]

    availability = summarize_availability(signatures, usable_by_sample)
    correlations = compute_correlations(all_rows, correlation_pairs)
    adjacency = compute_adjacency_permutations(
        all_rows,
        adjacency_sources,
        adjacency_targets,
        args.permutations,
        args.seed,
    )

    write_tsv(availability, args.out_dir / "gse217414_spatial_signature_availability.tsv")
    write_tsv(correlations, args.out_dir / "gse217414_spatial_correlations.tsv")
    write_tsv(adjacency, args.out_dir / "gse217414_spatial_adjacency_permutation.tsv")
    write_tsv(all_rows, args.out_dir / "gse217414_spatial_spot_scores.tsv")
    write_report(
        availability,
        correlations,
        adjacency,
        args.out_dir / "gse217414_spatial_external_report.md",
    )

    print(f"Samples: {len(usable_by_sample)}")
    print(f"Spots: {len(all_rows)}")
    print(f"Permutations per test: {args.permutations}")
    print("Report: gse217414_spatial_external_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
