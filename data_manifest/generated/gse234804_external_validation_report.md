# GSE234804 H5Seurat external validation screen

Generated at: 2026-04-27 06:32:27 UTC

## Purpose

Test whether CRC liver metastasis samples in GSE234804 show sample-level enrichment of the active CAF/MCAM and MET-MYC-glycolysis signals compared with primary CRC samples.

## Scope

- Downloaded only individual `CRC*` and `LM*` H5Seurat files.
- Excluded `PC*` samples from the first pass.
- Used `/assays/RNA/data` mean expression per sample.
- No cell-type labels were available in `meta.data`, so this is sample-level, not cell-type-resolved.

## Samples

| Sample | Tissue | Cells | Genes | CAF score | MCAM CAF | HGF-MET | MYC-glycolysis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CRC2 | CRC | 523 | 20629 | 0.008 | 0.011 | 0.264 | 6.440 |
| CRC3 | CRC | 2959 | 26802 | 0.011 | 0.018 | 0.188 | 2.538 |
| CRC4 | CRC | 4679 | 27179 | 0.176 | 0.280 | 0.045 | 0.960 |
| LM2 | LM | 3243 | 25474 | 0.022 | 0.034 | 0.350 | 1.560 |
| LM9 | LM | 2232 | 25054 | 0.013 | 0.024 | 0.278 | 1.723 |
| LM16 | LM | 1467 | 24022 | 0.029 | 0.037 | 0.127 | 1.361 |
| LM17 | LM | 3188 | 26068 | 0.046 | 0.082 | 0.087 | 5.576 |
| LM21 | LM | 7304 | 23724 | 0.025 | 0.007 | 0.100 | 0.859 |
| LM28 | LM | 6840 | 28978 | 0.141 | 0.161 | 0.124 | 1.577 |

## LM vs CRC Comparisons

| Metric | LM mean | CRC mean | LM-CRC | LM/CRC | p | Rank delta |
| --- | --- | --- | --- | --- | --- | --- |
| `score_mcam_caf` | 0.057 | 0.103 | -0.046 | 0.556 | 7.96e-01 | 0.111 |
| `score_caf_core` | 0.046 | 0.065 | -0.019 | 0.714 | 4.39e-01 | 0.333 |
| `score_hgf_met_axis` | 0.178 | 0.166 | 0.012 | 1.072 | 7.96e-01 | 0.111 |
| `score_myc_glycolysis_core` | 2.109 | 3.312 | -1.203 | 0.637 | 4.39e-01 | -0.333 |
| `score_caf_met_myc_glycolysis_composite` | 0.598 | 0.911 | -0.314 | 0.656 | 4.39e-01 | -0.333 |
| `HGF` | 0.014 | 0.011 | 0.003 | 1.311 | 1.00e+00 | 0.000 |
| `MET` | 0.341 | 0.236 | 0.105 | 1.443 | 7.96e-01 | 0.111 |
| `MYC` | 0.634 | 1.056 | -0.422 | 0.601 | 7.07e-02 | -0.778 |
| `MCAM` | 0.010 | 0.054 | -0.044 | 0.178 | 5.05e-01 | -0.333 |
| `COL1A1` | 0.066 | 0.125 | -0.059 | 0.528 | 7.96e-01 | -0.111 |
| `PGK1` | 1.486 | 3.301 | -1.815 | 0.450 | 3.02e-01 | -0.444 |
| `TPI1` | 7.035 | 9.003 | -1.969 | 0.781 | 7.96e-01 | -0.111 |

## Interpretation

- `score_mcam_caf` is lower in LM than CRC at sample level (LM mean 0.057, CRC mean 0.103).
- `score_myc_glycolysis_core` is lower in LM than CRC at sample level (LM mean 2.109, CRC mean 3.312).
- `MET` is modestly higher in LM (LM/CRC 1.443), while `HGF` is nearly unchanged/very low (LM/CRC 1.311).
- This does not externally replicate the full `CAF-high -> MET/MYC/glycolysis` model as a simple sample-level LM-vs-CRC signature.
- The negative result is still informative: it supports treating the hypothesis as spatial/cell-state-specific rather than as a universal bulk-like liver-metastasis signature.
- Sample count is small and no cell-type labels were available, so this is a falsification pressure test, not a final rejection.
