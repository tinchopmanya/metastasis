# GSE217414 external spatial CRLM validation

Generated at: 2026-04-27 20:52:26 UTC

## Purpose

Validate whether the CRLM layered-niche signal is visible in an independent four-patient Visium dataset, using the same CAF/SPP1-CXCL12/HLA-DRB5/MYC-glycolysis signature logic.

## Dataset

- GEO: GSE217414.
- Four colorectal cancer liver metastasis Visium sections.
- Raw processed GEO package is small enough for reproducible validation: H5 matrices plus spatial coordinates.

## Signature Availability

| Sample | Signature | Usable / Expected | Usable genes |
| --- | --- | --- | --- |
| 19G081 | `caf_core` | 7 / 7 | `COL1A1,COL1A2,ACTA2,FAP,POSTN,PDGFRA,PDGFRB` |
| 19G081 | `mcam_caf` | 4 / 4 | `MCAM,COL1A1,COL1A2,ACTA2` |
| 19G081 | `spp1_cxcl12_caf_myeloid_axis` | 7 / 7 | `SPP1,CXCL12,CD44,MIF,FN1,HIF1A,CTNNB1` |
| 19G081 | `spp1_cxcl12_axis_desoverlap_2026` | 5 / 5 | `CXCL12,CD44,FN1,HIF1A,CTNNB1` |
| 19G081 | `hla_drb5_macrophage_axis` | 6 / 7 | `HLA-DRB5,CD74,CXCR4,PTPRC,SPP1,MIF` |
| 19G081 | `hla_drb5_macrophage_axis_desoverlap_2026` | 4 / 5 | `HLA-DRB5,CD74,CXCR4,PTPRC` |
| 19G081 | `myc_glycolysis_core` | 5 / 7 | `MYC,SLC2A1,HK2,PGK1,ENO1` |
| 19G081 | `myc_glycolysis_desoverlap_2026` | 4 / 4 | `MYC,HK2,PGK1,ENO1` |
| 19G081 | `glut1_invasive_margin_axis` | 5 / 5 | `SLC2A1,CD8A,GZMB,PRF1,MKI67` |
| 19G081 | `cxcl13_t_cells` | 6 / 6 | `CXCL13,CD3D,CD3E,CD4,CD8A,CD8B` |
| 19G081 | `crlm_metabolic_vulnerabilities_2026` | 8 / 9 | `FTCD,GPD1,SOD2,EIF4B,NDRG1,PIM1,PIM2,PIM3` |
| 19G0619 | `caf_core` | 7 / 7 | `COL1A1,COL1A2,ACTA2,FAP,POSTN,PDGFRA,PDGFRB` |
| 19G0619 | `mcam_caf` | 4 / 4 | `MCAM,COL1A1,COL1A2,ACTA2` |
| 19G0619 | `spp1_cxcl12_caf_myeloid_axis` | 7 / 7 | `SPP1,CXCL12,CD44,MIF,FN1,HIF1A,CTNNB1` |
| 19G0619 | `spp1_cxcl12_axis_desoverlap_2026` | 5 / 5 | `CXCL12,CD44,FN1,HIF1A,CTNNB1` |
| 19G0619 | `hla_drb5_macrophage_axis` | 6 / 7 | `HLA-DRB5,CD74,CXCR4,PTPRC,SPP1,MIF` |
| 19G0619 | `hla_drb5_macrophage_axis_desoverlap_2026` | 4 / 5 | `HLA-DRB5,CD74,CXCR4,PTPRC` |
| 19G0619 | `myc_glycolysis_core` | 5 / 7 | `MYC,SLC2A1,HK2,PGK1,ENO1` |
| 19G0619 | `myc_glycolysis_desoverlap_2026` | 4 / 4 | `MYC,HK2,PGK1,ENO1` |
| 19G0619 | `glut1_invasive_margin_axis` | 5 / 5 | `SLC2A1,CD8A,GZMB,PRF1,MKI67` |
| 19G0619 | `cxcl13_t_cells` | 6 / 6 | `CXCL13,CD3D,CD3E,CD4,CD8A,CD8B` |
| 19G0619 | `crlm_metabolic_vulnerabilities_2026` | 8 / 9 | `FTCD,GPD1,SOD2,EIF4B,NDRG1,PIM1,PIM2,PIM3` |
| 19G0635 | `caf_core` | 7 / 7 | `COL1A1,COL1A2,ACTA2,FAP,POSTN,PDGFRA,PDGFRB` |
| 19G0635 | `mcam_caf` | 4 / 4 | `MCAM,COL1A1,COL1A2,ACTA2` |
| 19G0635 | `spp1_cxcl12_caf_myeloid_axis` | 7 / 7 | `SPP1,CXCL12,CD44,MIF,FN1,HIF1A,CTNNB1` |
| 19G0635 | `spp1_cxcl12_axis_desoverlap_2026` | 5 / 5 | `CXCL12,CD44,FN1,HIF1A,CTNNB1` |
| 19G0635 | `hla_drb5_macrophage_axis` | 6 / 7 | `HLA-DRB5,CD74,CXCR4,PTPRC,SPP1,MIF` |
| 19G0635 | `hla_drb5_macrophage_axis_desoverlap_2026` | 4 / 5 | `HLA-DRB5,CD74,CXCR4,PTPRC` |
| 19G0635 | `myc_glycolysis_core` | 5 / 7 | `MYC,SLC2A1,HK2,PGK1,ENO1` |
| 19G0635 | `myc_glycolysis_desoverlap_2026` | 4 / 4 | `MYC,HK2,PGK1,ENO1` |
| 19G0635 | `glut1_invasive_margin_axis` | 5 / 5 | `SLC2A1,CD8A,GZMB,PRF1,MKI67` |
| 19G0635 | `cxcl13_t_cells` | 6 / 6 | `CXCL13,CD3D,CD3E,CD4,CD8A,CD8B` |
| 19G0635 | `crlm_metabolic_vulnerabilities_2026` | 8 / 9 | `FTCD,GPD1,SOD2,EIF4B,NDRG1,PIM1,PIM2,PIM3` |
| 19G02977 | `caf_core` | 7 / 7 | `COL1A1,COL1A2,ACTA2,FAP,POSTN,PDGFRA,PDGFRB` |
| 19G02977 | `mcam_caf` | 4 / 4 | `MCAM,COL1A1,COL1A2,ACTA2` |
| 19G02977 | `spp1_cxcl12_caf_myeloid_axis` | 7 / 7 | `SPP1,CXCL12,CD44,MIF,FN1,HIF1A,CTNNB1` |
| 19G02977 | `spp1_cxcl12_axis_desoverlap_2026` | 5 / 5 | `CXCL12,CD44,FN1,HIF1A,CTNNB1` |
| 19G02977 | `hla_drb5_macrophage_axis` | 6 / 7 | `HLA-DRB5,CD74,CXCR4,PTPRC,SPP1,MIF` |
| 19G02977 | `hla_drb5_macrophage_axis_desoverlap_2026` | 4 / 5 | `HLA-DRB5,CD74,CXCR4,PTPRC` |
| 19G02977 | `myc_glycolysis_core` | 5 / 7 | `MYC,SLC2A1,HK2,PGK1,ENO1` |
| 19G02977 | `myc_glycolysis_desoverlap_2026` | 4 / 4 | `MYC,HK2,PGK1,ENO1` |
| 19G02977 | `glut1_invasive_margin_axis` | 5 / 5 | `SLC2A1,CD8A,GZMB,PRF1,MKI67` |
| 19G02977 | `cxcl13_t_cells` | 6 / 6 | `CXCL13,CD3D,CD3E,CD4,CD8A,CD8B` |
| 19G02977 | `crlm_metabolic_vulnerabilities_2026` | 8 / 9 | `FTCD,GPD1,SOD2,EIF4B,NDRG1,PIM1,PIM2,PIM3` |

