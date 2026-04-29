#!/usr/bin/env python3
"""Consolidate spatial niche effects across CRLM Visium datasets.

This script turns the GSE225857 and GSE217414 adjacency-permutation outputs
into one comparable table. The goal is not to create a new statistic; it is to
make reproducibility by sample visible enough for paper-grade triage.
"""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_manifest" / "generated"
GSE225857_PATH = OUT_DIR / "gse225857_spatial_2026_adjacency_permutation.tsv"
GSE217414_PATH = OUT_DIR / "gse217414_spatial_adjacency_permutation.tsv"


KEY_EFFECTS = [
    {
        "effect_id": "caf_to_spp1_cxcl12_lite",
        "source": "score_caf_core",
        "target": "score_spp1_cxcl12_axis_desoverlap_2026",
        "claim_layer": "CAF-to-stromal/myeloid",
    },
    {
        "effect_id": "caf_to_hla_drb5_lite",
        "source": "score_caf_core",
        "target": "score_hla_drb5_macrophage_axis_desoverlap_2026",
        "claim_layer": "CAF-to-myeloid",
    },
    {
        "effect_id": "spp1_cxcl12_lite_to_myc_glycolysis_lite",
        "source": "score_spp1_cxcl12_axis_desoverlap_2026",
        "target": "score_myc_glycolysis_desoverlap_2026",
        "claim_layer": "stromal/myeloid-to-tumor-metabolic",
    },
    {
        "effect_id": "hla_drb5_lite_to_myc_glycolysis_lite",
        "source": "score_hla_drb5_macrophage_axis_desoverlap_2026",
        "target": "score_myc_glycolysis_desoverlap_2026",
        "claim_layer": "myeloid-to-tumor-metabolic",
    },
    {
        "effect_id": "caf_to_met",
        "source": "score_caf_core",
        "target": "MET",
        "claim_layer": "CAF-to-MET",
    },
    {
        "effect_id": "spp1_cxcl12_lite_to_myc",
        "source": "score_spp1_cxcl12_axis_desoverlap_2026",
        "target": "MYC",
        "claim_layer": "stromal/myeloid-to-MYC",
    },
    {
        "effect_id": "hla_drb5_lite_to_myc",
        "source": "score_hla_drb5_macrophage_axis_desoverlap_2026",
        "target": "MYC",
        "claim_layer": "myeloid-to-MYC",
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


def fmt(value: object, digits: int = 3) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return "NA"
        return f"{value:.{digits}f}"
    return str(value)


def to_float(row: dict[str, str], key: str) -> float:
    try:
        return float(row[key])
    except (KeyError, TypeError, ValueError):
        return float("nan")


def normalize_rows(dataset: str, rows: list[dict[str, str]]) -> list[dict[str, object]]:
    effect_lookup = {(item["source"], item["target"]): item for item in KEY_EFFECTS}
    normalized: list[dict[str, object]] = []
    for row in rows:
        effect = effect_lookup.get((row.get("source", ""), row.get("target", "")))
        if not effect:
            continue
        sample = row.get("sample") or row.get("sample_id", "")
        if dataset == "GSE225857" and row.get("tissue") != "LCT":
            continue
        ratio = to_float(row, "observed_neighbor_vs_background_ratio")
        empirical_p = to_float(row, "empirical_p_ge_observed")
        normalized.append({
            "dataset": dataset,
            "sample_id": row.get("sample_id", ""),
            "sample": sample,
            "tissue": row.get("tissue", "CRLM"),
            "effect_id": effect["effect_id"],
            "claim_layer": effect["claim_layer"],
            "source": row.get("source", ""),
            "target": row.get("target", ""),
            "neighbor_background_ratio": ratio,
            "empirical_p_ge_observed": empirical_p,
            "z_score": to_float(row, "z_score"),
            "positive_ratio": int(ratio > 1) if not math.isnan(ratio) else "",
            "p_le_0_05": int(empirical_p <= 0.05) if not math.isnan(empirical_p) else "",
            "high_source_spots": row.get("high_source_spots", ""),
            "neighbor_spots": row.get("neighbor_spots", ""),
            "background_spots": row.get("background_spots", ""),
        })
    return normalized


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_effect: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_effect[str(row["effect_id"])].append(row)

    summaries: list[dict[str, object]] = []
    for effect_id, effect_rows in sorted(by_effect.items()):
        ratios = [float(row["neighbor_background_ratio"]) for row in effect_rows]
        ps = [float(row["empirical_p_ge_observed"]) for row in effect_rows]
        datasets = sorted({str(row["dataset"]) for row in effect_rows})
        summaries.append({
            "effect_id": effect_id,
            "claim_layer": str(effect_rows[0]["claim_layer"]),
            "datasets": ",".join(datasets),
            "n_samples": len(effect_rows),
            "positive_samples": sum(1 for value in ratios if value > 1),
            "p_le_0_05_samples": sum(1 for value in ps if value <= 0.05),
            "mean_ratio": mean(ratios),
            "median_ratio": median(ratios),
            "min_ratio": min(ratios),
            "max_ratio": max(ratios),
            "mean_empirical_p": mean(ps),
            "paper_grade_status": classify_effect(ratios, ps, datasets),
        })
    return summaries


def classify_effect(ratios: list[float], ps: list[float], datasets: list[str]) -> str:
    positive = sum(1 for value in ratios if value > 1)
    significant = sum(1 for value in ps if value <= 0.05)
    if len(datasets) >= 2 and positive == len(ratios) and significant >= len(ratios) - 1:
        return "strong_reproducible"
    if len(datasets) >= 2 and positive >= max(1, len(ratios) - 1):
        return "reproducible_but_heterogeneous"
    if positive >= max(1, math.ceil(len(ratios) / 2)):
        return "partial"
    return "weak_or_negative"


def write_report(rows: list[dict[str, object]], summaries: list[dict[str, object]], path: Path) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Spatial niche multi-dataset effect consolidation",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "",
        "Consolidate key CAF/SPP1-CXCL12/HLA-DRB5/MYC-glycolysis spatial adjacency effects across GSE225857 and GSE217414.",
        "",
        "## Summary",
        "",
        "| Effect | Layer | Samples | Positive | p<=0.05 | Mean ratio | Range | Status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summaries:
        lines.append(
            f"| `{row['effect_id']}` | {row['claim_layer']} | {row['n_samples']} | "
            f"{row['positive_samples']}/{row['n_samples']} | {row['p_le_0_05_samples']}/{row['n_samples']} | "
            f"{fmt(float(row['mean_ratio']))} | {fmt(float(row['min_ratio']))}-{fmt(float(row['max_ratio']))} | "
            f"{row['paper_grade_status']} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "- `strong_reproducible` means the effect is positive across all included samples and significant in all or all-but-one samples across at least two datasets.",
        "- This is still a first-pass consolidation, not a final statistical meta-analysis.",
        "- The next required step is specificity: negative signatures, expression-matched random signatures, and spatial nulls that control tissue autocorrelation.",
        "",
        "## Sample-Level Rows",
        "",
        "| Dataset | Sample | Effect | Ratio | p | z |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['dataset']} | {row['sample']} | `{row['effect_id']}` | "
            f"{fmt(float(row['neighbor_background_ratio']))} | "
            f"{fmt(float(row['empirical_p_ge_observed']))} | "
            f"{fmt(float(row['z_score']))} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    rows = []
    rows.extend(normalize_rows("GSE225857", read_tsv(GSE225857_PATH)))
    rows.extend(normalize_rows("GSE217414", read_tsv(GSE217414_PATH)))
    summaries = summarize(rows)
    write_tsv(rows, OUT_DIR / "spatial_niche_multidataset_effects.tsv")
    write_tsv(summaries, OUT_DIR / "spatial_niche_multidataset_summary.tsv")
    write_report(rows, summaries, OUT_DIR / "spatial_niche_multidataset_report.md")
    print(f"Effects: {len(rows)} sample-level rows")
    print(f"Summary rows: {len(summaries)}")
    print("Report: spatial_niche_multidataset_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
