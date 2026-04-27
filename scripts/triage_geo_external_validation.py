#!/usr/bin/env python3
"""Triage GEO series for lightweight external validation routes.

The goal is to avoid blind heavy downloads. The script fetches GEO supplementary
file lists, summarizes file sizes/types, and flags whether a dataset looks
usable for the active CRLM niche hypothesis with a lightweight workflow.

It does not download matrices. It downloads only `filelist.txt` metadata from
NCBI GEO FTP.
"""

from __future__ import annotations

import argparse
import csv
import ssl
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"

DEFAULT_ACCESSIONS = [
    "GSE225857",
    "GSE226997",
    "GSE231559",
    "GSE234804",
    "GSE178318",
]

SERIES_NOTES = {
    "GSE225857": {
        "role": "already-used CRLM single-cell + Visium anchor",
        "hypothesis_use": "positive control and internal benchmark",
    },
    "GSE226997": {
        "role": "CRC primary Visium spatial validation used in 2025 paper",
        "hypothesis_use": "CRC spatial plausibility, not direct CRLM validation",
    },
    "GSE231559": {
        "role": "CRC single-cell raw 10x matrices used by 2025 paper",
        "hypothesis_use": "possible tumor/normal CRC context; needs phenotype mapping",
    },
    "GSE234804": {
        "role": "CRC and liver-metastasis H5Seurat samples used by 2025 paper",
        "hypothesis_use": "best lightweight external CRLM route if H5Seurat can be parsed",
    },
    "GSE178318": {
        "role": "CRLM single-cell dataset referenced by 2025 macrophage/lipid paper",
        "hypothesis_use": "possible independent CRLM microenvironment validation",
    },
}


def series_prefix(accession: str) -> str:
    numeric = accession.replace("GSE", "")
    return f"GSE{numeric[:3]}nnn"


def filelist_url(accession: str) -> str:
    return f"https://ftp.ncbi.nlm.nih.gov/geo/series/{series_prefix(accession)}/{accession}/suppl/filelist.txt"


def gsm_prefix(gsm: str) -> str:
    numeric = gsm.replace("GSM", "")
    return f"GSM{numeric[:4]}nnn"


def supplementary_file_url(accession: str, name: str, archive_or_file: str) -> str:
    if archive_or_file == "File" and name.startswith("GSM"):
        gsm = name.split("_", 1)[0]
        return f"https://ftp.ncbi.nlm.nih.gov/geo/samples/{gsm_prefix(gsm)}/{gsm}/suppl/{name}"
    return f"https://ftp.ncbi.nlm.nih.gov/geo/series/{series_prefix(accession)}/{accession}/suppl/{name}"


def download_text(url: str) -> str:
    ctx = ssl.create_default_context()
    request = urllib.request.Request(url, headers={"User-Agent": "metastasis-research/0.1"})
    with urllib.request.urlopen(request, timeout=120, context=ctx) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_filelist(accession: str, text: str) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    reader = csv.DictReader(text.splitlines(), delimiter="\t")
    for row in reader:
        name = row.get("Name", "")
        if not name:
            continue
        try:
            size = int(row.get("Size", "0"))
        except ValueError:
            size = 0
        rows.append({
            "accession": accession,
            "archive_or_file": row.get("#Archive/File", ""),
            "name": name,
            "time": row.get("Time", ""),
            "size_bytes": size,
            "type": row.get("Type", ""),
            "url": supplementary_file_url(accession, name, row.get("#Archive/File", "")),
        })
    return rows


def size_mb(size_bytes: int) -> float:
    return size_bytes / (1024 * 1024)


def classify(accession: str, rows: list[dict[str, str | int]]) -> tuple[str, str]:
    names = [str(row["name"]).lower() for row in rows if row["archive_or_file"] == "File"]
    file_rows = [row for row in rows if row["archive_or_file"] == "File"]
    total_files_mb = sum(int(row["size_bytes"]) for row in file_rows) / (1024 * 1024)
    has_h5seurat = any(name.endswith(".h5seurat") for name in names)
    has_10x = any("matrix.mtx" in name for name in names) and any("features.tsv" in name for name in names)
    has_visium = any("tissue_positions" in name for name in names)
    has_only_huge_tar = not file_rows and any(row["archive_or_file"] == "Archive" for row in rows)
    has_huge_files = any(int(row["size_bytes"]) > 2_000_000_000 for row in file_rows)

    if accession == "GSE234804" and has_h5seurat and total_files_mb < 800:
        return "high", "Individual CRC/LM H5Seurat files are moderate-sized; best next external CRLM candidate."
    if accession == "GSE226997" and has_huge_files:
        return "low_now", "Only individual Visium TAR files are 9-13 GB; use only if a subset strategy is defined."
    if has_10x and total_files_mb < 1_500:
        return "medium", "Raw 10x files are split and manageable; needs sample phenotype/cell annotation mapping."
    if has_visium and total_files_mb < 1_500:
        return "medium", "Visium components are split and may be analyzable without images."
    if has_only_huge_tar:
        return "low_now", "Only archive-level access detected; avoid for first-pass validation."
    return "needs_review", "File structure requires manual review."


