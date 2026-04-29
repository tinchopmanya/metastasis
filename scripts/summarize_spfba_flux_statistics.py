#!/usr/bin/env python3
"""Summarize spFBA/FES flux_statistics.h5ad outputs from Zenodo 13988866.

This script intentionally reads only selected reaction columns from the large
AnnData/HDF5 files extracted under downloads/spfba. It does not require scanpy.

The main goal is to decide whether the 2026 spFBA flux maps support a real
lactate/pyruvate/transamination phenotype in colorectal primary/metastatic
samples, independently of our HLA-DRB5 proxy work.
"""

from __future__ import annotations

import argparse
import csv
import math
from datetime import datetime, timezone
from pathlib import Path

import h5py
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXTRACTED = ROOT / "downloads" / "spfba" / "extracted" / "output"
OUT_DIR = ROOT / "data_manifest" / "generated"

REACTIONS = {
    "EX_lac__L_e": "lactate_exchange_negative_is_uptake",
    "EX_glc__D_e": "glucose_exchange_negative_is_uptake",
    "EX_o2_e": "oxygen_exchange_negative_is_uptake",
    "EX_gln__L_e": "glutamine_exchange",
    "EX_glu__L_e": "glutamate_exchange",
    "EX_pyr_e": "pyruvate_exchange",
    "PYRt2m": "pyruvate_transport_to_mitochondria",
    "PDHm": "pyruvate_dehydrogenase_mitochondrial",
    "LDH_L": "lactate_dehydrogenase_l",
    "ASPTA": "aspartate_transaminase_cytosol",
    "ASPTAm": "aspartate_transaminase_mitochondria",
    "ASPGLUm": "aspartate_glutamate_mitochondrial_transport",
    "ALATA_L": "alanine_transaminase",
    "GLUN": "glutaminase",
    "GLUNm": "glutaminase_mitochondrial",
    "GLUDym": "glutamate_dehydrogenase",
    "AKGDm": "alpha_ketoglutarate_dehydrogenase",
    "AKGMALtm": "akg_malate_transport",
    "MDHm": "malate_dehydrogenase_mitochondrial",
    "MDH": "malate_dehydrogenase_cytosol",
    "CSm": "citrate_synthase_mitochondrial",
    "Biomass": "biomass_synthesis",
    "ATPS4mi": "atp_synthase",
}

SAMPLE_LABELS = {
    "SC087_C03445G5_PT": ("SC087", "PT", "primary", "Stereo-seq"),
    "SC087_A02991A2_LM4": ("SC087", "LM4", "liver_metastasis", "Stereo-seq"),
    "SC087_A03389C5_LM4r": ("SC087", "LM4r", "liver_metastasis", "Stereo-seq"),
    "SC087_C03445C6_LM7": ("SC087", "LM7", "liver_metastasis", "Stereo-seq"),
    "CRC_P1": ("CRC_VisiumHD", "P1", "crc_visiumhd", "VisiumHD"),
    "CRC_P2": ("CRC_VisiumHD", "P2", "crc_visiumhd", "VisiumHD"),
    "CRC_P5": ("CRC_VisiumHD", "P5", "crc_visiumhd", "VisiumHD"),
}


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


def decode(values: np.ndarray) -> list[str]:
    return [value.decode("utf-8") if isinstance(value, bytes) else str(value) for value in values]


def fmt(value: object, digits: int = 3) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return "NA"
        return f"{value:.{digits}f}"
    return str(value)


def sample_paths(base: Path) -> list[tuple[str, Path]]:
    paths = []
    for sample_dir in sorted(base.iterdir()):
        if not sample_dir.is_dir() or sample_dir.name not in SAMPLE_LABELS:
            continue
        path = sample_dir / "sampling" / "CBS" / "flux_statistics.h5ad"
        if path.exists():
            paths.append((sample_dir.name, path))
    return paths


def summarize_vector(values: np.ndarray) -> dict[str, float]:
    values = np.asarray(values, dtype=float)
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return {
            "mean": float("nan"),
            "median": float("nan"),
            "q25": float("nan"),
            "q75": float("nan"),
            "pct_negative": float("nan"),
            "pct_positive": float("nan"),
            "pct_zero": float("nan"),
        }
    return {
        "mean": float(np.mean(finite)),
        "median": float(np.median(finite)),
        "q25": float(np.quantile(finite, 0.25)),
        "q75": float(np.quantile(finite, 0.75)),
        "pct_negative": float(np.mean(finite < 0)),
        "pct_positive": float(np.mean(finite > 0)),
        "pct_zero": float(np.mean(finite == 0)),
    }


