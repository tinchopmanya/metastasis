#!/usr/bin/env python3
"""Lightweight spatial validation for GSE225857 Visium samples.

This script downloads only the Visium matrix/barcode/feature/position files
for GSE225857, skips histology images, extracts genes relevant to the
mCAF-HGF-MET-MYC-glycolysis hypothesis, and computes spot-level correlations.

It intentionally treats Visium as a coarse co-localization assay: positive
spot-level association does not prove cell-cell interaction, but it can support
or weaken the spatial plausibility of the paracrine niche hypothesis.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import math
import random
import ssl
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"
DEFAULT_RAW_DIR = DEFAULT_OUT_DIR / "gse225857_spatial_raw"

BASE_URL = "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM7058nnn"

SAMPLES = {
    "C1": {"gsm": "GSM7058756", "tissue": "CCT", "label": "primary_colon_C1"},
    "C2": {"gsm": "GSM7058757", "tissue": "CCT", "label": "primary_colon_C2"},
    "C3": {"gsm": "GSM7058758", "tissue": "CCT", "label": "primary_colon_C3"},
    "C4": {"gsm": "GSM7058759", "tissue": "CCT", "label": "primary_colon_C4"},
    "L1": {"gsm": "GSM7058760", "tissue": "LCT", "label": "liver_metastasis_L1"},
    "L2": {"gsm": "GSM7058761", "tissue": "LCT", "label": "liver_metastasis_L2"},
}

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
    "FAP",
    "ACTA2",
    "EPCAM",
    "KRT20",
]

SCORE_GENES = {
    "caf_score": ["COL1A1", "FAP", "MCAM", "ACTA2"],
    "glycolysis_score": ["SLC2A1", "HK2", "PGK1", "TPI1", "LDHA", "ENO1"],
    "tumor_score": ["EPCAM", "KRT20"],
}

CORRELATION_PAIRS = [
    ("HGF", "MET"),
    ("HGF", "tumor_score"),
    ("HGF", "glycolysis_score"),
    ("caf_score", "MET"),
    ("caf_score", "MYC"),
    ("caf_score", "glycolysis_score"),
    ("MET", "MYC"),
    ("MET", "glycolysis_score"),
    ("MYC", "glycolysis_score"),
    ("tumor_score", "glycolysis_score"),
]

ADJACENCY_SOURCES = ["caf_score", "HGF"]
ADJACENCY_TARGETS = ["MET", "MYC", "glycolysis_score"]
HEX_NEIGHBOR_OFFSETS = [
    (0, 2),
    (0, -2),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]


def geo_url(gsm: str, filename: str) -> str:
    return f"{BASE_URL}/{gsm}/suppl/{filename}"


def sample_files(sample_id: str, gsm: str) -> dict[str, str]:
    prefix = f"{gsm}_{sample_id}"
    return {
        "barcodes": f"{prefix}.barcodes.tsv.gz",
        "features": f"{prefix}.features.tsv.gz",
        "matrix": f"{prefix}.matrix.mtx.gz",
        "positions": f"{prefix}_tissue_positions_list.csv.gz",
    }


def download_file(url: str, out_path: Path) -> None:
    if out_path.exists() and out_path.stat().st_size > 0:
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context()
    request = urllib.request.Request(url, headers={"User-Agent": "metastasis-research/0.1"})
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    with urllib.request.urlopen(request, timeout=900, context=ctx) as response:
        tmp_path.write_bytes(response.read())
    tmp_path.replace(out_path)


def ensure_sample_files(sample_id: str, raw_dir: Path) -> dict[str, Path]:
    info = SAMPLES[sample_id]
    files = sample_files(sample_id, info["gsm"])
    paths: dict[str, Path] = {}
    for kind, filename in files.items():
        out_path = raw_dir / filename
        download_file(geo_url(info["gsm"], filename), out_path)
        paths[kind] = out_path
    return paths


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


def read_positions(path: Path) -> dict[str, dict[str, str]]:
    positions: dict[str, dict[str, str]] = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            parts = line.strip().split(",")
            if len(parts) < 6:
                continue
            if parts[0].lower() in {"barcode", "barcodes"}:
                continue
            positions[parts[0]] = {
                "in_tissue": parts[1],
                "array_row": parts[2],
                "array_col": parts[3],
                "pxl_row": parts[4],
                "pxl_col": parts[5],
            }
    return positions


def extract_gene_counts(
    matrix_path: Path,
    barcodes: list[str],
    row_to_gene: dict[int, str],
) -> dict[str, dict[str, float]]:
    values: dict[str, dict[str, float]] = {gene: defaultdict(float) for gene in set(row_to_gene.values())}
    with gzip.open(matrix_path, "rt", encoding="utf-8") as handle:
        header_seen = False
        dims_seen = False
        for line in handle:
            if line.startswith("%"):
                header_seen = True
                continue
            if not header_seen:
                continue
            if not dims_seen:
                dims_seen = True
                continue
            row_idx, col_idx, raw_value = line.strip().split()
            row = int(row_idx)
            if row not in row_to_gene:
                continue
            col = int(col_idx) - 1
            if col < 0 or col >= len(barcodes):
                continue
            gene = row_to_gene[row]
            values[gene][barcodes[col]] += float(raw_value)
    return {gene: dict(expr) for gene, expr in values.items()}


def log_value(gene_counts: dict[str, dict[str, float]], gene: str, barcode: str) -> float:
    return math.log1p(gene_counts.get(gene, {}).get(barcode, 0.0))


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


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


def build_spot_rows(sample_id: str, paths: dict[str, Path]) -> list[dict[str, str | float]]:
    info = SAMPLES[sample_id]
    barcodes = read_barcodes(paths["barcodes"])
    row_to_gene = read_features(paths["features"], set(TARGET_GENES))
    positions = read_positions(paths["positions"])
    gene_counts = extract_gene_counts(paths["matrix"], barcodes, row_to_gene)
    rows: list[dict[str, str | float]] = []

    for barcode in barcodes:
        pos = positions.get(barcode)
        if not pos or pos["in_tissue"] != "1":
            continue
        row: dict[str, str | float] = {
            "sample_id": sample_id,
            "tissue": info["tissue"],
            "label": info["label"],
            "barcode": barcode,
            "array_row": pos["array_row"],
            "array_col": pos["array_col"],
        }
        for gene in TARGET_GENES:
            row[gene] = log_value(gene_counts, gene, barcode)
        for score_name, genes in SCORE_GENES.items():
            row[score_name] = mean([float(row[gene]) for gene in genes])
        rows.append(row)
    return rows


def summarize_rows(rows: list[dict[str, str | float]]) -> list[dict[str, str | float]]:
    summaries: list[dict[str, str | float]] = []
    by_sample: dict[str, list[dict[str, str | float]]] = defaultdict(list)
    for row in rows:
        by_sample[str(row["sample_id"])].append(row)

    metrics = ["HGF", "MET", "MYC", "caf_score", "tumor_score", "glycolysis_score"]
    for sample_id, sample_rows in sorted(by_sample.items()):
        summary: dict[str, str | float] = {
            "sample_id": sample_id,
            "tissue": str(sample_rows[0]["tissue"]),
            "n_spots": len(sample_rows),
        }
        for metric in metrics:
            summary[f"mean_{metric}"] = mean([float(row[metric]) for row in sample_rows])
        summaries.append(summary)
    return summaries


def compute_correlations(rows: list[dict[str, str | float]]) -> list[dict[str, str | float]]:
    results: list[dict[str, str | float]] = []
    by_sample: dict[str, list[dict[str, str | float]]] = defaultdict(list)
    for row in rows:
        by_sample[str(row["sample_id"])].append(row)
    for sample_id, sample_rows in sorted(by_sample.items()):
        tissue = str(sample_rows[0]["tissue"])
        for x_name, y_name in CORRELATION_PAIRS:
            xs = [float(row[x_name]) for row in sample_rows]
            ys = [float(row[y_name]) for row in sample_rows]
            r, n = pearson(xs, ys)
            results.append({
                "sample_id": sample_id,
                "tissue": tissue,
                "x": x_name,
                "y": y_name,
                "pearson_r": r,
                "n_spots": n,
            })
    return results


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return float("nan")
    ordered = sorted(values)
    idx = int(round((len(ordered) - 1) * pct))
    return ordered[max(0, min(idx, len(ordered) - 1))]


def stable_seed(seed: int, label: str) -> int:
    value = seed
    for idx, char in enumerate(label, start=1):
        value += idx * ord(char)
    return value


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
        if float(row[source]) >= threshold and float(row[source]) > 0
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


def ratio_for_indices(values: list[float], neighbor_idxs: set[int], background_idxs: set[int]) -> tuple[float, float, float]:
    neighbor_mean = mean([values[idx] for idx in neighbor_idxs])
    background_mean = mean([values[idx] for idx in background_idxs])
    ratio = (
        neighbor_mean / background_mean
        if background_mean and not math.isnan(background_mean)
        else float("nan")
    )
    return neighbor_mean, background_mean, ratio


def compute_adjacency(rows: list[dict[str, str | float]]) -> list[dict[str, str | float]]:
    results: list[dict[str, str | float]] = []
    by_sample: dict[str, list[dict[str, str | float]]] = defaultdict(list)
    for row in rows:
        by_sample[str(row["sample_id"])].append(row)

    for sample_id, sample_rows in sorted(by_sample.items()):
        tissue = str(sample_rows[0]["tissue"])
        for source in ADJACENCY_SOURCES:
            threshold, high_idxs, neighbor_idxs, background_idxs = adjacency_regions(sample_rows, source)

            for target in ADJACENCY_TARGETS:
                target_values = [float(row[target]) for row in sample_rows]
                high_mean = mean([target_values[idx] for idx in high_idxs])
                neighbor_mean, background_mean, enrichment = ratio_for_indices(
                    target_values,
                    neighbor_idxs,
                    background_idxs,
                )
                results.append({
                    "sample_id": sample_id,
                    "tissue": tissue,
                    "source": source,
                    "target": target,
                    "source_threshold": threshold,
                    "high_source_spots": len(high_idxs),
                    "neighbor_spots": len(neighbor_idxs),
                    "background_spots": len(background_idxs),
                    "target_mean_in_high_source": high_mean,
                    "target_mean_in_neighbors": neighbor_mean,
                    "target_mean_in_background": background_mean,
                    "neighbor_vs_background_ratio": enrichment,
                })

    return results


def compute_adjacency_permutations(
    rows: list[dict[str, str | float]],
    permutations: int,
    seed: int,
) -> list[dict[str, str | float]]:
    if permutations <= 0:
        return []

    results: list[dict[str, str | float]] = []
    by_sample: dict[str, list[dict[str, str | float]]] = defaultdict(list)
    for row in rows:
        by_sample[str(row["sample_id"])].append(row)

    for sample_id, sample_rows in sorted(by_sample.items()):
        tissue = str(sample_rows[0]["tissue"])
        for source in ADJACENCY_SOURCES:
            threshold, high_idxs, neighbor_idxs, background_idxs = adjacency_regions(sample_rows, source)
            for target in ADJACENCY_TARGETS:
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

                null_mean = mean(null_ratios)
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
                    "tissue": tissue,
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


def write_tsv(rows: list[dict[str, str | float]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    if math.isnan(value):
        return "NA"
    return f"{value:.3f}"


def write_report(
    summaries: list[dict[str, str | float]],
    correlations: list[dict[str, str | float]],
    adjacency: list[dict[str, str | float]],
    permutations: list[dict[str, str | float]],
    out_path: Path,
) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# GSE225857 spatial spot-level validation",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "Test spatial plausibility of the mCAF-HGF-MET-MYC-glycolysis hypothesis using GSE225857 Visium spot-level data.",
        "",
        "## Scope",
        "- Downloaded only Visium barcodes, features, matrices, and tissue-position files.",
        "- Skipped histology images.",
        "- Treated spot-level co-expression as coarse co-localization, not proof of direct cell-cell interaction.",
        "",
        "## Sample Summary",
        "",
        "| Sample | Tissue | Spots | HGF | MET | MYC | CAF score | Tumor score | Glycolysis score |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summaries:
        lines.append(
            "| {sample_id} | {tissue} | {n_spots} | {hgf} | {met} | {myc} | {caf} | {tumor} | {gly} |".format(
                sample_id=row["sample_id"],
                tissue=row["tissue"],
                n_spots=row["n_spots"],
                hgf=fmt(float(row["mean_HGF"])),
                met=fmt(float(row["mean_MET"])),
                myc=fmt(float(row["mean_MYC"])),
                caf=fmt(float(row["mean_caf_score"])),
                tumor=fmt(float(row["mean_tumor_score"])),
                gly=fmt(float(row["mean_glycolysis_score"])),
            )
        )

    key_pairs = {
        ("caf_score", "MET"),
        ("caf_score", "MYC"),
        ("caf_score", "glycolysis_score"),
        ("HGF", "MET"),
        ("MET", "MYC"),
        ("MYC", "glycolysis_score"),
    }
    lines.extend([
        "",
        "## Key Spot-Level Correlations",
        "",
        "| Sample | Tissue | Pair | r | Spots |",
        "| --- | --- | --- | --- | --- |",
    ])
    for row in correlations:
        pair = (str(row["x"]), str(row["y"]))
        if pair not in key_pairs:
            continue
        lines.append(
            f"| {row['sample_id']} | {row['tissue']} | `{row['x']}~{row['y']}` | {fmt(float(row['pearson_r']))} | {row['n_spots']} |"
        )

    liver_caf_met = [
        float(row["pearson_r"]) for row in correlations
        if row["tissue"] == "LCT" and row["x"] == "caf_score" and row["y"] == "MET"
        and not math.isnan(float(row["pearson_r"]))
    ]
    liver_myc_gly = [
        float(row["pearson_r"]) for row in correlations
        if row["tissue"] == "LCT" and row["x"] == "MYC" and row["y"] == "glycolysis_score"
        and not math.isnan(float(row["pearson_r"]))
    ]
    lines.extend([
        "",
        "## Interpretation",
        f"- Mean LCT `caf_score~MET` correlation: {fmt(mean(liver_caf_met))}",
        f"- Mean LCT `MYC~glycolysis_score` correlation: {fmt(mean(liver_myc_gly))}",
        "- Positive correlations support spatial plausibility, but Visium spots mix cells and cannot prove paracrine causality.",
        "- Negative or weak `HGF~MET` spot correlations would not necessarily falsify the model because ligand and receptor may occupy adjacent rather than identical spots.",
        "",
        "## Adjacency Check",
        "",
        "| Sample | Tissue | Source | Target | High-source spots | Neighbor spots | Neighbor/background ratio |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])

    for row in adjacency:
        if row["tissue"] != "LCT":
            continue
        if row["target"] not in {"MET", "MYC", "glycolysis_score"}:
            continue
        lines.append(
            f"| {row['sample_id']} | {row['tissue']} | `{row['source']}` | `{row['target']}` | "
            f"{row['high_source_spots']} | {row['neighbor_spots']} | "
            f"{fmt(float(row['neighbor_vs_background_ratio']))} |"
        )

    caf_met_adj = [
        float(row["neighbor_vs_background_ratio"]) for row in adjacency
        if row["tissue"] == "LCT" and row["source"] == "caf_score" and row["target"] == "MET"
        and not math.isnan(float(row["neighbor_vs_background_ratio"]))
    ]
    hgf_met_adj = [
        float(row["neighbor_vs_background_ratio"]) for row in adjacency
        if row["tissue"] == "LCT" and row["source"] == "HGF" and row["target"] == "MET"
        and not math.isnan(float(row["neighbor_vs_background_ratio"]))
    ]

    lines.extend([
        "",
        f"- Mean LCT neighbor/background ratio for `caf_score -> MET`: {fmt(mean(caf_met_adj))}",
        f"- Mean LCT neighbor/background ratio for `HGF -> MET`: {fmt(mean(hgf_met_adj))}",
        "- Ratios above 1.0 suggest target signal is higher near source-high spots than background.",
        "",
        "## Permutation Check",
        "",
        "Target values were shuffled within each sample while keeping source-high spots, neighbors, and background fixed.",
        "",
        "| Sample | Tissue | Source | Target | Observed ratio | Null mean | z | Empirical p >= observed |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ])

    for row in permutations:
        if row["tissue"] != "LCT":
            continue
        if row["target"] not in {"MET", "MYC", "glycolysis_score"}:
            continue
        lines.append(
            f"| {row['sample_id']} | {row['tissue']} | `{row['source']}` | `{row['target']}` | "
            f"{fmt(float(row['observed_neighbor_vs_background_ratio']))} | "
            f"{fmt(float(row['null_ratio_mean']))} | {fmt(float(row['z_score']))} | "
            f"{fmt(float(row['empirical_p_ge_observed']))} |"
        )

    caf_met_perm = [
        float(row["empirical_p_ge_observed"]) for row in permutations
        if row["tissue"] == "LCT" and row["source"] == "caf_score" and row["target"] == "MET"
        and not math.isnan(float(row["empirical_p_ge_observed"]))
    ]
    hgf_met_perm = [
        float(row["empirical_p_ge_observed"]) for row in permutations
        if row["tissue"] == "LCT" and row["source"] == "HGF" and row["target"] == "MET"
        and not math.isnan(float(row["empirical_p_ge_observed"]))
    ]

    lines.extend([
        "",
        f"- LCT `caf_score -> MET` empirical p-values: {', '.join(fmt(value) for value in caf_met_perm) or 'NA'}",
        f"- LCT `HGF -> MET` empirical p-values: {', '.join(fmt(value) for value in hgf_met_perm) or 'NA'}",
        "- Low empirical p-values strengthen spatial enrichment beyond random redistribution of target expression.",
        "",
        "## Next Step",
        "Use the spatial and single-cell outputs together to prioritize a focused write-up of the revised niche model: PRELP/MCAM fibroblast HGF sources, MET+ tumor receivers, and MYC-glycolysis tumor response.",
        "",
    ])
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--samples", nargs="*", default=list(SAMPLES.keys()))
    parser.add_argument("--permutations", type=int, default=500)
    parser.add_argument("--seed", type=int, default=13)
    args = parser.parse_args()

    all_rows: list[dict[str, str | float]] = []
    for sample_id in args.samples:
        if sample_id not in SAMPLES:
            raise ValueError(f"Unknown sample: {sample_id}")
        print(f"[{sample_id}] downloading/reading Visium files...", flush=True)
        paths = ensure_sample_files(sample_id, args.raw_dir)
        sample_rows = build_spot_rows(sample_id, paths)
        print(f"  in-tissue spots: {len(sample_rows)}", flush=True)
        all_rows.extend(sample_rows)

    summaries = summarize_rows(all_rows)
    correlations = compute_correlations(all_rows)
    adjacency = compute_adjacency(all_rows)
    permutations = compute_adjacency_permutations(all_rows, args.permutations, args.seed)
    write_tsv(summaries, args.out_dir / "gse225857_spatial_sample_summary.tsv")
    write_tsv(correlations, args.out_dir / "gse225857_spatial_correlations.tsv")
    write_tsv(adjacency, args.out_dir / "gse225857_spatial_adjacency.tsv")
    write_tsv(permutations, args.out_dir / "gse225857_spatial_adjacency_permutation.tsv")
    write_tsv(all_rows, args.out_dir / "gse225857_spatial_spot_scores.tsv")
    write_report(summaries, correlations, adjacency, permutations, args.out_dir / "gse225857_spatial_report.md")

    print(f"Samples: {len(summaries)}")
    print(f"Spots: {len(all_rows)}")
    print(f"Permutations per test: {args.permutations}")
    print("Report: gse225857_spatial_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
