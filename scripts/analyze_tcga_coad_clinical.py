#!/usr/bin/env python3
"""Clinical association screen for TCGA-COAD CRLM niche signatures.

This is a lightweight, dependency-free analysis that joins previously computed
TCGA-COAD signature scores with UCSC Xena clinical annotations. It tests whether
the active CRLM niche signatures show screening-level associations with stage,
metastatic annotation, lymph-node status, and overall survival in primary colon
tumors.

Important limitation: TCGA-COAD primary tumors do not prove colorectal liver
metastasis biology. Positive associations are clinical plausibility signals;
negative associations do not falsify a spatial liver-metastatic niche.
"""

from __future__ import annotations

import argparse
import csv
import math
import ssl
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "data_manifest" / "generated"
DEFAULT_SCORES = DEFAULT_OUT_DIR / "tcga_coad_signature_scores.tsv"
DEFAULT_CLINICAL = DEFAULT_OUT_DIR / "tcga_coad_clinicalMatrix.tsv"
CLINICAL_URL = "https://tcga.xenahubs.net/download/TCGA.COAD.sampleMap/COAD_clinicalMatrix"

SIGNATURES_OF_INTEREST = [
    "caf_core",
    "mcam_caf",
    "hgf_met_axis",
    "myc_glycolysis_core",
    "plasticity_emt",
    "macrophage_lipid_candidate",
    "cxcl13_t_cells",
    "caf_met_myc_glycolysis_composite",
]


def download_file(url: str, out_path: Path) -> None:
    if out_path.exists() and out_path.stat().st_size > 0:
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context()
    request = urllib.request.Request(url, headers={"User-Agent": "metastasis-research/0.1"})
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    with urllib.request.urlopen(request, timeout=120, context=ctx) as response:
        tmp_path.write_bytes(response.read())
    tmp_path.replace(out_path)


def read_scores(path: Path) -> dict[str, dict[str, float]]:
    rows: dict[str, dict[str, float]] = {}
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            sample_id = row["sample_id"]
            values: dict[str, float] = {}
            for key, value in row.items():
                if key == "sample_id":
                    continue
                try:
                    values[key] = float(value)
                except (TypeError, ValueError):
                    values[key] = float("nan")
            composite_genes = [
                values.get("caf_core", float("nan")),
                values.get("mcam_caf", float("nan")),
                values.get("hgf_met_axis", float("nan")),
                values.get("myc_glycolysis_core", float("nan")),
            ]
            values["caf_met_myc_glycolysis_composite"] = mean(composite_genes)
            rows[sample_id] = values
    return rows