def read_sample(sample_key: str, path: Path) -> tuple[list[dict[str, object]], dict[str, np.ndarray]]:
    cohort, sample, sample_type, technology = SAMPLE_LABELS[sample_key]
    rows: list[dict[str, object]] = []
    vectors: dict[str, np.ndarray] = {}
    with h5py.File(path, "r") as handle:
        var_names = decode(handle["var"]["_index"][:])
        reaction_to_idx = {reaction: idx for idx, reaction in enumerate(var_names)}
        n_obs = handle["X"].shape[0]
        obs_ratio_columns = [key for key in handle["obs"].keys() if key.endswith("_mean")]
        ratio_values = {
            key: np.asarray(handle["obs"][key][:], dtype=float)
            for key in obs_ratio_columns
        }
        for reaction, description in REACTIONS.items():
            if reaction not in reaction_to_idx:
                continue
            idx = reaction_to_idx[reaction]
            normalized = np.asarray(handle["X"][:, idx], dtype=float)
            mean_flux = np.asarray(handle["layers"]["mean"][:, idx], dtype=float)
            vectors[reaction] = normalized
            for metric_name, vector in [("meanNormalized", normalized), ("meanFlux", mean_flux)]:
                stats = summarize_vector(vector)
                row = {
                    "cohort": cohort,
                    "sample_key": sample_key,
                    "sample": sample,
                    "sample_type": sample_type,
                    "technology": technology,
                    "n_spots": n_obs,
                    "reaction": reaction,
                    "description": description,
                    "metric": metric_name,
                }
                row.update(stats)
                rows.append(row)
        for ratio_name, vector in ratio_values.items():
            stats = summarize_vector(vector)
            row = {
                "cohort": cohort,
                "sample_key": sample_key,
                "sample": sample,
                "sample_type": sample_type,
                "technology": technology,
                "n_spots": n_obs,
                "reaction": ratio_name,
                "description": "precomputed_ratio_from_spfba",
                "metric": "obs",
            }
            row.update(stats)
            rows.append(row)
    return rows, vectors


