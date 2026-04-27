# CRLM gene availability report

Generated at: 2026-04-27 19:53:02 UTC

## Universes
- `hgnc_approved`: 44982 symbols; source: https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt
- `tcga_coad`: 59427 symbols; source: data_manifest/gene_universes/tcga_coad_genes.txt

## Signature Coverage
- `caf_core` in `hgnc_approved`: 7/7 available (100.0%)
- `caf_core` in `tcga_coad`: 7/7 available (100.0%)
- `caf_core_desoverlap_2026` in `hgnc_approved`: 6/6 available (100.0%)
- `caf_core_desoverlap_2026` in `tcga_coad`: 6/6 available (100.0%)
- `crlm_metabolic_vulnerabilities_2026` in `hgnc_approved`: 9/9 available (100.0%)
- `crlm_metabolic_vulnerabilities_2026` in `tcga_coad`: 9/9 available (100.0%)
- `cxcl13_t_cells` in `hgnc_approved`: 6/6 available (100.0%)
- `cxcl13_t_cells` in `tcga_coad`: 6/6 available (100.0%)
- `glut1_invasive_margin_axis` in `hgnc_approved`: 5/5 available (100.0%)
- `glut1_invasive_margin_axis` in `tcga_coad`: 5/5 available (100.0%)
- `hgf_met_axis` in `hgnc_approved`: 2/2 available (100.0%)
- `hgf_met_axis` in `tcga_coad`: 2/2 available (100.0%)
- `hla_drb5_macrophage_axis` in `hgnc_approved`: 7/7 available (100.0%)
- `hla_drb5_macrophage_axis` in `tcga_coad`: 7/7 available (100.0%)
- `hla_drb5_macrophage_axis_desoverlap_2026` in `hgnc_approved`: 5/5 available (100.0%)
- `hla_drb5_macrophage_axis_desoverlap_2026` in `tcga_coad`: 5/5 available (100.0%)
- `macrophage_lipid_candidate` in `hgnc_approved`: 8/8 available (100.0%)
- `macrophage_lipid_candidate` in `tcga_coad`: 8/8 available (100.0%)
- `marco_cash_macrophage_axis` in `hgnc_approved`: 5/5 available (100.0%)
- `marco_cash_macrophage_axis` in `tcga_coad`: 5/5 available (100.0%)
- `mcam_caf` in `hgnc_approved`: 4/4 available (100.0%)
- `mcam_caf` in `tcga_coad`: 4/4 available (100.0%)
- `myc_glycolysis_core` in `hgnc_approved`: 7/7 available (100.0%)
- `myc_glycolysis_core` in `tcga_coad`: 7/7 available (100.0%)
- `myc_glycolysis_desoverlap_2026` in `hgnc_approved`: 4/4 available (100.0%)
- `myc_glycolysis_desoverlap_2026` in `tcga_coad`: 4/4 available (100.0%)
- `plasticity_emt` in `hgnc_approved`: 6/6 available (100.0%)
- `plasticity_emt` in `tcga_coad`: 6/6 available (100.0%)
- `radioresistance_morf4l1` in `hgnc_approved`: 4/4 available (100.0%)
- `radioresistance_morf4l1` in `tcga_coad`: 4/4 available (100.0%)
- `sema3c_nrp2_lmic_axis` in `hgnc_approved`: 4/4 available (100.0%)
- `sema3c_nrp2_lmic_axis` in `tcga_coad`: 4/4 available (100.0%)
- `spp1_cxcl12_axis_desoverlap_2026` in `hgnc_approved`: 5/5 available (100.0%)
- `spp1_cxcl12_axis_desoverlap_2026` in `tcga_coad`: 5/5 available (100.0%)
- `spp1_cxcl12_caf_myeloid_axis` in `hgnc_approved`: 7/7 available (100.0%)
- `spp1_cxcl12_caf_myeloid_axis` in `tcga_coad`: 7/7 available (100.0%)
- `spp1_macrophage_fads1_pdgfb_axis` in `hgnc_approved`: 6/6 available (100.0%)
- `spp1_macrophage_fads1_pdgfb_axis` in `tcga_coad`: 6/6 available (100.0%)
- `stromal_myeloid_risk_2026` in `hgnc_approved`: 3/3 available (100.0%)
- `stromal_myeloid_risk_2026` in `tcga_coad`: 3/3 available (100.0%)

## Missing Genes
- None

## GEO Status
- `GSE225857`: processed GEO TAR is about 607 MB; defer heavy extraction until marker lists are refined.
- `GSE226997`: processed GEO TAR is about 41.2 GB; do not download in the first-pass checker.

## Next Step
Add local gene-universe files extracted from GEO/TCGA matrices and rerun this checker with `--universe name=path`.
