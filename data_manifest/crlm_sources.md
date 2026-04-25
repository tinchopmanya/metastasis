# CRLM data sources manifest

Fecha: 2026-04-25 01:06:15 -03:00

## Purpose
This manifest tracks the public resources that can be used to test the active hypothesis:

`mCAF-HGF-MET-MYC-glycolysis in colorectal cancer liver metastasis`

## Sources

| ID | Resource | Type | Priority | Use | URL |
| --- | --- | --- | --- | --- | --- |
| `GSE225857` | Single-cell and spatial transcriptome analysis of liver metastatic CRC | scRNA-seq + spatial | high | MCAM+ CAFs, CXCL13+ T cells, primary vs liver metastasis | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857 |
| `GSE226997` | Visium spatial transcriptomics of CRC | spatial | high | spatial validation of mCAF/High-M CRC/HGF-MET-MYC/glycolysis | https://www.omicsdi.org/dataset/geo/GSE226997 |
| `PMC12605286` | Spatially resolved single-cell CRLM landscape | paper + integrated datasets | high | hypothesis leader and marker extraction | https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/ |
| `PMC10275599` | Single-cell/spatial CRLM heterogeneity | paper + GEO | high | MCAM+ CAFs and CXCL13+ T cells | https://pmc.ncbi.nlm.nih.gov/articles/PMC10275599/ |
| `TCGA-COAD` | Colon adenocarcinoma bulk data | bulk RNA/genomics | medium | weak validation of correlations and prognosis | https://portal.gdc.cancer.gov/ |
| `TCIA-CRLM` | Colorectal-Liver-Metastases | CT + segmentations + clinical | medium | recurrence/survival line after molecular prioritization | https://www.cancerimagingarchive.net/collection/colorectal-liver-metastases/ |
| `META-PRISM` | metastatic refractory cancer cohort | exome + transcriptome | medium | metastatic external validation | https://pmc.ncbi.nlm.nih.gov/articles/PMC10157368/ |

## Current policy
Start with lightweight metadata, marker extraction, and gene-set scoring. Avoid heavy image downloads until the biological hypothesis has survived first-pass checks.
