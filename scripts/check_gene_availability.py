#!/usr/bin/env python3
"""Check CRLM signature genes against gene universes.

The first validation step is deliberately lightweight: confirm that every
signature gene is a current HGNC-approved human symbol before attempting heavy
GEO/TCGA downloads. The script also accepts local universe files, so later GEO
or TCGA gene lists can be checked with the same command.
"""

from __future__ import annotations

import argparse
import csv
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SIGNATURES = ROOT / "data_manifest" / "generated" / "signatures_normalized.tsv"
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"
HGNC_URL = "https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt"


def read_signature_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def download_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "metastasis-research-gene-checker/0.1",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def parse_hgnc_symbols(text: str) -> set[str]:
    reader = csv.DictReader(text.splitlines(), delimiter="\t")
    if not reader.fieldnames or "symbol" not in reader.fieldnames:
        raise ValueError("HGNC file did not include a 'symbol' column.")
    return {row["symbol"].strip().upper() for row in reader if row.get("symbol")}


def read_symbol_universe(path: Path) -> set[str]:
    symbols: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            text = line.strip()
            if not text or text.startswith("#"):
                continue
            if "\t" in text:
                text = text.split("\t", 1)[0]
            elif "," in text:
                text = text.split(",", 1)[0]
            symbols.add(text.upper())
    return symbols


def write_universe_symbols(symbols: set[str], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["gene_symbol"])
        for symbol in sorted(symbols):
            writer.writerow([symbol])


def parse_universe_arg(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError(
            "Universe must use name=path syntax, for example tcga_coad=data/genes.txt"
        )
    name, raw_path = value.split("=", 1)
    if not name.strip():
        raise argparse.ArgumentTypeError("Universe name cannot be empty.")
    return name.strip(), Path(raw_path)


def build_availability_rows(
    signature_rows: list[dict[str, str]],
    universes: dict[str, set[str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in signature_rows:
        gene = row["gene_symbol"].upper()
        for universe_name, symbols in universes.items():
            rows.append(
                {
                    "signature_id": row["signature_id"],
                    "gene_symbol": gene,
                    "universe": universe_name,
                    "available": "yes" if gene in symbols else "no",
                }
            )
    return rows


def write_availability(rows: list[dict[str, str]], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["signature_id", "gene_symbol", "universe", "available"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def summarize_by_signature(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, int]]:
    summary: dict[tuple[str, str], dict[str, int]] = {}
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        key = (row["signature_id"], row["universe"])
        summary.setdefault(key, {"available": 0, "missing": 0})
        dedupe_key = (row["signature_id"], row["universe"], row["gene_symbol"])
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        if row["available"] == "yes":
            summary[key]["available"] += 1
        else:
            summary[key]["missing"] += 1
    return summary


def write_report(
    rows: list[dict[str, str]],
    universes: dict[str, set[str]],
    universe_sources: dict[str, str],
    out_path: Path,
) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    summary = summarize_by_signature(rows)
    missing = [row for row in rows if row["available"] == "no"]

    lines = [
        "# CRLM gene availability report",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Universes",
    ]

    for name, symbols in universes.items():
        source = universe_sources.get(name, "local")
        lines.append(f"- `{name}`: {len(symbols)} symbols; source: {source}")

    lines.extend(["", "## Signature Coverage"])
    for (signature_id, universe), counts in sorted(summary.items()):
        total = counts["available"] + counts["missing"]
        pct = (counts["available"] / total * 100) if total else 0
        lines.append(
            f"- `{signature_id}` in `{universe}`: {counts['available']}/{total} available ({pct:.1f}%)"
        )

    lines.extend(["", "## Missing Genes"])
    if missing:
        for row in missing:
            lines.append(
                f"- `{row['gene_symbol']}` missing from `{row['universe']}` in `{row['signature_id']}`"
            )
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## GEO Status",
            "- `GSE225857`: processed GEO TAR is about 607 MB; defer heavy extraction until marker lists are refined.",
            "- `GSE226997`: processed GEO TAR is about 41.2 GB; do not download in the first-pass checker.",
            "",
            "## Next Step",
            "Add local gene-universe files extracted from GEO/TCGA matrices and rerun this checker with `--universe name=path`.",
            "",
        ]
    )

    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--signatures",
        type=Path,
        default=DEFAULT_SIGNATURES,
        help="Normalized signature TSV from prepare_signatures.py.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Output directory.",
    )
    parser.add_argument(
        "--skip-hgnc",
        action="store_true",
        help="Do not fetch the official HGNC approved-symbol universe.",
    )
    parser.add_argument(
        "--universe",
        action="append",
        type=parse_universe_arg,
        default=[],
        help="Additional universe in name=path format.",
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    signature_rows = read_signature_rows(args.signatures)
    universes: dict[str, set[str]] = {}
    universe_sources: dict[str, str] = {}

    if not args.skip_hgnc:
        hgnc_text = download_text(HGNC_URL)
        symbols = parse_hgnc_symbols(hgnc_text)
        universes["hgnc_approved"] = symbols
        universe_sources["hgnc_approved"] = HGNC_URL
        write_universe_symbols(
            symbols,
            args.out_dir / "hgnc_approved_symbols.tsv",
        )

    for universe_name, universe_path in args.universe:
        path = universe_path if universe_path.is_absolute() else ROOT / universe_path
        universes[universe_name] = read_symbol_universe(path)
        universe_sources[universe_name] = path.relative_to(ROOT).as_posix()

    if not universes:
        print("No gene universes configured.", file=sys.stderr)
        return 2

    rows = build_availability_rows(signature_rows, universes)
    availability_path = args.out_dir / "gene_availability.tsv"
    report_path = args.out_dir / "gene_availability_report.md"
    write_availability(rows, availability_path)
    write_report(rows, universes, universe_sources, report_path)

    missing_count = sum(1 for row in rows if row["available"] == "no")
    print(f"Signature rows: {len(signature_rows)}")
    print(f"Universes: {len(universes)}")
    print(f"Availability rows: {len(rows)}")
    print(f"Missing calls: {missing_count}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    return 1 if missing_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
