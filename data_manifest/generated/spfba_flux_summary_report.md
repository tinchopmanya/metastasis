# spFBA/FES flux statistics summary

Generated at: 2026-04-29 11:24:17 UTC

## Scope

Summarizes selected reaction-level FES metrics from Zenodo 13988866 `output.tar.gz` without expanding the full archive. The key files are `flux_statistics.h5ad` under `output/*/sampling/CBS/`.

## Sign Convention

- `meanNormalized` is `.X` in `flux_statistics.h5ad`: sampled mean flux normalized by the FVA range.
- `EX_lac__L_e < 0` is interpreted as lactate uptake/consumption; `EX_lac__L_e > 0` as lactate export/secretion.
- Internal reaction signs are reaction-definition specific; compare directions cautiously.

## SC087 Colorectal Stereo-seq Mean-Normalized FES

| Sample | Type | Reaction | Mean | Median | % negative | % positive |
| --- | --- | --- | --- | --- | --- | --- |
| LM4 | liver_metastasis | `EX_lac__L_e` | -0.083 | -0.075 | 92.6 | 7.4 |
| LM4 | liver_metastasis | `PYRt2m` | -0.051 | -0.057 | 92.0 | 8.0 |
| LM4 | liver_metastasis | `PDHm` | 0.046 | 0.044 | 0.0 | 100.0 |
| LM4 | liver_metastasis | `ASPTA` | 0.112 | 0.109 | 0.0 | 100.0 |
| LM4 | liver_metastasis | `ASPTAm` | 0.082 | 0.074 | 0.0 | 100.0 |
| LM4 | liver_metastasis | `AKGMALtm` | 0.074 | 0.085 | 27.4 | 72.6 |
| LM4 | liver_metastasis | `MDHm` | 0.094 | 0.096 | 2.2 | 97.8 |
| LM4 | liver_metastasis | `Biomass` | 0.007 | 0.006 | 0.0 | 100.0 |
| LM4r | liver_metastasis | `EX_lac__L_e` | -0.165 | -0.173 | 99.5 | 0.5 |
| LM4r | liver_metastasis | `PYRt2m` | -0.019 | -0.022 | 74.8 | 25.2 |
| LM4r | liver_metastasis | `PDHm` | 0.057 | 0.056 | 0.0 | 100.0 |
| LM4r | liver_metastasis | `ASPTA` | 0.118 | 0.112 | 0.1 | 99.9 |
| LM4r | liver_metastasis | `ASPTAm` | 0.167 | 0.168 | 0.0 | 100.0 |
| LM4r | liver_metastasis | `AKGMALtm` | 0.093 | 0.096 | 3.3 | 96.7 |
| LM4r | liver_metastasis | `MDHm` | 0.184 | 0.192 | 0.0 | 100.0 |
| LM4r | liver_metastasis | `Biomass` | 0.007 | 0.007 | 0.0 | 100.0 |
| LM7 | liver_metastasis | `EX_lac__L_e` | -0.153 | -0.145 | 98.2 | 1.8 |
| LM7 | liver_metastasis | `PYRt2m` | -0.054 | -0.053 | 91.7 | 8.3 |
| LM7 | liver_metastasis | `PDHm` | 0.050 | 0.049 | 0.0 | 100.0 |
| LM7 | liver_metastasis | `ASPTA` | 0.165 | 0.160 | 0.0 | 100.0 |
| LM7 | liver_metastasis | `ASPTAm` | 0.166 | 0.159 | 0.0 | 100.0 |
| LM7 | liver_metastasis | `AKGMALtm` | 0.027 | 0.029 | 23.7 | 76.3 |
| LM7 | liver_metastasis | `MDHm` | 0.203 | 0.195 | 0.0 | 100.0 |
| LM7 | liver_metastasis | `Biomass` | 0.010 | 0.010 | 0.0 | 100.0 |
| PT | primary | `EX_lac__L_e` | -0.175 | -0.180 | 99.0 | 1.0 |
| PT | primary | `PYRt2m` | -0.018 | -0.018 | 82.6 | 17.4 |
| PT | primary | `PDHm` | 0.043 | 0.042 | 0.0 | 100.0 |
| PT | primary | `ASPTA` | 0.125 | 0.128 | 0.2 | 99.8 |
| PT | primary | `ASPTAm` | 0.129 | 0.121 | 0.0 | 100.0 |
| PT | primary | `AKGMALtm` | 0.215 | 0.217 | 0.0 | 100.0 |
| PT | primary | `MDHm` | 0.138 | 0.136 | 0.0 | 100.0 |
| PT | primary | `Biomass` | 0.013 | 0.013 | 0.0 | 100.0 |

