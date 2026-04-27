# GSE225857 spatial spot-level validation

Generated at: 2026-04-27 03:28:57 UTC

## Purpose
Test spatial plausibility of the mCAF-HGF-MET-MYC-glycolysis hypothesis using GSE225857 Visium spot-level data.

## Scope
- Downloaded only Visium barcodes, features, matrices, and tissue-position files.
- Skipped histology images.
- Treated spot-level co-expression as coarse co-localization, not proof of direct cell-cell interaction.

## Sample Summary

| Sample | Tissue | Spots | HGF | MET | MYC | CAF score | Tumor score | Glycolysis score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | CCT | 2054 | 0.054 | 1.092 | 3.261 | 1.316 | 3.200 | 1.368 |
| C2 | CCT | 3305 | 0.053 | 0.404 | 1.682 | 1.499 | 1.776 | 0.691 |
| C3 | CCT | 3417 | 0.016 | 0.715 | 2.066 | 0.575 | 1.924 | 0.820 |
| C4 | CCT | 4016 | 0.019 | 0.325 | 0.312 | 1.232 | 0.626 | 0.371 |
| L1 | LCT | 4672 | 0.085 | 0.333 | 1.419 | 0.710 | 1.172 | 0.486 |
| L2 | LCT | 4796 | 0.011 | 0.118 | 0.710 | 0.382 | 0.719 | 0.190 |

## Key Spot-Level Correlations

| Sample | Tissue | Pair | r | Spots |
| --- | --- | --- | --- | --- |
| C1 | CCT | `HGF~MET` | 0.092 | 2054 |
| C1 | CCT | `caf_score~MET` | 0.314 | 2054 |
| C1 | CCT | `caf_score~MYC` | 0.274 | 2054 |
| C1 | CCT | `caf_score~glycolysis_score` | 0.365 | 2054 |
| C1 | CCT | `MET~MYC` | 0.772 | 2054 |
| C1 | CCT | `MYC~glycolysis_score` | 0.804 | 2054 |
| C2 | CCT | `HGF~MET` | 0.145 | 3305 |
| C2 | CCT | `caf_score~MET` | 0.427 | 3305 |
| C2 | CCT | `caf_score~MYC` | 0.556 | 3305 |
| C2 | CCT | `caf_score~glycolysis_score` | 0.550 | 3305 |
| C2 | CCT | `MET~MYC` | 0.756 | 3305 |
| C2 | CCT | `MYC~glycolysis_score` | 0.904 | 3305 |
| C3 | CCT | `HGF~MET` | 0.156 | 3417 |
| C3 | CCT | `caf_score~MET` | 0.600 | 3417 |
| C3 | CCT | `caf_score~MYC` | 0.674 | 3417 |
| C3 | CCT | `caf_score~glycolysis_score` | 0.690 | 3417 |
| C3 | CCT | `MET~MYC` | 0.791 | 3417 |
| C3 | CCT | `MYC~glycolysis_score` | 0.881 | 3417 |
| C4 | CCT | `HGF~MET` | -0.010 | 4016 |
| C4 | CCT | `caf_score~MET` | 0.229 | 4016 |
| C4 | CCT | `caf_score~MYC` | 0.152 | 4016 |
| C4 | CCT | `caf_score~glycolysis_score` | 0.437 | 4016 |
| C4 | CCT | `MET~MYC` | 0.206 | 4016 |
| C4 | CCT | `MYC~glycolysis_score` | 0.254 | 4016 |
| L1 | LCT | `HGF~MET` | 0.017 | 4672 |
| L1 | LCT | `caf_score~MET` | 0.328 | 4672 |
| L1 | LCT | `caf_score~MYC` | 0.343 | 4672 |
| L1 | LCT | `caf_score~glycolysis_score` | 0.408 | 4672 |
| L1 | LCT | `MET~MYC` | 0.498 | 4672 |
| L1 | LCT | `MYC~glycolysis_score` | 0.792 | 4672 |
| L2 | LCT | `HGF~MET` | 0.011 | 4796 |
| L2 | LCT | `caf_score~MET` | 0.244 | 4796 |
| L2 | LCT | `caf_score~MYC` | 0.379 | 4796 |
| L2 | LCT | `caf_score~glycolysis_score` | 0.501 | 4796 |
| L2 | LCT | `MET~MYC` | 0.199 | 4796 |
| L2 | LCT | `MYC~glycolysis_score` | 0.497 | 4796 |

## Interpretation
- Mean LCT `caf_score~MET` correlation: 0.286
- Mean LCT `MYC~glycolysis_score` correlation: 0.645
- Positive correlations support spatial plausibility, but Visium spots mix cells and cannot prove paracrine causality.
- Negative or weak `HGF~MET` spot correlations would not necessarily falsify the model because ligand and receptor may occupy adjacent rather than identical spots.

## Adjacency Check

| Sample | Tissue | Source | Target | High-source spots | Neighbor spots | Neighbor/background ratio |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | LCT | `caf_score` | `MET` | 1193 | 1116 | 2.029 |
| L1 | LCT | `caf_score` | `MYC` | 1193 | 1116 | 1.355 |
| L1 | LCT | `caf_score` | `glycolysis_score` | 1193 | 1116 | 1.624 |
| L1 | LCT | `HGF` | `MET` | 531 | 1667 | 0.874 |
| L1 | LCT | `HGF` | `MYC` | 531 | 1667 | 0.807 |
| L1 | LCT | `HGF` | `glycolysis_score` | 531 | 1667 | 0.810 |
| L2 | LCT | `caf_score` | `MET` | 1375 | 1305 | 1.866 |
| L2 | LCT | `caf_score` | `MYC` | 1375 | 1305 | 1.682 |
| L2 | LCT | `caf_score` | `glycolysis_score` | 1375 | 1305 | 1.817 |
| L2 | LCT | `HGF` | `MET` | 78 | 426 | 0.814 |
| L2 | LCT | `HGF` | `MYC` | 78 | 426 | 0.802 |
| L2 | LCT | `HGF` | `glycolysis_score` | 78 | 426 | 0.872 |

- Mean LCT neighbor/background ratio for `caf_score -> MET`: 1.948
- Mean LCT neighbor/background ratio for `HGF -> MET`: 0.844
- Ratios above 1.0 suggest target signal is higher near source-high spots than background.

## Next Step
Use the spatial and single-cell outputs together to prioritize a focused write-up of the revised niche model: PRELP/MCAM fibroblast HGF sources, MET+ tumor receivers, and MYC-glycolysis tumor response.
