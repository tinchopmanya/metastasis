# Spatial niche multi-dataset effect consolidation

Generated at: 2026-04-29 05:36:54 UTC

## Purpose

Consolidate key CAF/SPP1-CXCL12/HLA-DRB5/MYC-glycolysis spatial adjacency effects across GSE225857 and GSE217414.

## Summary

| Effect | Layer | Samples | Positive | p<=0.05 | Mean ratio | Range | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `caf_to_hla_drb5_lite` | CAF-to-myeloid | 6 | 6/6 | 6/6 | 1.417 | 1.080-1.859 | strong_reproducible |
| `caf_to_met` | CAF-to-MET | 6 | 6/6 | 5/6 | 1.723 | 1.012-1.955 | strong_reproducible |
| `caf_to_spp1_cxcl12_lite` | CAF-to-stromal/myeloid | 6 | 6/6 | 5/6 | 1.399 | 1.022-1.585 | strong_reproducible |
| `hla_drb5_lite_to_myc` | myeloid-to-MYC | 6 | 6/6 | 5/6 | 1.330 | 1.039-1.535 | strong_reproducible |
| `hla_drb5_lite_to_myc_glycolysis_lite` | myeloid-to-tumor-metabolic | 6 | 6/6 | 6/6 | 1.357 | 1.052-1.561 | strong_reproducible |
| `spp1_cxcl12_lite_to_myc` | stromal/myeloid-to-MYC | 6 | 6/6 | 6/6 | 1.625 | 1.344-2.125 | strong_reproducible |
| `spp1_cxcl12_lite_to_myc_glycolysis_lite` | stromal/myeloid-to-tumor-metabolic | 6 | 6/6 | 6/6 | 1.718 | 1.455-2.143 | strong_reproducible |

## Interpretation

- `strong_reproducible` means the effect is positive across all included samples and significant in all or all-but-one samples across at least two datasets.
- This is still a first-pass consolidation, not a final statistical meta-analysis.
- The next required step is specificity: negative signatures, expression-matched random signatures, and spatial nulls that control tissue autocorrelation.

## Sample-Level Rows

| Dataset | Sample | Effect | Ratio | p | z |
| --- | --- | --- | --- | --- | --- |
| GSE225857 | L1 | `caf_to_met` | 1.955 | 0.002 | 17.931 |
| GSE225857 | L1 | `caf_to_spp1_cxcl12_lite` | 1.585 | 0.002 | 30.881 |
| GSE225857 | L1 | `caf_to_hla_drb5_lite` | 1.859 | 0.002 | 33.910 |
| GSE225857 | L1 | `spp1_cxcl12_lite_to_myc` | 1.344 | 0.002 | 14.077 |
| GSE225857 | L1 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 1.471 | 0.002 | 19.642 |
| GSE225857 | L1 | `hla_drb5_lite_to_myc` | 1.132 | 0.002 | 5.194 |
| GSE225857 | L1 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.222 | 0.002 | 9.849 |
| GSE225857 | L2 | `caf_to_met` | 1.875 | 0.002 | 9.279 |
| GSE225857 | L2 | `caf_to_spp1_cxcl12_lite` | 1.424 | 0.002 | 14.059 |
| GSE225857 | L2 | `caf_to_hla_drb5_lite` | 1.080 | 0.030 | 1.952 |
| GSE225857 | L2 | `spp1_cxcl12_lite_to_myc` | 1.666 | 0.002 | 22.040 |
| GSE225857 | L2 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 1.734 | 0.002 | 26.307 |
| GSE225857 | L2 | `hla_drb5_lite_to_myc` | 1.039 | 0.128 | 1.140 |
| GSE225857 | L2 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.052 | 0.028 | 1.887 |
| GSE217414 | 19G081 | `caf_to_met` | 1.794 | 0.002 | 6.165 |
| GSE217414 | 19G081 | `caf_to_spp1_cxcl12_lite` | 1.407 | 0.002 | 19.376 |
| GSE217414 | 19G081 | `caf_to_hla_drb5_lite` | 1.491 | 0.002 | 8.176 |
| GSE217414 | 19G081 | `spp1_cxcl12_lite_to_myc` | 1.766 | 0.002 | 17.908 |
| GSE217414 | 19G081 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 1.945 | 0.002 | 28.101 |
| GSE217414 | 19G081 | `hla_drb5_lite_to_myc` | 1.535 | 0.002 | 7.070 |
| GSE217414 | 19G081 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.434 | 0.002 | 6.293 |
| GSE217414 | 19G0619 | `caf_to_met` | 1.012 | 0.471 | -0.099 |
| GSE217414 | 19G0619 | `caf_to_spp1_cxcl12_lite` | 1.022 | 0.128 | 1.171 |
| GSE217414 | 19G0619 | `caf_to_hla_drb5_lite` | 1.330 | 0.002 | 6.359 |
| GSE217414 | 19G0619 | `spp1_cxcl12_lite_to_myc` | 1.474 | 0.002 | 5.978 |
| GSE217414 | 19G0619 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 1.559 | 0.002 | 10.374 |
| GSE217414 | 19G0619 | `hla_drb5_lite_to_myc` | 1.474 | 0.010 | 3.101 |
| GSE217414 | 19G0619 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.561 | 0.002 | 5.515 |
| GSE217414 | 19G0635 | `caf_to_met` | 1.758 | 0.002 | 9.656 |
| GSE217414 | 19G0635 | `caf_to_spp1_cxcl12_lite` | 1.401 | 0.002 | 24.699 |
| GSE217414 | 19G0635 | `caf_to_hla_drb5_lite` | 1.514 | 0.002 | 8.473 |
| GSE217414 | 19G0635 | `spp1_cxcl12_lite_to_myc` | 1.378 | 0.002 | 21.781 |
| GSE217414 | 19G0635 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 1.455 | 0.002 | 21.174 |
| GSE217414 | 19G0635 | `hla_drb5_lite_to_myc` | 1.485 | 0.002 | 14.518 |
| GSE217414 | 19G0635 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.542 | 0.002 | 13.779 |
| GSE217414 | 19G02977 | `caf_to_met` | 1.942 | 0.040 | 1.967 |
| GSE217414 | 19G02977 | `caf_to_spp1_cxcl12_lite` | 1.553 | 0.002 | 15.634 |
| GSE217414 | 19G02977 | `caf_to_hla_drb5_lite` | 1.227 | 0.026 | 1.966 |
| GSE217414 | 19G02977 | `spp1_cxcl12_lite_to_myc` | 2.125 | 0.002 | 19.111 |
| GSE217414 | 19G02977 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 2.143 | 0.002 | 21.068 |
| GSE217414 | 19G02977 | `hla_drb5_lite_to_myc` | 1.315 | 0.002 | 5.082 |
| GSE217414 | 19G02977 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.330 | 0.002 | 6.156 |
