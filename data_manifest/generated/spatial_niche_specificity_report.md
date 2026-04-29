# Spatial signature specificity audit

Generated at: 2026-04-29 05:43:59 UTC

## Purpose

Run an initial reviewer-style specificity screen for the CRLM spatial niche effects using gene ablations and expression-matched random signatures drawn from the currently extracted gene panel.

## Important Limitation

This is not the final paper-grade control. Random signatures are matched within the extracted analysis gene panel, not the full transcriptome, and the spatial null is still a global target shuffle. Passing this screen means only that the effect survived obvious circularity checks.

## Summary

| Effect | Samples | Mean original ratio | Mean audited ratio | Positive after ablation | Beats random p<=0.05 | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `caf_to_cxcl12_fn1_cd44_ablation` | 6 | 1.399 | 1.290 | 5/6 | 0/6 | mixed_after_ablation |
| `caf_to_hla_drb5_no_ptprc` | 6 | 1.417 | 1.442 | 6/6 | 1/6 | positive_but_not_specific_vs_random |
| `cxcl12_fn1_cd44_to_myc_glycolysis_no_myc` | 6 | 1.718 | 1.530 | 6/6 | 0/6 | positive_but_not_specific_vs_random |
| `hla_drb5_no_ptprc_to_myc_glycolysis_no_myc` | 6 | 1.357 | 1.384 | 6/6 | 0/6 | positive_but_not_specific_vs_random |

## Sample-Level Audit

| Dataset | Sample | Effect | Original ratio | Audited ratio | Random mean | Random p>=observed | Global shuffle p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GSE217414 | 19G02977 | `caf_to_cxcl12_fn1_cd44_ablation` | 1.553 | 1.179 | 2.035 | 0.950 | 0.005 |
| GSE217414 | 19G02977 | `caf_to_hla_drb5_no_ptprc` | 1.227 | 1.288 | 2.252 | 0.851 | 0.025 |
| GSE217414 | 19G02977 | `cxcl12_fn1_cd44_to_myc_glycolysis_no_myc` | 2.143 | 1.850 | 1.567 | 0.134 | 0.005 |
| GSE217414 | 19G02977 | `hla_drb5_no_ptprc_to_myc_glycolysis_no_myc` | 1.330 | 1.391 | 1.424 | 0.493 | 0.005 |
| GSE217414 | 19G0619 | `caf_to_cxcl12_fn1_cd44_ablation` | 1.022 | 0.939 | 1.331 | 0.945 | 1.000 |
| GSE217414 | 19G0619 | `caf_to_hla_drb5_no_ptprc` | 1.330 | 1.342 | 1.231 | 0.463 | 0.005 |
| GSE217414 | 19G0619 | `cxcl12_fn1_cd44_to_myc_glycolysis_no_myc` | 1.559 | 1.139 | 1.346 | 0.667 | 0.035 |
| GSE217414 | 19G0619 | `hla_drb5_no_ptprc_to_myc_glycolysis_no_myc` | 1.561 | 1.673 | 1.730 | 0.413 | 0.005 |
| GSE217414 | 19G0635 | `caf_to_cxcl12_fn1_cd44_ablation` | 1.401 | 1.408 | 1.492 | 0.881 | 0.005 |
| GSE217414 | 19G0635 | `caf_to_hla_drb5_no_ptprc` | 1.514 | 1.502 | 1.853 | 1.000 | 0.005 |
| GSE217414 | 19G0635 | `cxcl12_fn1_cd44_to_myc_glycolysis_no_myc` | 1.455 | 1.478 | 1.517 | 0.542 | 0.005 |
| GSE217414 | 19G0635 | `hla_drb5_no_ptprc_to_myc_glycolysis_no_myc` | 1.542 | 1.560 | 1.628 | 0.627 | 0.005 |
| GSE217414 | 19G081 | `caf_to_cxcl12_fn1_cd44_ablation` | 1.407 | 1.389 | 1.611 | 1.000 | 0.005 |
| GSE217414 | 19G081 | `caf_to_hla_drb5_no_ptprc` | 1.491 | 1.599 | 1.680 | 0.701 | 0.005 |
| GSE217414 | 19G081 | `cxcl12_fn1_cd44_to_myc_glycolysis_no_myc` | 1.945 | 2.083 | 1.783 | 0.129 | 0.005 |
| GSE217414 | 19G081 | `hla_drb5_no_ptprc_to_myc_glycolysis_no_myc` | 1.434 | 1.267 | 1.531 | 1.000 | 0.005 |
| GSE225857 | L1 | `caf_to_cxcl12_fn1_cd44_ablation` | 1.585 | 1.555 | 1.580 | 0.537 | 0.005 |
| GSE225857 | L1 | `caf_to_hla_drb5_no_ptprc` | 1.859 | 1.811 | 1.530 | 0.005 | 0.005 |
| GSE225857 | L1 | `cxcl12_fn1_cd44_to_myc_glycolysis_no_myc` | 1.471 | 1.222 | 1.463 | 0.940 | 0.005 |
| GSE225857 | L1 | `hla_drb5_no_ptprc_to_myc_glycolysis_no_myc` | 1.222 | 1.310 | 1.518 | 0.930 | 0.005 |
| GSE225857 | L2 | `caf_to_cxcl12_fn1_cd44_ablation` | 1.424 | 1.268 | 1.678 | 0.965 | 0.005 |
| GSE225857 | L2 | `caf_to_hla_drb5_no_ptprc` | 1.080 | 1.110 | 1.644 | 0.995 | 0.020 |
| GSE225857 | L2 | `cxcl12_fn1_cd44_to_myc_glycolysis_no_myc` | 1.734 | 1.406 | 1.540 | 0.886 | 0.005 |
| GSE225857 | L2 | `hla_drb5_no_ptprc_to_myc_glycolysis_no_myc` | 1.052 | 1.104 | 1.326 | 0.985 | 0.010 |

## Interpretation

- Effects that remain positive after ablation but do not beat random controls should be treated as spatially broad, not specific.
- Effects that beat random controls still require stricter spatial nulls controlling histology, UMI depth and autocorrelation.
- The current safest language remains exploratory multi-dataset support, not causal niche proof.