def summarize(accession: str, rows: list[dict[str, str | int]]) -> dict[str, str | int | float]:
    file_rows = [row for row in rows if row["archive_or_file"] == "File"]
    archive_rows = [row for row in rows if row["archive_or_file"] == "Archive"]
    type_counts = Counter(str(row["type"]) for row in file_rows)
    recommendation, reason = classify(accession, rows)
    notes = SERIES_NOTES.get(accession, {})
    return {
        "accession": accession,
        "role": notes.get("role", ""),
        "hypothesis_use": notes.get("hypothesis_use", ""),
        "n_files": len(file_rows),
        "n_archives": len(archive_rows),
        "total_file_mb": round(sum(int(row["size_bytes"]) for row in file_rows) / (1024 * 1024), 2),
        "largest_file_mb": round(max([size_mb(int(row["size_bytes"])) for row in file_rows] or [0]), 2),
        "archive_mb": round(sum(int(row["size_bytes"]) for row in archive_rows) / (1024 * 1024), 2),
        "file_types": ", ".join(f"{key}:{value}" for key, value in sorted(type_counts.items())),
        "recommendation": recommendation,
        "reason": reason,
        "filelist_url": filelist_url(accession),
    }


def write_tsv(rows: list[dict[str, str | int | float]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(summary_rows: list[dict[str, str | int | float]], out_path: Path) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# External validation dataset triage",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "",
        "Identify the next lightweight external validation route for the refined CRLM niche hypothesis:",
        "",
        "`CAF-high spatial niches in CRLM associate with MET+ MYC/glycolytic tumor neighborhoods.`",
        "",
        "## Summary",
        "",
        "| Accession | Role | Files | Total file MB | Largest file MB | Types | Recommendation | Reason |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summary_rows:
        lines.append(
            f"| `{row['accession']}` | {row['role']} | {row['n_files']} | {row['total_file_mb']} | "
            f"{row['largest_file_mb']} | {row['file_types']} | `{row['recommendation']}` | {row['reason']} |"
        )

    best = [row for row in summary_rows if row["recommendation"] == "high"]
    medium = [row for row in summary_rows if row["recommendation"] == "medium"]
    lines.extend([
        "",
        "## Decision",
        "",
    ])
    if best:
        lines.append(
            f"- Best immediate candidate: `{best[0]['accession']}` because {best[0]['reason']}"
        )
    if medium:
        lines.append(
            "- Secondary candidates: "
            + ", ".join(f"`{row['accession']}`" for row in medium)
            + "."
        )
    lines.extend([
        "- Avoid `GSE226997` for now: it is spatially relevant but individual sample TAR files are too large for a quick external validation.",
        "- Next technical step: inspect one `GSE234804` H5Seurat file structure and determine whether expression plus metadata can be extracted without R/Seurat.",
        "",
        "## Caveat",
        "",
        "This triage only evaluates file accessibility and likely utility. It does not validate biology by itself.",
        "",
    ])
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accessions", nargs="*", default=DEFAULT_ACCESSIONS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    all_file_rows: list[dict[str, str | int]] = []
    summary_rows: list[dict[str, str | int | float]] = []

    for accession in args.accessions:
        print(f"[{accession}] fetching filelist...", flush=True)
        try:
            text = download_text(filelist_url(accession))
            rows = parse_filelist(accession, text)
            all_file_rows.extend(rows)
            summary = summarize(accession, rows)
        except Exception as exc:
            notes = SERIES_NOTES.get(accession, {})
            summary = {
                "accession": accession,
                "role": notes.get("role", ""),
                "hypothesis_use": notes.get("hypothesis_use", ""),
                "n_files": 0,
                "n_archives": 0,
                "total_file_mb": 0,
                "largest_file_mb": 0,
                "archive_mb": 0,
                "file_types": "",
                "recommendation": "unavailable",
                "reason": f"Could not fetch GEO filelist: {exc}",
                "filelist_url": filelist_url(accession),
            }
        summary_rows.append(summary)
        print(f"  files: {summary['n_files']}, recommendation: {summary['recommendation']}", flush=True)

    write_tsv(all_file_rows, args.out_dir / "geo_external_filelist.tsv")
    write_tsv(summary_rows, args.out_dir / "geo_external_validation_triage.tsv")
    write_report(summary_rows, args.out_dir / "geo_external_validation_triage_report.md")

    print("Report: geo_external_validation_triage_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
