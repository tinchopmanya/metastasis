#!/usr/bin/env python3
"""Validate cell-type-specific expression of key genes in GSE225857 single-cell data.

This script answers three critical questions for the mCAF-HGF-MET-MYC-glycolysis
hypothesis:

1. Is HGF expressed predominantly in MCAM+ CAFs (fibroblasts)?
2. Is MET expressed predominantly in tumor cells?
3. Is there a MET-MYC correlation within the tumor compartment?

It also checks glycolysis genes (SLC2A1, PGK1, TPI1) and MYC targets in tumor cells.

Data source:
  GSE225857 non-immune compartment (42k cells).
  - Metadata: gse225857_non_immune_meta.tsv
  - Counts: gse225857_non_immune_counts.tsv

Usage:
    python scripts/validate_sc_expression.py

    # Or specify paths explicitly:
    python scripts/validate_sc_expression.py \
        --meta data_manifest/generated/gse225857_non_immune_meta.tsv \
        --counts data_manifest/generated/gse225857_non_immune_counts.tsv
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_META = ROOT / "data_manifest" / "generated" / "gse225857_non_immune_meta.tsv"
DEFAULT_COUNTS = ROOT / "data_manifest" / "generated" / "gse225857_non_immune_counts.tsv"
DEFAULT_EXTRACTED = ROOT / "data_manifest" / "generated" / "gse225857_extracted_genes.json"
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"

# Genes of interest
GENES_OF_INTEREST = [
    "HGF", "MET", "MYC",
    "SLC2A1", "PGK1", "TPI1",   # glycolysis
    "MCAM", "COL1A1", "FAP",     # CAF markers
    "EPCAM", "KRT20",            # epithelial/tumor markers
    "CXCL13",                     # T-cell marker (should be rare in non-immune)
    "BHLHE40",                    # plasticity
]


def clean_field(s: str) -> str:
    """Remove surrounding quotes from a TSV field."""
    s = s.strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    return s


def load_metadata(path: Path) -> dict[str, dict]:
    """Load cell metadata TSV. Returns dict keyed by cell barcode."""
    cells = {}
    header = None
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if header is None:
                header = [clean_field(h) for h in parts]
                continue
            row = {}
            for i, val in enumerate(parts):
                if i < len(header):
                    row[header[i]] = clean_field(val)
            # First column is usually the cell barcode
            barcode = clean_field(parts[0])
            cells[barcode] = row
    return cells


def load_gene_expression(
    counts_path: Path,
    genes: list[str],
    cell_barcodes: set[str] | None = None,
) -> tuple[list[str], dict[str, dict[str, float]]]:
    """Load expression of specific genes from count matrix.

    The matrix format is: rows = genes, columns = cells.
    First column is gene name.

    Returns:
        cell_ids: list of cell IDs (column headers)
        gene_expr: dict[gene] -> dict[cell_id] -> expression_value
    """
    genes_upper = {g.upper() for g in genes}
    gene_expr: dict[str, dict[str, float]] = {}
    cell_ids: list[str] = []

    print(f"  Reading count matrix for {len(genes)} genes...", flush=True)

    with counts_path.open("r", encoding="utf-8") as f:
        # Read header
        header_line = f.readline().strip()
        parts = header_line.split("\t")
        # First element might be empty or "gene" or similar
        cell_ids = [clean_field(p) for p in parts[1:]]
        print(f"  Matrix has {len(cell_ids)} cells", flush=True)

        # Read rows, only keeping genes of interest
        found = 0
        total_rows = 0
        for line in f:
            total_rows += 1
            if total_rows % 5000 == 0:
                print(f"    Scanned {total_rows} genes, found {found}/{len(genes)}...",
                      flush=True)

            # Quick check: only parse if first field matches
            tab_pos = line.index("\t")
            gene_raw = clean_field(line[:tab_pos])

            if gene_raw.upper() in genes_upper:
                vals = line.strip().split("\t")
                gene_name = clean_field(vals[0])
                expr = {}
                for i, v in enumerate(vals[1:]):
                    if i < len(cell_ids):
                        try:
                            val = float(v)
                        except ValueError:
                            val = 0.0
                        if val > 0:  # sparse: only store non-zero
                            expr[cell_ids[i]] = val
                gene_expr[gene_name] = expr
                found += 1
                print(f"    Found {gene_name}: {len(expr)} non-zero cells", flush=True)

                if found >= len(genes):
                    break  # All genes found

        print(f"  Scanned {total_rows} rows, found {found}/{len(genes)} genes", flush=True)

    return cell_ids, gene_expr


def load_extracted_gene_expression(
    extracted_path: Path,
    genes: list[str],
) -> tuple[list[str], dict[str, dict[str, float]]]:
    """Load previously extracted sparse gene expression JSON.

    This is the preferred path for repeat runs because it avoids re-reading a
    very large count matrix and protects the report from partial TSV downloads.
    """
    print(f"  Reading extracted gene cache: {extracted_path.name}", flush=True)
    data = json.loads(extracted_path.read_text(encoding="utf-8"))
    cell_ids = [clean_field(cell_id) for cell_id in data.get("cell_ids", [])]
    raw_genes = data.get("genes", {})
    wanted = {gene.upper() for gene in genes}
    gene_expr: dict[str, dict[str, float]] = {}

    for gene, expr in raw_genes.items():
        gene_upper = gene.upper()
        if gene_upper not in wanted:
            continue
        gene_expr[gene_upper] = {
            clean_field(cell_id): float(value)
            for cell_id, value in expr.items()
            if float(value) > 0
        }
        print(f"    Found {gene_upper}: {len(gene_expr[gene_upper])} non-zero cells", flush=True)

    print(f"  Cache has {len(cell_ids)} cells", flush=True)
    return cell_ids, gene_expr


def harmonize_cell_ids(
    cell_ids: list[str],
    gene_expr: dict[str, dict[str, float]],
    metadata_ids: set[str],
) -> tuple[list[str], dict[str, dict[str, float]]]:
    """Map count/cache cell IDs onto metadata cell IDs.

    GSE225857 count matrices use a dot between sample tag and barcode, while
    metadata uses a dash. This normalization preserves exact IDs when possible
    and otherwise replaces the first dot with a dash.
    """
    id_map: dict[str, str] = {}
    for cell_id in cell_ids:
        if cell_id in metadata_ids:
            id_map[cell_id] = cell_id
            continue
        candidate = cell_id.replace(".", "-", 1)
        if candidate in metadata_ids:
            id_map[cell_id] = candidate

    mapped_cell_ids = [id_map[cell_id] for cell_id in cell_ids if cell_id in id_map]
    mapped_expr: dict[str, dict[str, float]] = {}
    for gene, expr in gene_expr.items():
        mapped_expr[gene] = {
            id_map[cell_id]: value
            for cell_id, value in expr.items()
            if cell_id in id_map
        }

    print(f"  Matched {len(mapped_cell_ids)}/{len(cell_ids)} expression cells to metadata", flush=True)
    return mapped_cell_ids, mapped_expr


def classify_cell(cluster: str) -> str:
    """Map cluster to broad category."""
    if cluster.startswith("Tu"):
        return "Tumor"
    elif cluster.startswith("F"):
        return "Fibroblast"
    elif cluster.startswith("E"):
        return "Endothelial"
    return "Other"


def compute_mean_by_celltype(
    gene_expr: dict[str, float],
    cells_meta: dict[str, dict],
    cell_ids: list[str],
) -> dict[str, tuple[float, int, int]]:
    """Compute mean expression per cell type.

    Returns dict[celltype] -> (mean_expr, n_expressing, n_total)
    """
    sums: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    expressing: dict[str, int] = defaultdict(int)

    for cell_id in cell_ids:
        meta = cells_meta.get(cell_id)
        if meta is None:
            continue
        ct = meta.get("cluster", "unknown")
        val = gene_expr.get(cell_id, 0.0)
        sums[ct] += val
        counts[ct] += 1
        if val > 0:
            expressing[ct] += 1

    result = {}
    for ct in counts:
        n = counts[ct]
        mean = sums[ct] / n if n > 0 else 0.0
        result[ct] = (mean, expressing[ct], n)
    return result


def compute_mean_by_category(
    gene_expr: dict[str, float],
    cells_meta: dict[str, dict],
    cell_ids: list[str],
) -> dict[str, tuple[float, int, int]]:
    """Compute mean expression per broad category (Tumor, Fibroblast, etc.)."""
    sums: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    expressing: dict[str, int] = defaultdict(int)

    for cell_id in cell_ids:
        meta = cells_meta.get(cell_id)
        if meta is None:
            continue
        ct = meta.get("cluster", "unknown")
        cat = classify_cell(ct)
        val = gene_expr.get(cell_id, 0.0)
        sums[cat] += val
        counts[cat] += 1
        if val > 0:
            expressing[cat] += 1

    result = {}
    for cat in counts:
        n = counts[cat]
        mean = sums[cat] / n if n > 0 else 0.0
        result[cat] = (mean, expressing[cat], n)
    return result


def pearson_r(x: list[float], y: list[float]) -> tuple[float, int]:
    """Compute Pearson correlation coefficient."""
    n = len(x)
    if n < 3:
        return 0.0, n

    mx = sum(x) / n
    my = sum(y) / n

    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    sx = math.sqrt(sum((xi - mx) ** 2 for xi in x))
    sy = math.sqrt(sum((yi - my) ** 2 for yi in y))

    if sx == 0 or sy == 0:
        return 0.0, n

    return cov / (sx * sy), n


def p_value_approx(r: float, n: int) -> float:
    """Approximate two-tailed p-value for Pearson r using t-distribution."""
    if n <= 2 or abs(r) >= 1.0:
        return 1.0
    t = r * math.sqrt((n - 2) / (1 - r * r))
    # Approximate using normal for large n
    df = n - 2
    if df > 100:
        # Normal approximation
        p = 2 * (1 - _norm_cdf(abs(t)))
    else:
        # Beta incomplete approximation
        x = df / (df + t * t)
        p = _betai(0.5 * df, 0.5, x)
    return max(p, 1e-300)


def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _betai(a: float, b: float, x: float) -> float:
    """Incomplete beta function (regularized), crude approximation."""
    if x < 0 or x > 1:
        return 0.0
    if x == 0 or x == 1:
        return x

    # Use continued fraction for numerical stability
    if x > (a + 1) / (a + b + 2):
        return 1.0 - _betai(b, a, 1.0 - x)

    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(
        math.log(x) * a + math.log(1 - x) * b + lbeta
    ) / a

    # Lentz's continued fraction
    f = 1.0
    c = 1.0
    d = 1.0 - (a + b) * x / (a + 1)
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    f = d

    for m in range(1, 200):
        # Even step
        numerator = m * (b - m) * x / ((a + 2 * m - 1) * (a + 2 * m))
        d = 1.0 + numerator * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + numerator / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        f *= d * c

        # Odd step
        numerator = -(a + m) * (a + b + m) * x / ((a + 2 * m) * (a + 2 * m + 1))
        d = 1.0 + numerator * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + numerator / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        f *= delta

        if abs(delta - 1.0) < 1e-8:
            break

    return front * f


def write_report(
    gene_by_category: dict[str, dict[str, tuple[float, int, int]]],
    gene_by_celltype: dict[str, dict[str, tuple[float, int, int]]],
    correlations: list[dict],
    organ_expression: dict[str, dict[str, tuple[float, int, int]]],
    out_path: Path,
) -> None:
    """Write the validation report."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# GSE225857 single-cell expression validation",
        "",
        f"Generated at: {ts}",
        "",
        "## Purpose",
        "",
        "Validate cell-type-specific expression of key genes in the",
        "mCAF-HGF-MET-MYC-glycolysis hypothesis using GSE225857 scRNA-seq data.",
        "",
    ]

    # HGF assessment
    lines.extend([
        "## Question 1: Is HGF expressed in fibroblasts (mCAFs)?",
        "",
    ])
    if "HGF" in gene_by_category:
        hgf = gene_by_category["HGF"]
        lines.append("| Category | Mean expr | % expressing | N cells |")
        lines.append("| --- | --- | --- | --- |")
        for cat in ["Fibroblast", "Tumor", "Endothelial", "Other"]:
            if cat in hgf:
                mean, n_exp, n_tot = hgf[cat]
                pct = n_exp / n_tot * 100 if n_tot else 0
                lines.append(f"| {cat} | {mean:.4f} | {pct:.1f}% | {n_tot} |")
        lines.append("")

        # Detailed by fibroblast subtype
        if "HGF" in gene_by_celltype:
            hgf_ct = gene_by_celltype["HGF"]
            fib_types = {k: v for k, v in hgf_ct.items() if k.startswith("F")}
            if fib_types:
                lines.append("### HGF in fibroblast subtypes")
                lines.append("")
                lines.append("| Cell type | Mean expr | % expressing | N cells |")
                lines.append("| --- | --- | --- | --- |")
                for ct in sorted(fib_types, key=lambda x: -fib_types[x][0]):
                    mean, n_exp, n_tot = fib_types[ct]
                    pct = n_exp / n_tot * 100 if n_tot else 0
                    lines.append(f"| `{ct}` | {mean:.4f} | {pct:.1f}% | {n_tot} |")
                lines.append("")

    # MET assessment
    lines.extend([
        "## Question 2: Is MET expressed in tumor cells?",
        "",
    ])
    if "MET" in gene_by_category:
        met = gene_by_category["MET"]
        lines.append("| Category | Mean expr | % expressing | N cells |")
        lines.append("| --- | --- | --- | --- |")
        for cat in ["Tumor", "Fibroblast", "Endothelial", "Other"]:
            if cat in met:
                mean, n_exp, n_tot = met[cat]
                pct = n_exp / n_tot * 100 if n_tot else 0
                lines.append(f"| {cat} | {mean:.4f} | {pct:.1f}% | {n_tot} |")
        lines.append("")

    # MET-MYC correlation in tumor
    lines.extend([
        "## Question 3: MET-MYC correlation in tumor cells",
        "",
    ])
    met_myc = [c for c in correlations if c["gene_x"] == "MET" and c["gene_y"] == "MYC"
               and c["compartment"] == "Tumor"]
    if met_myc:
        c = met_myc[0]
        lines.extend([
            f"- Pearson r = {c['r']:.4f}",
            f"- N cells = {c['n']}",
            f"- p-value = {c['p']:.2e}" if c['p'] > 1e-300 else f"- p-value < 1e-300",
            f"- Interpretation: {c['interpretation']}",
            "",
        ])
    else:
        lines.append("Not computed (insufficient data).")
        lines.append("")

    # Additional correlations
    other_corr = [c for c in correlations if not (c["gene_x"] == "MET" and c["gene_y"] == "MYC"
                   and c["compartment"] == "Tumor")]
    if other_corr:
        lines.extend([
            "## Additional correlations",
            "",
            "| Gene X | Gene Y | Compartment | r | N | p-value | Interpretation |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ])
        for c in other_corr:
            p_str = f"{c['p']:.2e}" if c['p'] > 1e-300 else "< 1e-300"
            lines.append(
                f"| {c['gene_x']} | {c['gene_y']} | {c['compartment']} | "
                f"{c['r']:.4f} | {c['n']} | {p_str} | {c['interpretation']} |"
            )
        lines.append("")

    # Organ-specific expression
    lines.extend([
        "## Expression by tissue (CCT vs LCT)",
        "",
    ])
    for gene in ["HGF", "MET", "MYC", "SLC2A1"]:
        if gene in organ_expression:
            org_data = organ_expression[gene]
            lines.append(f"### {gene}")
            lines.append("")
            lines.append("| Tissue | Mean expr | % expressing | N cells |")
            lines.append("| --- | --- | --- | --- |")
            for organ in ["CCT", "LCT"]:
                if organ in org_data:
                    mean, n_exp, n_tot = org_data[organ]
                    pct = n_exp / n_tot * 100 if n_tot else 0
                    lines.append(f"| {organ} | {mean:.4f} | {pct:.1f}% | {n_tot} |")
            lines.append("")

    # Overall assessment
    lines.extend([
        "## Overall hypothesis assessment",
        "",
    ])

    # Auto-assess
    hgf_in_fib = False
    met_in_tum = False
    met_myc_corr = False

    if "HGF" in gene_by_category:
        hgf_cat = gene_by_category["HGF"]
        fib_mean = hgf_cat.get("Fibroblast", (0, 0, 0))[0]
        tum_mean = hgf_cat.get("Tumor", (0, 0, 0))[0]
        if fib_mean > tum_mean:
            hgf_in_fib = True

    if "MET" in gene_by_category:
        met_cat = gene_by_category["MET"]
        tum_mean = met_cat.get("Tumor", (0, 0, 0))[0]
        fib_mean = met_cat.get("Fibroblast", (0, 0, 0))[0]
        if tum_mean > fib_mean:
            met_in_tum = True

    if met_myc:
        if met_myc[0]["r"] > 0.1 and met_myc[0]["p"] < 0.05:
            met_myc_corr = True

    lines.extend([
        f"1. **HGF in fibroblasts > tumor**: {'CONFIRMED' if hgf_in_fib else 'NOT CONFIRMED'}",
        f"2. **MET in tumor > fibroblasts**: {'CONFIRMED' if met_in_tum else 'NOT CONFIRMED'}",
        f"3. **MET-MYC correlation in tumor**: {'CONFIRMED' if met_myc_corr else 'NOT CONFIRMED'}",
        "",
    ])

    score = sum([hgf_in_fib, met_in_tum, met_myc_corr])
    if score == 3:
        lines.append("**Conclusion**: All three expression predictions confirmed. "
                      "The mCAF-HGF-MET-MYC axis has strong single-cell support.")
    elif score == 2:
        lines.append("**Conclusion**: Two of three predictions confirmed. "
                      "The hypothesis retains support but one link is weaker than expected.")
    elif score == 1:
        lines.append("**Conclusion**: Only one prediction confirmed. "
                      "The hypothesis needs revision or additional evidence.")
    else:
        lines.append("**Conclusion**: No predictions confirmed at single-cell level. "
                      "Consider alternative mechanisms or data quality issues.")

    lines.append("")

    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--meta", type=Path, default=DEFAULT_META)
    parser.add_argument("--counts", type=Path, default=DEFAULT_COUNTS)
    parser.add_argument("--extracted", type=Path, default=DEFAULT_EXTRACTED)
    parser.add_argument("--force-counts", action="store_true",
                        help="Read the full count matrix even if extracted JSON exists.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    if not args.meta.exists():
        print(f"ERROR: Metadata not found: {args.meta}", file=sys.stderr)
        print("Run: python scripts/download_gse225857.py --meta-only", file=sys.stderr)
        return 1

    if args.force_counts and not args.counts.exists():
        print(f"ERROR: Count matrix not found: {args.counts}", file=sys.stderr)
        print("Run: python scripts/download_gse225857.py --non-immune", file=sys.stderr)
        return 1

    # Load metadata
    print("Step 1: Loading metadata...", flush=True)
    cells_meta = load_metadata(args.meta)
    print(f"  {len(cells_meta)} cells in metadata", flush=True)

    # Load expression for genes of interest
    print("\nStep 2: Loading expression data...", flush=True)
    if args.extracted.exists() and not args.force_counts:
        cell_ids, gene_expr = load_extracted_gene_expression(args.extracted, GENES_OF_INTEREST)
    else:
        if not args.counts.exists():
            print(f"ERROR: Count matrix not found: {args.counts}", file=sys.stderr)
            print("Run: python scripts/download_gse225857.py --non-immune", file=sys.stderr)
            return 1
        cell_ids, gene_expr = load_gene_expression(
            args.counts, GENES_OF_INTEREST, set(cells_meta.keys())
        )
    cell_ids, gene_expr = harmonize_cell_ids(cell_ids, gene_expr, set(cells_meta.keys()))
    print(f"  Found {len(gene_expr)}/{len(GENES_OF_INTEREST)} genes", flush=True)

    # Compute expression by category and cell type
    print("\nStep 3: Computing expression by cell type...", flush=True)
    gene_by_category: dict[str, dict[str, tuple[float, int, int]]] = {}
    gene_by_celltype: dict[str, dict[str, tuple[float, int, int]]] = {}

    for gene, expr in gene_expr.items():
        gene_by_category[gene] = compute_mean_by_category(expr, cells_meta, cell_ids)
        gene_by_celltype[gene] = compute_mean_by_celltype(expr, cells_meta, cell_ids)

        # Quick print
        cat_data = gene_by_category[gene]
        parts = []
        for cat in ["Tumor", "Fibroblast", "Endothelial"]:
            if cat in cat_data:
                mean, n_exp, n_tot = cat_data[cat]
                parts.append(f"{cat}: mean={mean:.3f} ({n_exp}/{n_tot})")
        print(f"  {gene}: {', '.join(parts)}", flush=True)

    # Compute expression by organ
    print("\nStep 4: Computing expression by tissue...", flush=True)
    organ_expression: dict[str, dict[str, tuple[float, int, int]]] = {}
    for gene, expr in gene_expr.items():
        organ_data: dict[str, tuple[float, int, int]] = {}
        sums: dict[str, float] = defaultdict(float)
        counts: dict[str, int] = defaultdict(int)
        expressing: dict[str, int] = defaultdict(int)

        for cell_id in cell_ids:
            meta = cells_meta.get(cell_id)
            if meta is None:
                continue
            organ = meta.get("organs", "unknown")
            val = expr.get(cell_id, 0.0)
            sums[organ] += val
            counts[organ] += 1
            if val > 0:
                expressing[organ] += 1

        for organ in counts:
            n = counts[organ]
            mean = sums[organ] / n if n > 0 else 0.0
            organ_data[organ] = (mean, expressing[organ], n)
        organ_expression[gene] = organ_data

    # Compute correlations
    print("\nStep 5: Computing correlations...", flush=True)
    correlations: list[dict] = []

    correlation_pairs = [
        ("MET", "MYC", "Tumor"),
        ("MET", "MYC", "Fibroblast"),
        ("MET", "SLC2A1", "Tumor"),
        ("MYC", "SLC2A1", "Tumor"),
        ("MYC", "PGK1", "Tumor"),
        ("MYC", "TPI1", "Tumor"),
        ("HGF", "MCAM", "Fibroblast"),
        ("HGF", "COL1A1", "Fibroblast"),
        ("HGF", "FAP", "Fibroblast"),
    ]

    for gene_x, gene_y, compartment in correlation_pairs:
        if gene_x not in gene_expr or gene_y not in gene_expr:
            continue

        expr_x = gene_expr[gene_x]
        expr_y = gene_expr[gene_y]

        # Filter to cells in the compartment
        x_vals = []
        y_vals = []
        for cell_id in cell_ids:
            meta = cells_meta.get(cell_id)
            if meta is None:
                continue
            ct = meta.get("cluster", "unknown")
            cat = classify_cell(ct)
            if cat != compartment:
                continue
            x_vals.append(expr_x.get(cell_id, 0.0))
            y_vals.append(expr_y.get(cell_id, 0.0))

        if len(x_vals) < 10:
            continue

        r, n = pearson_r(x_vals, y_vals)
        p = p_value_approx(r, n)

        if abs(r) >= 0.3:
            interp = "strong" if abs(r) >= 0.5 else "moderate"
        elif abs(r) >= 0.1:
            interp = "weak"
        else:
            interp = "negligible"

        if p < 0.001:
            interp += ", highly significant"
        elif p < 0.05:
            interp += ", significant"
        else:
            interp += ", not significant"

        correlations.append({
            "gene_x": gene_x,
            "gene_y": gene_y,
            "compartment": compartment,
            "r": r,
            "n": n,
            "p": p,
            "interpretation": interp,
        })
        print(f"  {gene_x}-{gene_y} in {compartment}: r={r:.4f}, n={n}, p={p:.2e}",
              flush=True)

    # Write report
    print("\nStep 6: Writing report...", flush=True)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.out_dir / "gse225857_sc_expression_report.md"
    write_report(gene_by_category, gene_by_celltype, correlations,
                 organ_expression, report_path)
    print(f"  Report: {report_path.name}", flush=True)

    # Write expression summary TSV
    summary_path = args.out_dir / "gse225857_gene_expression_summary.tsv"
    with summary_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["gene", "category", "mean_expr", "pct_expressing", "n_cells"])
        for gene in sorted(gene_by_category):
            for cat in ["Tumor", "Fibroblast", "Endothelial", "Other"]:
                if cat in gene_by_category[gene]:
                    mean, n_exp, n_tot = gene_by_category[gene][cat]
                    pct = n_exp / n_tot * 100 if n_tot else 0
                    writer.writerow([gene, cat, f"{mean:.4f}", f"{pct:.1f}", n_tot])
    print(f"  Summary: {summary_path.name}", flush=True)

    # Write correlations TSV
    corr_path = args.out_dir / "gse225857_sc_correlations.tsv"
    with corr_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["gene_x", "gene_y", "compartment", "pearson_r", "n", "p_value",
                         "interpretation"])
        for c in correlations:
            writer.writerow([c["gene_x"], c["gene_y"], c["compartment"],
                             f"{c['r']:.4f}", c["n"], f"{c['p']:.2e}",
                             c["interpretation"]])
    print(f"  Correlations: {corr_path.name}", flush=True)

    # Final summary
    print("\n=== VALIDATION SUMMARY ===", flush=True)
    if "HGF" in gene_by_category:
        hgf = gene_by_category["HGF"]
        fib = hgf.get("Fibroblast", (0, 0, 0))
        tum = hgf.get("Tumor", (0, 0, 0))
        status = "CONFIRMED" if fib[0] > tum[0] else "NOT CONFIRMED"
        print(f"  HGF in Fibroblast (mean={fib[0]:.4f}) vs Tumor (mean={tum[0]:.4f}): {status}",
              flush=True)

    if "MET" in gene_by_category:
        met = gene_by_category["MET"]
        tum = met.get("Tumor", (0, 0, 0))
        fib = met.get("Fibroblast", (0, 0, 0))
        status = "CONFIRMED" if tum[0] > fib[0] else "NOT CONFIRMED"
        print(f"  MET in Tumor (mean={tum[0]:.4f}) vs Fibroblast (mean={fib[0]:.4f}): {status}",
              flush=True)

    met_myc = [c for c in correlations
               if c["gene_x"] == "MET" and c["gene_y"] == "MYC" and c["compartment"] == "Tumor"]
    if met_myc:
        c = met_myc[0]
        status = "CONFIRMED" if c["r"] > 0.1 and c["p"] < 0.05 else "NOT CONFIRMED"
        print(f"  MET-MYC in Tumor: r={c['r']:.4f}, p={c['p']:.2e}: {status}", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
