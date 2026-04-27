#!/usr/bin/env python3
"""2026 layered-niche spatial analysis for GSE225857.

This script extends the previous GSE225857 Visium analysis from the original
CAF/MET/MYC/glycolysis axis into the 2026 literature pivot: CAF-high metabolic
interfaces plus SPP1/CXCL12/HLA-DRB5 myeloid/T-cell interfaces.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from analyze_gse225857_spatial import (
    DEFAULT_OUT_DIR,
    DEFAULT_RAW_DIR,
    HEX_NEIGHBOR_OFFSETS,
    SAMPLES,
    ensure_sample_files,
    extract_gene_counts,
    fmt,
    log_value,
    mean,
    pearson,
    percentile,
    read_barcodes,
    read_features,
    read_positions,
    ratio_for_indices,
    stable_seed,
    write_tsv,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SIGNATURES = DEFAULT_OUT_DIR / "signatures_normalized.tsv"

SELECTED_SIGNATURES = [
    "caf_core",
    "mcam_caf",
    "myc_glycolysis_core",
    "cxcl13_t_cells",
    "spp1_cxcl12_caf_myeloid_axis",
    "spp1_macrophage_fads1_pdgfb_axis",
    "hla_drb5_macrophage_axis",
    "stromal_myeloid_risk_2026",
    "sema3c_nrp2_lmic_axis",
    "crlm_metabolic_vulnerabilities_2026",
    "radioresistance_morf4l1",
    "marco_cash_macrophage_axis",
    "glut1_invasive_margin_axis",
    "caf_core_desoverlap_2026",
    "spp1_cxcl12_axis_desoverlap_2026",
    "hla_drb5_macrophage_axis_desoverlap_2026",
    "myc_glycolysis_desoverlap_2026",
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


def score_col(signature_id: str) -> str:
    return f"score_{signature_id}"


def read_signatures(path: Path, selected: list[str]) -> dict[str, list[str]]:
    signatures: dict[str, list[str]] = {signature_id: [] for signature_id in selected}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            signature_id = row["signature_id"]
            if signature_id in signatures:
                signatures[signature_id].append(row["gene_symbol"].upper())
    return {key: genes for key, genes in signatures.items() if genes}


def build_spot_rows_2026(
    sample_id: str,
    paths: dict[str, Path],
    target_genes: set[str],
    signatures: dict[str, list[str]],
) -> tuple[list[dict[str, str | float]], dict[str, list[str]]]:
    info = SAMPLES[sample_id]
    barcodes = read_barcodes(paths["barcodes"])
    row_to_gene = read_features(paths["features"], target_genes)
    present_genes = set(row_to_gene.values())
    positions = read_positions(paths["positions"])
    gene_counts = extract_gene_counts(paths["matrix"], barcodes, row_to_gene)
    usable_signature_genes = {
        signature_id: [gene for gene in genes if gene in present_genes]
        for signature_id, genes in signatures.items()
    }

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
        for gene in sorted(target_genes):
            row[gene] = log_value(gene_counts, gene, barcode)
        for signature_id, genes in usable_signature_genes.items():
            row[score_col(signature_id)] = mean([float(row[gene]) for gene in genes])
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


def compute_correlations(
    rows: list[dict[str, str | float]],
    pairs: list[tuple[str, str]],
) -> list[dict[str, str | float]]:
    results: list[dict[str, str | float]] = []
    by_sample: dict[str, list[dict[str, str | float]]] = defaultdict(list)
    for row in rows:
        by_sample[str(row["sample_id"])].append(row)
    for sample_id, sample_rows in sorted(by_sample.items()):
        tissue = str(sample_rows[0]["tissue"])
        for x_name, y_name in pairs:
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


def compute_adjacency_permutations(
    rows: list[dict[str, str | float]],
    sources: list[str],
    targets: list[str],
    permutations: int,
    seed: int,
    tissue_filter: str,
) -> list[dict[str, str | float]]:
    results: list[dict[str, str | float]] = []
    by_sample: dict[str, list[dict[str, str | float]]] = defaultdict(list)
    for row in rows:
        by_sample[str(row["sample_id"])].append(row)

    for sample_id, sample_rows in sorted(by_sample.items()):
        tissue = str(sample_rows[0]["tissue"])
        if tissue_filter and tissue != tissue_filter:
            continue
        for source in sources:
            threshold, high_idxs, neighbor_idxs, background_idxs = adjacency_regions(sample_rows, source)
            for target in targets:
                target_values = [float(row[target]) for row in sample_rows]
                observed_neighbor_mean, observed_background_mean, observed_ratio = ratio_for_indices(
                    target_values,
                    neighbor_idxs,
                    background_idxs,
                )
                rng = random.Random(stable_seed(seed, f"2026:{sample_id}:{source}:{target}"))
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


def summarize_signature_availability(
    signatures: dict[str, list[str]],
    usable_by_sample: dict[str, dict[str, list[str]]],
) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for sample_id, usable in sorted(usable_by_sample.items()):
        for signature_id, genes in signatures.items():
            present = usable.get(signature_id, [])
            rows.append({
                "sample_id": sample_id,
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
    lines = [
        "# GSE225857 spatial 2026 layered-niche analysis",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "Test the 2026 pivot from a linear HGF-MET-MYC model to a CAF-high layered niche model with metabolic and immunosuppressive interfaces.",
        "",
        "## Signature Availability",
        "",
        "| Sample | Signature | Usable / Expected | Usable genes |",
        "| --- | --- | --- | --- |",
    ]
    for row in availability:
        if row["sample_id"] not in {"L1", "L2"}:
            continue
        lines.append(
            f"| {row['sample_id']} | `{row['signature_id']}` | {row['usable_genes']} / {row['expected_genes']} | `{row['usable_gene_symbols']}` |"
        )

    key_pairs = [
        (score_col("caf_core"), score_col("spp1_cxcl12_caf_myeloid_axis")),
        (score_col("mcam_caf"), score_col("spp1_cxcl12_caf_myeloid_axis")),
        (score_col("caf_core"), score_col("hla_drb5_macrophage_axis")),
        (score_col("spp1_cxcl12_caf_myeloid_axis"), score_col("hla_drb5_macrophage_axis")),
        (score_col("spp1_cxcl12_caf_myeloid_axis"), score_col("myc_glycolysis_core")),
        (score_col("hla_drb5_macrophage_axis"), score_col("myc_glycolysis_core")),
        (score_col("caf_core_desoverlap_2026"), score_col("spp1_cxcl12_axis_desoverlap_2026")),
        (score_col("caf_core_desoverlap_2026"), score_col("hla_drb5_macrophage_axis_desoverlap_2026")),
        (score_col("spp1_cxcl12_axis_desoverlap_2026"), score_col("myc_glycolysis_desoverlap_2026")),
        (score_col("hla_drb5_macrophage_axis_desoverlap_2026"), score_col("myc_glycolysis_desoverlap_2026")),
        ("SPP1", "CXCL12"),
        ("SPP1", "CD44"),
        ("MIF", "CXCR4"),
        ("HLA-DRB5", "LGALS9"),
    ]
    lines.extend([
        "",
        "## LCT Key Correlations",
        "",
        "| Sample | Pair | r | Spots |",
        "| --- | --- | --- | --- |",
    ])
    for row in correlations:
        if row["tissue"] != "LCT":
            continue
        if (row["x"], row["y"]) not in key_pairs:
            continue
        lines.append(
            f"| {row['sample_id']} | `{row['x']}~{row['y']}` | {fmt(float(row['pearson_r']))} | {row['n_spots']} |"
        )

    lines.extend([
        "",
        "## LCT Adjacency With Permutation Null",
        "",
        "| Sample | Source | Target | Observed ratio | Null mean | z | Empirical p >= observed |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in adjacency:
        if row["source"] == row["target"]:
            continue
        lines.append(
            f"| {row['sample_id']} | `{row['source']}` | `{row['target']}` | "
            f"{fmt(float(row['observed_neighbor_vs_background_ratio']))} | "
            f"{fmt(float(row['null_ratio_mean']))} | {fmt(float(row['z_score']))} | "
            f"{fmt(float(row['empirical_p_ge_observed']))} |"
        )

    def lct_values(source: str, target: str, field: str) -> list[float]:
        return [
            float(row[field]) for row in adjacency
            if row["source"] == source and row["target"] == target
            and not math.isnan(float(row[field]))
        ]

    caf_spp1_ratio = mean(lct_values(
        score_col("caf_core"),
        score_col("spp1_cxcl12_caf_myeloid_axis"),
        "observed_neighbor_vs_background_ratio",
    ))
    caf_hla_ratio = mean(lct_values(
        score_col("caf_core"),
        score_col("hla_drb5_macrophage_axis"),
        "observed_neighbor_vs_background_ratio",
    ))
    spp1_myc_ratio = mean(lct_values(
        score_col("spp1_cxcl12_caf_myeloid_axis"),
        score_col("myc_glycolysis_core"),
        "observed_neighbor_vs_background_ratio",
    ))
    hla_myc_ratio = mean(lct_values(
        score_col("hla_drb5_macrophage_axis"),
        score_col("myc_glycolysis_core"),
        "observed_neighbor_vs_background_ratio",
    ))
    caf_spp1_desoverlap_ratio = mean(lct_values(
        score_col("caf_core_desoverlap_2026"),
        score_col("spp1_cxcl12_axis_desoverlap_2026"),
        "observed_neighbor_vs_background_ratio",
    ))
    caf_hla_desoverlap_ratio = mean(lct_values(
        score_col("caf_core_desoverlap_2026"),
        score_col("hla_drb5_macrophage_axis_desoverlap_2026"),
        "observed_neighbor_vs_background_ratio",
    ))
    spp1_myc_desoverlap_ratio = mean(lct_values(
        score_col("spp1_cxcl12_axis_desoverlap_2026"),
        score_col("myc_glycolysis_desoverlap_2026"),
        "observed_neighbor_vs_background_ratio",
    ))
    hla_myc_desoverlap_ratio = mean(lct_values(
        score_col("hla_drb5_macrophage_axis_desoverlap_2026"),
        score_col("myc_glycolysis_desoverlap_2026"),
        "observed_neighbor_vs_background_ratio",
    ))

    lines.extend([
        "",
        "## Interpretation",
        f"- Mean LCT `CAF -> SPP1/CXCL12 axis` neighbor/background ratio: {fmt(caf_spp1_ratio)}.",
        f"- Mean LCT `CAF -> HLA-DRB5 macrophage axis` neighbor/background ratio: {fmt(caf_hla_ratio)}.",
        f"- Mean LCT `SPP1/CXCL12 axis -> MYC/glycolysis` neighbor/background ratio: {fmt(spp1_myc_ratio)}.",
        f"- Mean LCT `HLA-DRB5 macrophage axis -> MYC/glycolysis` neighbor/background ratio: {fmt(hla_myc_ratio)}.",
        f"- Desoverlap control `CAF -> SPP1/CXCL12-lite` ratio: {fmt(caf_spp1_desoverlap_ratio)}.",
        f"- Desoverlap control `CAF -> HLA-DRB5-lite` ratio: {fmt(caf_hla_desoverlap_ratio)}.",
        f"- Desoverlap control `SPP1/CXCL12-lite -> MYC/glycolysis-lite` ratio: {fmt(spp1_myc_desoverlap_ratio)}.",
        f"- Desoverlap control `HLA-DRB5-lite -> MYC/glycolysis-lite` ratio: {fmt(hla_myc_desoverlap_ratio)}.",
        "- Ratios above 1 against an in-sample permutation null support spatial coupling; ratios below 1 suggest separation or compartmentalization.",
        "- The desoverlap control supports the SPP1/CXCL12 arm more robustly than the HLA-DRB5-lite arm, which is lesion-sensitive and weaker in L2.",
        "- The current signal looks more like an overlapping CAF/myeloid/tumor macro-niche than proof of sharply separated microscopic layers.",
        "",
        "## Limitations",
        "- Visium spots mix cells, so this cannot prove ligand-receptor direction or cell-cell causality.",
        "- Several 2026 signatures are broad and share genes; this can inflate coupling among scores.",
        "- Individual ligand-pair correlations are weaker than signature-level correlations, especially `SPP1~CXCL12`.",
        "- Some genes are absent from the Visium feature universe for this dataset, including `LGALS9`, `KLF2`, `SHMT1`, `TPI1`, and `LDHA` in the tested signatures.",
        "",
        "## Next Step",
        "If the 2026 immune/myeloid axes enrich near CAF-high regions, extend the report into a full investigation of whether metabolic and immunosuppressive interfaces are layered, overlapping, or spatially separated.",
        "",
    ])
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--signatures", type=Path, default=DEFAULT_SIGNATURES)
    parser.add_argument("--samples", nargs="*", default=list(SAMPLES.keys()))
    parser.add_argument("--permutations", type=int, default=200)
    parser.add_argument("--seed", type=int, default=23)
    parser.add_argument("--permutation-tissue", default="LCT")
    args = parser.parse_args()

    signatures = read_signatures(args.signatures, SELECTED_SIGNATURES)
    target_genes = set(CORE_GENES)
    for genes in signatures.values():
        target_genes.update(genes)

    all_rows: list[dict[str, str | float]] = []
    usable_by_sample: dict[str, dict[str, list[str]]] = {}
    for sample_id in args.samples:
        if sample_id not in SAMPLES:
            raise ValueError(f"Unknown sample: {sample_id}")
        print(f"[{sample_id}] scoring 2026 signatures...", flush=True)
        paths = ensure_sample_files(sample_id, args.raw_dir)
        sample_rows, usable_signature_genes = build_spot_rows_2026(
            sample_id,
            paths,
            target_genes,
            signatures,
        )
        print(f"  in-tissue spots: {len(sample_rows)}", flush=True)
        all_rows.extend(sample_rows)
        usable_by_sample[sample_id] = usable_signature_genes

    correlation_pairs = [
        (score_col("caf_core"), score_col("spp1_cxcl12_caf_myeloid_axis")),
        (score_col("mcam_caf"), score_col("spp1_cxcl12_caf_myeloid_axis")),
        (score_col("caf_core"), score_col("hla_drb5_macrophage_axis")),
        (score_col("spp1_cxcl12_caf_myeloid_axis"), score_col("hla_drb5_macrophage_axis")),
        (score_col("spp1_cxcl12_caf_myeloid_axis"), score_col("myc_glycolysis_core")),
        (score_col("hla_drb5_macrophage_axis"), score_col("myc_glycolysis_core")),
        (score_col("crlm_metabolic_vulnerabilities_2026"), score_col("myc_glycolysis_core")),
        (score_col("glut1_invasive_margin_axis"), score_col("cxcl13_t_cells")),
        (score_col("caf_core_desoverlap_2026"), score_col("spp1_cxcl12_axis_desoverlap_2026")),
        (score_col("caf_core_desoverlap_2026"), score_col("hla_drb5_macrophage_axis_desoverlap_2026")),
        (score_col("spp1_cxcl12_axis_desoverlap_2026"), score_col("myc_glycolysis_desoverlap_2026")),
        (score_col("hla_drb5_macrophage_axis_desoverlap_2026"), score_col("myc_glycolysis_desoverlap_2026")),
        ("MET", score_col("myc_glycolysis_core")),
        ("MYC", score_col("myc_glycolysis_core")),
        ("SPP1", "CXCL12"),
        ("SPP1", "CD44"),
        ("MIF", "CXCR4"),
        ("HLA-DRB5", "LGALS9"),
    ]
    adjacency_sources = [
        score_col("caf_core"),
        score_col("mcam_caf"),
        score_col("spp1_cxcl12_caf_myeloid_axis"),
        score_col("hla_drb5_macrophage_axis"),
        score_col("caf_core_desoverlap_2026"),
        score_col("spp1_cxcl12_axis_desoverlap_2026"),
        score_col("hla_drb5_macrophage_axis_desoverlap_2026"),
    ]
    adjacency_targets = [
        "MET",
        "MYC",
        score_col("myc_glycolysis_core"),
        score_col("myc_glycolysis_desoverlap_2026"),
        score_col("spp1_cxcl12_caf_myeloid_axis"),
        score_col("spp1_cxcl12_axis_desoverlap_2026"),
        score_col("hla_drb5_macrophage_axis"),
        score_col("hla_drb5_macrophage_axis_desoverlap_2026"),
        score_col("cxcl13_t_cells"),
        score_col("glut1_invasive_margin_axis"),
        score_col("crlm_metabolic_vulnerabilities_2026"),
    ]

    availability = summarize_signature_availability(signatures, usable_by_sample)
    correlations = compute_correlations(all_rows, correlation_pairs)
    adjacency = compute_adjacency_permutations(
        all_rows,
        adjacency_sources,
        adjacency_targets,
        args.permutations,
        args.seed,
        args.permutation_tissue,
    )

    write_tsv(availability, args.out_dir / "gse225857_spatial_2026_signature_availability.tsv")
    write_tsv(correlations, args.out_dir / "gse225857_spatial_2026_correlations.tsv")
    write_tsv(adjacency, args.out_dir / "gse225857_spatial_2026_adjacency_permutation.tsv")
    write_tsv(all_rows, args.out_dir / "gse225857_spatial_2026_spot_scores.tsv")
    write_report(
        availability,
        correlations,
        adjacency,
        args.out_dir / "gse225857_spatial_2026_report.md",
    )

    print(f"Samples: {len(args.samples)}")
    print(f"Spots: {len(all_rows)}")
    print(f"Permutations per LCT test: {args.permutations}")
    print("Report: gse225857_spatial_2026_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
