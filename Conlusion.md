# Conclusión dinámica vigente

Fecha de actualización: 2026-04-27 03:32:49 -03:00

## Línea activa
La línea activa queda fijada en:

`nicho metastásico hepático en cáncer colorrectal`

## Hipótesis principal
CAFs/mCAFs hepáticos crean nichos metabólicos e inmunomoduladores que favorecen células tumorales colorrectales plásticas. La versión refinada ya no depende de `HGF` como marcador único: el patrón fuerte es un nicho espacial `CAF-high` asociado a células tumorales `MET+` con activación `MYC` y glicólisis local.

## Por qué esta hipótesis manda ahora
- Es mecanística: conecta estroma, tumor, metabolismo, espacialidad e inmunidad.
- Tiene soporte reciente en single-cell, spatial transcriptomics y validación funcional.
- Usa datasets públicos concretos: `GSE225857`, `GSE226997`, TCGA-COAD, TCIA CRLM y cohorts metastásicas.
- Es falsable: si no hay co-localización, correlación o enriquecimiento reproducible de las firmas, la hipótesis pierde fuerza.
- Permite salida computacional útil sin prometer validación clínica inmediata.

## Núcleo de evidencia
- Un estudio 2025 integró 35 datasets single-cell y spatial y propuso un eje `mCAF -> HGF-MET -> MYC/glycolysis` en nichos de metástasis hepática colorrectal.
- `GSE225857` aporta soporte independiente para heterogeneidad celular en CRLM, incluyendo fibroblastos `MCAM+` y células T `CXCL13+`.
- La literatura 2025 sobre macrófagos sugiere que el metabolismo lipídico puede reprogramar estados mieloides en CRLM, lo que encaja con el hígado como órgano metabólico e inmunomodulador.

## Validación computacional completada

### Bulk TCGA-COAD (329 muestras)
- `MET-MYC` r = 0.515 (fuerte). `MYC-glycolysis` r = 0.422 (moderada). `CAF-HGF` r = 0.675 (fuerte).
- `HGF-MET` r = -0.08: consistente con señalización paracrina diluida en bulk.

### Composición celular GSE225857 (41,892 células)
- MCAM+ CAFs: 83% en hígado (fold 2.86x). CONFIRMADO.
- Tu02_DEFA5: 97% hígado-específico (fold 20.4x). CONFIRMADO.

### Expresión single-cell GSE225857 (17,516 genes x 41,892 células)
- HGF en fibroblastos (mean 0.674) vs tumor (mean 0.004): ratio 168x. CONFIRMADO.
- MET en tumor (mean 0.399) vs fibroblastos (mean 0.009): ratio 44x. CONFIRMADO.
- MET-MYC en tumor: r = 0.1438, n = 23,954, p < 1e-300. CONFIRMADO.
- MYC-PGK1 r = 0.36, MYC-TPI1 r = 0.42 en tumor. CONFIRMADO.
- Patrón paracrino HGF(estroma)→MET(tumor) validado a nivel single-cell.

### Refinamiento
- La fuente de HGF en hígado no es solo MCAM+ CAFs sino también PRELP+ fibroblasts (F01).
- MYC es 45% más alto en metástasis hepática que en tumor primario.
- MET-MYC es débil per-cell (r=0.14) pero robusto estadísticamente, sugiriendo heterogeneidad espacial.

### Spatial GSE225857 Visium (6 muestras, 22,260 spots)
- Se descargaron sólo matrices, barcodes, features y posiciones; no imágenes.
- En metástasis hepática, `caf_score~MET` spot-level promedio r = 0.286.
- En metástasis hepática, `MYC~glycolysis_score` spot-level promedio r = 0.645.
- Análisis de vecindad: spots vecinos a CAF alto tienen MET casi 2x sobre fondo en LCT (ratio medio 1.948).
- Vecinos de HGF alto no muestran enriquecimiento de MET en LCT (ratio medio 0.844).
- Permutaciones dentro de muestra (500 por test): `CAF -> MET` conserva p empírico 0.002 en L1 y L2.
- `CAF-high` también enriquece vecinos `MYC` y `glycolysis_score` contra el nulo con p empírico 0.002.
- `HGF-high -> MET` no supera el nulo en LCT (p empírico 0.994 y 0.936).

