# Señales prioritarias en CRLM

Fecha: 2026-04-25 01:06:15 -03:00

## Núcleo de la hipótesis líder

| Señal | Rol esperado | Célula/contexto | Validación inicial |
| --- | --- | --- | --- |
| `HGF` | Ligando estromal | CAF/mCAF | enriquecimiento en fibroblastos, co-localización con tumor receptor |
| `MET` | Receptor tumoral | High-M CRC / epitelial maligno | expresión tumoral, correlación con `MYC` |
| `MYC` | regulador transcripcional | células tumorales plásticas | actividad de targets MYC |
| `SLC2A1` | transporte de glucosa | tumor glicolítico | score glicólisis |
| `HK2` | glicólisis | tumor glicolítico | score glicólisis |
| `PGK1` | glicólisis | tumor glicolítico | score glicólisis |
| `TPI1` | glicólisis | tumor glicolítico | score glicólisis |
| `LDHA` | lactato/glicólisis | tumor/metabolismo | score glicólisis e hipoxia |

## Estroma
- `MCAM`
- `COL1A1`
- `COL1A2`
- `ACTA2`
- `FAP`
- `POSTN`
- marcadores mCAF/ECM del paper 2025

## Inmunidad
- `CXCL13`
- `CD8A`
- `CD4`
- ligandos/receptores Notch
- marcadores de macrófagos CD1C+, CXCL10+, CX3CR1+
- genes de complemento, VEGF e integrinas

## Plasticidad tumoral
- `BHLHE40`
- `VIM`
- `ZEB1`
- `LGR5`
- `EPCAM`
- `CDH1`
- vías `TGF-beta`, `KRAS`, `MYC`, EMT parcial, stemness

## Metabolismo
- Hallmark glycolysis
- oxidative phosphorylation como contraste
- metabolismo lipídico en macrófagos
- hipoxia
- lactato

## Ranking actual
1. `HGF-MET-MYC-glycolysis`
2. `MCAM+ CAFs / Notch / CXCL13+ T cells`
3. macrófagos de alto metabolismo lipídico
4. plasticidad/EMT tumoral
5. radiomics de recurrencia como validación indirecta
