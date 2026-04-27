#!/usr/bin/env python3
"""Search PubMed for recent CRLM niche literature.

The script uses NCBI E-utilities to collect a reproducible literature snapshot
focused on 2025-2026 colorectal liver metastasis (CRLM), spatial/single-cell
omics, CAFs, HGF-MET-MYC-glycolysis, macrophages, metabolism, and immune niches.
It writes a TSV plus a compact Markdown report for research planning.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"

QUERIES = {
    "crlm_spatial_single_cell": (
        '("colorectal liver metastasis"[Title/Abstract] OR "colorectal cancer liver metastasis"[Title/Abstract] '
        'OR CRLM[Title/Abstract]) AND ("spatial transcriptomics"[Title/Abstract] OR "single-cell"[Title/Abstract] '
        'OR "single cell"[Title/Abstract]) AND ("2025"[Date - Publication] : "2026"[Date - Publication])'
    ),
    "caf_fibroblast_crlm": (
        '("colorectal liver metastasis"[Title/Abstract] OR "colorectal cancer liver metastasis"[Title/Abstract] '
        'OR CRLM[Title/Abstract]) AND (CAF[Title/Abstract] OR fibroblast[Title/Abstract] '
        'OR "cancer-associated fibroblast"[Title/Abstract]) AND ("2025"[Date - Publication] : "2026"[Date - Publication])'
    ),
    "hgf_met_myc_glycolysis": (
        '(colorectal[Title/Abstract] AND liver[Title/Abstract] AND metastasis[Title/Abstract]) '
        'AND (HGF[Title/Abstract] OR MET[Title/Abstract] OR MYC[Title/Abstract] OR glycolysis[Title/Abstract]) '
        'AND ("2025"[Date - Publication] : "2026"[Date - Publication])'
    ),
    "macrophage_immune_crlm": (
        '("colorectal liver metastasis"[Title/Abstract] OR "colorectal cancer liver metastasis"[Title/Abstract] '
        'OR CRLM[Title/Abstract]) AND (macrophage[Title/Abstract] OR myeloid[Title/Abstract] '
        'OR immune[Title/Abstract] OR SPP1[Title/Abstract]) AND ("2025"[Date - Publication] : "2026"[Date - Publication])'
    ),
    "metabolism_proteomics_crlm": (
        '("colorectal liver metastasis"[Title/Abstract] OR "colorectal cancer liver metastasis"[Title/Abstract] '
        'OR CRLM[Title/Abstract]) AND (metabolic[Title/Abstract] OR metabolism[Title/Abstract] '
        'OR proteomic[Title/Abstract] OR phosphoproteomic[Title/Abstract]) '
        'AND ("2025"[Date - Publication] : "2026"[Date - Publication])'
    ),
}


EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def get_url(url: str, attempts: int = 3) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "metastasis-research/0.1"})
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return response.read()
        except Exception as exc:  # noqa: BLE001 - keep the script dependency-free.
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(1.5 * attempt)
    raise RuntimeError(f"Failed to fetch URL after {attempts} attempts: {url}") from last_error


def esearch(query: str, retmax: int) -> list[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": str(retmax),
        "sort": "pub+date",
        "retmode": "xml",
    }
    url = f"{EUTILS}/esearch.fcgi?{urllib.parse.urlencode(params)}"
    root = ET.fromstring(get_url(url))
    return [node.text or "" for node in root.findall(".//Id")]


def text_of(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return "".join(node.itertext()).strip()


def article_date(article: ET.Element) -> str:
    pub_date = article.find(".//JournalIssue/PubDate")
    if pub_date is None:
        return ""
    year = text_of(pub_date.find("Year"))
    month = text_of(pub_date.find("Month"))
    day = text_of(pub_date.find("Day"))
    medline = text_of(pub_date.find("MedlineDate"))
    if year:
        return "-".join(part for part in [year, month, day] if part)
    return medline


def doi_for(article: ET.Element) -> str:
    for node in article.findall(".//ArticleId"):
        if node.attrib.get("IdType") == "doi":
            return text_of(node)
    for node in article.findall(".//ELocationID"):
        if node.attrib.get("EIdType") == "doi":
            return text_of(node)
    return ""


def publication_date_key(pub_date: str) -> tuple[int, int, int]:
    """Return a sortable date tuple from PubMed's mixed date strings."""
    match = re.search(r"(\d{4})(?:-([A-Za-z]{3}|\d{1,2}))?(?:-(\d{1,2}))?", pub_date)
    if not match:
        return (0, 0, 0)
    year = int(match.group(1))
    raw_month = match.group(2) or "1"
    if raw_month.isdigit():
        month = int(raw_month)
    else:
        month = MONTHS.get(raw_month[:3].lower(), 1)
    day = int(match.group(3) or "1")
    return (year, month, day)


def pmid_key(pmid: str) -> int:
    return int(pmid) if pmid.isdigit() else 0