def read_clinical(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            sample_id = row.get("sampleID", "")
            if sample_id:
                rows[sample_id] = row
    return rows


def mean(values: list[float]) -> float:
    valid = [v for v in values if not math.isnan(v)]
    return sum(valid) / len(valid) if valid else float("nan")


def std(values: list[float]) -> float:
    valid = [v for v in values if not math.isnan(v)]
    if len(valid) < 2:
        return float("nan")
    m = sum(valid) / len(valid)
    return math.sqrt(sum((v - m) ** 2 for v in valid) / (len(valid) - 1))


def median(values: list[float]) -> float:
    valid = sorted(v for v in values if not math.isnan(v))
    if not valid:
        return float("nan")
    mid = len(valid) // 2
    if len(valid) % 2:
        return valid[mid]
    return (valid[mid - 1] + valid[mid]) / 2


def normal_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def mann_whitney(group_a: list[float], group_b: list[float]) -> tuple[float, float, float]:
    """Return U for group_a, normal-approx two-sided p, and Cliff-like delta."""
    a = [v for v in group_a if not math.isnan(v)]
    b = [v for v in group_b if not math.isnan(v)]
    n1, n2 = len(a), len(b)
    if n1 == 0 or n2 == 0:
        return float("nan"), float("nan"), float("nan")

    combined = [(v, 0) for v in a] + [(v, 1) for v in b]
    combined.sort(key=lambda item: item[0])

    ranks: list[float] = [0.0] * len(combined)
    i = 0
    while i < len(combined):
        j = i + 1
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j

    rank_sum_a = sum(rank for rank, (_, group) in zip(ranks, combined) if group == 0)
    u1 = rank_sum_a - n1 * (n1 + 1) / 2
    mean_u = n1 * n2 / 2
    sd_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if sd_u == 0:
        return u1, float("nan"), float("nan")
    z = (u1 - mean_u) / sd_u
    p = 2 * (1 - normal_cdf(abs(z)))
    delta = (2 * u1 / (n1 * n2)) - 1
    return u1, max(p, 1e-300), delta


def cohen_d(group_a: list[float], group_b: list[float]) -> float:
    a = [v for v in group_a if not math.isnan(v)]
    b = [v for v in group_b if not math.isnan(v)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    pooled_num = (len(a) - 1) * std(a) ** 2 + (len(b) - 1) * std(b) ** 2
    pooled_den = len(a) + len(b) - 2
    if pooled_den <= 0 or pooled_num <= 0:
        return float("nan")
    return (mean(a) - mean(b)) / math.sqrt(pooled_num / pooled_den)


def stage_group(stage: str) -> str:
    normalized = (stage or "").strip().upper()
    if "STAGE I" == normalized or normalized.startswith("STAGE IA") or normalized.startswith("STAGE IB"):
        return "early"
    if normalized.startswith("STAGE II") and not normalized.startswith("STAGE III"):
        return "early"
    if normalized.startswith("STAGE III") or normalized.startswith("STAGE IV"):
        return "advanced"
    return ""


def binary_status(value: str, positive_prefixes: tuple[str, ...], negative_values: tuple[str, ...]) -> str:
    normalized = (value or "").strip().upper()
    if normalized in negative_values:
        return "negative"
    if any(normalized.startswith(prefix) for prefix in positive_prefixes):
        return "positive"
    return ""


def parse_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def survival_time_event(clinical: dict[str, str]) -> tuple[float, int]:
    vital = (clinical.get("vital_status") or "").strip().upper()
    death = parse_float(clinical.get("days_to_death", ""))
    followup = parse_float(clinical.get("days_to_last_followup", ""))
    if vital == "DECEASED" and not math.isnan(death) and death > 0:
        return death, 1
    if not math.isnan(followup) and followup > 0:
        return followup, 0
    if not math.isnan(death) and death > 0:
        return death, 1 if vital == "DECEASED" else 0
    return float("nan"), 0


def logrank_test(low: list[tuple[float, int]], high: list[tuple[float, int]]) -> tuple[float, int, int, float, float]:
    """Two-group log-rank test with chi-square(1) p approximation."""
    low = [(t, e) for t, e in low if not math.isnan(t) and t > 0]
    high = [(t, e) for t, e in high if not math.isnan(t) and t > 0]
    event_times = sorted({t for t, e in low + high if e == 1})
    if not event_times:
        return float("nan"), len(low), len(high), 0, float("nan")

    observed_high = 0.0
    expected_high = 0.0
    variance_high = 0.0
    for t in event_times:
        risk_low = sum(1 for time, _ in low if time >= t)
        risk_high = sum(1 for time, _ in high if time >= t)
        events_low = sum(1 for time, event in low if time == t and event == 1)
        events_high = sum(1 for time, event in high if time == t and event == 1)
        risk_total = risk_low + risk_high
        events_total = events_low + events_high
        if risk_total <= 1 or events_total == 0:
            continue
        observed_high += events_high
        expected_high += events_total * (risk_high / risk_total)
        variance_high += (
            risk_low * risk_high * events_total * (risk_total - events_total)
        ) / (risk_total ** 2 * (risk_total - 1))

    if variance_high <= 0:
        return float("nan"), len(low), len(high), observed_high, expected_high

    chi_square = (observed_high - expected_high) ** 2 / variance_high
    # Survival function for chi-square with 1 df.
    p = math.erfc(math.sqrt(chi_square / 2))
    return max(p, 1e-300), len(low), len(high), observed_high, expected_high


def joined_records(
    scores: dict[str, dict[str, float]],
    clinical: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for sample_id, score_values in scores.items():
        clin = clinical.get(sample_id)
        if not clin:
            continue
        rows.append({
            "sample_id": sample_id,
            "scores": score_values,
            "clinical": clin,
        })
    return rows


def compare_groups(
    records: list[dict[str, object]],
    group_name: str,
    group_getter,
) -> list[dict[str, str | float | int]]:
    results: list[dict[str, str | float | int]] = []
    for sig in SIGNATURES_OF_INTEREST:
        group_values: dict[str, list[float]] = defaultdict(list)
        for rec in records:
            group = group_getter(rec["clinical"])  # type: ignore[index]
            if group:
                group_values[group].append(rec["scores"].get(sig, float("nan")))  # type: ignore[index]
        if set(group_values) != {"negative", "positive"} and set(group_values) != {"early", "advanced"}:
            continue
        if "advanced" in group_values:
            positive_label, negative_label = "advanced", "early"
        else:
            positive_label, negative_label = "positive", "negative"
        positive = group_values[positive_label]
        negative = group_values[negative_label]
        _, p, delta = mann_whitney(positive, negative)
        results.append({
            "comparison": group_name,
            "signature": sig,
            "positive_label": positive_label,
            "negative_label": negative_label,
            "n_positive": len([v for v in positive if not math.isnan(v)]),
            "n_negative": len([v for v in negative if not math.isnan(v)]),
            "mean_positive": mean(positive),
            "mean_negative": mean(negative),
            "mean_difference": mean(positive) - mean(negative),
            "cohen_d": cohen_d(positive, negative),
            "mann_whitney_p": p,
            "rank_delta": delta,
        })
    return results


def survival_results(records: list[dict[str, object]]) -> list[dict[str, str | float | int]]:
    results: list[dict[str, str | float | int]] = []
    for sig in SIGNATURES_OF_INTEREST:
        scored = [
            (
                rec["scores"].get(sig, float("nan")),  # type: ignore[index]
                survival_time_event(rec["clinical"]),  # type: ignore[arg-type]
            )
            for rec in records
        ]
        valid_scores = [score for score, (time, _) in scored if not math.isnan(score) and not math.isnan(time)]
        cutoff = median(valid_scores)
        if math.isnan(cutoff):
            continue
        low = [(time, event) for score, (time, event) in scored if not math.isnan(score) and score < cutoff and not math.isnan(time)]
        high = [(time, event) for score, (time, event) in scored if not math.isnan(score) and score >= cutoff and not math.isnan(time)]
        p, n_low, n_high, observed_high, expected_high = logrank_test(low, high)
        results.append({
            "signature": sig,
            "cutoff_median": cutoff,
            "n_low": n_low,
            "n_high": n_high,
            "events_low": sum(event for _, event in low),
            "events_high": sum(event for _, event in high),
            "observed_events_high": observed_high,
            "expected_events_high": expected_high,
            "logrank_p": p,
        })
    return results


def write_tsv(rows: list[dict[str, str | float | int]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: object, digits: int = 3) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return "NA"
        return f"{value:.{digits}f}"
    return str(value)


def best_rows(rows: list[dict[str, str | float | int]], p_key: str, limit: int = 8) -> list[dict[str, str | float | int]]:
    return sorted(rows, key=lambda row: float(row[p_key]) if not math.isnan(float(row[p_key])) else 1.0)[:limit]


def write_report(
    records: list[dict[str, object]],
    group_rows: list[dict[str, str | float | int]],
    survival_rows: list[dict[str, str | float | int]],
    out_path: Path,
) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# TCGA-COAD clinical association screen",
        "",
        f"Generated at: {generated_at}",
        "",
        "## Purpose",
        "",
        "Screen whether CRLM niche signatures scored in TCGA-COAD primary tumors associate with clinical stage, metastatic annotation, lymph-node status, or overall survival.",
        "",
        "## Data",
        "",
        "- Expression-derived signature scores: `tcga_coad_signature_scores.tsv`.",
        "- Clinical annotations: UCSC Xena `TCGA.COAD.sampleMap/COAD_clinicalMatrix`.",
        f"- Joined samples: {len(records)}.",
        "",
        "## Strongest Stage/Status Associations",
        "",
        "| Comparison | Signature | Positive group | Negative group | Mean diff | Cohen d | Mann-Whitney p | Rank delta |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in best_rows(group_rows, "mann_whitney_p", 12):
        lines.append(
            f"| {row['comparison']} | `{row['signature']}` | {row['positive_label']} n={row['n_positive']} | "
            f"{row['negative_label']} n={row['n_negative']} | {fmt(row['mean_difference'])} | "
            f"{fmt(row['cohen_d'])} | {float(row['mann_whitney_p']):.2e} | {fmt(row['rank_delta'])} |"
        )

    lines.extend([
        "",
        "## Survival Median-Split Screen",
        "",
        "| Signature | Low n/events | High n/events | Observed high events | Expected high events | Log-rank p |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for row in best_rows(survival_rows, "logrank_p", len(survival_rows)):
        lines.append(
            f"| `{row['signature']}` | {row['n_low']}/{row['events_low']} | {row['n_high']}/{row['events_high']} | "
            f"{fmt(row['observed_events_high'])} | {fmt(row['expected_events_high'])} | "
            f"{float(row['logrank_p']):.2e} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "- TCGA-COAD primary tumors are a weak clinical plausibility screen, not a CRLM validation cohort.",
        "- Associations with advanced stage or M/N status would suggest the signatures track aggressive disease biology.",
        "- Lack of survival signal does not falsify a liver-metastatic spatial niche because TCGA lacks spatial and liver-metastasis sampling.",
        "- Treat all p-values as exploratory and unadjusted; this is for prioritization, not biomarker reporting.",
        "",
    ])
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", type=Path, default=DEFAULT_SCORES)
    parser.add_argument("--clinical", type=Path, default=DEFAULT_CLINICAL)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    download_file(CLINICAL_URL, args.clinical)
    scores = read_scores(args.scores)
    clinical = read_clinical(args.clinical)
    records = joined_records(scores, clinical)

    group_rows: list[dict[str, str | float | int]] = []
    group_rows.extend(compare_groups(records, "advanced_stage_vs_early", lambda c: stage_group(c.get("pathologic_stage", ""))))
    group_rows.extend(compare_groups(records, "m_positive_vs_m0", lambda c: binary_status(c.get("pathologic_M", ""), ("M1",), ("M0",))))
    group_rows.extend(compare_groups(records, "n_positive_vs_n0", lambda c: binary_status(c.get("pathologic_N", ""), ("N1", "N2"), ("N0",))))
    group_rows.extend(compare_groups(records, "lymphatic_invasion_yes_vs_no", lambda c: binary_status(c.get("lymphatic_invasion", ""), ("YES",), ("NO",))))
    group_rows.extend(compare_groups(records, "venous_invasion_yes_vs_no", lambda c: binary_status(c.get("venous_invasion", ""), ("YES",), ("NO",))))

    surv_rows = survival_results(records)

    write_tsv(group_rows, args.out_dir / "tcga_coad_clinical_signature_associations.tsv")
    write_tsv(surv_rows, args.out_dir / "tcga_coad_signature_survival.tsv")
    write_report(records, group_rows, surv_rows, args.out_dir / "tcga_coad_clinical_association_report.md")

    print(f"Joined samples: {len(records)}")
    print(f"Clinical comparisons: {len(group_rows)}")
    print(f"Survival tests: {len(surv_rows)}")
    print("Report: tcga_coad_clinical_association_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