## Lactate Exchange Across CRC Samples

`EX_lac__L_e < 0` means lactate uptake/consumption. The SC087 liver metastases show widespread lactate uptake, but the paired SC087 primary is even more negative on average. The CRC VisiumHD samples are mixed and should not be treated as metastasis-specific without matching annotations.

| Cohort | Sample | Type | Technology | Spots | Mean | Median | % negative | % positive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CRC_VisiumHD | P1 | crc_visiumhd | VisiumHD | 26687 | 0.016 | 0.015 | 39.2 | 60.8 |
| CRC_VisiumHD | P2 | crc_visiumhd | VisiumHD | 31414 | -0.016 | -0.009 | 57.2 | 42.8 |
| CRC_VisiumHD | P5 | crc_visiumhd | VisiumHD | 31773 | 0.012 | 0.015 | 39.8 | 60.2 |
| SC087 | LM4 | liver_metastasis | Stereo-seq | 9539 | -0.083 | -0.075 | 92.6 | 7.4 |
| SC087 | LM4r | liver_metastasis | Stereo-seq | 11919 | -0.165 | -0.173 | 99.5 | 0.5 |
| SC087 | LM7 | liver_metastasis | Stereo-seq | 20729 | -0.153 | -0.145 | 98.2 | 1.8 |
| SC087 | PT | primary | Stereo-seq | 14956 | -0.175 | -0.180 | 99.0 | 1.0 |

## LM-vs-PT Directional Snapshot

| Reaction | Metric | PT mean | LM mean | LM-PT | Direction hint |
| --- | --- | --- | --- | --- | --- |
| `EX_lac__L_e` | meanNormalized | -0.175 | -0.133 | 0.041 | LM_more_lactate_export_or_less_uptake_than_PT |
| `PYRt2m` | meanNormalized | -0.018 | -0.041 | -0.023 | LM_lower_forward_FES_than_PT |
| `PDHm` | meanNormalized | 0.043 | 0.051 | 0.008 | LM_higher_forward_FES_than_PT |
| `ASPTA` | meanNormalized | 0.125 | 0.132 | 0.007 | LM_higher_forward_FES_than_PT |
| `ASPTAm` | meanNormalized | 0.129 | 0.138 | 0.009 | LM_higher_forward_FES_than_PT |
| `AKGMALtm` | meanNormalized | 0.215 | 0.065 | -0.150 | LM_lower_forward_FES_than_PT |
| `MDHm` | meanNormalized | 0.138 | 0.160 | 0.022 | LM_higher_forward_FES_than_PT |
| `Biomass` | meanNormalized | 0.013 | 0.008 | -0.005 | LM_lower_forward_FES_than_PT |

## Strongest Lactate Uptake Couplings Across CRC Samples

`lactate_uptake_score = -EX_lac__L_e`; positive Spearman r means stronger lactate uptake co-occurs with higher target FES in the same sample.

