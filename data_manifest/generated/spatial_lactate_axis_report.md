# Spatial lactate-axis exploratory analysis

Generated at: 2026-04-29 06:01:18 UTC

## Purpose

Explore whether the CRLM stromal/myeloid niche connects to lactate-import/anabolic metabolism proxies inspired by the 2026 spFBA lactate-consumption result.

## Caveat

This is not spFBA and not metabolite flux. It is a transcript proxy screen using genes available in the current Visium feature universes. LDHB/LDHA were not available in the tested feature sets, so lactate import/export labels are approximate.

## Summary

| Effect | Samples | Positive delta | Block p<=0.05 | Mean ratio | Mean delta | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `cxcl12_fn1_cd44_to_glutamate_transamination` | 6 | 6/6 | 2/6 | 1.966 | 0.084 | positive_but_block_explained |
| `cxcl12_fn1_cd44_to_lactate_export_glycolytic` | 6 | 6/6 | 3/6 | 1.811 | 0.159 | partial_lactate_proxy_adjacency |
| `cxcl12_fn1_cd44_to_lactate_import_anabolic` | 6 | 6/6 | 2/6 | 1.871 | 0.120 | positive_but_block_explained |
| `cxcl12_fn1_cd44_to_pyruvate_mito_entry` | 6 | 6/6 | 2/6 | 1.893 | 0.163 | positive_but_block_explained |
| `hla_drb5_to_glutamate_transamination` | 6 | 6/6 | 5/6 | 1.764 | 0.074 | strong_lactate_proxy_adjacency |
| `hla_drb5_to_lactate_export_glycolytic` | 6 | 6/6 | 4/6 | 1.375 | 0.100 | partial_lactate_proxy_adjacency |
| `hla_drb5_to_lactate_import_anabolic` | 6 | 6/6 | 4/6 | 1.564 | 0.099 | partial_lactate_proxy_adjacency |
| `hla_drb5_to_pyruvate_mito_entry` | 6 | 6/6 | 5/6 | 1.571 | 0.130 | strong_lactate_proxy_adjacency |
| `lactate_export_glycolytic_to_myc_glycolysis` | 6 | 6/6 | 1/6 | 1.706 | 0.201 | positive_but_block_explained |
| `lactate_import_anabolic_to_myc_glycolysis` | 6 | 6/6 | 1/6 | 1.630 | 0.224 | positive_but_block_explained |

## Strongest current signal

- `hla_drb5_to_glutamate_transamination` survived block permutation in 5/6 samples (mean ratio 1.764, mean block p 0.025).
- `hla_drb5_to_pyruvate_mito_entry` survived block permutation in 5/6 samples (mean ratio 1.571, mean block p 0.026).

## Interpretation

- The HLA-DRB5-like myeloid source is currently more interesting than the CXCL12/FN1/CD44-like source for this branch because its pyruvate-entry and glutamate-transamination adjacencies survive block permutation in 5/6 samples.
- This does not prove lactate flux. It suggests a spatial bridge between an immune myeloid state and the non-canonical pyruvate/transamination route described by recent spFBA work.
- If both import/anabolic and export/glycolytic proxies move together, part of the signal may still be a broad regional metabolic program rather than a specific lactate economy.
- The strongest next step is to obtain the spFBA 2026 processed flux outputs or run spFBA-like analysis directly, then test whether HLA-DRB5-like neighborhoods predict lactate-consumption flux maps.

## Literature anchors

- spFBA 2026 lactate-consumption paper: https://www.nature.com/articles/s41540-026-00654-x
- HLA-DRB5+ macrophage CRLM paper: https://link.springer.com/article/10.1186/s12967-026-07853-4
