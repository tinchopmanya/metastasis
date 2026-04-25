# Scripts

This folder will hold lightweight validation scripts for CRLM.

Initial direction:

1. Read `data_manifest/signatures.yml`.
2. Fetch or document metadata for GEO sources.
3. Prepare first-pass gene set scoring.
4. Keep image downloads out of scope until the molecular hypothesis is prioritized.

Preferred first script:

`prepare_signatures.py`

Expected output:

- normalized signature table
- signature-gene matrix
- markdown summary for the next research log

## Current script
Run:

```powershell
python scripts/prepare_signatures.py
```

Generated files:

- `data_manifest/generated/signatures_normalized.tsv`
- `data_manifest/generated/signature_gene_matrix.tsv`
- `data_manifest/generated/signature_report.md`

## Gene Availability
Run:

```powershell
python scripts/check_gene_availability.py
```

Generated files:

- `data_manifest/generated/hgnc_approved_symbols.tsv`
- `data_manifest/generated/gene_availability.tsv`
- `data_manifest/generated/gene_availability_report.md`

Later, add dataset-specific gene lists:

```powershell
python scripts/check_gene_availability.py --universe tcga_coad=data_manifest/gene_universes/tcga_coad_genes.txt
```