| Cohort | Sample | Type | Target | Pearson r | Spearman r | Spots |
| --- | --- | --- | --- | --- | --- | --- |
| SC087 | LM7 | liver_metastasis | `ASPTA` | 0.768 | 0.776 | 20729 |
| SC087 | LM7 | liver_metastasis | `MDHm` | 0.631 | 0.643 | 20729 |
| CRC_VisiumHD | P2 | crc_visiumhd | `PDHm` | 0.587 | 0.615 | 31414 |
| SC087 | LM4 | liver_metastasis | `AKGMALtm` | 0.532 | 0.575 | 9539 |
| CRC_VisiumHD | P2 | crc_visiumhd | `ASPTA` | 0.532 | 0.529 | 31414 |
| CRC_VisiumHD | P5 | crc_visiumhd | `PDHm` | 0.649 | 0.527 | 31773 |
| SC087 | LM4r | liver_metastasis | `ASPTA` | 0.481 | 0.520 | 11919 |
| CRC_VisiumHD | P2 | crc_visiumhd | `MDHm` | 0.477 | 0.511 | 31414 |
| CRC_VisiumHD | P5 | crc_visiumhd | `ASPTA` | 0.475 | 0.504 | 31773 |
| SC087 | LM4r | liver_metastasis | `MDHm` | 0.601 | 0.489 | 11919 |
| CRC_VisiumHD | P5 | crc_visiumhd | `MDHm` | 0.609 | 0.431 | 31773 |
| CRC_VisiumHD | P2 | crc_visiumhd | `ASPTAm` | 0.389 | 0.427 | 31414 |
| SC087 | PT | primary | `ASPTAm` | 0.434 | 0.415 | 14956 |
| CRC_VisiumHD | P5 | crc_visiumhd | `ASPTAm` | 0.558 | 0.406 | 31773 |
| SC087 | LM4r | liver_metastasis | `PDHm` | 0.462 | 0.404 | 11919 |
| SC087 | PT | primary | `MDHm` | 0.404 | 0.400 | 14956 |
| SC087 | PT | primary | `ASPTA` | 0.314 | 0.366 | 14956 |
| SC087 | LM4r | liver_metastasis | `ASPTAm` | 0.496 | 0.355 | 11919 |

## Lactate Uptake Coupling Within SC087 Samples

`lactate_uptake_score = -EX_lac__L_e`; positive correlation means stronger lactate uptake co-occurs with higher target FES.

| Sample | Type | Target | Pearson r | Spearman r |
| --- | --- | --- | --- | --- |
| LM4 | liver_metastasis | `PYRt2m` | -0.532 | -0.546 |
| LM4 | liver_metastasis | `PDHm` | -0.203 | -0.274 |
| LM4 | liver_metastasis | `ASPTA` | 0.349 | 0.288 |
| LM4 | liver_metastasis | `ASPTAm` | 0.209 | 0.221 |
| LM4 | liver_metastasis | `AKGMALtm` | 0.532 | 0.575 |
| LM4 | liver_metastasis | `MDHm` | 0.025 | -0.050 |
| LM4 | liver_metastasis | `Biomass` | -0.186 | 0.039 |
| LM4r | liver_metastasis | `PYRt2m` | -0.444 | -0.463 |
| LM4r | liver_metastasis | `PDHm` | 0.462 | 0.404 |
| LM4r | liver_metastasis | `ASPTA` | 0.481 | 0.520 |
| LM4r | liver_metastasis | `ASPTAm` | 0.496 | 0.355 |
| LM4r | liver_metastasis | `AKGMALtm` | 0.208 | 0.157 |
| LM4r | liver_metastasis | `MDHm` | 0.601 | 0.489 |
| LM4r | liver_metastasis | `Biomass` | -0.076 | -0.068 |
| LM7 | liver_metastasis | `PYRt2m` | -0.712 | -0.714 |
| LM7 | liver_metastasis | `PDHm` | -0.079 | -0.038 |
| LM7 | liver_metastasis | `ASPTA` | 0.768 | 0.776 |
| LM7 | liver_metastasis | `ASPTAm` | 0.271 | 0.208 |
| LM7 | liver_metastasis | `AKGMALtm` | -0.164 | -0.211 |
| LM7 | liver_metastasis | `MDHm` | 0.631 | 0.643 |
| LM7 | liver_metastasis | `Biomass` | -0.356 | -0.382 |
| PT | primary | `PYRt2m` | -0.117 | -0.181 |
| PT | primary | `PDHm` | 0.338 | 0.324 |
| PT | primary | `ASPTA` | 0.314 | 0.366 |
| PT | primary | `ASPTAm` | 0.434 | 0.415 |
| PT | primary | `AKGMALtm` | 0.081 | 0.009 |
| PT | primary | `MDHm` | 0.404 | 0.400 |
| PT | primary | `Biomass` | -0.349 | -0.160 |

## Interpretation

- These FES samples are not the same sections as GSE225857/GSE217414, so they cannot directly validate spot-level HLA-DRB5 neighborhoods from our earlier Visium analyses.
- They can test whether an independent colorectal primary/metastasis dataset contains the lactate/pyruvate/transamination flux phenotype required by the hypothesis.
- A rescue of the HLA-DRB5/lactate branch would still require either expression/annotation from the same spFBA samples or a registered spatial link between immune modules and FES maps.
