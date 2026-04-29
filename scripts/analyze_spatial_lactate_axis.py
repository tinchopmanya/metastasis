#!/usr/bin/env python3
"""Explore a lactate-consumption metabolic angle for the CRLM niche.

The 2026 spFBA paper suggests CRC liver metastases may consume lactate rather
than simply secrete it through canonical Warburg metabolism. This script asks a
first-pass, deliberately proxy-based question in our spatial datasets:

Do CXCL12/FN1/CD44-like or HLA-DRB5-like regions sit near spots with lactate
import/anabolic-metabolism proxies, and are those regions also adjacent to the
MYC/glycolysis program?

This is not flux inference. It is a fast hypothesis generator to decide whether
spFBA/lactate should become the next serious branch.
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


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_manifest" / "generated"
GSE225857_SPOTS = OUT_DIR / "gse225857_spatial_2026_spot_scores.tsv"
GSE217414_SPOTS = OUT_DIR / "gse217414_spatial_spot_scores.tsv"
GSE225857_RAW = OUT_DIR / "gse225857_spatial_raw"
GSE217414_RAW = OUT_DIR / "gse217414_spatial_raw"

GSE225857_FILES = {
    "L1": "GSM7058760_L1",
    "L2": "GSM7058761_L2",
}

GSE217414_FILES = {
    "19G081": "GSM6716963_19G081_filtered_feature_bc_matrix.h5",
    "19G0619": "GSM6716964_19G0619_filtered_feature_bc_matrix.h5",
    "19G0635": "GSM6716965_19G0635_filtered_feature_bc_matrix.h5",
    "19G02977": "GSM6716966_19G02977_filtered_feature_bc_matrix.h5",
}

EXTRA_GENES = [
    "SLC16A1",
    "SLC16A3",
    "PDHA1",
    "PDHB",
    "MPC1",
    "MPC2",
    "GOT1",
    "GOT2",
    "IDH1",
    "IDH2",
    "ACLY",
    "ACSS2",
    "CS",
    "MDH1",
    "MDH2",
    "GLUD1",
    "GLS",
    "SLC2A1",
    "HK2",
    "PGK1",
    "ENO1",
    "MYC",
]

PROXY_SIGNATURES = {
    # No LDHB is available in the tested Visium feature universes, so this is
    # an import/anabolic proxy rather than a true lactate flux signature.
    "score_lactate_import_anabolic_proxy": [
        "SLC16A1",
        "MPC1",
        "MPC2",
        "GOT1",
        "GOT2",
        "IDH2",
        "ACLY",
        "ACSS2",
    ],
    "score_pyruvate_mito_entry_proxy": ["MPC1", "MPC2", "PDHA1", "PDHB"],
    "score_tca_malate_proxy": ["CS", "MDH1", "MDH2", "IDH2"],
    "score_lactate_export_glycolytic_proxy": ["SLC16A3", "SLC2A1", "HK2", "PGK1", "ENO1"],
    "score_glutamate_transamination_proxy": ["GOT1", "GOT2", "GLUD1", "GLS"],
}

EFFECTS = [
    ("cxcl12_fn1_cd44_to_lactate_import_anabolic", "score_spp1_cxcl12_axis_desoverlap_2026", "score_lactate_import_anabolic_proxy"),
    ("hla_drb5_to_lactate_import_anabolic", "score_hla_drb5_macrophage_axis_desoverlap_2026", "score_lactate_import_anabolic_proxy"),
    ("cxcl12_fn1_cd44_to_lactate_export_glycolytic", "score_spp1_cxcl12_axis_desoverlap_2026", "score_lactate_export_glycolytic_proxy"),
    ("hla_drb5_to_lactate_export_glycolytic", "score_hla_drb5_macrophage_axis_desoverlap_2026", "score_lactate_export_glycolytic_proxy"),
    ("lactate_import_anabolic_to_myc_glycolysis", "score_lactate_import_anabolic_proxy", "score_myc_glycolysis_desoverlap_2026"),
    ("lactate_export_glycolytic_to_myc_glycolysis", "score_lactate_export_glycolytic_proxy", "score_myc_glycolysis_desoverlap_2026"),
    ("cxcl12_fn1_cd44_to_pyruvate_mito_entry", "score_spp1_cxcl12_axis_desoverlap_2026", "score_pyruvate_mito_entry_proxy"),
    ("hla_drb5_to_pyruvate_mito_entry", "score_hla_drb5_macrophage_axis_desoverlap_2026", "score_pyruvate_mito_entry_proxy"),
    ("cxcl12_fn1_cd44_to_glutamate_transamination", "score_spp1_cxcl12_axis_desoverlap_2026", "score_glutamate_transamination_proxy"),
    ("hla_drb5_to_glutamate_transamination", "score_hla_drb5_macrophage_axis_desoverlap_2026", "score_glutamate_transamination_proxy"),
]

HEX_NEIGHBOR_OFFSETS = [
    (0, 2),
    (0, -2),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
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


def read_gse225857_gene_logs(sample: str, genes: set[str]) -> dict[str, dict[str, float]]:
    prefix = GSE225857_FILES[sample]
    barcodes_path = GSE225857_RAW / f"{prefix}.barcodes.tsv.gz"
    features_path = GSE225857_RAW / f"{prefix}.features.tsv.gz"
    matrix_path = GSE225857_RAW / f"{prefix}.matrix.mtx.gz"
    with gzip.open(barcodes_path, "rt", encoding="utf-8") as handle:
        barcodes = [line.strip() for line in handle if line.strip()]
    row_to_gene: dict[int, str] = {}
    with gzip.open(features_path, "rt", encoding="utf-8") as handle:
        for idx, line in enumerate(handle, start=1):
            parts = line.rstrip("\n").split("\t")
            if len(parts) > 1 and parts[1].upper() in genes:
                row_to_gene[idx] = parts[1].upper()
    values: dict[str, dict[str, float]] = {gene: defaultdict(float) for gene in set(row_to_gene.values())}
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
            barcode = barcodes[int(col_idx) - 1]
            values[gene][barcode] += float(raw_value)
    return {
        gene: {barcode: math.log1p(value) for barcode, value in barcode_values.items()}
        for gene, barcode_values in values.items()
    }


def read_gse217414_gene_logs(sample: str, genes: set[str]) -> dict[str, dict[str, float]]:
    path = GSE217414_RAW / GSE217414_FILES[sample]
    with h5py.File(path, "r") as handle:
        matrix = handle["matrix"]
        barcodes = [value.decode("utf-8") for value in matrix["barcodes"][:]]
        feature_names = [value.decode("utf-8").upper() for value in matrix["features"]["name"][:]]
        target_rows = {
            idx: gene for idx, gene in enumerate(feature_names)
            if gene in genes
        }
        values: dict[str, dict[str, float]] = {gene: defaultdict(float) for gene in set(target_rows.values())}
        data = matrix["data"][:]
        indices = matrix["indices"][:]
        indptr = matrix["indptr"][:]
        for col_idx, barcode in enumerate(barcodes):
            start = int(indptr[col_idx])
            end = int(indptr[col_idx + 1])
            for row_idx, raw_value in zip(indices[start:end], data[start:end]):
                gene = target_rows.get(int(row_idx))
                if gene:
                    values[gene][barcode] += float(raw_value)
    return {
        gene: {barcode: math.log1p(value) for barcode, value in barcode_values.items()}
        for gene, barcode_values in values.items()
    }


def score_genes(row: dict[str, object], genes: list[str]) -> float:
    return mean([as_float(row.get(gene, float("nan"))) for gene in genes])


def load_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in read_tsv(GSE225857_SPOTS):
        if row.get("tissue") != "LCT":
            continue
        converted: dict[str, object] = {"dataset": "GSE225857", "sample": row["sample_id"]}
        converted.update(row)
        rows.append(converted)
    for row in read_tsv(GSE217414_SPOTS):
        converted = {"dataset": "GSE217414"}
        converted.update(row)
        rows.append(converted)

    by_dataset_sample: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_dataset_sample[(str(row["dataset"]), str(row["sample"]))].append(row)

    genes = set(EXTRA_GENES)
    for (dataset, sample), sample_rows in by_dataset_sample.items():
        if dataset == "GSE225857":
            gene_logs = read_gse225857_gene_logs(sample, genes)
        else:
            gene_logs = read_gse217414_gene_logs(sample, genes)
        for row in sample_rows:
            barcode = str(row["barcode"])
            for gene in genes:
                row[gene] = gene_logs.get(gene, {}).get(barcode, 0.0)
            for score_name, score_genes_list in PROXY_SIGNATURES.items():
                row[score_name] = score_genes(row, score_genes_list)
    return rows


def group_rows(rows: list[dict[str, object]]) -> dict[tuple[str, str], list[dict[str, object]]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["dataset"]), str(row["sample"]))].append(row)
    return grouped


def adjacency_regions(sample_rows: list[dict[str, object]], source_values: list[float]) -> tuple[set[int], set[int], set[int]]:
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
    return high_idxs, neighbor_idxs, background_idxs


def ratio_delta(values: list[float], neighbor_idxs: set[int], background_idxs: set[int]) -> tuple[float, float, float, float]:
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
    high_idxs, neighbor_idxs, background_idxs = adjacency_regions(sample_rows, source_values)
    neighbor_mean, background_mean, observed_delta, observed_ratio = ratio_delta(target_values, neighbor_idxs, background_idxs)
    blocks = spatial_blocks(sample_rows, block_size)
    rng = random.Random(stable_seed(seed, f"{dataset}:{sample}:{effect_id}"))
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
        "source": source,
        "target": target,
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


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["effect_id"])].append(row)
    summary_rows: list[dict[str, object]] = []
    for effect_id, effect_rows in sorted(grouped.items()):
        ratios = [as_float(row["observed_ratio"]) for row in effect_rows]
        deltas = [as_float(row["observed_delta"]) for row in effect_rows]
        ps = [as_float(row["block_empirical_p_delta_ge_observed"]) for row in effect_rows]
        summary_rows.append({
            "effect_id": effect_id,
            "n_samples": len(effect_rows),
            "positive_ratio_samples": sum(1 for value in ratios if value > 1),
            "positive_delta_samples": sum(1 for value in deltas if value > 0),
            "block_delta_p_le_0_05": sum(1 for value in ps if value <= 0.05),
            "mean_ratio": mean(ratios),
            "mean_delta": mean(deltas),
            "mean_block_p": mean(ps),
            "status": classify(effect_rows),
        })
    return summary_rows


def classify(rows: list[dict[str, object]]) -> str:
    n = len(rows)
    positive = sum(1 for row in rows if as_float(row["observed_delta"]) > 0)
    significant = sum(1 for row in rows if as_float(row["block_empirical_p_delta_ge_observed"]) <= 0.05)
    if positive == n and significant >= n - 1:
        return "strong_lactate_proxy_adjacency"
    if positive == n and significant >= math.ceil(n / 2):
        return "partial_lactate_proxy_adjacency"
    if positive == n:
        return "positive_but_block_explained"
    return "mixed_or_weak"


def write_report(rows: list[dict[str, object]], summary_rows: list[dict[str, object]], path: Path) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    strong_rows = [
        row for row in summary_rows
        if row["status"] == "strong_lactate_proxy_adjacency"
    ]
    lines = [
        "# Spatial lactate-axis exploratory analysis",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "",
        "Explore whether the CRLM stromal/myeloid niche connects to lactate-import/anabolic metabolism proxies inspired by the 2026 spFBA lactate-consumption result.",
        "",
        "## Caveat",
        "",
        "This is not spFBA and not metabolite flux. It is a transcript proxy screen using genes available in the current Visium feature universes. LDHB/LDHA were not available in the tested feature sets, so lactate import/export labels are approximate.",
        "",
        "## Summary",
        "",
        "| Effect | Samples | Positive delta | Block p<=0.05 | Mean ratio | Mean delta | Status |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summary_rows:
        lines.append(
            f"| `{row['effect_id']}` | {row['n_samples']} | {row['positive_delta_samples']}/{row['n_samples']} | "
            f"{row['block_delta_p_le_0_05']}/{row['n_samples']} | {fmt(float(row['mean_ratio']))} | "
            f"{fmt(float(row['mean_delta']))} | {row['status']} |"
        )
    if strong_rows:
        lines.extend([
            "",
            "## Strongest current signal",
            "",
        ])
        for row in strong_rows:
            lines.append(
                f"- `{row['effect_id']}` survived block permutation in "
                f"{row['block_delta_p_le_0_05']}/{row['n_samples']} samples "
                f"(mean ratio {fmt(float(row['mean_ratio']))}, mean block p {fmt(float(row['mean_block_p']))})."
            )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- The HLA-DRB5-like myeloid source is currently more interesting than the CXCL12/FN1/CD44-like source for this branch because its pyruvate-entry and glutamate-transamination adjacencies survive block permutation in 5/6 samples.",
        "- This does not prove lactate flux. It suggests a spatial bridge between an immune myeloid state and the non-canonical pyruvate/transamination route described by recent spFBA work.",
        "- If both import/anabolic and export/glycolytic proxies move together, part of the signal may still be a broad regional metabolic program rather than a specific lactate economy.",
        "- The strongest next step is to obtain the spFBA 2026 processed flux outputs or run spFBA-like analysis directly, then test whether HLA-DRB5-like neighborhoods predict lactate-consumption flux maps.",
        "",
        "## Literature anchors",
        "",
        "- spFBA 2026 lactate-consumption paper: https://www.nature.com/articles/s41540-026-00654-x",
        "- HLA-DRB5+ macrophage CRLM paper: https://link.springer.com/article/10.1186/s12967-026-07853-4",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--permutations", type=int, default=500)
    parser.add_argument("--block-size", type=int, default=12)
    parser.add_argument("--seed", type=int, default=97)
    args = parser.parse_args()

    rows = load_rows()
    grouped = group_rows(rows)
    effect_rows: list[dict[str, object]] = []
    for (dataset, sample), sample_rows in sorted(grouped.items()):
        for effect_id, source, target in EFFECTS:
            effect_rows.append(
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
    summary_rows = summarize(effect_rows)
    write_tsv(effect_rows, OUT_DIR / "spatial_lactate_axis_effects.tsv")
    write_tsv(summary_rows, OUT_DIR / "spatial_lactate_axis_summary.tsv")
    write_report(effect_rows, summary_rows, OUT_DIR / "spatial_lactate_axis_report.md")
    print(f"Rows: {len(effect_rows)}")
    print(f"Summary rows: {len(summary_rows)}")
    print("Report: spatial_lactate_axis_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
