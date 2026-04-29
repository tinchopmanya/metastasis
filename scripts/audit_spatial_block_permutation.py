#!/usr/bin/env python3
"""Block-permutation audit for CRLM spatial niche effects.

The original spatial tests used global target shuffles within a sample. This
script adds a stricter null by shuffling target values only within coarse
spatial blocks, preserving regional gradients better than a global shuffle.
It is still not histology-aware, but it is a useful next reviewer-style stress
test for spatial autocorrelation.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_manifest" / "generated"
GSE225857_SPOTS = OUT_DIR / "gse225857_spatial_2026_spot_scores.tsv"
GSE217414_SPOTS = OUT_DIR / "gse217414_spatial_spot_scores.tsv"

HEX_NEIGHBOR_OFFSETS = [
    (0, 2),
    (0, -2),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]

EFFECTS = [
    ("caf_to_spp1_cxcl12_lite", "score_caf_core", "score_spp1_cxcl12_axis_desoverlap_2026"),
    ("caf_to_hla_drb5_lite", "score_caf_core", "score_hla_drb5_macrophage_axis_desoverlap_2026"),
    ("spp1_cxcl12_lite_to_myc_glycolysis_lite", "score_spp1_cxcl12_axis_desoverlap_2026", "score_myc_glycolysis_desoverlap_2026"),
    ("hla_drb5_lite_to_myc_glycolysis_lite", "score_hla_drb5_macrophage_axis_desoverlap_2026", "score_myc_glycolysis_desoverlap_2026"),
    ("caf_to_met", "score_caf_core", "MET"),
    ("spp1_cxcl12_lite_to_myc", "score_spp1_cxcl12_axis_desoverlap_2026", "MYC"),
    ("hla_drb5_lite_to_myc", "score_hla_drb5_macrophage_axis_desoverlap_2026", "MYC"),
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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


def load_spot_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for dataset, path in [("GSE225857", GSE225857_SPOTS), ("GSE217414", GSE217414_SPOTS)]:
        for row in read_tsv(path):
            if dataset == "GSE225857" and row.get("tissue") != "LCT":
                continue
            converted: dict[str, object] = {"dataset": dataset}
            converted.update(row)
            if "sample" not in converted:
                converted["sample"] = converted.get("sample_id", "")
            rows.append(converted)
    return rows


def group_rows(rows: list[dict[str, object]]) -> dict[tuple[str, str], list[dict[str, object]]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["dataset"]), str(row["sample"]))].append(row)
    return grouped


def adjacency_regions(
    sample_rows: list[dict[str, object]],
    source_values: list[float],
) -> tuple[float, set[int], set[int], set[int]]:
    coord_to_idx: dict[tuple[int, int], int] = {}
    for idx, row in enumerate(sample_rows):
        coord_to_idx[(int(row["array_row"]), int(row["array_col"]))] = idx
    threshold = percentile(source_values, 0.75)
    high_idxs = {
        idx for idx, value in enumerate(source_values)
        if not math.isnan(value) and value >= threshold and value > 0
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
    ratio = neighbor_mean / background_mean if background_mean and not math.isnan(background_mean) else float("nan")
    return neighbor_mean, background_mean, ratio


def spatial_blocks(sample_rows: list[dict[str, object]], block_size: int) -> list[list[int]]:
    grouped: dict[tuple[int, int], list[int]] = defaultdict(list)
    for idx, row in enumerate(sample_rows):
        block = (int(row["array_row"]) // block_size, int(row["array_col"]) // block_size)
        grouped[block].append(idx)
    return [indices for indices in grouped.values() if len(indices) > 1]


def shuffle_within_blocks(values: list[float], blocks: list[list[int]], rng: random.Random) -> list[float]:
    shuffled = values[:]
    for indices in blocks:
        block_values = [shuffled[idx] for idx in indices]
        rng.shuffle(block_values)
        for idx, value in zip(indices, block_values):
            shuffled[idx] = value
    return shuffled


def audit_effect(
    dataset: str,
    sample: str,
    sample_rows: list[dict[str, object]],
    effect_id: str,
    source: str,
    target: str,
    permutations: int,
    block_size: int,
    seed: int,
) -> dict[str, object]:
    source_values = [as_float(row.get(source, float("nan"))) for row in sample_rows]
    target_values = [as_float(row.get(target, float("nan"))) for row in sample_rows]
    _, high_idxs, neighbor_idxs, background_idxs = adjacency_regions(sample_rows, source_values)
    _, _, observed_ratio = ratio_for_indices(target_values, neighbor_idxs, background_idxs)
    blocks = spatial_blocks(sample_rows, block_size)
    rng = random.Random(stable_seed(seed, f"{dataset}:{sample}:{effect_id}:{block_size}"))
    null_ratios: list[float] = []
    for _ in range(permutations):
        shuffled = shuffle_within_blocks(target_values, blocks, rng)
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
    return {
        "dataset": dataset,
        "sample": sample,
        "effect_id": effect_id,
        "source": source,
        "target": target,
        "block_size": block_size,
        "high_source_spots": len(high_idxs),
        "neighbor_spots": len(neighbor_idxs),
        "background_spots": len(background_idxs),
        "observed_neighbor_vs_background_ratio": observed_ratio,
        "block_null_permutations": len(null_ratios),
        "block_null_ratio_mean": null_mean,
        "block_null_ratio_sd": null_sd,
        "block_z_score": z_score,
        "block_empirical_p_ge_observed": empirical_p,
        "survives_block_p_0_05": int(empirical_p <= 0.05) if not math.isnan(empirical_p) else "",
    }


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["effect_id"])].append(row)
    summary_rows: list[dict[str, object]] = []
    for effect_id, effect_rows in sorted(grouped.items()):
        ratios = [as_float(row["observed_neighbor_vs_background_ratio"]) for row in effect_rows]
        ps = [as_float(row["block_empirical_p_ge_observed"]) for row in effect_rows]
        summary_rows.append({
            "effect_id": effect_id,
            "n_samples": len(effect_rows),
            "positive_samples": sum(1 for value in ratios if value > 1),
            "survives_block_p_0_05": sum(1 for value in ps if value <= 0.05),
            "mean_ratio": mean(ratios),
            "mean_block_p": mean(ps),
            "status": classify(effect_rows),
        })
    return summary_rows


def classify(rows: list[dict[str, object]]) -> str:
    n = len(rows)
    positive = sum(1 for row in rows if as_float(row["observed_neighbor_vs_background_ratio"]) > 1)
    significant = sum(1 for row in rows if as_float(row["block_empirical_p_ge_observed"]) <= 0.05)
    if positive == n and significant >= n - 1:
        return "survives_block_null"
    if positive == n and significant >= math.ceil(n / 2):
        return "partially_survives_block_null"
    if positive == n:
        return "positive_but_explained_by_blocks"
    return "mixed_or_weak"


def write_report(rows: list[dict[str, object]], summary_rows: list[dict[str, object]], path: Path) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Spatial niche block-permutation audit",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "",
        "Stress-test key CRLM spatial niche effects against a block-permutation null that shuffles target values only within coarse spatial blocks.",
        "",
        "## Summary",
        "",
        "| Effect | Samples | Positive | Block p<=0.05 | Mean ratio | Mean block p | Status |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summary_rows:
        lines.append(
            f"| `{row['effect_id']}` | {row['n_samples']} | {row['positive_samples']}/{row['n_samples']} | "
            f"{row['survives_block_p_0_05']}/{row['n_samples']} | {fmt(float(row['mean_ratio']))} | "
            f"{fmt(float(row['mean_block_p']))} | {row['status']} |"
        )
    lines.extend([
        "",
        "## Sample-Level Rows",
        "",
        "| Dataset | Sample | Effect | Ratio | Block null mean | Block p | z |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['dataset']} | {row['sample']} | `{row['effect_id']}` | "
            f"{fmt(float(row['observed_neighbor_vs_background_ratio']))} | "
            f"{fmt(float(row['block_null_ratio_mean']))} | "
            f"{fmt(float(row['block_empirical_p_ge_observed']))} | "
            f"{fmt(float(row['block_z_score']))} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- Passing this audit is stronger than passing a global shuffle, because regional expression gradients are partly preserved.",
        "- Failing this audit does not disprove biology; it means the effect may be explained by coarse tissue domains and needs histology/deconvolution-aware testing.",
        "- This is still not a final null: block size is heuristic and no manual histology annotation is used.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--permutations", type=int, default=500)
    parser.add_argument("--block-size", type=int, default=12)
    parser.add_argument("--seed", type=int, default=83)
    args = parser.parse_args()

    rows = load_spot_rows()
    grouped = group_rows(rows)
    audit_rows: list[dict[str, object]] = []
    for (dataset, sample), sample_rows in sorted(grouped.items()):
        for effect_id, source, target in EFFECTS:
            audit_rows.append(
                audit_effect(
                    dataset,
                    sample,
                    sample_rows,
                    effect_id,
                    source,
                    target,
                    args.permutations,
                    args.block_size,
                    args.seed,
                )
            )
    summary_rows = summarize(audit_rows)
    write_tsv(audit_rows, OUT_DIR / "spatial_niche_block_permutation.tsv")
    write_tsv(summary_rows, OUT_DIR / "spatial_niche_block_permutation_summary.tsv")
    write_report(audit_rows, summary_rows, OUT_DIR / "spatial_niche_block_permutation_report.md")
    print(f"Audit rows: {len(audit_rows)}")
    print(f"Summary rows: {len(summary_rows)}")
    print("Report: spatial_niche_block_permutation_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
