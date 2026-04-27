# External validation dataset triage

Generated at: 2026-04-27 06:18:51 UTC

## Purpose

Identify the next lightweight external validation route for the refined CRLM niche hypothesis:

`CAF-high spatial niches in CRLM associate with MET+ MYC/glycolytic tumor neighborhoods.`

## Summary

| Accession | Role | Files | Total file MB | Largest file MB | Types | Recommendation | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GSE225857` | already-used CRLM single-cell + Visium anchor | 58 | 606.97 | 213.95 | CSV:6, JPG:12, JSON:6, MTX:6, PNG:12, TSV:12, TXT:4 | `medium` | Raw 10x files are split and manageable; needs sample phenotype/cell annotation mapping. |
| `GSE226997` | CRC primary Visium spatial validation used in 2025 paper | 4 | 42146.37 | 12267.33 | TAR:4 | `low_now` | Only individual Visium TAR files are 9-13 GB; use only if a subset strategy is defined. |
| `GSE231559` | CRC single-cell raw 10x matrices used by 2025 paper | 78 | 692.0 | 49.07 | MTX:26, TSV:52 | `medium` | Raw 10x files are split and manageable; needs sample phenotype/cell annotation mapping. |
| `GSE234804` | CRC and liver-metastasis H5Seurat samples used by 2025 paper | 13 | 568.8 | 89.18 | H5SEURAT:13 | `high` | Individual CRC/LM H5Seurat files are moderate-sized; best next external CRLM candidate. |
| `GSE178318` | CRLM single-cell dataset referenced by 2025 macrophage/lipid paper | 0 | 0 | 0 |  | `unavailable` | Could not fetch GEO filelist: HTTP Error 404: Not Found |

## Decision

- Best immediate candidate: `GSE234804` because Individual CRC/LM H5Seurat files are moderate-sized; best next external CRLM candidate.
- Secondary candidates: `GSE225857`, `GSE231559`.
- Avoid `GSE226997` for now: it is spatially relevant but individual sample TAR files are too large for a quick external validation.
- Next technical step: inspect one `GSE234804` H5Seurat file structure and determine whether expression plus metadata can be extracted without R/Seurat.

## Caveat

This triage only evaluates file accessibility and likely utility. It does not validate biology by itself.
