#!/usr/bin/env python3
"""Score CRLM gene signatures in TCGA-COAD bulk expression data.

This script:
1. Loads a gene expression matrix (samples x genes, log2-normalized).
2. Loads normalized signature gene lists.
3. Computes per-sample z-score means for each signature.
4. Computes pairwise correlations between key genes and signatures.
5. Outputs score tables and a plausibility report.

The goal is NOT to prove the mCAF-HGF-MET-MYC-glycolysis hypothesis in bulk
data (bulk cannot resolve cell types). The goal is to check whether the
correlations expected under the hypothesis are at least plausible at the
tissue level, before investing in heavier single-cell analyses.

Dependency-free: uses only Python stdlib + basic math.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPRESSION = ROOT / "data_manifest" / "generated" / "tcga_coad_expression.tsv"
DEFAULT_SIGNATURES = ROOT / "data_manifest" / "generated" / "signatures_normalized.tsv"
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_expression_matrix(path: Path) -> tuple[list[str], dict[str, list[float]]]:
    """Load expression matrix: returns (sample_ids, {gene: [values]})."""
    gene_data: dict[str, list[float]] = {}
    samples: list[str] = []

    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        samples = header[1:]  # first column is gene name

        for row in reader:
            gene = row[0].upper()
            values = []
            for v in row[1:]:
                try:
                    values.append(float(v))
                except (ValueError, IndexError):
                    values.append(float("nan"))
            gene_data[gene] = values

    return samples, gene_data


def load_signatures(path: Path) -> dict[str, list[str]]:
    """Load signature -> gene list mapping."""
    sigs: dict[str, list[str]] = defaultdict(list)
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            sigs[row["signature_id"]].append(row["gene_symbol"].upper())
    return dict(sigs)


# ---------------------------------------------------------------------------
# Statistics (stdlib only)
# ---------------------------------------------------------------------------

def mean(xs: list[float]) -> float:
    valid = [x for x in xs if not math.isnan(x)]
    return sum(valid) / len(valid) if valid else float("nan")


def std(xs: list[float]) -> float:
    valid = [x for x in xs if not math.isnan(x)]
    if len(valid) < 2:
        return float("nan")
    m = sum(valid) / len(valid)
    variance = sum((x - m) ** 2 for x in valid) / (len(valid) - 1)
    return math.sqrt(variance)


def zscore_vector(xs: list[float]) -> list[float]:
    m = mean(xs)
    s = std(xs)
    if math.isnan(s) or s == 0:
        return [0.0] * len(xs)
    return [(x - m) / s if not math.isnan(x) else float("nan") for x in xs]


def pearson_r(xs: list[float], ys: list[float]) -> tuple[float, int]:
    """Pearson correlation and n for paired non-NaN values."""
    pairs = [
        (x, y) for x, y in zip(xs, ys)
        if not math.isnan(x) and not math.isnan(y)
    ]
    n = len(pairs)
    if n < 3:
        return float("nan"), n

    mx = sum(p[0] for p in pairs) / n
    my = sum(p[1] for p in pairs) / n

    cov = sum((p[0] - mx) * (p[1] - my) for p in pairs)
    sx = math.sqrt(sum((p[0] - mx) ** 2 for p in pairs))
    sy = math.sqrt(sum((p[1] - my) ** 2 for p in pairs))

    if sx == 0 or sy == 0:
        return float("nan"), n

    return cov / (sx * sy), n


def p_value_approx(r: float, n: int) -> float:
    """Approximate two-tailed p-value for Pearson r using t-distribution.

    Uses the t = r * sqrt((n-2)/(1-r^2)) transformation.
    For large n, approximates p via normal distribution.
    """
    if math.isnan(r) or n < 3:
        return float("nan")
    if abs(r) >= 1.0:
        return 0.0

    t_stat = abs(r) * math.sqrt((n - 2) / (1 - r * r))
    # Approximate using normal for large n (>30)
    # For smaller n this is rough but sufficient for screening
    df = n - 2
    if df > 30:
        # Normal approximation
        p = 2 * (1 - _normal_cdf(t_stat))
    else:
        # Very rough approximation via Abramowitz & Stegun
        p = 2 * (1 - _t_cdf_approx(t_stat, df))
    return max(p, 1e-300)  # avoid exact zero


def _normal_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _t_cdf_approx(t: float, df: int) -> float:
    """Rough t-CDF approximation sufficient for screening."""
    # Use normal approximation with correction
    x = t * (1 - 1 / (4 * df)) / math.sqrt(1 + t * t / (2 * df))
    return _normal_cdf(x)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def compute_signature_scores(
    samples: list[str],
    gene_data: dict[str, list[float]],
    signatures: dict[str, list[str]],
) -> dict[str, list[float]]:
    """Compute per-sample signature scores as mean of gene z-scores."""
    n_samples = len(samples)
    scores: dict[str, list[float]] = {}

    for sig_id, genes in signatures.items():
        # Get z-scored expression for each gene in signature
        gene_zscores: list[list[float]] = []
        for gene in genes:
            if gene in gene_data:
                gene_zscores.append(zscore_vector(gene_data[gene]))

        if not gene_zscores:
            scores[sig_id] = [float("nan")] * n_samples
            continue

        # Mean z-score across genes for each sample
        sample_scores: list[float] = []
        for i in range(n_samples):
            vals = [gz[i] for gz in gene_zscores if not math.isnan(gz[i])]
            sample_scores.append(sum(vals) / len(vals) if vals else float("nan"))

        scores[sig_id] = sample_scores

    return scores


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_scores(
    samples: list[str],
    scores: dict[str, list[float]],
    out_path: Path,
) -> None:
    sig_ids = sorted(scores.keys())
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["sample_id", *sig_ids])
        for i, sample in enumerate(samples):
            row = [sample]
            for sid in sig_ids:
                v = scores[sid][i]
                row.append(f"{v:.6f}" if not math.isnan(v) else "NA")
            writer.writerow(row)


def write_correlations(
    correlations: list[dict],
    out_path: Path,
) -> None:
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["var_x", "var_y", "pearson_r", "p_value", "n", "interpretation"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(correlations)


def interpret_r(r: float, p: float) -> str:
    if math.isnan(r):
        return "insufficient data"
    abs_r = abs(r)
    sig = "significant" if p < 0.05 else "not significant"
    if abs_r < 0.1:
        return f"negligible ({sig})"
    elif abs_r < 0.3:
        return f"weak ({sig})"
    elif abs_r < 0.5:
        return f"moderate ({sig})"
    elif abs_r < 0.7:
        return f"strong ({sig})"
    else:
        return f"very strong ({sig})"


def write_report(
    samples: list[str],
    scores: dict[str, list[float]],
    gene_data: dict[str, list[float]],
    correlations: list[dict],
    signatures: dict[str, list[str]],
    out_path: Path,
) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# CRLM bulk plausibility report: TCGA-COAD",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "",
        "This report checks whether correlations expected under the",
        "`mCAF-HGF-MET-MYC-glycolysis` hypothesis are plausible at the bulk",
        "tissue level in TCGA-COAD primary tumors. Bulk data cannot resolve",
        "cell types, so positive correlations are necessary but not sufficient",
        "evidence. Absence of correlation in bulk would weaken (not disprove)",
        "the hypothesis.",
        "",
        "## Data source",
        "",
        "- TCGA-COAD HiSeqV2 from UCSC Xena (log2 normalized counts).",
        f"- Samples: {len(samples)}.",
        f"- Genes in matrix: {len(gene_data)}.",
        f"- Signatures scored: {len(signatures)}.",
        "",
        "## Signature score summary",
        "",
        "| Signature | Genes | Score mean | Score SD | Score range |",
        "| --- | --- | --- | --- | --- |",
    ]

    for sig_id in sorted(scores.keys()):
        vals = [v for v in scores[sig_id] if not math.isnan(v)]
        n_genes = len(signatures.get(sig_id, []))
        if vals:
            m = sum(vals) / len(vals)
            s = std(vals)
            lo, hi = min(vals), max(vals)
            lines.append(
                f"| `{sig_id}` | {n_genes} | {m:.3f} | {s:.3f} | [{lo:.2f}, {hi:.2f}] |"
            )
        else:
            lines.append(f"| `{sig_id}` | {n_genes} | NA | NA | NA |")

    lines.extend([
        "",
        "## Key correlations",
        "",
        "| Variable X | Variable Y | Pearson r | p-value | n | Interpretation |",
        "| --- | --- | --- | --- | --- | --- |",
    ])

    for c in correlations:
        p_str = f"{float(c['p_value']):.2e}" if c['p_value'] != "NA" else "NA"
        r_str = f"{float(c['pearson_r']):.4f}" if c['pearson_r'] != "NA" else "NA"
        lines.append(
            f"| `{c['var_x']}` | `{c['var_y']}` | {r_str} | {p_str} | {c['n']} | {c['interpretation']} |"
        )

    # Overall assessment
    lines.extend([
        "",
        "## Assessment",
        "",
    ])

    # Check key correlations
    met_myc = next((c for c in correlations if c["var_x"] == "MET" and c["var_y"] == "MYC"), None)
    hgf_met = next((c for c in correlations if c["var_x"] == "HGF" and c["var_y"] == "MET"), None)
    myc_glyc = next((c for c in correlations if c["var_x"] == "MYC" and c["var_y"] == "score:myc_glycolysis_core"), None)
    met_glyc = next((c for c in correlations if c["var_x"] == "MET" and c["var_y"] == "score:myc_glycolysis_core"), None)
    caf_hgf = next((c for c in correlations if c["var_x"] == "score:caf_core" and c["var_y"] == "HGF"), None)

    for label, entry in [
        ("MET-MYC gene correlation", met_myc),
        ("HGF-MET gene correlation", hgf_met),
        ("MYC vs glycolysis score", myc_glyc),
        ("MET vs glycolysis score", met_glyc),
        ("CAF score vs HGF", caf_hgf),
    ]:
        if entry and entry["pearson_r"] != "NA":
            r = float(entry["pearson_r"])
            p = float(entry["p_value"])
            direction = "positive" if r > 0 else "negative"
            sig = "statistically significant" if p < 0.05 else "not statistically significant"
            lines.append(f"- **{label}**: r = {r:.4f} ({direction}, {sig})")
        else:
            lines.append(f"- **{label}**: insufficient data")

    lines.extend([
        "",
        "## Epistemological caveat",
        "",
        "Bulk RNA-seq mixes all cell types in a tissue sample. A positive",
        "MET-MYC correlation in bulk could reflect tumor-intrinsic biology,",
        "stromal contamination, or confounding by tumor purity. These results",
        "are screening-level evidence of plausibility, not proof of the",
        "cell-type-specific mechanism proposed by the hypothesis.",
        "",
        "## Next steps",
        "",
        "- If correlations are plausible: proceed to single-cell validation",
        "  (GSE225857 or equivalent) to test cell-type specificity.",
        "- If correlations are absent: reconsider whether the axis operates",
        "  at tissue level or is purely a niche-level phenomenon.",
        "- Either outcome is informative for prioritizing the hypothesis.",
        "",
    ])

    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--expression", type=Path, default=DEFAULT_EXPRESSION,
        help="Expression matrix TSV (genes x samples)",
    )
    parser.add_argument(
        "--signatures", type=Path, default=DEFAULT_SIGNATURES,
        help="Normalized signatures TSV",
    )
    parser.add_argument(
        "--out-dir", type=Path, default=DEFAULT_OUT_DIR,
        help="Output directory",
    )
    args = parser.parse_args()

    # Load data
    print("Loading expression matrix...", flush=True)
    samples, gene_data = load_expression_matrix(args.expression)
    print(f"  {len(gene_data)} genes x {len(samples)} samples", flush=True)

    print("Loading signatures...", flush=True)
    signatures = load_signatures(args.signatures)
    print(f"  {len(signatures)} signatures", flush=True)

    # Check gene availability
    for sig_id, genes in signatures.items():
        found = [g for g in genes if g in gene_data]
        missing = [g for g in genes if g not in gene_data]
        if missing:
            print(f"  WARNING: {sig_id} missing {missing}", flush=True)

    # Compute scores
    print("Computing signature scores...", flush=True)
    scores = compute_signature_scores(samples, gene_data, signatures)

    # Write scores
    args.out_dir.mkdir(parents=True, exist_ok=True)
    scores_path = args.out_dir / "tcga_coad_signature_scores.tsv"
    write_scores(samples, scores, scores_path)
    print(f"  Scores written to {scores_path.name}", flush=True)

    # Compute correlations
    print("Computing correlations...", flush=True)
    correlation_pairs: list[tuple[str, str, list[float], list[float]]] = []

    # Gene-gene key correlations
    key_gene_pairs = [
        ("MET", "MYC"),
        ("HGF", "MET"),
        ("HGF", "MYC"),
        ("MYC", "SLC2A1"),
        ("MYC", "HK2"),
        ("MYC", "LDHA"),
        ("MYC", "ENO1"),
        ("MET", "SLC2A1"),
        ("HGF", "COL1A1"),
        ("HGF", "FAP"),
        ("MCAM", "COL1A1"),
    ]

    for gx, gy in key_gene_pairs:
        if gx in gene_data and gy in gene_data:
            correlation_pairs.append((gx, gy, gene_data[gx], gene_data[gy]))

    # Score-gene correlations
    score_gene_pairs = [
        ("score:caf_core", "HGF"),
        ("score:caf_core", "MET"),
        ("score:myc_glycolysis_core", "HGF"),
        ("MYC", "score:myc_glycolysis_core"),
        ("MET", "score:myc_glycolysis_core"),
        ("HGF", "score:caf_core"),
        ("score:hgf_met_axis", "score:myc_glycolysis_core"),
        ("score:hgf_met_axis", "score:caf_core"),
        ("score:mcam_caf", "score:cxcl13_t_cells"),
        ("score:plasticity_emt", "score:myc_glycolysis_core"),
        ("score:macrophage_lipid_candidate", "score:caf_core"),
    ]

    for sx, sy in score_gene_pairs:
        vx = scores.get(sx.replace("score:", "")) if sx.startswith("score:") else gene_data.get(sx)
        vy = scores.get(sy.replace("score:", "")) if sy.startswith("score:") else gene_data.get(sy)
        if vx is not None and vy is not None:
            correlation_pairs.append((sx, sy, vx, vy))

    correlations: list[dict] = []
    for var_x, var_y, vx, vy in correlation_pairs:
        r, n = pearson_r(vx, vy)
        p = p_value_approx(r, n)
        correlations.append({
            "var_x": var_x,
            "var_y": var_y,
            "pearson_r": f"{r:.6f}" if not math.isnan(r) else "NA",
            "p_value": f"{p:.2e}" if not math.isnan(p) else "NA",
            "n": n,
            "interpretation": interpret_r(r, p),
        })

    # Write correlations
    corr_path = args.out_dir / "tcga_coad_correlations.tsv"
    write_correlations(correlations, corr_path)
    print(f"  Correlations written to {corr_path.name}", flush=True)

    # Write report
    report_path = args.out_dir / "tcga_coad_bulk_plausibility_report.md"
    write_report(samples, scores, gene_data, correlations, signatures, report_path)
    print(f"  Report written to {report_path.name}", flush=True)

    # Print summary
    print("\n=== Key results ===", flush=True)
    for c in correlations:
        if c["var_x"] in ("MET", "HGF", "MYC", "score:hgf_met_axis", "score:caf_core") or \
           c["var_y"] in ("MYC", "score:myc_glycolysis_core"):
            print(f"  {c['var_x']} ~ {c['var_y']}: r={c['pearson_r']}, p={c['p_value']}, {c['interpretation']}", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
