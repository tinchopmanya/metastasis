# Gene universes

This directory contains dataset-specific gene universe files. Each file is a plain text list of gene symbols available in a particular expression dataset.

## Purpose

Before scoring gene signatures in a dataset, we verify that all signature genes are actually measured in that dataset. A gene universe file captures which genes are present.

## Format

Each file is a `.txt` with one HGNC-approved gene symbol per line. Lines starting with `#` are comments. The first non-comment line may be a header (`gene_symbol`) or directly a gene.

## Naming convention

`{source}_{cohort}_genes.txt`

Examples:

- `tcga_coad_genes.txt` — genes from TCGA-COAD RNA-Seq (HTSeq counts via GDC).
- `tcga_read_genes.txt` — genes from TCGA-READ RNA-Seq.
- `gse225857_genes.txt` — genes from GSE225857 expression matrix.

## How they are created

- **GDC/TCGA**: `scripts/fetch_gdc_gene_universe.py` queries the GDC API for gene-level quantification file metadata and extracts the gene list from a single small STAR-Counts file without downloading full matrices.
- **GEO**: future scripts will extract gene lists from GEO series matrix headers or processed count files.
- **Manual/provisional**: if automated extraction is blocked, a provisional universe can be built from GENCODE annotation and clearly marked as such.

## Usage

```bash
python scripts/check_gene_availability.py \
    --universe tcga_coad=data_manifest/gene_universes/tcga_coad_genes.txt
```
