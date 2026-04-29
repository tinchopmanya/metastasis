# Lactate/HLA-DRB5 axis robustness audit

Generated at: 2026-04-29 06:22:38 UTC

## Purpose

Stress-test the exploratory `HLA-DRB5-like -> pyruvate/transamination` spatial branch before treating it as a paper-grade hypothesis.

## Block-Size Sensitivity

| Effect | Block | Samples | Positive delta | Block p<=0.05 | Mean ratio | Mean block p |
| --- | --- | --- | --- | --- | --- | --- |
| `hla_drb5_original_to_glutamate_transamination` | 8 | 6 | 6/6 | 2/6 | 1.764 | 0.094 |
| `hla_drb5_original_to_glutamate_transamination` | 12 | 6 | 6/6 | 5/6 | 1.764 | 0.028 |
| `hla_drb5_original_to_glutamate_transamination` | 16 | 6 | 6/6 | 4/6 | 1.764 | 0.044 |
| `hla_drb5_original_to_glutamate_transamination` | 20 | 6 | 6/6 | 5/6 | 1.764 | 0.017 |
| `hla_drb5_original_to_lactate_export_glycolytic` | 8 | 6 | 6/6 | 3/6 | 1.375 | 0.213 |
| `hla_drb5_original_to_lactate_export_glycolytic` | 12 | 6 | 6/6 | 4/6 | 1.375 | 0.113 |
| `hla_drb5_original_to_lactate_export_glycolytic` | 16 | 6 | 6/6 | 4/6 | 1.375 | 0.057 |
| `hla_drb5_original_to_lactate_export_glycolytic` | 20 | 6 | 6/6 | 4/6 | 1.375 | 0.114 |
| `hla_drb5_original_to_lactate_import_anabolic` | 8 | 6 | 6/6 | 2/6 | 1.564 | 0.179 |
| `hla_drb5_original_to_lactate_import_anabolic` | 12 | 6 | 6/6 | 4/6 | 1.564 | 0.036 |
| `hla_drb5_original_to_lactate_import_anabolic` | 16 | 6 | 6/6 | 3/6 | 1.564 | 0.095 |
| `hla_drb5_original_to_lactate_import_anabolic` | 20 | 6 | 6/6 | 5/6 | 1.564 | 0.020 |
| `hla_drb5_original_to_pyruvate_mito_entry` | 8 | 6 | 6/6 | 4/6 | 1.571 | 0.133 |
| `hla_drb5_original_to_pyruvate_mito_entry` | 12 | 6 | 6/6 | 5/6 | 1.571 | 0.035 |
| `hla_drb5_original_to_pyruvate_mito_entry` | 16 | 6 | 6/6 | 4/6 | 1.571 | 0.102 |
| `hla_drb5_original_to_pyruvate_mito_entry` | 20 | 6 | 6/6 | 6/6 | 1.571 | 0.008 |

## Ablation Summary

