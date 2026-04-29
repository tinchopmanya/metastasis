#!/usr/bin/env python3
"""Initial specificity audit for CRLM spatial niche signatures.

This is a fast, deliberately conservative audit layer over the existing
GSE225857/GSE217414 spot-score tables. It does not replace paper-grade spatial
nulls; it asks whether the headline effects survive obvious gene-ablation
checks and whether they beat expression-matched random signatures drawn from
the currently extracted gene panel.
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

METADATA_COLUMNS = {
    "sample_id",
    "sample",
    "patient",
    "tissue",
    "label",
    "barcode",
    "array_row",
    "array_col",
}

DERIVED_SIGNATURES = {
    "score_cxcl12_fn1_cd44_stromal_stress": ["CXCL12", "FN1", "CD44"],
    "score_hla_drb5_no_ptprc": ["HLA-DRB5", "CD74", "CXCR4", "LGALS9"],
    "score_hla_drb5_no_cd74_ptprc": ["HLA-DRB5", "CXCR4", "LGALS9"],
    "score_myc_glycolysis_no_myc": ["HK2", "PGK1", "ENO1", "TPI1", "LDHA"],
}

AUDIT_EFFECTS = [
    {
        "effect_id": "caf_to_cxcl12_fn1_cd44_ablation",
        "source": "score_caf_core",
        "target": "score_cxcl12_fn1_cd44_stromal_stress",
        "original_source": "score_caf_core",
        "original_target": "score_spp1_cxcl12_axis_desoverlap_2026",
        "source_genes": ["COL1A1", "COL1A2", "ACTA2", "FAP", "POSTN", "PDGFRA", "PDGFRB"],
        "target_genes": ["CXCL12", "FN1", "CD44"],
        "risk_tested": "SPP1/CXCL12-lite label without HIF1A/CTNNB1 broad-stress genes",
    },
    {
        "effect_id": "caf_to_hla_drb5_no_ptprc",
        "source": "score_caf_core",
        "target": "score_hla_drb5_no_ptprc",
        "original_source": "score_caf_core",
        "original_target": "score_hla_drb5_macrophage_axis_desoverlap_2026",
        "source_genes": ["COL1A1", "COL1A2", "ACTA2", "FAP", "POSTN", "PDGFRA", "PDGFRB"],
        "target_genes": ["HLA-DRB5", "CD74", "CXCR4", "LGALS9"],
        "risk_tested": "PTPRC leakage in HLA-DRB5-lite module",
    },
    {
        "effect_id": "cxcl12_fn1_cd44_to_myc_glycolysis_no_myc",
        "source": "score_cxcl12_fn1_cd44_stromal_stress",
        "target": "score_myc_glycolysis_no_myc",
        "original_source": "score_spp1_cxcl12_axis_desoverlap_2026",
        "original_target": "score_myc_glycolysis_desoverlap_2026",
        "source_genes": ["CXCL12", "FN1", "CD44"],
        "target_genes": ["HK2", "PGK1", "ENO1", "TPI1", "LDHA"],
        "risk_tested": "MYC circularity and broad HIF1A/CTNNB1 source contribution",
    },
    {
        "effect_id": "hla_drb5_no_ptprc_to_myc_glycolysis_no_myc",
        "source": "score_hla_drb5_no_ptprc",
        "target": "score_myc_glycolysis_no_myc",
        "original_source": "score_hla_drb5_macrophage_axis_desoverlap_2026",
        "original_target": "score_myc_glycolysis_desoverlap_2026",
        "source_genes": ["HLA-DRB5", "CD74", "CXCR4", "LGALS9"],
        "target_genes": ["HK2", "PGK1", "ENO1", "TPI1", "LDHA"],
        "risk_tested": "PTPRC leakage plus MYC circularity",
    },
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


def score_genes(row: dict[str, object], genes: list[str]) -> float:
    return mean([as_float(row.get(gene, float("nan"))) for gene in genes])


def add_derived_scores(rows: list[dict[str, object]]) -> None:
    for row in rows:
        for score_name, genes in DERIVED_SIGNATURES.items():
            row[score_name] = score_genes(row, genes)


def group_rows(rows: list[dict[str, object]]) -> dict[tuple[str, str], list[dict[str, object]]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        sample = row.get("sample") or row.get("sample_id")
        grouped[(str(row["dataset"]), str(sample))].append(row)
    return grouped


def gene_columns(rows: list[dict[str, object]]) -> list[str]:
    if not rows:
        return []
    columns = []
    for key in rows[0]:
        if key in METADATA_COLUMNS or key.startswith("score_") or key == "dataset":
            continue
        if key.upper() == key and any(char.isalpha() for char in key):
            columns.append(key)
    return columns


def gene_stats(rows: list[dict[str, object]], genes: list[str]) -> dict[str, dict[str, float]]:
    stats: dict[str, dict[str, float]] = {}
    for gene in genes:
        values = [as_float(row.get(gene, float("nan"))) for row in rows]
        valid = [value for value in values if not math.isnan(value)]
        if not valid:
            continue
        stats[gene] = {
            "mean": mean(valid),
            "pct_positive": sum(1 for value in valid if value > 0) / len(valid),
        }
    return stats


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


def global_shuffle_p(
    target_values: list[float],
    observed_ratio: float,
    neighbor_idxs: set[int],
    background_idxs: set[int],
    permutations: int,
    rng: random.Random,
) -> tuple[float, float, float]:
    shuffled = target_values[:]
    null_ratios: list[float] = []
    for _ in range(permutations):
        rng.shuffle(shuffled)
        _, _, null_ratio = ratio_for_indices(shuffled, neighbor_idxs, background_idxs)
        if not math.isnan(null_ratio):
            null_ratios.append(null_ratio)
    if not null_ratios or math.isnan(observed_ratio):
        return float("nan"), float("nan"), float("nan")
    null_mean = mean(null_ratios)
    null_sd = (
        math.sqrt(sum((value - null_mean) ** 2 for value in null_ratios) / (len(null_ratios) - 1))
        if len(null_ratios) > 1
        else float("nan")
    )
    p = (1 + sum(value >= observed_ratio for value in null_ratios)) / (len(null_ratios) + 1)
    return null_mean, null_sd, p


def nearest_genes(
    wanted_genes: list[str],
    stats: dict[str, dict[str, float]],
    excluded: set[str],
    rng: random.Random,
) -> list[str]:
    candidates = [gene for gene in stats if gene not in excluded and stats[gene]["mean"] > 0]
    chosen: list[str] = []
    used: set[str] = set()
    for gene in wanted_genes:
        if gene not in stats:
            continue
        target_mean = stats[gene]["mean"]
        ranked = [
            candidate for candidate in candidates
            if candidate not in used
        ]
        if not ranked:
            break
        ranked.sort(key=lambda candidate: (abs(stats[candidate]["mean"] - target_mean), rng.random()))
        pick_window = ranked[: min(8, len(ranked))]
        picked = rng.choice(pick_window)
        chosen.append(picked)
        used.add(picked)
    return chosen


def random_signature_ratios(
    sample_rows: list[dict[str, object]],
    source_values: list[float],
    target_genes: list[str],
    excluded: set[str],
    stats: dict[str, dict[str, float]],
    random_controls: int,
    rng: random.Random,
) -> list[float]:
    _, _, neighbor_idxs, background_idxs = adjacency_regions(sample_rows, source_values)
    ratios: list[float] = []
    for _ in range(random_controls):
        random_genes = nearest_genes(target_genes, stats, excluded, rng)
        if not random_genes:
            continue
        random_values = [score_genes(row, random_genes) for row in sample_rows]
        _, _, ratio = ratio_for_indices(random_values, neighbor_idxs, background_idxs)
        if not math.isnan(ratio):
            ratios.append(ratio)
    return ratios


def audit_sample_effect(
    dataset: str,
    sample: str,
    sample_rows: list[dict[str, object]],
    effect: dict[str, object],
    stats: dict[str, dict[str, float]],
    permutations: int,
    random_controls: int,
    seed: int,
) -> dict[str, object]:
    source_name = str(effect["source"])
    target_name = str(effect["target"])
    original_source_name = str(effect["original_source"])
    original_target_name = str(effect["original_target"])
    source_values = [as_float(row.get(source_name, float("nan"))) for row in sample_rows]
    target_values = [as_float(row.get(target_name, float("nan"))) for row in sample_rows]
    original_source_values = [as_float(row.get(original_source_name, float("nan"))) for row in sample_rows]
    original_target_values = [as_float(row.get(original_target_name, float("nan"))) for row in sample_rows]

    _, _, neighbor_idxs, background_idxs = adjacency_regions(sample_rows, source_values)
    _, _, audited_ratio = ratio_for_indices(target_values, neighbor_idxs, background_idxs)
    rng = random.Random(stable_seed(seed, f"{dataset}:{sample}:{effect['effect_id']}:perm"))
    null_mean, null_sd, global_p = global_shuffle_p(
        target_values,
        audited_ratio,
        neighbor_idxs,
        background_idxs,
        permutations,
        rng,
    )

    _, _, original_neighbor_idxs, original_background_idxs = adjacency_regions(sample_rows, original_source_values)
    _, _, original_ratio = ratio_for_indices(original_target_values, original_neighbor_idxs, original_background_idxs)

    excluded = set(effect["source_genes"]) | set(effect["target_genes"])
    rng_controls = random.Random(stable_seed(seed, f"{dataset}:{sample}:{effect['effect_id']}:random"))
    random_target_ratios = random_signature_ratios(
        sample_rows,
        source_values,
        list(effect["target_genes"]),
        excluded,
        stats,
        random_controls,
        rng_controls,
    )
    random_p = (
        (1 + sum(value >= audited_ratio for value in random_target_ratios)) / (len(random_target_ratios) + 1)
        if random_target_ratios and not math.isnan(audited_ratio)
        else float("nan")
    )
    return {
        "dataset": dataset,
        "sample": sample,
        "effect_id": effect["effect_id"],
        "risk_tested": effect["risk_tested"],
        "source": source_name,
        "target": target_name,
        "original_source": original_source_name,
        "original_target": original_target_name,
        "original_ratio": original_ratio,
        "audited_ratio": audited_ratio,
        "ratio_retention_vs_original": audited_ratio / original_ratio if original_ratio else float("nan"),
        "global_shuffle_null_mean": null_mean,
        "global_shuffle_null_sd": null_sd,
        "global_shuffle_p_ge_observed": global_p,
        "random_target_controls": len(random_target_ratios),
        "random_target_mean_ratio": mean(random_target_ratios),
        "random_target_median_ratio": median(random_target_ratios),
        "random_target_p95_ratio": percentile(random_target_ratios, 0.95),
        "random_target_p_ge_observed": random_p,
        "positive_after_ablation": int(audited_ratio > 1) if not math.isnan(audited_ratio) else "",
        "beats_random_p_0_05": int(random_p <= 0.05) if not math.isnan(random_p) else "",
    }


def stable_seed(seed: int, label: str) -> int:
    value = seed
    for idx, char in enumerate(label, start=1):
        value += idx * ord(char)
    return value


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["effect_id"])].append(row)
    summary_rows: list[dict[str, object]] = []
    for effect_id, effect_rows in sorted(grouped.items()):
        audited_ratios = [as_float(row["audited_ratio"]) for row in effect_rows]
        original_ratios = [as_float(row["original_ratio"]) for row in effect_rows]
        random_ps = [as_float(row["random_target_p_ge_observed"]) for row in effect_rows]
        global_ps = [as_float(row["global_shuffle_p_ge_observed"]) for row in effect_rows]
        summary_rows.append({
            "effect_id": effect_id,
            "n_samples": len(effect_rows),
            "mean_original_ratio": mean(original_ratios),
            "mean_audited_ratio": mean(audited_ratios),
            "median_audited_ratio": median(audited_ratios),
            "min_audited_ratio": min(audited_ratios),
            "positive_after_ablation": sum(1 for value in audited_ratios if value > 1),
            "global_shuffle_p_le_0_05": sum(1 for value in global_ps if value <= 0.05),
            "beats_random_p_0_05": sum(1 for value in random_ps if value <= 0.05),
            "mean_random_p": mean(random_ps),
            "audit_status": classify(effect_rows),
        })
    return summary_rows


def classify(rows: list[dict[str, object]]) -> str:
    n = len(rows)
    positive = sum(1 for row in rows if as_float(row["audited_ratio"]) > 1)
    beats_random = sum(1 for row in rows if as_float(row["random_target_p_ge_observed"]) <= 0.05)
    if positive == n and beats_random >= n - 1:
        return "survives_initial_specificity_screen"
    if positive == n:
        return "positive_but_not_specific_vs_random"
    if positive >= max(1, math.ceil(n / 2)):
        return "mixed_after_ablation"
    return "weak_after_ablation"


def write_report(rows: list[dict[str, object]], summary_rows: list[dict[str, object]], path: Path) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Spatial signature specificity audit",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "",
        "Run an initial reviewer-style specificity screen for the CRLM spatial niche effects using gene ablations and expression-matched random signatures drawn from the currently extracted gene panel.",
        "",
        "## Important Limitation",
        "",
        "This is not the final paper-grade control. Random signatures are matched within the extracted analysis gene panel, not the full transcriptome, and the spatial null is still a global target shuffle. Passing this screen means only that the effect survived obvious circularity checks.",
        "",
        "## Summary",
        "",
        "| Effect | Samples | Mean original ratio | Mean audited ratio | Positive after ablation | Beats random p<=0.05 | Status |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summary_rows:
        lines.append(
            f"| `{row['effect_id']}` | {row['n_samples']} | {fmt(float(row['mean_original_ratio']))} | "
            f"{fmt(float(row['mean_audited_ratio']))} | {row['positive_after_ablation']}/{row['n_samples']} | "
            f"{row['beats_random_p_0_05']}/{row['n_samples']} | {row['audit_status']} |"
        )
    lines.extend([
        "",
        "## Sample-Level Audit",
        "",
        "| Dataset | Sample | Effect | Original ratio | Audited ratio | Random mean | Random p>=observed | Global shuffle p |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['dataset']} | {row['sample']} | `{row['effect_id']}` | "
            f"{fmt(float(row['original_ratio']))} | {fmt(float(row['audited_ratio']))} | "
            f"{fmt(float(row['random_target_mean_ratio']))} | "
            f"{fmt(float(row['random_target_p_ge_observed']))} | "
            f"{fmt(float(row['global_shuffle_p_ge_observed']))} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- Effects that remain positive after ablation but do not beat random controls should be treated as spatially broad, not specific.",
        "- Effects that beat random controls still require stricter spatial nulls controlling histology, UMI depth and autocorrelation.",
        "- The current safest language remains exploratory multi-dataset support, not causal niche proof.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def load_spot_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for dataset, path in [("GSE225857", GSE225857_SPOTS), ("GSE217414", GSE217414_SPOTS)]:
        for row in read_tsv(path):
            if dataset == "GSE225857" and row.get("tissue") != "LCT":
                continue
            converted: dict[str, object] = {"dataset": dataset}
            converted.update(row)
            rows.append(converted)
    add_derived_scores(rows)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--permutations", type=int, default=200)
    parser.add_argument("--random-controls", type=int, default=200)
    parser.add_argument("--seed", type=int, default=71)
    args = parser.parse_args()

    rows = load_spot_rows()
    grouped = group_rows(rows)
    audit_rows: list[dict[str, object]] = []
    for (dataset, sample), sample_rows in sorted(grouped.items()):
        genes = gene_columns(sample_rows)
        stats = gene_stats(sample_rows, genes)
        for effect in AUDIT_EFFECTS:
            audit_rows.append(
                audit_sample_effect(
                    dataset,
                    sample,
                    sample_rows,
                    effect,
                    stats,
                    args.permutations,
                    args.random_controls,
                    args.seed,
                )
            )
    summary_rows = summarize(audit_rows)
    write_tsv(audit_rows, OUT_DIR / "spatial_niche_specificity_audit.tsv")
    write_tsv(summary_rows, OUT_DIR / "spatial_niche_specificity_summary.tsv")
    write_report(audit_rows, summary_rows, OUT_DIR / "spatial_niche_specificity_report.md")
    print(f"Audit rows: {len(audit_rows)}")
    print(f"Summary rows: {len(summary_rows)}")
    print("Report: spatial_niche_specificity_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
