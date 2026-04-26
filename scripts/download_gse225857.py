#!/usr/bin/env python3
"""Download GSE225857 supplementary files for CRLM single-cell analysis.

Downloads individual files from GEO FTP instead of the full 607 MB TAR.
Each file is downloaded separately so you can pick what you need.

Usage:
    # Download only metadata files (tiny, ~12 MB total)
    python scripts/download_gse225857.py --meta-only

    # Download non-immune compartment (meta + counts, ~88 MB)
    python scripts/download_gse225857.py --non-immune

    # Download everything except spatial images (~300 MB)
    python scripts/download_gse225857.py --all-counts
"""

from __future__ import annotations

import argparse
import gzip
import ssl
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"

BASE_URL = "https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM7058nnn"

FILES = {
    "immune_meta": {
        "url": f"{BASE_URL}/GSM7058754/suppl/GSM7058754_immune_meta.txt.gz",
        "out": "gse225857_immune_meta.tsv",
        "group": "meta",
        "desc": "Immune cell metadata (196k cells, ~10 MB)",
    },
    "immune_counts": {
        "url": f"{BASE_URL}/GSM7058754/suppl/GSM7058754_immune_counts.txt.gz",
        "out": "gse225857_immune_counts.tsv",
        "group": "immune",
        "desc": "Immune cell count matrix (~214 MB)",
    },
    "non_immune_meta": {
        "url": f"{BASE_URL}/GSM7058755/suppl/GSM7058755_non_immune_meta.txt.gz",
        "out": "gse225857_non_immune_meta.tsv",
        "group": "meta",
        "desc": "Non-immune cell metadata (42k cells, ~2 MB)",
    },
    "non_immune_counts": {
        "url": f"{BASE_URL}/GSM7058755/suppl/GSM7058755_non_immune_counts.txt.gz",
        "out": "gse225857_non_immune_counts.tsv",
        "group": "non_immune",
        "desc": "Non-immune cell count matrix (~86 MB)",
    },
}


def download_and_decompress(url: str, out_path: Path) -> bool:
    """Download a gzipped file and save decompressed."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers={"User-Agent": "metastasis-research/0.1"})
    try:
        print(f"  Downloading from GEO...", flush=True)
        with urllib.request.urlopen(req, timeout=600, context=ctx) as resp:
            compressed = resp.read()
        print(f"  Downloaded {len(compressed)/(1024*1024):.1f} MB compressed", flush=True)

        text = gzip.decompress(compressed)
        print(f"  Decompressed to {len(text)/(1024*1024):.1f} MB", flush=True)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("wb") as f:
            f.write(text)
        print(f"  Saved to {out_path.name}", flush=True)
        return True
    except Exception as e:
        print(f"  FAILED: {e}", file=sys.stderr, flush=True)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--meta-only", action="store_true",
                        help="Download only metadata files (~12 MB)")
    parser.add_argument("--non-immune", action="store_true",
                        help="Download non-immune meta + counts (~88 MB)")
    parser.add_argument("--all-counts", action="store_true",
                        help="Download all meta + count files (~312 MB)")
    args = parser.parse_args()

    if not any([args.meta_only, args.non_immune, args.all_counts]):
        args.meta_only = True
        print("No mode specified, defaulting to --meta-only", flush=True)

    groups = set()
    if args.meta_only:
        groups.add("meta")
    if args.non_immune:
        groups.add("meta")
        groups.add("non_immune")
    if args.all_counts:
        groups.add("meta")
        groups.add("non_immune")
        groups.add("immune")

    success = 0
    failed = 0
    for name, info in FILES.items():
        if info["group"] not in groups:
            continue

        out_path = args.out_dir / info["out"]
        if out_path.exists():
            print(f"[SKIP] {name}: {out_path.name} already exists", flush=True)
            success += 1
            continue

        print(f"[{name}] {info['desc']}", flush=True)
        if download_and_decompress(info["url"], out_path):
            success += 1
        else:
            failed += 1

    print(f"\nDone: {success} succeeded, {failed} failed", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