def fetch_details(pmids: list[str]) -> list[dict[str, str]]:
    if not pmids:
        return []
    rows: list[dict[str, str]] = []
    for i in range(0, len(pmids), 40):
        chunk = pmids[i:i + 40]
        params = {
            "db": "pubmed",
            "id": ",".join(chunk),
            "retmode": "xml",
        }
        url = f"{EUTILS}/efetch.fcgi?{urllib.parse.urlencode(params)}"
        root = ET.fromstring(get_url(url))
        for article in root.findall(".//PubmedArticle"):
            pmid = text_of(article.find(".//PMID"))
            title = html.unescape(text_of(article.find(".//ArticleTitle")))
            journal = text_of(article.find(".//Journal/Title"))
            abstract = " ".join(text_of(node) for node in article.findall(".//Abstract/AbstractText"))
            doi = doi_for(article)
            rows.append({
                "pmid": pmid,
                "title": title,
                "journal": journal,
                "pub_date": article_date(article),
                "doi": doi,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
                "abstract": html.unescape(abstract),
            })
        time.sleep(0.34)
    return rows


def tag_article(row: dict[str, str]) -> str:
    blob = f"{row['title']} {row['abstract']}".lower()
    tags: list[str] = []
    tag_patterns = [
        ("spatial", [r"\bspatial\b", r"\bvisium\b", r"hd spatial"]),
        ("single_cell", [r"\bsingle-cell\b", r"\bsingle cell\b", r"\bscrna\b"]),
        ("caf", [r"\bcaf\b", r"\bcafs\b", r"\bfibroblast", r"cancer-associated fibroblast"]),
        ("hgf_met_myc", [r"\bhgf\b", r"\bmet\b", r"\bmyc\b"]),
        ("glycolysis_metabolism", [r"\bglycolysis\b", r"\bmetabolic\b", r"\bmetabolism\b", r"\bproteomic\b", r"\bphosphoproteomic\b"]),
        ("immune_myeloid", [r"\bmacrophage", r"\bmyeloid\b", r"\bimmune\b", r"\bspp1\b", r"\bhla-drb5\b", r"\bt cell\b", r"\btreg\b"]),
        ("therapy_resistance", [r"\btherapy\b", r"\bimmunotherapy\b", r"\bresistance\b", r"\bprognostic\b"]),
    ]
    for label, patterns in tag_patterns:
        if any(re.search(pattern, blob) for pattern in patterns):
            tags.append(label)
    return ",".join(tags)


def write_tsv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = ["pmid", "title", "journal", "pub_date", "doi", "url", "queries", "tags", "abstract"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict[str, str]], query_counts: dict[str, int], out_path: Path) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    by_tag: dict[str, int] = defaultdict(int)
    for row in rows:
        for tag in row["tags"].split(","):
            if tag:
                by_tag[tag] += 1

    prioritized = []
    priority_terms = ["spatial", "single_cell", "caf", "hgf_met_myc", "glycolysis_metabolism", "immune_myeloid"]
    for row in rows:
        score = sum(1 for tag in priority_terms if tag in row["tags"].split(","))
        if score >= 2:
            prioritized.append((score, row))
    prioritized.sort(
        key=lambda item: (
            publication_date_key(item[1]["pub_date"]),
            item[0],
            pmid_key(item[1]["pmid"]),
        ),
        reverse=True,
    )

    lines = [
        "# PubMed latest CRLM niche literature snapshot",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Query Counts",
        "",
        "| Query | PMIDs |",
        "| --- | --- |",
    ]
    for query, count in query_counts.items():
        lines.append(f"| `{query}` | {count} |")

    lines.extend([
        "",
        "## Tag Counts",
        "",
        "| Tag | Articles |",
        "| --- | --- |",
    ])
    for tag, count in sorted(by_tag.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{tag}` | {count} |")

    lines.extend([
        "",
        "## Prioritized Articles",
        "",
        "| Date | PMID | Title | Tags |",
        "| --- | --- | --- | --- |",
    ])
    for _, row in prioritized[:20]:
        lines.append(
            f"| {row['pub_date']} | [{row['pmid']}]({row['url']}) | {row['title']} | `{row['tags']}` |"
        )

    lines.extend([
        "",
        "## Immediate Research Reading",
        "",
        "- Compare new 2026 immune/myeloid and SPP1/CXCL12/CAF papers against the current CAF-high spatial-niche model.",
        "- Treat HGF-MET-MYC as one candidate stromal-tumor axis, not the entire niche.",
        "- Prioritize spatial/cell-state evidence over sample-level averages.",
        "",
    ])
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retmax", type=int, default=50)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    pmid_to_queries: dict[str, set[str]] = defaultdict(set)
    query_counts: dict[str, int] = {}
    for name, query in QUERIES.items():
        print(f"[{name}] searching PubMed...", flush=True)
        pmids = esearch(query, args.retmax)
        query_counts[name] = len(pmids)
        for pmid in pmids:
            pmid_to_queries[pmid].add(name)
        print(f"  PMIDs: {len(pmids)}", flush=True)
        time.sleep(0.34)

    all_pmids = sorted(pmid_to_queries.keys())
    print(f"Fetching details for {len(all_pmids)} unique PMIDs...", flush=True)
    rows = fetch_details(all_pmids)
    for row in rows:
        row["queries"] = ",".join(sorted(pmid_to_queries[row["pmid"]]))
        row["tags"] = tag_article(row)

    rows.sort(
        key=lambda row: (publication_date_key(row["pub_date"]), pmid_key(row["pmid"])),
        reverse=True,
    )
    write_tsv(rows, args.out_dir / "pubmed_crlm_latest_2025_2026.tsv")
    write_report(rows, query_counts, args.out_dir / "pubmed_crlm_latest_2025_2026_report.md")

    print(f"Unique PMIDs: {len(rows)}")
    print("Report: pubmed_crlm_latest_2025_2026_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