## Key Spatial Adjacency Tests

| Sample | Source | Target | Observed ratio | Null mean | z | Empirical p >= observed |
| --- | --- | --- | --- | --- | --- | --- |
| 19G081 | `score_caf_core` | `MET` | 1.794 | 1.007 | 6.165 | 0.002 |
| 19G081 | `score_caf_core` | `score_spp1_cxcl12_axis_desoverlap_2026` | 1.407 | 1.000 | 19.376 | 0.002 |
| 19G081 | `score_caf_core` | `score_hla_drb5_macrophage_axis_desoverlap_2026` | 1.491 | 1.005 | 8.176 | 0.002 |
| 19G081 | `score_spp1_cxcl12_axis_desoverlap_2026` | `MYC` | 1.766 | 0.997 | 17.908 | 0.002 |
| 19G081 | `score_spp1_cxcl12_axis_desoverlap_2026` | `score_myc_glycolysis_desoverlap_2026` | 1.945 | 1.000 | 28.101 | 0.002 |
| 19G081 | `score_hla_drb5_macrophage_axis_desoverlap_2026` | `MYC` | 1.535 | 1.000 | 7.070 | 0.002 |
| 19G081 | `score_hla_drb5_macrophage_axis_desoverlap_2026` | `score_myc_glycolysis_desoverlap_2026` | 1.434 | 1.011 | 6.293 | 0.002 |
| 19G0619 | `score_caf_core` | `MET` | 1.012 | 1.040 | -0.099 | 0.471 |
| 19G0619 | `score_caf_core` | `score_spp1_cxcl12_axis_desoverlap_2026` | 1.022 | 1.001 | 1.171 | 0.128 |
| 19G0619 | `score_caf_core` | `score_hla_drb5_macrophage_axis_desoverlap_2026` | 1.330 | 0.998 | 6.359 | 0.002 |
| 19G0619 | `score_spp1_cxcl12_axis_desoverlap_2026` | `MYC` | 1.474 | 1.004 | 5.978 | 0.002 |
| 19G0619 | `score_spp1_cxcl12_axis_desoverlap_2026` | `score_myc_glycolysis_desoverlap_2026` | 1.559 | 0.996 | 10.374 | 0.002 |
| 19G0619 | `score_hla_drb5_macrophage_axis_desoverlap_2026` | `MYC` | 1.474 | 1.015 | 3.101 | 0.010 |
| 19G0619 | `score_hla_drb5_macrophage_axis_desoverlap_2026` | `score_myc_glycolysis_desoverlap_2026` | 1.561 | 1.000 | 5.515 | 0.002 |
| 19G0635 | `score_caf_core` | `MET` | 1.758 | 1.013 | 9.656 | 0.002 |
| 19G0635 | `score_caf_core` | `score_spp1_cxcl12_axis_desoverlap_2026` | 1.401 | 1.001 | 24.699 | 0.002 |
| 19G0635 | `score_caf_core` | `score_hla_drb5_macrophage_axis_desoverlap_2026` | 1.514 | 1.000 | 8.473 | 0.002 |
| 19G0635 | `score_spp1_cxcl12_axis_desoverlap_2026` | `MYC` | 1.378 | 1.000 | 21.781 | 0.002 |
| 19G0635 | `score_spp1_cxcl12_axis_desoverlap_2026` | `score_myc_glycolysis_desoverlap_2026` | 1.455 | 1.000 | 21.174 | 0.002 |
| 19G0635 | `score_hla_drb5_macrophage_axis_desoverlap_2026` | `MYC` | 1.485 | 1.002 | 14.518 | 0.002 |
| 19G0635 | `score_hla_drb5_macrophage_axis_desoverlap_2026` | `score_myc_glycolysis_desoverlap_2026` | 1.542 | 1.001 | 13.779 | 0.002 |
| 19G02977 | `score_caf_core` | `MET` | 1.942 | 1.054 | 1.967 | 0.040 |
| 19G02977 | `score_caf_core` | `score_spp1_cxcl12_axis_desoverlap_2026` | 1.553 | 0.999 | 15.634 | 0.002 |
| 19G02977 | `score_caf_core` | `score_hla_drb5_macrophage_axis_desoverlap_2026` | 1.227 | 1.002 | 1.966 | 0.026 |
| 19G02977 | `score_spp1_cxcl12_axis_desoverlap_2026` | `MYC` | 2.125 | 0.996 | 19.111 | 0.002 |
| 19G02977 | `score_spp1_cxcl12_axis_desoverlap_2026` | `score_myc_glycolysis_desoverlap_2026` | 2.143 | 1.005 | 21.068 | 0.002 |
| 19G02977 | `score_hla_drb5_macrophage_axis_desoverlap_2026` | `MYC` | 1.315 | 0.999 | 5.082 | 0.002 |
| 19G02977 | `score_hla_drb5_macrophage_axis_desoverlap_2026` | `score_myc_glycolysis_desoverlap_2026` | 1.330 | 1.001 | 6.156 | 0.002 |

## Mean External Spatial Effects

- `CAF -> SPP1/CXCL12-lite`: mean neighbor/background ratio 1.346.
- `CAF -> HLA-DRB5-lite`: mean neighbor/background ratio 1.391.
- `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: mean neighbor/background ratio 1.776.
- `HLA-DRB5-lite -> MYC/glycolysis-lite`: mean neighbor/background ratio 1.467.

## Interpretation Guardrails

- This is independent spatial validation, but still Visium-level and exploratory.
- Ratios above 1 with low empirical p suggest local coupling beyond random in-sample placement.
- Heterogeneous samples matter: a paper-grade claim should model patient/section variability, not just pooled averages.
- Positive GSE217414 plus positive GSE225857 would justify a manuscript-style storyline; discordance would sharpen the niche-specific boundary.