| Source variant | Target variant | Samples | Positive delta | Block p<=0.05 | Mean ratio | Mean block p |
| --- | --- | --- | --- | --- | --- | --- |
| `hla_drb5_no_cd74_ptprc` | `glutamate_transamination` | 6 | 6/6 | 2/6 | 1.320 | 0.191 |
| `hla_drb5_no_cd74_ptprc` | `glutamate_transamination_minus_GLS` | 6 | 6/6 | 2/6 | 1.309 | 0.213 |
| `hla_drb5_no_cd74_ptprc` | `glutamate_transamination_minus_GLUD1` | 6 | 6/6 | 2/6 | 1.332 | 0.168 |
| `hla_drb5_no_cd74_ptprc` | `glutamate_transamination_minus_GOT1` | 6 | 6/6 | 2/6 | 1.295 | 0.221 |
| `hla_drb5_no_cd74_ptprc` | `glutamate_transamination_minus_GOT2` | 6 | 6/6 | 2/6 | 1.353 | 0.208 |
| `hla_drb5_no_cd74_ptprc` | `pyruvate_mito_entry` | 6 | 5/6 | 3/6 | 1.238 | 0.294 |
| `hla_drb5_no_cd74_ptprc` | `pyruvate_mito_entry_minus_MPC1` | 6 | 5/6 | 3/6 | 1.239 | 0.219 |
| `hla_drb5_no_cd74_ptprc` | `pyruvate_mito_entry_minus_MPC2` | 6 | 5/6 | 3/6 | 1.228 | 0.343 |
| `hla_drb5_no_cd74_ptprc` | `pyruvate_mito_entry_minus_PDHA1` | 6 | 6/6 | 3/6 | 1.239 | 0.271 |
| `hla_drb5_no_cd74_ptprc` | `pyruvate_mito_entry_minus_PDHB` | 6 | 6/6 | 3/6 | 1.248 | 0.251 |
| `hla_drb5_no_ptprc` | `glutamate_transamination` | 6 | 6/6 | 5/6 | 1.705 | 0.036 |
| `hla_drb5_no_ptprc` | `glutamate_transamination_minus_GLS` | 6 | 6/6 | 3/6 | 1.712 | 0.054 |
| `hla_drb5_no_ptprc` | `glutamate_transamination_minus_GLUD1` | 6 | 6/6 | 4/6 | 1.746 | 0.041 |
| `hla_drb5_no_ptprc` | `glutamate_transamination_minus_GOT1` | 6 | 6/6 | 4/6 | 1.677 | 0.083 |
| `hla_drb5_no_ptprc` | `glutamate_transamination_minus_GOT2` | 6 | 6/6 | 4/6 | 1.699 | 0.084 |
| `hla_drb5_no_ptprc` | `pyruvate_mito_entry` | 6 | 6/6 | 5/6 | 1.557 | 0.038 |
| `hla_drb5_no_ptprc` | `pyruvate_mito_entry_minus_MPC1` | 6 | 6/6 | 6/6 | 1.549 | 0.020 |
| `hla_drb5_no_ptprc` | `pyruvate_mito_entry_minus_MPC2` | 6 | 6/6 | 4/6 | 1.544 | 0.083 |
| `hla_drb5_no_ptprc` | `pyruvate_mito_entry_minus_PDHA1` | 6 | 6/6 | 5/6 | 1.576 | 0.068 |
| `hla_drb5_no_ptprc` | `pyruvate_mito_entry_minus_PDHB` | 6 | 6/6 | 5/6 | 1.579 | 0.046 |
| `hla_drb5_only` | `glutamate_transamination` | 6 | 1/6 | 0/6 | 1.062 | 0.703 |
| `hla_drb5_only` | `glutamate_transamination_minus_GLS` | 6 | 1/6 | 0/6 | 1.082 | 0.743 |
| `hla_drb5_only` | `glutamate_transamination_minus_GLUD1` | 6 | 1/6 | 0/6 | 1.030 | 0.792 |
| `hla_drb5_only` | `glutamate_transamination_minus_GOT1` | 6 | 1/6 | 0/6 | 1.069 | 0.475 |
| `hla_drb5_only` | `glutamate_transamination_minus_GOT2` | 6 | 1/6 | 0/6 | 1.079 | 0.574 |
| `hla_drb5_only` | `pyruvate_mito_entry` | 6 | 1/6 | 0/6 | 1.106 | 0.267 |
| `hla_drb5_only` | `pyruvate_mito_entry_minus_MPC1` | 6 | 1/6 | 0/6 | 1.100 | 0.337 |
| `hla_drb5_only` | `pyruvate_mito_entry_minus_MPC2` | 6 | 1/6 | 0/6 | 1.089 | 0.515 |
| `hla_drb5_only` | `pyruvate_mito_entry_minus_PDHA1` | 6 | 1/6 | 0/6 | 1.102 | 0.396 |
| `hla_drb5_only` | `pyruvate_mito_entry_minus_PDHB` | 6 | 1/6 | 0/6 | 1.134 | 0.218 |
| `hla_drb5_original` | `glutamate_transamination` | 6 | 6/6 | 5/6 | 1.764 | 0.030 |
| `hla_drb5_original` | `glutamate_transamination_minus_GLS` | 6 | 6/6 | 4/6 | 1.825 | 0.069 |
| `hla_drb5_original` | `glutamate_transamination_minus_GLUD1` | 6 | 6/6 | 3/6 | 1.766 | 0.074 |
| `hla_drb5_original` | `glutamate_transamination_minus_GOT1` | 6 | 6/6 | 5/6 | 1.746 | 0.081 |
| `hla_drb5_original` | `glutamate_transamination_minus_GOT2` | 6 | 6/6 | 5/6 | 1.759 | 0.045 |
| `hla_drb5_original` | `pyruvate_mito_entry` | 6 | 6/6 | 5/6 | 1.571 | 0.033 |
| `hla_drb5_original` | `pyruvate_mito_entry_minus_MPC1` | 6 | 6/6 | 4/6 | 1.556 | 0.028 |
| `hla_drb5_original` | `pyruvate_mito_entry_minus_MPC2` | 6 | 6/6 | 5/6 | 1.604 | 0.051 |
| `hla_drb5_original` | `pyruvate_mito_entry_minus_PDHA1` | 6 | 6/6 | 4/6 | 1.591 | 0.096 |
| `hla_drb5_original` | `pyruvate_mito_entry_minus_PDHB` | 6 | 6/6 | 4/6 | 1.578 | 0.051 |

## Full-Universe Random Target Controls

| Source variant | Target | Samples | Beats random p<=0.05 | Mean observed ratio | Mean random p |
| --- | --- | --- | --- | --- | --- |
| `hla_drb5_no_ptprc` | `glutamate_transamination` | 6 | 0/6 | 1.705 | 0.409 |
| `hla_drb5_no_ptprc` | `pyruvate_mito_entry` | 6 | 0/6 | 1.557 | 0.419 |
| `hla_drb5_original` | `glutamate_transamination` | 6 | 0/6 | 1.764 | 0.347 |
| `hla_drb5_original` | `pyruvate_mito_entry` | 6 | 0/6 | 1.571 | 0.353 |

## Residualized Coordinate/Depth Audit

| Source variant | Target | Samples | Positive residual delta | Block p<=0.05 | Mean residual delta | Mean block p |
| --- | --- | --- | --- | --- | --- | --- |
| `hla_drb5_no_ptprc` | `glutamate_transamination` | 6 | 4/6 | 0/6 | 0.001 | 0.578 |
| `hla_drb5_no_ptprc` | `pyruvate_mito_entry` | 6 | 4/6 | 1/6 | 0.005 | 0.414 |
| `hla_drb5_original` | `glutamate_transamination` | 6 | 4/6 | 0/6 | 0.002 | 0.596 |
| `hla_drb5_original` | `pyruvate_mito_entry` | 6 | 4/6 | 0/6 | 0.002 | 0.526 |

## Interpretation Rules

- A robust effect should survive multiple block sizes, source/target ablation, and residualization.
- Random controls are drawn from the full feature universe of each spatial sample and matched approximately by expression and dropout.
- Residualized ratios are not used because residuals can be negative; residualized tests use neighbor-minus-background delta.
- This still does not prove lactate flux. The next decisive test is spFBA/FES validation.
