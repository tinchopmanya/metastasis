# CRLM bulk plausibility report: TCGA-COAD

Generated at: 2026-04-26 00:26:32 UTC

## Purpose

This report checks whether correlations expected under the
`mCAF-HGF-MET-MYC-glycolysis` hypothesis are plausible at the bulk
tissue level in TCGA-COAD primary tumors. Bulk data cannot resolve
cell types, so positive correlations are necessary but not sufficient
evidence. Absence of correlation in bulk would weaken (not disprove)
the hypothesis.

## Data source

- TCGA-COAD HiSeqV2 from UCSC Xena (log2 normalized counts).
- Samples: 329.
- Genes in matrix: 20530.
- Signatures scored: 7.

## Signature score summary

| Signature | Genes | Score mean | Score SD | Score range |
| --- | --- | --- | --- | --- |
| `caf_core` | 7 | -0.000 | 0.853 | [-2.34, 2.43] |
| `cxcl13_t_cells` | 6 | -0.000 | 0.858 | [-3.08, 2.23] |
| `hgf_met_axis` | 2 | -0.000 | 0.678 | [-1.59, 1.71] |
| `macrophage_lipid_candidate` | 8 | 0.000 | 0.711 | [-1.88, 1.99] |
| `mcam_caf` | 4 | -0.000 | 0.881 | [-2.69, 2.64] |
| `myc_glycolysis_core` | 7 | -0.000 | 0.613 | [-1.78, 1.73] |
| `plasticity_emt` | 6 | 0.000 | 0.436 | [-1.30, 1.17] |

## Key correlations

| Variable X | Variable Y | Pearson r | p-value | n | Interpretation |
| --- | --- | --- | --- | --- | --- |
| `MET` | `MYC` | 0.5152 | 1.00e-300 | 329 | strong (significant) |
| `HGF` | `MET` | -0.0805 | 1.44e-01 | 329 | negligible (not significant) |
| `HGF` | `MYC` | 0.0169 | 7.60e-01 | 329 | negligible (not significant) |
| `MYC` | `SLC2A1` | 0.2498 | 3.09e-06 | 329 | weak (significant) |
| `MYC` | `HK2` | -0.3029 | 9.10e-09 | 329 | moderate (significant) |
| `MYC` | `LDHA` | 0.2011 | 2.05e-04 | 329 | weak (significant) |
| `MYC` | `ENO1` | 0.2772 | 1.81e-07 | 329 | weak (significant) |
| `MET` | `SLC2A1` | 0.3550 | 6.55e-12 | 329 | moderate (significant) |
| `HGF` | `COL1A1` | 0.4704 | 1.00e-300 | 329 | moderate (significant) |
| `HGF` | `FAP` | 0.4086 | 4.44e-16 | 329 | moderate (significant) |
| `MCAM` | `COL1A1` | 0.5833 | 1.00e-300 | 329 | strong (significant) |
| `score:caf_core` | `HGF` | 0.6749 | 1.00e-300 | 329 | strong (significant) |
| `score:caf_core` | `MET` | 0.0241 | 6.62e-01 | 329 | negligible (not significant) |
| `score:myc_glycolysis_core` | `HGF` | -0.2127 | 8.26e-05 | 329 | weak (significant) |
| `MYC` | `score:myc_glycolysis_core` | 0.4219 | 1.00e-300 | 329 | moderate (significant) |
| `MET` | `score:myc_glycolysis_core` | 0.3195 | 1.08e-09 | 329 | moderate (significant) |
| `HGF` | `score:caf_core` | 0.6749 | 1.00e-300 | 329 | strong (significant) |
| `score:hgf_met_axis` | `score:myc_glycolysis_core` | 0.0787 | 1.53e-01 | 329 | negligible (not significant) |
| `score:hgf_met_axis` | `score:caf_core` | 0.5154 | 1.00e-300 | 329 | strong (significant) |
| `score:mcam_caf` | `score:cxcl13_t_cells` | 0.2884 | 5.14e-08 | 329 | weak (significant) |
| `score:plasticity_emt` | `score:myc_glycolysis_core` | -0.0453 | 4.12e-01 | 329 | negligible (not significant) |
| `score:macrophage_lipid_candidate` | `score:caf_core` | 0.6853 | 1.00e-300 | 329 | strong (significant) |

## Assessment

- **MET-MYC gene correlation**: r = 0.5152 (positive, statistically significant)
- **HGF-MET gene correlation**: r = -0.0805 (negative, not statistically significant)
- **MYC vs glycolysis score**: r = 0.4219 (positive, statistically significant)
- **MET vs glycolysis score**: r = 0.3195 (positive, statistically significant)
- **CAF score vs HGF**: r = 0.6749 (positive, statistically significant)

## Epistemological caveat

Bulk RNA-seq mixes all cell types in a tissue sample. A positive
MET-MYC correlation in bulk could reflect tumor-intrinsic biology,
stromal contamination, or confounding by tumor purity. These results
are screening-level evidence of plausibility, not proof of the
cell-type-specific mechanism proposed by the hypothesis.

## Next steps

- If correlations are plausible: proceed to single-cell validation
  (GSE225857 or equivalent) to test cell-type specificity.
- If correlations are absent: reconsider whether the axis operates
  at tissue level or is purely a niche-level phenomenon.
- Either outcome is informative for prioritizing the hypothesis.
