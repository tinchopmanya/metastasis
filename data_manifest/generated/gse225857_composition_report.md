# GSE225857 cell composition analysis

Generated at: 2026-04-26 01:31:24 UTC

## Purpose

Validate cell composition predictions of the mCAF-HGF-MET-MYC-glycolysis
hypothesis using single-cell metadata from GSE225857.

## Data

- Total non-immune cells: 41892
- Primary colon tumor (CCT): 15456 cells
- Liver metastasis (LCT): 26436 cells
- Cell types annotated: 23

## Cell composition by tissue

| Cell type | Category | CCT | LCT | % in LCT | Fold enrichment |
| --- | --- | --- | --- | --- | --- |
| `E06_endothelial_CLEC4G` | Endothelial | 1 | 41 | 98% | 23.97 |
| `Tu02_DEFA5` | Tumor | 132 | 4615 | 97% | 20.44 |
| `Tu08_GNG13` | Tumor | 79 | 465 | 85% | 3.44 |
| `E03_endothelial_NOTCH3` | Endothelial | 64 | 368 | 85% | 3.36 |
| `F04_fibroblast_C3` | Fibroblast | 266 | 1343 | 83% | 2.95 |
| `F02_fibrblast_MCAM` | Fibroblast | 692 | 3387 | 83% | 2.86 |
| `F01_fibroblast_PRELP` | Fibroblast | 1127 | 5091 | 82% | 2.64 |
| `E02_endothelial_DLL4` | Endothelial | 175 | 751 | 81% | 2.51 |
| `Tu05_PCNA` | Tumor | 817 | 1760 | 68% | 1.26 |
| `E01_endothelial_SELP` | Endothelial | 369 | 752 | 67% | 1.19 |
| `Tu07_MKI67` | Tumor | 782 | 1406 | 64% | 1.05 |
| `Tu01_AREG` | Tumor | 1685 | 2951 | 64% | 1.02 |
| `E05_cycling_MKI67` | Endothelial | 22 | 34 | 61% | 0.90 |
| `F05_fibroblast_COCH` | Fibroblast | 180 | 267 | 60% | 0.87 |
| `Tu10_COL3A1` | Tumor | 141 | 208 | 60% | 0.86 |
| `Tu04_RGMB` | Tumor | 997 | 1210 | 55% | 0.71 |
| `F06_cycling_MKI67` | Fibroblast | 110 | 117 | 52% | 0.62 |
| `Tu03_SRRM2` | Tumor | 2171 | 1289 | 37% | 0.35 |
| `Tu11_PLA2G2A` | Tumor | 157 | 60 | 28% | 0.22 |
| `E04_endothelial_CD36` | Endothelial | 194 | 74 | 28% | 0.22 |
| `Tu09_MUC2` | Tumor | 167 | 53 | 24% | 0.19 |
| `F03_fibroblast_CXCL14` | Fibroblast | 2367 | 146 | 6% | 0.04 |
| `Tu06_NKD1` | Tumor | 2761 | 48 | 2% | 0.01 |

## Key findings

### MCAM+ fibroblasts (F02_fibroblast_MCAM)

- 3387 cells in liver vs 692 in primary.
- 83% of all MCAM+ CAFs are in liver metastasis.
- Fold enrichment: 2.86x.
- **Prediction confirmed**: MCAM+ CAFs are enriched in liver metastasis.

### CXCL14+ fibroblasts (F03_fibroblast_CXCL14)

- 2367 cells in primary vs 146 in liver.
- Only 6% in liver. Fold: 0.04x.
- **Confirmed**: F3+ fibroblasts enriched in primary, opposite to MCAM+.

### Liver-dominant tumor subtype (Tu02_DEFA5)

- 4615 cells in liver (97%), only 132 in primary.
- Fold enrichment: 20.4x.

## Hypothesis assessment from composition

1. **MCAM+ CAFs liver-enriched**: CONFIRMED (83% in LCT, fold 2.9x).
2. **Distinct fibroblast programs**: CONFIRMED (CXCL14+ in CCT, MCAM+ in LCT).
3. **Liver-specific tumor subtypes**: CONFIRMED (Tu02_DEFA5 97% in LCT).

## Requires expression matrix (~86 MB)

- Whether HGF is expressed specifically in MCAM+ CAFs.
- Whether MET is expressed specifically in tumor cells.
- Whether MET-MYC correlation exists within tumor cells.
- Run: `python scripts/download_gse225857.py --non-immune`
- Then: `python scripts/validate_hgf_met_singlecell.py`
