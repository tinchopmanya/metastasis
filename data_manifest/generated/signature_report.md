# CRLM signature preparation report

Generated at: 2026-04-27 19:52:39 UTC

## Active hypothesis
CAF-high layered CRLM niche with MET/MYC-glycolysis and SPP1/CXCL12-myeloid/T-cell interfaces

## Summary
- Signatures: 20
- Signature-gene rows: 110
- Unique genes: 77
- Basic warnings: 0

## Generated files
- `data_manifest/generated/signatures_normalized.tsv`
- `data_manifest/generated/signature_gene_matrix.tsv`

## Reused genes across signatures
- `ACTA2`: caf_core, caf_core_desoverlap_2026, mcam_caf
- `CD44`: spp1_cxcl12_axis_desoverlap_2026, spp1_cxcl12_caf_myeloid_axis
- `CD74`: hla_drb5_macrophage_axis, hla_drb5_macrophage_axis_desoverlap_2026
- `CD8A`: cxcl13_t_cells, glut1_invasive_margin_axis, marco_cash_macrophage_axis
- `COL1A1`: caf_core, caf_core_desoverlap_2026, mcam_caf
- `COL1A2`: caf_core, caf_core_desoverlap_2026, mcam_caf
- `CTNNB1`: spp1_cxcl12_axis_desoverlap_2026, spp1_cxcl12_caf_myeloid_axis
- `CXCL12`: spp1_cxcl12_axis_desoverlap_2026, spp1_cxcl12_caf_myeloid_axis
- `CXCR4`: hla_drb5_macrophage_axis, hla_drb5_macrophage_axis_desoverlap_2026
- `ENO1`: myc_glycolysis_core, myc_glycolysis_desoverlap_2026
- `FAP`: caf_core, caf_core_desoverlap_2026
- `FN1`: spp1_cxcl12_axis_desoverlap_2026, spp1_cxcl12_caf_myeloid_axis
- `HIF1A`: radioresistance_morf4l1, spp1_cxcl12_axis_desoverlap_2026, spp1_cxcl12_caf_myeloid_axis
- `HK2`: myc_glycolysis_core, myc_glycolysis_desoverlap_2026
- `HLA-DRB5`: hla_drb5_macrophage_axis, hla_drb5_macrophage_axis_desoverlap_2026
- `LGALS9`: hla_drb5_macrophage_axis, hla_drb5_macrophage_axis_desoverlap_2026
- `MIF`: hla_drb5_macrophage_axis, spp1_cxcl12_caf_myeloid_axis
- `MYC`: myc_glycolysis_core, myc_glycolysis_desoverlap_2026
- `PDGFRA`: caf_core, caf_core_desoverlap_2026
- `PDGFRB`: caf_core, spp1_macrophage_fads1_pdgfb_axis
- `PGK1`: myc_glycolysis_core, myc_glycolysis_desoverlap_2026
- `POSTN`: caf_core, caf_core_desoverlap_2026
- `PTPRC`: hla_drb5_macrophage_axis, hla_drb5_macrophage_axis_desoverlap_2026
- `SLC2A1`: glut1_invasive_margin_axis, myc_glycolysis_core
- `SPP1`: hla_drb5_macrophage_axis, spp1_cxcl12_caf_myeloid_axis, spp1_macrophage_fads1_pdgfb_axis
- `VIM`: plasticity_emt, spp1_macrophage_fads1_pdgfb_axis
- `ZEB1`: plasticity_emt, spp1_macrophage_fads1_pdgfb_axis

## Warnings
- None

## Next refinements
- Compare full 2026 signatures against desoverlap controls in GSE225857 spatial.
- Test whether CAF-high neighborhoods split into metabolic tumor and immunosuppressive myeloid/T-cell interfaces after removing shared genes.
- Extract marker lists directly from 2026 CRLM spatial/single-cell papers and replace broad signatures with paper-derived top markers.

## Next technical step
Use these tables to check gene availability in GEO/TCGA expression matrices before scoring signatures.