def rankdata(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    ranks[order] = np.arange(len(values), dtype=float)
    unique_values, inverse, counts = np.unique(values, return_inverse=True, return_counts=True)
    del unique_values
    sums = np.bincount(inverse, weights=ranks)
    mean_ranks = sums / counts
    return mean_ranks[inverse]


def correlation(x: np.ndarray, y: np.ndarray, method: str = "pearson") -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    valid = np.isfinite(x) & np.isfinite(y)
    if valid.sum() < 3:
        return float("nan")
    xv = x[valid]
    yv = y[valid]
    if method == "spearman":
        xv = rankdata(xv)
        yv = rankdata(yv)
    xsd = np.std(xv)
    ysd = np.std(yv)
    if xsd == 0 or ysd == 0:
        return float("nan")
    return float(np.corrcoef(xv, yv)[0, 1])


def build_correlation_rows(sample_vectors: dict[str, dict[str, np.ndarray]]) -> list[dict[str, object]]:
    targets = [
        "PYRt2m",
        "PDHm",
        "LDH_L",
        "ASPTA",
        "ASPTAm",
        "ASPGLUm",
        "ALATA_L",
        "GLUN",
        "GLUNm",
        "GLUDym",
        "AKGDm",
        "AKGMALtm",
        "MDHm",
        "MDH",
        "CSm",
        "Biomass",
        "ATPS4mi",
    ]
    rows: list[dict[str, object]] = []
    for sample_key, vectors in sorted(sample_vectors.items()):
        if "EX_lac__L_e" not in vectors:
            continue
        cohort, sample, sample_type, technology = SAMPLE_LABELS[sample_key]
        lactate_uptake = -vectors["EX_lac__L_e"]
        for target in targets:
            if target not in vectors:
                continue
            target_values = vectors[target]
            rows.append({
                "cohort": cohort,
                "sample_key": sample_key,
                "sample": sample,
                "sample_type": sample_type,
                "technology": technology,
                "anchor": "lactate_uptake_score_minus_EX_lac__L_e",
                "target_reaction": target,
                "target_description": REACTIONS.get(target, ""),
                "pearson_r": correlation(lactate_uptake, target_values, "pearson"),
                "spearman_r": correlation(lactate_uptake, target_values, "spearman"),
                "n_spots": len(lactate_uptake),
            })
    return rows


def build_comparisons(summary_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    comparisons: list[dict[str, object]] = []
    wanted = [
        "EX_lac__L_e",
        "PYRt2m",
        "PDHm",
        "ASPTA",
        "ASPTAm",
        "AKGMALtm",
        "MDHm",
        "Biomass",
        "lac_glc_mean",
        "o2_lac_mean",
    ]
    by_reaction_metric: dict[tuple[str, str], list[dict[str, object]]] = {}
    for row in summary_rows:
        if row["cohort"] != "SC087":
            continue
        key = (str(row["reaction"]), str(row["metric"]))
        by_reaction_metric.setdefault(key, []).append(row)
    for reaction in wanted:
        for metric in ["meanNormalized", "meanFlux", "obs"]:
            rows = by_reaction_metric.get((reaction, metric), [])
            if not rows:
                continue
            primary = [row for row in rows if row["sample_type"] == "primary"]
            metastasis = [row for row in rows if row["sample_type"] == "liver_metastasis"]
            if not primary or not metastasis:
                continue
            primary_mean = float(primary[0]["mean"])
            lm_means = [float(row["mean"]) for row in metastasis]
            lm_mean = float(np.mean(lm_means))
            comparisons.append({
                "cohort": "SC087",
                "reaction": reaction,
                "metric": metric,
                "primary_sample": primary[0]["sample"],
                "primary_mean": primary_mean,
                "lm_samples": ",".join(str(row["sample"]) for row in metastasis),
                "lm_mean_of_sample_means": lm_mean,
                "lm_minus_primary": lm_mean - primary_mean,
                "direction_hint": direction_hint(reaction, lm_mean - primary_mean),
            })
    return comparisons


def direction_hint(reaction: str, delta: float) -> str:
    if reaction == "EX_lac__L_e":
        if delta < 0:
            return "LM_more_lactate_uptake_or_less_export_than_PT"
        if delta > 0:
            return "LM_more_lactate_export_or_less_uptake_than_PT"
    if reaction == "EX_glc__D_e" and delta < 0:
        return "LM_more_glucose_uptake_or_less_export_than_PT"
    if reaction in {"PYRt2m", "PDHm", "ASPTA", "ASPTAm", "AKGMALtm", "MDHm", "Biomass"}:
        if delta > 0:
            return "LM_higher_forward_FES_than_PT"
        if delta < 0:
            return "LM_lower_forward_FES_than_PT"
    return "sign_reaction_specific"


def write_report(
    summary_rows: list[dict[str, object]],
    comparisons: list[dict[str, object]],
    correlation_rows: list[dict[str, object]],
    path: Path,
) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    sc087 = [
        row for row in summary_rows
        if row["cohort"] == "SC087"
        and row["metric"] == "meanNormalized"
        and row["reaction"] in {"EX_lac__L_e", "PYRt2m", "PDHm", "ASPTA", "ASPTAm", "AKGMALtm", "MDHm", "Biomass"}
    ]
    lactate_rows = [
        row for row in summary_rows
        if row["metric"] == "meanNormalized"
        and row["reaction"] == "EX_lac__L_e"
    ]
    top_couplings = sorted(
        [
            row for row in correlation_rows
            if row["target_reaction"] in {"PDHm", "ASPTA", "ASPTAm", "AKGMALtm", "MDHm", "Biomass"}
            and math.isfinite(float(row["spearman_r"]))
        ],
        key=lambda row: float(row["spearman_r"]),
        reverse=True,
    )[:18]
    lines = [
        "# spFBA/FES flux statistics summary",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Scope",
        "",
        "Summarizes selected reaction-level FES metrics from Zenodo 13988866 `output.tar.gz` without expanding the full archive. The key files are `flux_statistics.h5ad` under `output/*/sampling/CBS/`.",
        "",
        "## Sign Convention",
        "",
        "- `meanNormalized` is `.X` in `flux_statistics.h5ad`: sampled mean flux normalized by the FVA range.",
        "- `EX_lac__L_e < 0` is interpreted as lactate uptake/consumption; `EX_lac__L_e > 0` as lactate export/secretion.",
        "- Internal reaction signs are reaction-definition specific; compare directions cautiously.",
        "",
        "## SC087 Colorectal Stereo-seq Mean-Normalized FES",
        "",
        "| Sample | Type | Reaction | Mean | Median | % negative | % positive |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in sc087:
        lines.append(
            f"| {row['sample']} | {row['sample_type']} | `{row['reaction']}` | "
            f"{fmt(float(row['mean']))} | {fmt(float(row['median']))} | "
            f"{fmt(float(row['pct_negative']) * 100, 1)} | {fmt(float(row['pct_positive']) * 100, 1)} |"
        )
    lines.extend([
        "",
        "## Lactate Exchange Across CRC Samples",
        "",
        "`EX_lac__L_e < 0` means lactate uptake/consumption. The SC087 liver metastases show widespread lactate uptake, but the paired SC087 primary is even more negative on average. The CRC VisiumHD samples are mixed and should not be treated as metastasis-specific without matching annotations.",
        "",
        "| Cohort | Sample | Type | Technology | Spots | Mean | Median | % negative | % positive |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in lactate_rows:
        lines.append(
            f"| {row['cohort']} | {row['sample']} | {row['sample_type']} | {row['technology']} | "
            f"{row['n_spots']} | {fmt(float(row['mean']))} | {fmt(float(row['median']))} | "
            f"{fmt(float(row['pct_negative']) * 100, 1)} | {fmt(float(row['pct_positive']) * 100, 1)} |"
        )
    lines.extend([
        "",
        "## LM-vs-PT Directional Snapshot",
        "",
        "| Reaction | Metric | PT mean | LM mean | LM-PT | Direction hint |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for row in comparisons:
        if row["metric"] != "meanNormalized":
            continue
        lines.append(
            f"| `{row['reaction']}` | {row['metric']} | {fmt(float(row['primary_mean']))} | "
            f"{fmt(float(row['lm_mean_of_sample_means']))} | {fmt(float(row['lm_minus_primary']))} | "
            f"{row['direction_hint']} |"
        )
    lines.extend([
        "",
        "## Strongest Lactate Uptake Couplings Across CRC Samples",
        "",
        "`lactate_uptake_score = -EX_lac__L_e`; positive Spearman r means stronger lactate uptake co-occurs with higher target FES in the same sample.",
        "",
        "| Cohort | Sample | Type | Target | Pearson r | Spearman r | Spots |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in top_couplings:
        lines.append(
            f"| {row['cohort']} | {row['sample']} | {row['sample_type']} | `{row['target_reaction']}` | "
            f"{fmt(float(row['pearson_r']))} | {fmt(float(row['spearman_r']))} | {row['n_spots']} |"
        )
    corr_subset = [
        row for row in correlation_rows
        if row["cohort"] == "SC087"
        and row["target_reaction"] in {"PYRt2m", "PDHm", "ASPTA", "ASPTAm", "AKGMALtm", "MDHm", "Biomass"}
    ]
    lines.extend([
        "",
        "## Lactate Uptake Coupling Within SC087 Samples",
        "",
        "`lactate_uptake_score = -EX_lac__L_e`; positive correlation means stronger lactate uptake co-occurs with higher target FES.",
        "",
        "| Sample | Type | Target | Pearson r | Spearman r |",
        "| --- | --- | --- | --- | --- |",
    ])
    for row in corr_subset:
        lines.append(
            f"| {row['sample']} | {row['sample_type']} | `{row['target_reaction']}` | "
            f"{fmt(float(row['pearson_r']))} | {fmt(float(row['spearman_r']))} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- These FES samples are not the same sections as GSE225857/GSE217414, so they cannot directly validate spot-level HLA-DRB5 neighborhoods from our earlier Visium analyses.",
        "- They can test whether an independent colorectal primary/metastasis dataset contains the lactate/pyruvate/transamination flux phenotype required by the hypothesis.",
        "- A rescue of the HLA-DRB5/lactate branch would still require either expression/annotation from the same spFBA samples or a registered spatial link between immune modules and FES maps.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extracted-output", type=Path, default=DEFAULT_EXTRACTED)
    args = parser.parse_args()

    all_rows: list[dict[str, object]] = []
    sample_vectors: dict[str, dict[str, np.ndarray]] = {}
    for sample_key, path in sample_paths(args.extracted_output):
        rows, vectors = read_sample(sample_key, path)
        all_rows.extend(rows)
        sample_vectors[sample_key] = vectors
    comparisons = build_comparisons(all_rows)
    correlation_rows = build_correlation_rows(sample_vectors)
    write_tsv(all_rows, OUT_DIR / "spfba_flux_selected_reaction_summary.tsv")
    write_tsv(comparisons, OUT_DIR / "spfba_flux_lm_vs_pt_comparisons.tsv")
    write_tsv(correlation_rows, OUT_DIR / "spfba_lactate_uptake_correlation_summary.tsv")
    write_report(all_rows, comparisons, correlation_rows, OUT_DIR / "spfba_flux_summary_report.md")
    print(f"Summary rows: {len(all_rows)}")
    print(f"Comparisons: {len(comparisons)}")
    print(f"Correlation rows: {len(correlation_rows)}")
    print("Report: spfba_flux_summary_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