### Clinica TCGA-COAD (329 muestras unidas)
- `mcam_caf` es mas alto en N positivo vs N0 (p = 6.95e-04) y en invasion linfatica positiva vs negativa (p = 1.15e-03).
- `caf_core` muestra el mismo patron: N positivo vs N0 (p = 8.57e-04) e invasion linfatica (p = 2.27e-03).
- `caf_core` alto y `mcam_caf` alto muestran peor supervivencia exploratoria por mediana (log-rank p = 0.020 y 0.027).
- El composite `CAF/MET/MYC/glicolisis` no muestra supervivencia significativa en bulk (p = 0.493), y `HGF-MET` aislado tampoco (p = 0.531).

### Validacion externa GSE234804 H5Seurat (3 CRC, 6 LM)
- Se procesaron 9 muestras externas: 3 CRC y 6 liver metastasis, 32,435 celulas en total.
- A nivel muestra, `mcam_caf` no aumenta en LM: LM mean 0.057 vs CRC mean 0.103.
- `caf_core` tampoco aumenta en LM: 0.046 vs 0.065.
- `myc_glycolysis_core` es menor en LM: 2.109 vs 3.312.
- `MET` es modestamente mayor en LM: 0.341 vs 0.236, pero sin soporte estadistico fuerte.
- `HGF` es muy bajo/casi igual: 0.014 vs 0.011.
- Lectura: GSE234804 no confirma la hipotesis como firma sample-level LM-vs-CRC.

## Estado de la hipótesis: fuerte, pero refinada
La hipótesis `mCAF-HGF-MET-MYC-glycolysis` sigue siendo prometedora como arquitectura espacial/celular, pero no como firma promedio universal. GSE225857 apoya con fuerza el patron local `CAF-high -> MET/MYC/glicolisis`; TCGA-COAD apoya que CAF/MCAM tiene sombra clinica; GSE234804, en cambio, no replica una elevacion sample-level de CAF/MCAM o MYC-glicolisis en LM. Esto obliga a formular el posible hallazgo como nicho espacial especifico, no como biomarcador bulk.

## Mejor output próximo
El siguiente avance útil es validación cruzada:

- reproducibilidad en dataset independiente
- co-localización espacial mCAF-tumor
- especificidad CRLM vs metástasis general (META-PRISM)
- supervivencia/pronóstico en TCGA-COAD con firmas validadas

## Señales prioritarias
- `HGF`
- `MET`
- `MYC`
- `SLC2A1`
- `HK2`
- `PGK1`
- `TPI1`
- `MCAM`
- `CXCL13`
- `BHLHE40`
- CAF/mCAF, EMT-like CAF, macrófagos lipídicos, T cells `CXCL13+`

## Próximo paso técnico
Extensión y validación cruzada:

1. Buscar anotaciones celulares o spatial externo para validar arquitectura, no promedio de muestra.
2. Explorar GSE231559 o scCRLM/Cancer Diversity Asia para una ruta cell-type/spatial manejable.
3. Reanalizar GSE225857 con nulos espaciales mas estrictos y/o regiones tumor-high/CAF-high.
4. Mantener META-PRISM y TCIA como lineas secundarias, no como prueba inmediata del mecanismo espacial.

## Cuidado epistemológico
Esta hipótesis es fuerte como programa de descubrimiento, no como afirmación clínica. Todavía no debemos decir que el eje es causal en pacientes ni que existe una intervención validada. La salida correcta por ahora es priorización de hipótesis y validación computacional reproducible.
