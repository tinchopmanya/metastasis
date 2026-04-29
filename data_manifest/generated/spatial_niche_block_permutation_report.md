# Spatial niche block-permutation audit

Generated at: 2026-04-29 05:46:24 UTC

## Purpose

Stress-test key CRLM spatial niche effects against a block-permutation null that shuffles target values only within coarse spatial blocks.

## Summary

| Effect | Samples | Positive | Block p<=0.05 | Mean ratio | Mean block p | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `caf_to_hla_drb5_lite` | 6 | 6/6 | 5/6 | 1.417 | 0.047 | survives_block_null |
| `caf_to_met` | 6 | 6/6 | 2/6 | 1.723 | 0.275 | positive_but_explained_by_blocks |
| `caf_to_spp1_cxcl12_lite` | 6 | 6/6 | 4/6 | 1.399 | 0.243 | partially_survives_block_null |
| `hla_drb5_lite_to_myc` | 6 | 6/6 | 5/6 | 1.330 | 0.068 | survives_block_null |
| `hla_drb5_lite_to_myc_glycolysis_lite` | 6 | 6/6 | 5/6 | 1.357 | 0.047 | survives_block_null |
| `spp1_cxcl12_lite_to_myc` | 6 | 6/6 | 5/6 | 1.625 | 0.021 | survives_block_null |
| `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 6 | 6/6 | 6/6 | 1.718 | 0.003 | survives_block_null |

## Sample-Level Rows

| Dataset | Sample | Effect | Ratio | Block null mean | Block p | z |
| --- | --- | --- | --- | --- | --- | --- |
| GSE217414 | 19G02977 | `caf_to_spp1_cxcl12_lite` | 1.553 | 1.638 | 0.984 | -2.127 |
| GSE217414 | 19G02977 | `caf_to_hla_drb5_lite` | 1.227 | 1.020 | 0.016 | 2.295 |
| GSE217414 | 19G02977 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 2.143 | 1.844 | 0.002 | 3.693 |
| GSE217414 | 19G02977 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.330 | 1.157 | 0.002 | 3.755 |
| GSE217414 | 19G02977 | `caf_to_met` | 1.942 | 3.172 | 0.858 | -0.878 |
| GSE217414 | 19G02977 | `spp1_cxcl12_lite_to_myc` | 2.125 | 1.907 | 0.026 | 2.173 |
| GSE217414 | 19G02977 | `hla_drb5_lite_to_myc` | 1.315 | 1.132 | 0.002 | 3.449 |
| GSE217414 | 19G0619 | `caf_to_spp1_cxcl12_lite` | 1.022 | 0.974 | 0.002 | 4.101 |
| GSE217414 | 19G0619 | `caf_to_hla_drb5_lite` | 1.330 | 1.182 | 0.008 | 2.770 |
| GSE217414 | 19G0619 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 1.559 | 1.392 | 0.008 | 2.617 |
| GSE217414 | 19G0619 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.561 | 1.457 | 0.240 | 0.700 |
| GSE217414 | 19G0619 | `caf_to_met` | 1.012 | 0.858 | 0.194 | 0.809 |
| GSE217414 | 19G0619 | `spp1_cxcl12_lite_to_myc` | 1.474 | 1.343 | 0.094 | 1.404 |
| GSE217414 | 19G0619 | `hla_drb5_lite_to_myc` | 1.474 | 1.425 | 0.373 | 0.235 |
| GSE217414 | 19G0635 | `caf_to_spp1_cxcl12_lite` | 1.401 | 1.223 | 0.002 | 12.686 |
| GSE217414 | 19G0635 | `caf_to_hla_drb5_lite` | 1.514 | 1.358 | 0.016 | 2.311 |
| GSE217414 | 19G0635 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 1.455 | 1.239 | 0.002 | 10.560 |
| GSE217414 | 19G0635 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.542 | 1.295 | 0.002 | 5.005 |
| GSE217414 | 19G0635 | `caf_to_met` | 1.758 | 1.361 | 0.002 | 4.511 |
| GSE217414 | 19G0635 | `spp1_cxcl12_lite_to_myc` | 1.378 | 1.204 | 0.002 | 11.170 |
| GSE217414 | 19G0635 | `hla_drb5_lite_to_myc` | 1.485 | 1.290 | 0.002 | 4.338 |
| GSE217414 | 19G081 | `caf_to_spp1_cxcl12_lite` | 1.407 | 1.289 | 0.002 | 7.315 |
| GSE217414 | 19G081 | `caf_to_hla_drb5_lite` | 1.491 | 1.281 | 0.004 | 3.309 |
| GSE217414 | 19G081 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 1.945 | 1.721 | 0.002 | 5.864 |
| GSE217414 | 19G081 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.434 | 1.290 | 0.020 | 2.162 |
| GSE217414 | 19G081 | `caf_to_met` | 1.794 | 1.521 | 0.062 | 1.582 |
| GSE217414 | 19G081 | `spp1_cxcl12_lite_to_myc` | 1.766 | 1.610 | 0.002 | 3.522 |
| GSE217414 | 19G081 | `hla_drb5_lite_to_myc` | 1.535 | 1.277 | 0.008 | 2.819 |
| GSE225857 | L1 | `caf_to_spp1_cxcl12_lite` | 1.585 | 1.446 | 0.002 | 8.955 |
| GSE225857 | L1 | `caf_to_hla_drb5_lite` | 1.859 | 1.681 | 0.002 | 7.213 |
| GSE225857 | L1 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 1.471 | 1.310 | 0.002 | 10.475 |
| GSE225857 | L1 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.222 | 1.144 | 0.002 | 5.750 |
| GSE225857 | L1 | `caf_to_met` | 1.955 | 1.505 | 0.002 | 7.218 |
| GSE225857 | L1 | `spp1_cxcl12_lite_to_myc` | 1.344 | 1.222 | 0.002 | 7.999 |
| GSE225857 | L1 | `hla_drb5_lite_to_myc` | 1.132 | 1.074 | 0.002 | 3.981 |
| GSE225857 | L2 | `caf_to_spp1_cxcl12_lite` | 1.424 | 1.421 | 0.463 | 0.115 |
| GSE225857 | L2 | `caf_to_hla_drb5_lite` | 1.080 | 1.057 | 0.238 | 0.674 |
| GSE225857 | L2 | `spp1_cxcl12_lite_to_myc_glycolysis_lite` | 1.734 | 1.570 | 0.002 | 4.991 |
| GSE225857 | L2 | `hla_drb5_lite_to_myc_glycolysis_lite` | 1.052 | 1.006 | 0.016 | 2.352 |
| GSE225857 | L2 | `caf_to_met` | 1.875 | 1.880 | 0.535 | -0.031 |
| GSE225857 | L2 | `spp1_cxcl12_lite_to_myc` | 1.666 | 1.523 | 0.002 | 3.576 |
| GSE225857 | L2 | `hla_drb5_lite_to_myc` | 1.039 | 0.985 | 0.018 | 2.157 |

## Interpretation

- Passing this audit is stronger than passing a global shuffle, because regional expression gradients are partly preserved.
- Failing this audit does not disprove biology; it means the effect may be explained by coarse tissue domains and needs histology/deconvolution-aware testing.
- This is still not a final null: block size is heuristic and no manual histology annotation is used.
