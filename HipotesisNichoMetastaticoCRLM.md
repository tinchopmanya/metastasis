# Hipótesis priorizadas del nicho metastásico hepático en CRLM

Fecha: 2026-04-25 01:06:15 -03:00

## Marco
Este archivo convierte la ola 003 en una matriz de trabajo. Cada hipótesis debe poder ser fortalecida, debilitada o descartada con datos públicos.

## Matriz inicial

| Prioridad | Hipótesis | Mecanismo propuesto | Células | Genes/vías | Evidencia | Datasets | Validación computacional | Criterio de falsación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mCAF-HGF-MET-MYC-glycolysis` | mCAFs producen `HGF`; células tumorales `MET+` activan `MYC` y glicólisis, aumentando plasticidad/invasión | mCAF, High-M CRC | `HGF`, `MET`, `MYC`, `SLC2A1`, `HK2`, `PGK1`, `TPI1`, `LDHA` | Estudio 2025 integrativo single-cell/spatial con validación funcional | GSE231559, GSE234804, GSE226997, TCGA-COAD | score mCAF, score High-M CRC, co-localización espacial, correlación `MET-MYC`, score glicólisis | No hay HGF estromal, no hay MET tumoral, no hay co-localización ni asociación con glicólisis |
| 2 | `MCAM+ CAFs -> Notch -> CXCL13+ T cells` | Fibroblastos `MCAM+` en metástasis hepática modulan estados T `CXCL13+` vía Notch | MCAM+ CAF, CD8_CXCL13, CD4_CXCL13 | `MCAM`, `CXCL13`, ligandos/receptores Notch | GSE225857/Science Advances | GSE225857, GSE50760 si accesible | deconvolución espacial, score MCAM CAF, score CXCL13 T, análisis ligand-receptor | MCAM+ no se enriquece en LM o no se asocia con estados T CXCL13 |
| 3 | Macrófagos lipídicos sostienen inmunomodulación hepática | Macrófagos con metabolismo lipídico alto aparecen enriquecidos en CRLM y remodelan VEGF/complemento/integrinas | Macrófagos CD1C+, CXCL10+, CX3CR1+ | lipid metabolism, `VEGFA`, `VEGFC`, complement, integrinas | Journal of Translational Medicine 2025 | GSE225857, GSE178318, spatial scCRLM | score de metabolismo lipídico en macrófagos, comparación pCRC vs CRLM | La actividad lipídica no aumenta en CRLM o no se concentra en macrófagos |
| 4 | Plasticidad/EMT amplifica respuesta al nicho | Células tumorales plásticas responden mejor a señales estromales y colonizan hígado | High-M CRC, EMT-like tumor cells | `BHLHE40`, `VIM`, `ZEB1`, `TGF-beta`, `KRAS`, `MYC` | papers single-cell/spatial y trabajos sobre BHLHE40/EMT | GSE225857, TCGA-COAD, cohorts metastásicas | score EMT/plasticidad cruzado con MET/MYC/glicólisis | Plasticidad no se asocia a metástasis ni a scores del eje principal |
| 5 | Señal temprana de tropismo hepático desde primario | Parte del programa metastásico ya está presente antes de la lesión hepática visible | Tumor primario, High-M-like CRC | `MET`, `MYC`, glicólisis, stemness | NCI/Nature Genetics sobre siembra temprana | TCGA-COAD/READ, GEO primario-metástasis | buscar firma High-M/mCAF-adjacent en primarios con outcome | Cohorts primarias no muestran asociación o etiquetas son insuficientes |
| 6 | Nicho radiobiológico visible en CT | El nicho biológico deja huella en imagen preoperatoria o riesgo de recurrencia | Tumor, parénquima hepático, interfaz | radiomics, volumen, textura, bordes | TCIA CRLM 197 pacientes | TCIA Colorectal-Liver-Metastases | asociar features con recurrencia/supervivencia y, luego, con firmas biológicas | Modelo no supera baseline clínico o no generaliza |

## Hipótesis líder
La hipótesis líder es `mCAF-HGF-MET-MYC-glycolysis`.

Razones:

- Tiene mecanismo claro.
- Tiene soporte reciente y validación funcional.
- Es espacialmente testeable.
- Se conecta con metabolismo y plasticidad, no sólo con expresión diferencial.
- Puede cruzarse con otras hipótesis, especialmente MCAM+ CAFs y macrófagos lipídicos.

## Refinamiento tras validacion espacial por permutaciones

Actualizacion: 2026-04-27 00:40:23 -03:00

La hipotesis lider ya no debe leerse como una flecha simple `HGF -> MET`. La evidencia acumulada favorece una formulacion mas robusta:

`CAF-high spatial niches in CRLM associate with MET+ MYC/glycolytic tumor neighborhoods.`

Soporte nuevo:

- En GSE225857 Visium, vecinos de `CAF-high` enriquecen `MET` en LCT con ratios 2.029 y 1.866.
- Contra 500 permutaciones dentro de muestra, `CAF -> MET` conserva p empirico 0.002 en L1 y L2.
- `CAF-high` tambien enriquece vecinos `MYC` y `glycolysis_score` con p empirico 0.002.
- `HGF-high` no enriquece vecinos `MET` en LCT; ratios 0.874 y 0.814.

Interpretacion:

- `HGF` sigue siendo plausible como parte del circuito paracrino por la evidencia single-cell.
- El marcador espacial mas fuerte es el programa CAF compuesto, no `HGF` aislado.
- Las validaciones futuras deben puntuar firmas CAF/PRELP/MCAM y no depender de un solo ligando.

## Presion de falsacion externa GSE234804

Actualizacion: 2026-04-27 03:32:49 -03:00

Se probo `GSE234804` como dataset externo CRLM sample-level: 3 CRC vs 6 LM, 32,435 celulas en H5Seurat. El resultado no confirma una version promedio de la hipotesis:

- `score_mcam_caf`: LM 0.057 vs CRC 0.103.
- `score_caf_core`: LM 0.046 vs CRC 0.065.
- `score_myc_glycolysis_core`: LM 2.109 vs CRC 3.312.
- `MET`: LM 0.341 vs CRC 0.236.
- `HGF`: LM 0.014 vs CRC 0.011.

Decision interpretativa:

- La hipotesis no debe formularse como "LM tiene mas CAF/MCAM/MYC-glicolisis en promedio".
- La version defendible queda restringida a arquitectura local/celular: `CAF-high neighborhoods` asociados con tumor `MET+` y respuesta `MYC/glicolisis`.
- El siguiente test critico debe usar anotaciones celulares o spatial externo.

## Primer experimento computacional sugerido
Construir gene sets mínimos:

- `mCAF`: marcadores del paper 2025 y genes ECM/matriz.
- `High-M CRC`: top markers de High-M CRC del paper 2025.
- `HGF-MET`: `HGF`, `MET`, targets downstream.
- `MYC activity`: targets Hallmark MYC.
- `Glycolysis`: Hallmark glycolysis y genes `SLC2A1`, `HK2`, `PGK1`, `TPI1`, `LDHA`.

Luego:

1. Probar enrichment por célula o spot.
2. Comparar primario vs metástasis.
3. Medir proximidad espacial si hay coordenadas.
4. Medir correlaciones en bulk TCGA-COAD como validación débil.

## Fuentes
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
- https://pubmed.ncbi.nlm.nih.gov/41234356/
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10275599/
- https://link.springer.com/article/10.1186/s12967-025-07581-1

## Refinamiento por literatura 2026: modelo CAF-high en capas

Actualizacion: 2026-04-27 16:22:03 -03:00

La busqueda PubMed 2025-2026 mueve la hipotesis lider hacia un modelo mas amplio:

`CAF-high layered niche model in CRLM`

Formulacion:

`Niches CAF-high in CRLM may coordinate a tumor metabolic interface (MET/MYC/glycolysis/one-carbon metabolism) and an immunosuppressive myeloid/T-cell interface (SPP1/CXCL12/MIF/CD44/FN1/HLA-DRB5/CD74/CXCR4/LGALS9).`

Por que sube prioridad:

- El resultado propio en GSE225857 ya sostiene `CAF-high -> MET/MYC/glycolysis` contra permutaciones.
- La literatura 2026 sostiene de manera independiente una arquitectura mCAF - SPP1+ macrophage - T-cell stress/exhaustion.
- `SPP1/CXCL12` aparece como eje funcional de inmunoresistencia y exclusion CD8.
- `HLA-DRB5+` macrophages agregan una segunda rama mieloide espacial.
- La proteogenomica CRLM 2026 expande la rama metabolica hacia `SHMT1`, `PIM/NDRG1` y subtipos metabolicos.

Nueva matriz corta de hipotesis:

| Prioridad | Hipotesis | Mecanismo | Genes/vias | Proximo test |
| --- | --- | --- | --- | --- |
| 1 | `CAF-high layered niche` | CAF-high organiza interfaz metabolica tumoral e interfaz inmunosupresora mieloide/T | `MET`, `MYC`, `SPP1`, `CXCL12`, `MIF`, `CD44`, `HLA-DRB5` | Spatial GSE225857 con vecindad/capas |
| 2 | `SPP1/CXCL12 CAF-myeloid axis` | SPP1 induce CXCL12 en CAFs y favorece EMT/exclusion CD8 | `SPP1`, `CXCL12`, `CD44`, `MIF`, `FN1`, `HIF1A`, `CTNNB1` | Score por spot y vecinos CAF-high |
| 3 | `HLA-DRB5 macrophage immune axis` | Macrofagos HLA-DRB5+ comunican con T/NK y moldean inmunidad | `HLA-DRB5`, `LGALS9`, `PTPRC`, `CD74`, `CXCR4` | Proximidad a CD8/T exhaustion y CAF |
| 4 | `SPP1+ macrophage-FADS1+ tumor` | Macrofago SPP1+ secreta PDGFB y activa tumor FADS1+/PDGFRB/EMT | `SPP1`, `PDGFB`, `PDGFRB`, `FADS1`, `VIM`, `ZEB1` | Test cell-type/spatial si los genes estan detectables |
| 5 | `Metabolic vulnerabilities 2026` | CRLM tiene vulnerabilidades de carbono/one-carbon y PIM/NDRG1 | `SHMT1`, `FTCD`, `GPD1`, `SOD2`, `EIF4B`, `NDRG1`, `PIM1/2/3` | Score en tumor/metastasis y relacion con CAF-high |

Criterio de hallazgo fuerte:

- Si los scores 2026 muestran una disposicion espacial reproducible en capas alrededor de CAF-high y tumor, la hipotesis gana novedad computacional.
- Si los scores aparecen mezclados sin estructura o dependen solo de composicion celular, la hipotesis baja a "convergencia bibliografica", no hallazgo.

Fuentes 2026 principales:

- https://pubmed.ncbi.nlm.nih.gov/41807965/
- https://pubmed.ncbi.nlm.nih.gov/41051794/
- https://pubmed.ncbi.nlm.nih.gov/41715121/
- https://pubmed.ncbi.nlm.nih.gov/41655559/
- https://pubmed.ncbi.nlm.nih.gov/41195591/
- https://pubmed.ncbi.nlm.nih.gov/41940986/

## Primera validacion espacial del modelo en capas

Actualizacion: 2026-04-27 16:50:00 -03:00

Se ejecuto `scripts/analyze_gse225857_spatial_2026.py` sobre 22,260 spots Visium de GSE225857, con 500 permutaciones por prueba LCT.

Resultado principal:

- `caf_core -> spp1_cxcl12_caf_myeloid_axis`: L1 ratio 1.497, L2 ratio 1.522, p empirico 0.002 en ambas.
- `caf_core -> hla_drb5_macrophage_axis`: L1 ratio 1.564, L2 ratio 1.403, p empirico 0.002 en ambas.
- `caf_core -> myc_glycolysis_core`: L1 ratio 1.423, L2 ratio 1.847, p empirico 0.002.
- `spp1_cxcl12_axis -> myc_glycolysis_core`: L1 ratio 1.578, L2 ratio 1.932, p empirico 0.002.
- `hla_drb5_axis -> myc_glycolysis_core`: L1 ratio 1.548, L2 ratio 1.563, p empirico 0.002.

Decision:

La hipotesis `CAF-high layered niche` sube prioridad. La formulacion mas honesta ahora es:

`En GSE225857, los nichos CAF-high de CRLM se acoplan a programas metabolicos tumorales y a programas mieloides/inmunomoduladores 2026, sugiriendo un macro-nicho estromal-inmune-metabolico.`

Cuidado:

- Esto no prueba capas microscopicas separadas.
- Visium mezcla celulas.
- Las firmas 2026 comparten genes y pueden inflar correlaciones.
- La validacion externa sigue siendo necesaria.

Control desolapado:

- `SPP1/CXCL12-lite` mantiene la senal despues de remover `SPP1` y `MIF`: `CAF -> SPP1/CXCL12-lite` ratio medio 1.513, `SPP1/CXCL12-lite -> MYC/glycolysis-lite` ratio medio 1.602.
- `HLA-DRB5-lite` se debilita despues de remover genes compartidos: fuerte en L1, debil/marginal en L2.
- Ajuste de prioridad: el brazo `SPP1/CXCL12` pasa a ser la extension 2026 principal; `HLA-DRB5` queda como rama secundaria que necesita mejor especificidad.
