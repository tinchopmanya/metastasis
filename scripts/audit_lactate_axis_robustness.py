#!/usr/bin/env python3
"""Reviewer-style robustness audit for the HLA-DRB5/lactate-axis branch.

The current most interesting CRLM signal is:

    HLA-DRB5-like neighborhoods -> pyruvate/transamination proxies

This script tries to break that signal before we invest in flux-level work. It
adds four stress tests:

1. sensitivity to spatial block size;
2. source/target leave-one-gene-out ablation;
3. full-feature-universe expression/dropout-matched random target controls;
4. residualization by sequencing depth and spatial coordinates.

It remains a transcript-proxy audit, not spFBA and not causal validation.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import math
import random
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import h5py
import numpy as np

import analyze_spatial_lactate_axis as lactate


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_manifest" / "generated"

SOURCE_SIGNATURES = {
    "hla_drb5_original": ["HLA-DRB5", "CD74", "CXCR4", "LGALS9", "PTPRC"],
    "hla_drb5_no_ptprc": ["HLA-DRB5", "CD74", "CXCR4", "LGALS9"],
    "hla_drb5_no_cd74_ptprc": ["HLA-DRB5", "CXCR4", "LGALS9"],
    "hla_drb5_only": ["HLA-DRB5"],
}

TARGET_SIGNATURES = {
    "pyruvate_mito_entry": ["MPC1", "MPC2", "PDHA1", "PDHB"],
    "glutamate_transamination": ["GOT1", "GOT2", "GLUD1", "GLS"],
    "lactate_import_anabolic": ["SLC16A1", "MPC1", "MPC2", "GOT1", "GOT2", "IDH2", "ACLY", "ACSS2"],
    "lactate_export_glycolytic": ["SLC16A3", "SLC2A1", "HK2", "PGK1", "ENO1"],
}

BLOCK_TARGETS = [
    "pyruvate_mito_entry",
    "glutamate_transamination",
    "lactate_import_anabolic",
    "lactate_export_glycolytic",
]

RANDOM_TARGETS = ["pyruvate_mito_entry", "glutamate_transamination"]
RESIDUAL_TARGETS = ["pyruvate_mito_entry", "glutamate_transamination"]

HEX_NEIGHBOR_OFFSETS = [
    (0, 2),
    (0, -2),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]


def write_tsv(rows: list[dict[str, object]], path: Path) -> None:
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


def as_float(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def mean(values: list[float]) -> float:
    valid = [value for value in values if not math.isnan(value)]
    return sum(valid) / len(valid) if valid else float("nan")


def median(values: list[float]) -> float:
    valid = sorted(value for value in values if not math.isnan(value))
    if not valid:
        return float("nan")
    midpoint = len(valid) // 2
    if len(valid) % 2:
        return valid[midpoint]
    return (valid[midpoint - 1] + valid[midpoint]) / 2


def percentile(values: list[float], pct: float) -> float:
    valid = sorted(value for value in values if not math.isnan(value))
    if not valid:
        return float("nan")
    idx = int(round((len(valid) - 1) * pct))
    return valid[max(0, min(idx, len(valid) - 1))]


def fmt(value: object, digits: int = 3) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return "NA"
        return f"{value:.{digits}f}"
    return str(value)


def stable_seed(seed: int, label: str) -> int:
    value = seed
    for idx, char in enumerate(label, start=1):
        value += idx * ord(char)
    return value


def score_genes(row: dict[str, object], genes: list[str]) -> float:
    return mean([as_float(row.get(gene, float("nan"))) for gene in genes])


def add_scores(rows: list[dict[str, object]]) -> None:
    for row in rows:
        for name, genes in SOURCE_SIGNATURES.items():
            row[f"score_{name}"] = score_genes(row, genes)
        for name, genes in TARGET_SIGNATURES.items():
            row[f"score_{name}"] = score_genes(row, genes)


def group_rows(rows: list[dict[str, object]]) -> dict[tuple[str, str], list[dict[str, object]]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["dataset"]), str(row["sample"]))].append(row)
    return grouped


def adjacency_regions(
    sample_rows: list[dict[str, object]],
    source_values: list[float],
    require_positive: bool = True,
) -> tuple[set[int], set[int], set[int]]:
    coord_to_idx: dict[tuple[int, int], int] = {}
    for idx, row in enumerate(sample_rows):
        coord_to_idx[(int(row["array_row"]), int(row["array_col"]))] = idx
    threshold = percentile(source_values, 0.75)
    high_idxs = {
        idx for idx, value in enumerate(source_values)
        if not math.isnan(value) and value >= threshold and (not require_positive or value > 0)
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
    return high_idxs, neighbor_idxs, background_idxs


def ratio_delta(
    values: list[float],
    neighbor_idxs: set[int],
    background_idxs: set[int],
) -> tuple[float, float, float, float]:
    neighbor_mean = mean([values[idx] for idx in neighbor_idxs])
    background_mean = mean([values[idx] for idx in background_idxs])
    ratio = neighbor_mean / background_mean if background_mean and not math.isnan(background_mean) else float("nan")
    return neighbor_mean, background_mean, neighbor_mean - background_mean, ratio


def spatial_blocks(sample_rows: list[dict[str, object]], block_size: int) -> list[list[int]]:
    grouped: dict[tuple[int, int], list[int]] = defaultdict(list)
    for idx, row in enumerate(sample_rows):
        grouped[(int(row["array_row"]) // block_size, int(row["array_col"]) // block_size)].append(idx)
    return [indices for indices in grouped.values() if len(indices) > 1]


def shuffle_within_blocks(values: list[float], blocks: list[list[int]], rng: random.Random) -> list[float]:
    shuffled = values[:]
    for indices in blocks:
        block_values = [shuffled[idx] for idx in indices]
        rng.shuffle(block_values)
        for idx, value in zip(indices, block_values):
            shuffled[idx] = value
    return shuffled


def block_audit(
    dataset: str,
    sample: str,
    sample_rows: list[dict[str, object]],
    effect_id: str,
    source_values: list[float],
    target_values: list[float],
    block_size: int,
    permutations: int,
    seed: int,
    require_positive_source: bool = True,
) -> dict[str, object]:
    high_idxs, neighbor_idxs, background_idxs = adjacency_regions(
        sample_rows,
        source_values,
        require_positive=require_positive_source,
    )
    neighbor_mean, background_mean, observed_delta, observed_ratio = ratio_delta(
        target_values,
        neighbor_idxs,
        background_idxs,
    )
    blocks = spatial_blocks(sample_rows, block_size)
    rng = random.Random(stable_seed(seed, f"{dataset}:{sample}:{effect_id}:{block_size}"))
    null_deltas: list[float] = []
    null_ratios: list[float] = []
    for _ in range(permutations):
        shuffled = shuffle_within_blocks(target_values, blocks, rng)
        _, _, null_delta, null_ratio = ratio_delta(shuffled, neighbor_idxs, background_idxs)
        if not math.isnan(null_delta):
            null_deltas.append(null_delta)
        if not math.isnan(null_ratio):
            null_ratios.append(null_ratio)
    p_delta = (
        (1 + sum(value >= observed_delta for value in null_deltas)) / (len(null_deltas) + 1)
        if null_deltas and not math.isnan(observed_delta)
        else float("nan")
    )
    return {
        "dataset": dataset,
        "sample": sample,
        "effect_id": effect_id,
        "block_size": block_size,
        "high_source_spots": len(high_idxs),
        "neighbor_spots": len(neighbor_idxs),
        "background_spots": len(background_idxs),
        "neighbor_mean": neighbor_mean,
        "background_mean": background_mean,
        "observed_delta": observed_delta,
        "observed_ratio": observed_ratio,
        "block_null_delta_mean": mean(null_deltas),
        "block_null_ratio_mean": mean(null_ratios),
        "block_empirical_p_delta_ge_observed": p_delta,
        "survives_block_delta_p_0_05": int(p_delta <= 0.05) if not math.isnan(p_delta) else "",
    }


def summarize_block_rows(rows: list[dict[str, object]], keys: list[str]) -> list[dict[str, object]]:
    grouped: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    summary_rows: list[dict[str, object]] = []
    for key_values, effect_rows in sorted(grouped.items()):
        deltas = [as_float(row["observed_delta"]) for row in effect_rows]
        ratios = [as_float(row["observed_ratio"]) for row in effect_rows]
        ps = [as_float(row["block_empirical_p_delta_ge_observed"]) for row in effect_rows]
        out = {key: value for key, value in zip(keys, key_values)}
        out.update({
            "n_samples": len(effect_rows),
            "positive_delta_samples": sum(1 for value in deltas if value > 0),
            "positive_ratio_samples": sum(1 for value in ratios if value > 1),
            "block_delta_p_le_0_05": sum(1 for value in ps if value <= 0.05),
            "mean_ratio": mean(ratios),
            "mean_delta": mean(deltas),
            "mean_block_p": mean(ps),
        })
        summary_rows.append(out)
    return summary_rows


def read_gse225857_universe(sample: str) -> tuple[dict[str, dict[str, float]], dict[str, float]]:
    prefix = lactate.GSE225857_FILES[sample]
    barcodes_path = lactate.GSE225857_RAW / f"{prefix}.barcodes.tsv.gz"
    features_path = lactate.GSE225857_RAW / f"{prefix}.features.tsv.gz"
    matrix_path = lactate.GSE225857_RAW / f"{prefix}.matrix.mtx.gz"
    with gzip.open(barcodes_path, "rt", encoding="utf-8") as handle:
        barcodes = [line.strip() for line in handle if line.strip()]
    row_to_gene: dict[int, str] = {}
    with gzip.open(features_path, "rt", encoding="utf-8") as handle:
        for idx, line in enumerate(handle, start=1):
            parts = line.rstrip("\n").split("\t")
            if len(parts) > 1:
                row_to_gene[idx] = parts[1].upper()
    log_sums: dict[str, float] = defaultdict(float)
    positives: dict[str, int] = defaultdict(int)
    totals: dict[str, float] = defaultdict(float)
    with gzip.open(matrix_path, "rt", encoding="utf-8") as handle:
        dims_seen = False
        for line in handle:
            if line.startswith("%"):
                continue
            if not dims_seen:
                dims_seen = True
                continue
            row_idx, col_idx, raw_value = line.strip().split()
            gene = row_to_gene.get(int(row_idx))
            if not gene:
                continue
            value = float(raw_value)
            barcode = barcodes[int(col_idx) - 1]
            log_sums[gene] += math.log1p(value)
            positives[gene] += 1
            totals[barcode] += value
    n_spots = len(barcodes)
    stats = {
        gene: {
            "mean": log_sums[gene] / n_spots,
            "pct_positive": positives[gene] / n_spots,
        }
        for gene in log_sums
    }
    total_logs = {barcode: math.log1p(totals.get(barcode, 0.0)) for barcode in barcodes}
    return stats, total_logs


def read_gse217414_universe(sample: str) -> tuple[dict[str, dict[str, float]], dict[str, float]]:
    path = lactate.GSE217414_RAW / lactate.GSE217414_FILES[sample]
    with h5py.File(path, "r") as handle:
        matrix = handle["matrix"]
        barcodes = [value.decode("utf-8") for value in matrix["barcodes"][:]]
        feature_names = [value.decode("utf-8").upper() for value in matrix["features"]["name"][:]]
        data = matrix["data"][:]
        indices = matrix["indices"][:]
        indptr = matrix["indptr"][:]
        log_sums: dict[str, float] = defaultdict(float)
        positives: dict[str, int] = defaultdict(int)
        totals: dict[str, float] = defaultdict(float)
        for col_idx, barcode in enumerate(barcodes):
            start = int(indptr[col_idx])
            end = int(indptr[col_idx + 1])
            for row_idx, raw_value in zip(indices[start:end], data[start:end]):
                gene = feature_names[int(row_idx)]
                value = float(raw_value)
                log_sums[gene] += math.log1p(value)
                positives[gene] += 1
                totals[barcode] += value
    n_spots = len(barcodes)
    stats = {
        gene: {
            "mean": log_sums[gene] / n_spots,
            "pct_positive": positives[gene] / n_spots,
        }
        for gene in log_sums
    }
    total_logs = {barcode: math.log1p(totals.get(barcode, 0.0)) for barcode in barcodes}
    return stats, total_logs


def read_universe(dataset: str, sample: str) -> tuple[dict[str, dict[str, float]], dict[str, float]]:
    if dataset == "GSE225857":
        return read_gse225857_universe(sample)
    return read_gse217414_universe(sample)


def read_gene_logs(dataset: str, sample: str, genes: set[str]) -> dict[str, dict[str, float]]:
    if dataset == "GSE225857":
        return lactate.read_gse225857_gene_logs(sample, genes)
    return lactate.read_gse217414_gene_logs(sample, genes)


def matched_random_genes(
    wanted_genes: list[str],
    stats: dict[str, dict[str, float]],
    excluded: set[str],
    rng: random.Random,
) -> list[str]:
    candidates = [
        gene for gene, gene_stats in stats.items()
        if gene not in excluded and gene_stats["mean"] > 0 and gene_stats["pct_positive"] > 0
    ]
    chosen: list[str] = []
    used: set[str] = set()
    for gene in wanted_genes:
        if gene not in stats:
            continue
        target_mean = stats[gene]["mean"]
        target_pct = stats[gene]["pct_positive"]
        ranked = [candidate for candidate in candidates if candidate not in used]
        if not ranked:
            break
        ranked.sort(
            key=lambda candidate: (
                abs(math.log1p(stats[candidate]["mean"]) - math.log1p(target_mean))
                + abs(stats[candidate]["pct_positive"] - target_pct),
                rng.random(),
            )
        )
        window = ranked[: min(30, len(ranked))]
        picked = rng.choice(window)
        chosen.append(picked)
        used.add(picked)
    return chosen


def run_random_controls(
    rows_by_sample: dict[tuple[str, str], list[dict[str, object]]],
    universes: dict[tuple[str, str], tuple[dict[str, dict[str, float]], dict[str, float]]],
    random_controls: int,
    seed: int,
) -> list[dict[str, object]]:
    random_rows: list[dict[str, object]] = []
    all_known_genes = set().union(*SOURCE_SIGNATURES.values(), *TARGET_SIGNATURES.values())
    for (dataset, sample), sample_rows in sorted(rows_by_sample.items()):
        stats, _ = universes[(dataset, sample)]
        for source_name in ["hla_drb5_original", "hla_drb5_no_ptprc"]:
            source_values = [as_float(row[f"score_{source_name}"]) for row in sample_rows]
            _, neighbor_idxs, background_idxs = adjacency_regions(sample_rows, source_values)
            for target_name in RANDOM_TARGETS:
                target_genes = TARGET_SIGNATURES[target_name]
                target_values = [as_float(row[f"score_{target_name}"]) for row in sample_rows]
                _, _, observed_delta, observed_ratio = ratio_delta(target_values, neighbor_idxs, background_idxs)
                rng = random.Random(stable_seed(seed, f"{dataset}:{sample}:{source_name}:{target_name}:random"))
                random_gene_sets = [
                    matched_random_genes(target_genes, stats, all_known_genes, rng)
                    for _ in range(random_controls)
                ]
                selected_genes = {gene for gene_set in random_gene_sets for gene in gene_set}
                gene_logs = read_gene_logs(dataset, sample, selected_genes)
                random_deltas: list[float] = []
                random_ratios: list[float] = []
                for gene_set in random_gene_sets:
                    if not gene_set:
                        continue
                    values = []
                    for row in sample_rows:
                        barcode = str(row["barcode"])
                        values.append(mean([gene_logs.get(gene, {}).get(barcode, 0.0) for gene in gene_set]))
                    _, _, random_delta, random_ratio = ratio_delta(values, neighbor_idxs, background_idxs)
                    if not math.isnan(random_delta):
                        random_deltas.append(random_delta)
                    if not math.isnan(random_ratio):
                        random_ratios.append(random_ratio)
                p_delta = (
                    (1 + sum(value >= observed_delta for value in random_deltas)) / (len(random_deltas) + 1)
                    if random_deltas and not math.isnan(observed_delta)
                    else float("nan")
                )
                random_rows.append({
                    "dataset": dataset,
                    "sample": sample,
                    "source_variant": source_name,
                    "target": target_name,
                    "observed_delta": observed_delta,
                    "observed_ratio": observed_ratio,
                    "random_controls": len(random_deltas),
                    "random_delta_mean": mean(random_deltas),
                    "random_ratio_mean": mean(random_ratios),
                    "random_delta_p_ge_observed": p_delta,
                    "beats_random_delta_p_0_05": int(p_delta <= 0.05) if not math.isnan(p_delta) else "",
                })
    return random_rows


def residualize(values: list[float], sample_rows: list[dict[str, object]]) -> list[float]:
    y = np.array(values, dtype=float)
    covariates = []
    for row in sample_rows:
        covariates.append([
            as_float(row.get("log_total_counts", 0.0)),
            as_float(row.get("array_row", 0.0)),
            as_float(row.get("array_col", 0.0)),
        ])
    x = np.array(covariates, dtype=float)
    x = np.column_stack([x, x[:, 1] ** 2, x[:, 2] ** 2, x[:, 1] * x[:, 2]])
    for idx in range(x.shape[1]):
        col = x[:, idx]
        sd = col.std()
        x[:, idx] = (col - col.mean()) / sd if sd else 0.0
    design = np.column_stack([np.ones(x.shape[0]), x])
    valid = ~np.isnan(y)
    if valid.sum() < design.shape[1] + 2:
        return [float("nan")] * len(values)
    beta, *_ = np.linalg.lstsq(design[valid], y[valid], rcond=None)
    residuals = y - design.dot(beta)
    return [float(value) for value in residuals]


def write_report(
    block_summary: list[dict[str, object]],
    ablation_summary: list[dict[str, object]],
    random_summary: list[dict[str, object]],
    residual_summary: list[dict[str, object]],
    path: Path,
) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Lactate/HLA-DRB5 axis robustness audit",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "",
        "Stress-test the exploratory `HLA-DRB5-like -> pyruvate/transamination` spatial branch before treating it as a paper-grade hypothesis.",
        "",
        "## Block-Size Sensitivity",
        "",
        "| Effect | Block | Samples | Positive delta | Block p<=0.05 | Mean ratio | Mean block p |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in block_summary:
        lines.append(
            f"| `{row['effect_id']}` | {row['block_size']} | {row['n_samples']} | "
            f"{row['positive_delta_samples']}/{row['n_samples']} | {row['block_delta_p_le_0_05']}/{row['n_samples']} | "
            f"{fmt(float(row['mean_ratio']))} | {fmt(float(row['mean_block_p']))} |"
        )
    lines.extend([
        "",
        "## Ablation Summary",
        "",
        "| Source variant | Target variant | Samples | Positive delta | Block p<=0.05 | Mean ratio | Mean block p |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in ablation_summary:
        lines.append(
            f"| `{row['source_variant']}` | `{row['target_variant']}` | {row['n_samples']} | "
            f"{row['positive_delta_samples']}/{row['n_samples']} | {row['block_delta_p_le_0_05']}/{row['n_samples']} | "
            f"{fmt(float(row['mean_ratio']))} | {fmt(float(row['mean_block_p']))} |"
        )
    lines.extend([
        "",
        "## Full-Universe Random Target Controls",
        "",
        "| Source variant | Target | Samples | Beats random p<=0.05 | Mean observed ratio | Mean random p |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for row in random_summary:
        lines.append(
            f"| `{row['source_variant']}` | `{row['target']}` | {row['n_samples']} | "
            f"{row['beats_random_delta_p_0_05']}/{row['n_samples']} | {fmt(float(row['mean_observed_ratio']))} | "
            f"{fmt(float(row['mean_random_p']))} |"
        )
    lines.extend([
        "",
        "## Residualized Coordinate/Depth Audit",
        "",
        "| Source variant | Target | Samples | Positive residual delta | Block p<=0.05 | Mean residual delta | Mean block p |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in residual_summary:
        lines.append(
            f"| `{row['source_variant']}` | `{row['target']}` | {row['n_samples']} | "
            f"{row['positive_delta_samples']}/{row['n_samples']} | {row['block_delta_p_le_0_05']}/{row['n_samples']} | "
            f"{fmt(float(row['mean_delta']))} | {fmt(float(row['mean_block_p']))} |"
        )
    lines.extend([
        "",
        "## Interpretation Rules",
        "",
        "- A robust effect should survive multiple block sizes, source/target ablation, and residualization.",
        "- Random controls are drawn from the full feature universe of each spatial sample and matched approximately by expression and dropout.",
        "- Residualized ratios are not used because residuals can be negative; residualized tests use neighbor-minus-background delta.",
        "- This still does not prove lactate flux. The next decisive test is spFBA/FES validation.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def summarize_random(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["source_variant"]), str(row["target"]))].append(row)
    summary: list[dict[str, object]] = []
    for (source_variant, target), effect_rows in sorted(grouped.items()):
        ratios = [as_float(row["observed_ratio"]) for row in effect_rows]
        ps = [as_float(row["random_delta_p_ge_observed"]) for row in effect_rows]
        summary.append({
            "source_variant": source_variant,
            "target": target,
            "n_samples": len(effect_rows),
            "beats_random_delta_p_0_05": sum(1 for value in ps if value <= 0.05),
            "mean_observed_ratio": mean(ratios),
            "mean_random_p": mean(ps),
        })
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--permutations", type=int, default=200)
    parser.add_argument("--ablation-permutations", type=int, default=100)
    parser.add_argument("--random-controls", type=int, default=100)
    parser.add_argument("--block-sizes", default="8,12,16,20")
    parser.add_argument("--seed", type=int, default=109)
    args = parser.parse_args()

    block_sizes = [int(value.strip()) for value in args.block_sizes.split(",") if value.strip()]
    rows = lactate.load_rows()
    add_scores(rows)
    rows_by_sample = group_rows(rows)

    universes: dict[tuple[str, str], tuple[dict[str, dict[str, float]], dict[str, float]]] = {}
    for key, sample_rows in rows_by_sample.items():
        universes[key] = read_universe(*key)
        _, total_logs = universes[key]
        for row in sample_rows:
            row["log_total_counts"] = total_logs.get(str(row["barcode"]), 0.0)

    block_rows: list[dict[str, object]] = []
    for (dataset, sample), sample_rows in sorted(rows_by_sample.items()):
        source_values = [as_float(row["score_hla_drb5_original"]) for row in sample_rows]
        for target_name in BLOCK_TARGETS:
            target_values = [as_float(row[f"score_{target_name}"]) for row in sample_rows]
            for block_size in block_sizes:
                row = block_audit(
                    dataset,
                    sample,
                    sample_rows,
                    f"hla_drb5_original_to_{target_name}",
                    source_values,
                    target_values,
                    block_size,
                    args.permutations,
                    args.seed,
                )
                row["target"] = target_name
                block_rows.append(row)
    block_summary = summarize_block_rows(block_rows, ["effect_id", "block_size"])

    ablation_rows: list[dict[str, object]] = []
    for (dataset, sample), sample_rows in sorted(rows_by_sample.items()):
        for source_variant in SOURCE_SIGNATURES:
            source_values = [as_float(row[f"score_{source_variant}"]) for row in sample_rows]
            for target_family in ["pyruvate_mito_entry", "glutamate_transamination"]:
                genes = TARGET_SIGNATURES[target_family]
                variants = [(target_family, genes)]
                variants.extend((f"{target_family}_minus_{gene}", [g for g in genes if g != gene]) for gene in genes)
                for target_variant, target_genes in variants:
                    target_values = [score_genes(row, target_genes) for row in sample_rows]
                    audit_row = block_audit(
                        dataset,
                        sample,
                        sample_rows,
                        f"{source_variant}_to_{target_variant}",
                        source_values,
                        target_values,
                        12,
                        args.ablation_permutations,
                        args.seed,
                    )
                    audit_row["source_variant"] = source_variant
                    audit_row["target_family"] = target_family
                    audit_row["target_variant"] = target_variant
                    ablation_rows.append(audit_row)
    ablation_summary = summarize_block_rows(ablation_rows, ["source_variant", "target_variant"])

    random_rows = run_random_controls(rows_by_sample, universes, args.random_controls, args.seed)
    random_summary = summarize_random(random_rows)

    residual_rows: list[dict[str, object]] = []
    for (dataset, sample), sample_rows in sorted(rows_by_sample.items()):
        for source_variant in ["hla_drb5_original", "hla_drb5_no_ptprc"]:
            raw_source = [as_float(row[f"score_{source_variant}"]) for row in sample_rows]
            residual_source = residualize(raw_source, sample_rows)
            for target_name in RESIDUAL_TARGETS:
                raw_target = [as_float(row[f"score_{target_name}"]) for row in sample_rows]
                residual_target = residualize(raw_target, sample_rows)
                audit_row = block_audit(
                    dataset,
                    sample,
                    sample_rows,
                    f"residual_{source_variant}_to_{target_name}",
                    residual_source,
                    residual_target,
                    12,
                    args.ablation_permutations,
                    args.seed,
                    require_positive_source=False,
                )
                audit_row["source_variant"] = source_variant
                audit_row["target"] = target_name
                residual_rows.append(audit_row)
    residual_summary = summarize_block_rows(residual_rows, ["source_variant", "target"])

    write_tsv(block_rows, OUT_DIR / "lactate_axis_robustness_blocksize.tsv")
    write_tsv(block_summary, OUT_DIR / "lactate_axis_robustness_blocksize_summary.tsv")
    write_tsv(ablation_rows, OUT_DIR / "lactate_axis_robustness_ablation.tsv")
    write_tsv(ablation_summary, OUT_DIR / "lactate_axis_robustness_ablation_summary.tsv")
    write_tsv(random_rows, OUT_DIR / "lactate_axis_robustness_random_controls.tsv")
    write_tsv(random_summary, OUT_DIR / "lactate_axis_robustness_random_controls_summary.tsv")
    write_tsv(residual_rows, OUT_DIR / "lactate_axis_robustness_residualized.tsv")
    write_tsv(residual_summary, OUT_DIR / "lactate_axis_robustness_residualized_summary.tsv")
    write_report(
        block_summary,
        ablation_summary,
        random_summary,
        residual_summary,
        OUT_DIR / "lactate_axis_robustness_report.md",
    )
    print(f"Block rows: {len(block_rows)}")
    print(f"Ablation rows: {len(ablation_rows)}")
    print(f"Random-control rows: {len(random_rows)}")
    print(f"Residualized rows: {len(residual_rows)}")
    print("Report: lactate_axis_robustness_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
