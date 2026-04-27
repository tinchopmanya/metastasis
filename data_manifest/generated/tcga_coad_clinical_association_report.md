# TCGA-COAD clinical association screen

Generated at: 2026-04-27 05:21:49 UTC

## Purpose

Screen whether CRLM niche signatures scored in TCGA-COAD primary tumors associate with clinical stage, metastatic annotation, lymph-node status, or overall survival.

## Data

- Expression-derived signature scores: `tcga_coad_signature_scores.tsv`.
- Clinical annotations: UCSC Xena `TCGA.COAD.sampleMap/COAD_clinicalMatrix`.
- Joined samples: 329.

## Strongest Stage/Status Associations

| Comparison | Signature | Positive group | Negative group | Mean diff | Cohen d | Mann-Whitney p | Rank delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| n_positive_vs_n0 | `mcam_caf` | positive n=131 | negative n=195 | 0.332 | 0.382 | 6.95e-04 | 0.222 |
| n_positive_vs_n0 | `caf_core` | positive n=131 | negative n=195 | 0.301 | 0.357 | 8.57e-04 | 0.218 |
| lymphatic_invasion_yes_vs_no | `mcam_caf` | positive n=90 | negative n=199 | 0.358 | 0.418 | 1.15e-03 | 0.239 |
| lymphatic_invasion_yes_vs_no | `caf_core` | positive n=90 | negative n=199 | 0.312 | 0.374 | 2.27e-03 | 0.224 |
| n_positive_vs_n0 | `plasticity_emt` | positive n=131 | negative n=195 | 0.143 | 0.331 | 2.98e-03 | 0.194 |
| lymphatic_invasion_yes_vs_no | `caf_met_myc_glycolysis_composite` | positive n=90 | negative n=199 | 0.183 | 0.338 | 4.74e-03 | 0.207 |
| n_positive_vs_n0 | `caf_met_myc_glycolysis_composite` | positive n=131 | negative n=195 | 0.164 | 0.301 | 5.68e-03 | 0.181 |
| advanced_stage_vs_early | `mcam_caf` | advanced n=134 | early n=182 | 0.259 | 0.298 | 1.24e-02 | 0.165 |
| advanced_stage_vs_early | `plasticity_emt` | advanced n=134 | early n=182 | 0.119 | 0.274 | 1.61e-02 | 0.158 |
| advanced_stage_vs_early | `caf_core` | advanced n=134 | early n=182 | 0.228 | 0.269 | 1.64e-02 | 0.158 |
| venous_invasion_yes_vs_no | `mcam_caf` | positive n=66 | negative n=217 | 0.250 | 0.290 | 2.19e-02 | 0.186 |
| m_positive_vs_m0 | `cxcl13_t_cells` | positive n=46 | negative n=217 | -0.265 | -0.324 | 2.32e-02 | -0.213 |

## Survival Median-Split Screen

| Signature | Low n/events | High n/events | Observed high events | Expected high events | Log-rank p |
| --- | --- | --- | --- | --- | --- |
| `caf_core` | 157/33 | 158/46 | 46.000 | 35.791 | 2.03e-02 |
| `mcam_caf` | 157/33 | 158/46 | 46.000 | 36.252 | 2.70e-02 |
| `myc_glycolysis_core` | 157/43 | 158/36 | 36.000 | 42.710 | 1.28e-01 |
| `macrophage_lipid_candidate` | 157/38 | 158/41 | 41.000 | 34.743 | 1.51e-01 |
| `caf_met_myc_glycolysis_composite` | 157/39 | 158/40 | 40.000 | 36.980 | 4.93e-01 |
| `hgf_met_axis` | 157/45 | 158/34 | 34.000 | 36.757 | 5.31e-01 |
| `cxcl13_t_cells` | 157/44 | 158/35 | 35.000 | 37.350 | 5.95e-01 |
| `plasticity_emt` | 157/42 | 158/37 | 37.000 | 36.637 | 9.34e-01 |

## Interpretation

- TCGA-COAD primary tumors are a weak clinical plausibility screen, not a CRLM validation cohort.
- Associations with advanced stage or M/N status would suggest the signatures track aggressive disease biology.
- Lack of survival signal does not falsify a liver-metastatic spatial niche because TCGA lacks spatial and liver-metastasis sampling.
- Treat all p-values as exploratory and unadjusted; this is for prioritization, not biomarker reporting.
