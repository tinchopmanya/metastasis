# GSE245552 paired scRNA external validation

Generated at: 2026-04-27 20:45:59 UTC

## Purpose

Pressure-test whether the 2026 `CAF/SPP1-CXCL12/metabolic` macro-niche has support in an independent paired primary CRC/liver-metastasis scRNA cohort.

## Dataset

- Samples in GEO metadata: 39.
- Processed samples: 39.
- Tissues include primary tumor, liver metastasis, colon adjacent tissue, and liver adjacent tissue.
- This is not spatial; it is a paired single-cell sample/compartment-proxy validation.

## Key LM vs Primary Comparisons

| Metric | LM mean | Primary mean | LM-primary | LM/primary | p | Rank delta | Paired mean delta | Positive pairs | Sign p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `score_spp1_cxcl12_axis_desoverlap_2026` | 0.393 | 0.345 | 0.048 | 1.140 | 3.68e-01 | 0.184 | 0.029 | 7/13 | 1.000 |
| `score_spp1_cxcl12_caf_myeloid_axis` | 0.582 | 0.471 | 0.111 | 1.236 | 2.80e-02 | 0.449 | 0.100 | 8/13 | 0.581 |
| `score_myc_glycolysis_desoverlap_2026` | 0.569 | 0.473 | 0.096 | 1.202 | 8.38e-02 | 0.353 | 0.088 | 8/13 | 0.581 |
| `score_hla_drb5_macrophage_axis_desoverlap_2026` | 0.758 | 0.600 | 0.158 | 1.264 | 1.60e-01 | 0.287 | 0.124 | 8/13 | 0.581 |
| `score_caf_core_desoverlap_2026` | 0.080 | 0.103 | -0.023 | 0.780 | 4.28e-01 | -0.162 | -0.030 | 5/13 | 0.581 |
| `fraction_caf_proxy` | 0.034 | 0.065 | -0.031 | 0.526 | 1.30e-01 | -0.309 | -0.034 | 6/13 | 1.000 |
| `fraction_myeloid_proxy` | 0.274 | 0.264 | 0.010 | 1.037 | 6.92e-01 | -0.081 | -0.016 | 5/13 | 0.581 |
| `fraction_tumor_epithelial_proxy` | 0.374 | 0.294 | 0.080 | 1.273 | 9.14e-01 | -0.022 | 0.097 | 8/13 | 0.581 |
| `caf_proxy__score_spp1_cxcl12_axis_desoverlap_2026` | 0.993 | 0.730 | 0.263 | 1.361 | 3.07e-02 | 0.441 | 0.268 | 11/13 | 0.022 |
| `myeloid_proxy__score_spp1_cxcl12_axis_desoverlap_2026` | 0.563 | 0.306 | 0.258 | 1.844 | 1.34e-04 | 0.779 | 0.275 | 13/13 | 0.000 |
| `tumor_epithelial_proxy__score_myc_glycolysis_desoverlap_2026` | 0.758 | 0.784 | -0.026 | 0.967 | 6.92e-01 | -0.081 | -0.073 | 5/13 | 0.581 |
| `myeloid_proxy__score_hla_drb5_macrophage_axis_desoverlap_2026` | 1.482 | 1.003 | 0.479 | 1.478 | 1.72e-03 | 0.640 | 0.500 | 12/13 | 0.003 |

## Interpretation

- Whole-sample `SPP1/CXCL12-lite` LM/primary ratio: 1.140.
- Whole-sample `MYC/glycolysis-lite` LM/primary ratio: 1.202.
- Whole-sample `HLA-DRB5-lite` LM/primary ratio: 1.264.
- CAF-proxy `SPP1/CXCL12-lite` LM/primary ratio: 1.361.
- Myeloid-proxy `SPP1/CXCL12-lite` LM/primary ratio: 1.844.
- Tumor-proxy `MYC/glycolysis-lite` LM/primary ratio: 0.967.
- Myeloid-proxy `HLA-DRB5-lite` LM/primary ratio: 1.478.

## Caveats

- Coarse cell proxies are marker-based, not curated annotations.
- Expression is computed from raw 10x counts with log1p summaries, not full scRNA normalization/integration.
- This validates sample/cell-state pressure, not spatial adjacency.
- Strong positive results here would motivate a paper-grade integrated analysis; weak results would push the claim back toward spatial specificity.
