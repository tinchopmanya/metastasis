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

## Actualizacion 2026: senales que suben prioridad

Fecha: 2026-04-27 16:22:03 -03:00

El ranking cambia de eje lineal a nicho en capas. `HGF-MET-MYC-glycolysis` queda como rama metabolica tumoral, pero las senales 2026 agregan una rama inmunosupresora mieloide/T-cell.

### Eje CAF/SPP1/CXCL12

| Senal | Rol esperado | Contexto |
| --- | --- | --- |
| `SPP1` | ligando central compartido por fibroblastos/macrofagos en varios papers | CAF, TAM, interfaz tumor-estroma |
| `CXCL12` | quimioquina CAF inducida por SPP1; exclusion CD8/inmunoresistencia | CAF, estroma |
| `CD44` | receptor de SPP1/FN1 en tumor/immune | tumor, T cells, macrophages |
| `MIF` | eje de estres/exhaustion y comunicacion mieloide | macrophage/T-cell niche |
| `FN1` | matriz/interaccion CD44; componente estructural | ECM/CAF |
| `HIF1A` | puente hipoxia/transcripcion CXCL12 | CAF/tumor |
| `CTNNB1` | beta-catenin vinculada a induccion CXCL12 | CAF/tumor |

### Macrofagos y comunicacion inmune

| Senal | Rol esperado | Contexto |
| --- | --- | --- |
| `HLA-DRB5` | macrofago asociado a microambiente inmune y pronostico | macrophage |
| `CD74` | receptor/componente MIF axis | macrophage/B/T context |
| `CXCR4` | receptor CXCL12/MIF-related | immune/tumor |
| `LGALS9` | comunicacion con T/NK via CD45/PTPRC | macrophage/immune |
| `PTPRC` | CD45; marcador pan-immune/receptor de LGALS9 | immune |
| `MARCO` | macrofago inmunosupresor en CASH/recurrencia CRLM | macrophage |
| `TOX` | T-cell exhaustion | T cell |
| `DNAJB1` | NK stress en CASH | NK/stress |

### Tumor/metabolismo 2026

| Senal | Rol esperado | Contexto |
| --- | --- | --- |
| `FADS1` | tumor cell state vinculado a SPP1+ macrophage/PDGFB axis | tumor |
| `PDGFB` | ligando secretado por macrophage SPP1+ segun paper 2026 | macrophage |
| `PDGFRB` | receptor/circuito stromal-tumor; tambien CAF/pericyte-like | tumor/stroma |
| `SHMT1` | one-carbon metabolism, formate/AMPK | tumor/metabolismo |
| `NDRG1` | rama PIM/NDRG1 phosphorylation/degradation | tumor/metabolismo |
| `PIM1`, `PIM2`, `PIM3` | kinases asociadas al eje NDRG1 | tumor/metabolismo |
| `FTCD`, `GPD1`, `SOD2`, `EIF4B` | marcadores proteogenomicos/subtipos metabolicos CRLM | metastasis |
| `MORF4L1` | resistencia a radioterapia, DDR/metabolismo/inmunoevasion | tumor |
| `SLC2A1` | GLUT1; debe interpretarse por compartimento/margen | tumor/immune margin |

### Nuevo ranking operativo

1. `CAF-high layered niche`: CAF-high + `MET/MYC/glycolysis` + `SPP1/CXCL12/myeloid/T-cell`.
2. `SPP1/CXCL12/MIF/CD44` como eje inmunomodulador inmediato.
3. `HLA-DRB5/LGALS9/CD74/CXCR4` como rama macrofago-immune.
4. `MET/MYC/glycolysis` como respuesta tumoral metabolica local.
5. `SHMT1/PIM/NDRG1` como expansion metabolica proteogenomica.
6. `MORF4L1` y `MARCO/CASH` como rutas secundarias hacia tratamiento/recurrencia.

## Ranking anterior
1. `HGF-MET-MYC-glycolysis`
2. `MCAM+ CAFs / Notch / CXCL13+ T cells`
3. macrófagos de alto metabolismo lipídico
4. plasticidad/EMT tumoral
5. radiomics de recurrencia como validación indirecta
