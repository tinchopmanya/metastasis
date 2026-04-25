#!/usr/bin/env python3
"""Prepare CRLM gene signatures for first-pass validation.

The project intentionally starts with a tiny, dependency-free script. It reads
the local YAML-like signature manifest, normalizes gene symbols, checks for
basic issues, and writes tables that later analysis scripts can consume.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data_manifest" / "signatures.yml"
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"
GENE_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9.-]*$")


def strip_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_signature_manifest(path: Path) -> dict:
    """Parse the narrow YAML subset used by data_manifest/signatures.yml."""
    result: dict = {"metadata": {}, "signatures": {}, "next_refinement": []}
    section: str | None = None
    current_signature: str | None = None
    current_list: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        text = line.strip()

        if indent == 0 and text.endswith(":"):
            section = text[:-1]
            current_signature = None
            current_list = None
            continue

        if indent == 0 and ":" in text:
            key, value = text.split(":", 1)
            result["metadata"][key.strip()] = strip_value(value)
            continue

        if section == "signatures":
            if indent == 2 and text.endswith(":"):
                current_signature = text[:-1]
                result["signatures"][current_signature] = {
                    "description": "",
                    "genes": [],
                }
                current_list = None
                continue

            if current_signature and indent == 4 and ":" in text:
                key, value = text.split(":", 1)
                key = key.strip()
                value = strip_value(value)
                if key == "genes":
                    current_list = "genes"
                else:
                    result["signatures"][current_signature][key] = value
                    current_list = None
                continue

            if current_signature and current_list == "genes" and indent >= 6:
                if text.startswith("- "):
                    result["signatures"][current_signature]["genes"].append(
                        strip_value(text[2:])
                    )
                continue

        if section == "next_refinement" and text.startswith("- "):
            result["next_refinement"].append(strip_value(text[2:]))

    return result


def normalize_gene(gene: str) -> str:
    return gene.strip().upper()


def build_rows(manifest: dict) -> tuple[list[dict], list[str], dict[str, list[str]]]:
    rows: list[dict] = []
    warnings: list[str] = []
    gene_to_signatures: dict[str, list[str]] = defaultdict(list)

    for signature_id, signature in manifest["signatures"].items():
        description = signature.get("description", "")
        seen_in_signature: set[str] = set()

        for order, raw_gene in enumerate(signature.get("genes", []), start=1):
            normalized = normalize_gene(raw_gene)
            valid = bool(GENE_PATTERN.match(normalized))

            if normalized in seen_in_signature:
                warnings.append(
                    f"Duplicate gene {normalized} inside signature {signature_id}."
                )
            seen_in_signature.add(normalized)
            gene_to_signatures[normalized].append(signature_id)

            if not valid:
                warnings.append(
                    f"Potentially invalid gene symbol {raw_gene!r} in {signature_id}."
                )

            rows.append(
                {
                    "signature_id": signature_id,
                    "signature_description": description,
                    "gene_order": order,
                    "gene_symbol": normalized,
                    "raw_gene_symbol": raw_gene,
                    "is_valid_symbol_shape": "yes" if valid else "no",
                }
            )

    return rows, warnings, gene_to_signatures


def write_signature_tables(
    rows: list[dict], gene_to_signatures: dict[str, list[str]], out_dir: Path
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    normalized_path = out_dir / "signatures_normalized.tsv"
    matrix_path = out_dir / "signature_gene_matrix.tsv"

    with normalized_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "signature_id",
            "signature_description",
            "gene_order",
            "gene_symbol",
            "raw_gene_symbol",
            "is_valid_symbol_shape",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    signature_ids = sorted({row["signature_id"] for row in rows})
    genes = sorted(gene_to_signatures)
    with matrix_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["gene_symbol", *signature_ids])
        for gene in genes:
            memberships = set(gene_to_signatures[gene])
            writer.writerow([gene, *["1" if sid in memberships else "0" for sid in signature_ids]])

    return {
        "normalized": normalized_path,
        "matrix": matrix_path,
    }


def write_report(
    manifest: dict,
    rows: list[dict],
    warnings: list[str],
    gene_to_signatures: dict[str, list[str]],
    output_paths: dict[str, Path],
    out_dir: Path,
) -> Path:
    report_path = out_dir / "signature_report.md"
    signature_count = len(manifest["signatures"])
    unique_gene_count = len(gene_to_signatures)
    repeated = {
        gene: signatures
        for gene, signatures in sorted(gene_to_signatures.items())
        if len(set(signatures)) > 1
    }
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# CRLM signature preparation report",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Active hypothesis",
        manifest["metadata"].get("active_hypothesis", "unknown"),
        "",
        "## Summary",
        f"- Signatures: {signature_count}",
        f"- Signature-gene rows: {len(rows)}",
        f"- Unique genes: {unique_gene_count}",
        f"- Basic warnings: {len(warnings)}",
        "",
        "## Generated files",
        f"- `{output_paths['normalized'].relative_to(ROOT).as_posix()}`",
        f"- `{output_paths['matrix'].relative_to(ROOT).as_posix()}`",
        "",
        "## Reused genes across signatures",
    ]

    if repeated:
        for gene, signatures in repeated.items():
            joined = ", ".join(sorted(set(signatures)))
            lines.append(f"- `{gene}`: {joined}")
    else:
        lines.append("- None")

    lines.extend(["", "## Warnings"])
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Next refinements",
        ]
    )
    for item in manifest.get("next_refinement", []):
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Next technical step",
            "Use these tables to check gene availability in GEO/TCGA expression matrices before scoring signatures.",
            "",
        ]
    )

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Path to signatures.yml",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Directory for generated tables and report",
    )
    args = parser.parse_args()

    manifest = parse_signature_manifest(args.input)
    rows, warnings, gene_to_signatures = build_rows(manifest)
    output_paths = write_signature_tables(rows, gene_to_signatures, args.out_dir)
    report_path = write_report(
        manifest,
        rows,
        warnings,
        gene_to_signatures,
        output_paths,
        args.out_dir,
    )

    print(f"Signatures: {len(manifest['signatures'])}")
    print(f"Rows: {len(rows)}")
    print(f"Unique genes: {len(gene_to_signatures)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
