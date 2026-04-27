#!/usr/bin/env python3
"""Fetch a lightweight gene universe from GDC/TCGA without heavy downloads.

Strategy:
1. Query the GDC API for STAR-Counts gene expression files in a given project
   (e.g. TCGA-COAD or TCGA-READ).
2. Pick one small file and download it (typically ~1 MB uncompressed TSV).
3. Extract the gene symbol column to produce a universe file.

This avoids downloading full expression matrices or BAM/FASTQ files.

If the GDC API is unreachable or returns unexpected data, the script falls back
to building a provisional universe from GENCODE v36 annotation (the reference
used by GDC for STAR alignment), clearly marking it as provisional.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "gene_universes"

GDC_FILES_ENDPOINT = "https://api.gdc.cancer.gov/files"
GDC_DATA_ENDPOINT = "https://api.gdc.cancer.gov/data"

# GENCODE v36 is the annotation version used by GDC STAR pipeline.
# We use it as fallback if GDC data download fails.
GENCODE_URL = (
    "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/"
    "release_36/gencode.v36.annotation.gtf.gz"
)


def gdc_request(url: str, payload: dict | None = None, timeout: int = 60) -> dict:
    """Send a request to GDC API and return parsed JSON."""
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    else:
        req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_star_counts_file(project: str) -> str | None:
    """Find a single STAR-Counts file UUID for a GDC project."""
    payload = {
        "filters": {
            "op": "and",
            "content": [
                {
                    "op": "=",
                    "content": {
                        "field": "cases.project.project_id",
                        "value": project,
                    },
                },
                {
                    "op": "=",
                    "content": {
                        "field": "data_type",
                        "value": "Gene Expression Quantification",
                    },
                },
                {
                    "op": "=",
                    "content": {
                        "field": "analysis.workflow_type",
                        "value": "STAR - Counts",
                    },
                },
                {
                    "op": "=",
                    "content": {
                        "field": "data_format",
                        "value": "TSV",
                    },
                },
            ],
        },
        "fields": "file_id,file_name,file_size",
        "size": 1,
    }
    result = gdc_request(GDC_FILES_ENDPOINT, payload)
    hits = result.get("data", {}).get("hits", [])
    if not hits:
        return None
    return hits[0]["file_id"]


def download_gdc_file(file_id: str, timeout: int = 120) -> bytes:
    """Download a single file from GDC by UUID."""
    url = f"{GDC_DATA_ENDPOINT}/{file_id}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def extract_genes_from_star_counts(content: bytes) -> list[str]:
    """Extract gene symbols from a GDC STAR-Counts TSV.

    The file has columns: gene_id, gene_name, gene_type, unstranded, ...
    We want gene_name for protein-coding and other biotypes, excluding
    special rows (N_unmapped, N_multimapping, etc.).
    """
    # Try to decompress if gzipped
    try:
        text = gzip.decompress(content).decode("utf-8")
    except (gzip.BadGzipFile, OSError):
        text = content.decode("utf-8")

    # Strip comment lines (e.g. "# gene-model: GENCODE v36")
    filtered_lines = [
        line for line in text.splitlines() if not line.startswith("#")
    ]
    if not filtered_lines:
        return []

    genes: list[str] = []
    reader = csv.DictReader(filtered_lines, delimiter="\t")

    if not reader.fieldnames:
        return genes

    # Find the gene name column (could be gene_name or gene_id)
    name_col = None
    for candidate in ["gene_name", "gene_id"]:
        if candidate in reader.fieldnames:
            name_col = candidate
            break

    if name_col is None:
        return genes

    seen: set[str] = set()
    for row in reader:
        symbol = row.get(name_col, "").strip()
        if not symbol:
            continue
        # Skip STAR special counters
        if symbol.startswith("N_") or symbol.startswith("__"):
            continue
        # If gene_id is Ensembl, skip (we want symbols)
        if symbol.startswith("ENSG"):
            continue
        symbol_upper = symbol.upper()
        if symbol_upper not in seen:
            seen.add(symbol_upper)
            genes.append(symbol)

    return genes


def fetch_gencode_gene_names(timeout: int = 120) -> list[str]:
    """Fallback: extract gene names from GENCODE v36 GTF (gene lines only).

    Downloads the full GTF (~40 MB compressed) but only keeps gene_name from
    gene-level entries. This is heavier than a single STAR file but still
    much lighter than expression matrices.
    """
    print("Falling back to GENCODE v36 annotation...", file=sys.stderr)
    req = urllib.request.Request(
        GENCODE_URL,
        headers={"User-Agent": "metastasis-research/0.1"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        compressed = resp.read()

    text = gzip.decompress(compressed).decode("utf-8")
    seen: set[str] = set()
    genes: list[str] = []

    for line in text.splitlines():
        if line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) < 9:
            continue
        if fields[2] != "gene":
            continue
        attrs = fields[8]
        # Extract gene_name from GTF attributes
        for attr in attrs.split(";"):
            attr = attr.strip()
            if attr.startswith("gene_name"):
                # gene_name "FOO"
                parts = attr.split('"')
                if len(parts) >= 2:
                    name = parts[1].strip()
                    name_upper = name.upper()
                    if name_upper not in seen:
                        seen.add(name_upper)
                        genes.append(name)
                break

    return genes


def write_universe(genes: list[str], out_path: Path, source: str, project: str) -> None:
    """Write a gene universe file with metadata header."""
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(f"# Gene universe: {project}\n")
        f.write(f"# Source: {source}\n")
        f.write(f"# Generated: {generated_at}\n")
        f.write(f"# Genes: {len(genes)}\n")
        for gene in sorted(genes, key=str.upper):
            f.write(f"{gene}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project",
        default="TCGA-COAD",
        help="GDC project ID (default: TCGA-COAD)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Output directory for gene universe files",
    )
    parser.add_argument(
        "--force-gencode",
        action="store_true",
        help="Skip GDC and use GENCODE v36 annotation directly",
    )
    args = parser.parse_args()

    project_slug = args.project.lower().replace("-", "_")
    out_path = args.out_dir / f"{project_slug}_genes.txt"

    source = ""
    genes: list[str] = []

    if not args.force_gencode:
        print(f"Querying GDC for STAR-Counts files in {args.project}...", flush=True)
        try:
            file_id = find_star_counts_file(args.project)
            if file_id:
                print(f"Found file: {file_id}", flush=True)
                print("Downloading single STAR-Counts file...", flush=True)
                content = download_gdc_file(file_id)
                genes = extract_genes_from_star_counts(content)
                source = f"GDC STAR-Counts file {file_id} from {args.project}"
                print(f"Extracted {len(genes)} gene symbols from STAR-Counts.", flush=True)
            else:
                print(f"No STAR-Counts TSV files found for {args.project}.", file=sys.stderr, flush=True)
        except Exception as exc:
            print(f"GDC query/download failed: {exc}", file=sys.stderr, flush=True)

    if not genes:
        print("GDC extraction failed or skipped. Using GENCODE v36 fallback.", flush=True)
        try:
            genes = fetch_gencode_gene_names()
            source = f"GENCODE v36 annotation (provisional, not {args.project}-specific)"
        except Exception as exc:
            print(f"GENCODE fallback also failed: {exc}", file=sys.stderr, flush=True)
            return 1

    if not genes:
        print("No genes extracted from any source.", file=sys.stderr, flush=True)
        return 1

    write_universe(genes, out_path, source, args.project)
    print(f"Wrote {len(genes)} genes to {out_path.relative_to(ROOT)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
