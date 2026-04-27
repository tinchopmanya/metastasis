# Plan de validación computacional para CRLM

Fecha: 2026-04-25 01:06:15 -03:00

## Estado técnico
Actualización: 2026-04-25 01:16:54 -03:00

Fase 1 iniciada y ejecutada con `scripts/prepare_signatures.py`.

Resultados:

- 7 firmas preparadas.
- 40 filas firma-gen normalizadas.
- 37 genes únicos.
- 0 advertencias de formato.
- Tabla normalizada generada en `data_manifest/generated/signatures_normalized.tsv`.
- Matriz gen-firma generada en `data_manifest/generated/signature_gene_matrix.tsv`.
- Reporte generado en `data_manifest/generated/signature_report.md`.

Siguiente paso técnico:

Crear un checker de disponibilidad de genes por dataset antes de puntuar firmas. El orden recomendado es GEO primero, TCGA después.

Implementación autónoma en curso:

- Crear `scripts/check_gene_availability.py`.
- Verificar todos los genes contra HGNC aprobado como control de nomenclatura.
- Preparar interfaz `--universe name=path` para agregar universos GEO/TCGA sin cambiar código.
- Registrar que `GSE225857` y `GSE226997` requieren extracción pesada antes de validación dataset-específica.

Resultado ejecutado: 2026-04-25 01:21:28 -03:00

- `scripts/check_gene_availability.py` creado y ejecutado.
- Universo `hgnc_approved` descargado desde HGNC/Google Cloud Storage.
- 44,982 símbolos HGNC aprobados cargados.
- 40 filas firma-gen evaluadas.
- 0 genes faltantes.
- Todas las firmas tienen 100% de cobertura contra HGNC aprobado.
- Reporte generado en `data_manifest/generated/gene_availability_report.md`.

Tercer avance técnico ejecutado: 2026-04-26

- `scripts/fetch_gdc_gene_universe.py` creado.
- El script consulta la API de GDC, descarga un único archivo STAR-Counts TSV (~4 MB) y extrae los gene symbols sin descargar matrices completas.
- Fallback automático a GENCODE v36 si GDC no responde.
- `data_manifest/gene_universes/` creado con README explicativo.
- Universo TCGA-COAD generado: 59,427 genes desde GDC STAR-Counts file `ff710149-0fc6-464a-93cb-e3b9bdcf3525`.
- TCGA-READ usa el mismo pipeline STAR/GENCODE v36, por lo que el universo génico es idéntico al de TCGA-COAD.
- `check_gene_availability.py` ejecutado con `--universe tcga_coad=data_manifest/gene_universes/tcga_coad_genes.txt`.
- Resultado: 7/7 firmas con 100% de cobertura contra TCGA-COAD.
- Resultado combinado: 0 genes faltantes en HGNC aprobado ni en TCGA-COAD.
- Las 7 firmas están listas para scoring en datos TCGA-COAD bulk.

Cuarto avance técnico ejecutado: 2026-04-26

- `scripts/score_signatures_bulk.py` creado (sin dependencias externas).
- Matriz de expresión TCGA-COAD descargada desde UCSC Xena: 20,530 genes x 329 muestras (log2 normalized, 16.7 MB comprimido).
- 37/37 genes de firma presentes en la matriz.
- Scores de firma calculados por muestra (z-score medio) para las 7 firmas.
- 22 correlaciones clave calculadas (gen-gen y score-gen).

Resultados principales de plausibilidad:

- `MET-MYC` gene correlation: r = 0.515, p < 1e-300 (fuerte, significativa). La señal más fuerte del eje.
- `MYC` vs score glycolysis: r = 0.422, p < 1e-300 (moderada, significativa).
- `MET` vs score glycolysis: r = 0.320, p = 1e-9 (moderada, significativa).
- `CAF score` vs `HGF`: r = 0.675, p < 1e-300 (fuerte). Señal CAF-HGF robusta.
- `HGF-MET` gene correlation: r = -0.08, no significativa. Esperable en señalización paracrina diluida en bulk.
- `score:hgf_met_axis` vs `score:myc_glycolysis_core`: r = 0.079, no significativa. El composite no predice glicólisis en bulk, pero MET solo sí.
- Reporte completo en `data_manifest/generated/tcga_coad_bulk_plausibility_report.md`.

Interpretación: el eje MET-MYC-glycolysis es plausible en bulk. La ausencia de correlación HGF-MET directa es consistente con señalización paracrina. La hipótesis sigue justificando inversión en validación single-cell.

Quinto avance técnico ejecutado: 2026-04-26

- Se descubrió que GSE225857 tiene archivos individuales accesibles por muestra (no solo el TAR de 607 MB).
- `gse225857_non_immune_meta.tsv` descargado (1.9 MB, 41,892 células).
- Análisis de composición celular ejecutado.

Resultados de composición (predicciones de la hipótesis vs datos):

- **MCAM+ CAFs enriquecidos en hígado**: CONFIRMADO (3,387 en LCT vs 692 en CCT, 83% en hígado, fold 2.86x).
- **Programas fibroblásticos distintos**: CONFIRMADO (CXCL14+ 94% en colon, MCAM+ 83% en hígado).
- **Subtipos tumorales hígado-específicos**: CONFIRMADO (Tu02_DEFA5 97% en hígado, fold 20.4x).
- Reporte: `data_manifest/generated/gse225857_composition_report.md`.
- Tabla: `data_manifest/generated/gse225857_cell_enrichment.tsv`.

Sexto avance técnico ejecutado: 2026-04-26

- Count matrix non-immune descargada (90 MB gz, 1.4 GB decompressed, 17,516 genes x 41,892 células).
- Extracción selectiva de 13 genes de interés directamente desde .gz (sin descomprimir los 1.4 GB completos).
- `scripts/validate_sc_expression.py` creado.
- Fix aplicado: cell IDs usan `.` en counts y `-` en metadata. 41,892/41,892 matched.

Resultados de expresión single-cell:

- **HGF en fibroblastos >> tumor**: CONFIRMADO. Fibroblast mean=0.674 (30.1%), Tumor mean=0.004 (0.3%). Ratio 168x.
- **MET en tumor >> fibroblastos**: CONFIRMADO. Tumor mean=0.399 (27.6%), Fibroblast mean=0.009 (0.7%). Ratio 44x.
- **MET-MYC en tumor**: CONFIRMADO. Pearson r=0.1438, n=23,954, p<1e-300.
- **MYC-glicólisis en tumor**: CONFIRMADO. MYC-PGK1 r=0.36, MYC-TPI1 r=0.42.
- **Patrón paracrino HGF→MET**: CONFIRMADO. Compartimentos no-solapantes a nivel single-cell.

Refinamiento: HGF no viene solo de MCAM+ CAFs. CXCL14+ fibroblasts tienen mayor expresión per-cell (mean 1.664), pero están 94% en colon. En hígado, PRELP+ (F01, 5,091 células) y MCAM+ (F02, 3,387 células) son los productores dominantes de HGF.

- Reporte: `data_manifest/generated/gse225857_sc_expression_report.md`.
- Tabla resumen: `data_manifest/generated/gse225857_gene_expression_summary.tsv`.
- Correlaciones: `data_manifest/generated/gse225857_sc_correlations.tsv`.

Siguiente paso técnico:

- Evaluar co-localización espacial mCAF-tumor si GSE225857 incluye coordenadas Visium/MERFISH.
- Cruzar resultados con META-PRISM para especificidad CRLM vs metástasis general.
- Buscar validación independiente en GSE226997 o datasets 2025.

Séptimo avance técnico ejecutado: 2026-04-27

- `scripts/analyze_gse225857_spatial.py` creado.
- GSE225857 spatial filelist revisado: 6 muestras Visium (`C1-C4`, `L1-L2`) con matrices individuales manejables.
- Se descargaron sólo `barcodes`, `features`, `matrix.mtx` y `tissue_positions`; se omitieron imágenes.
- 6 muestras analizadas, 22,260 spots in-tissue.
- Reporte: `data_manifest/generated/gse225857_spatial_report.md`.
- Tablas: `gse225857_spatial_sample_summary.tsv`, `gse225857_spatial_correlations.tsv`, `gse225857_spatial_adjacency.tsv`, `gse225857_spatial_spot_scores.tsv`.

Resultados espaciales principales:

- LCT `caf_score~MET` spot-level promedio r = 0.286.
- LCT `MYC~glycolysis_score` spot-level promedio r = 0.645.
- Vecinos de spots CAF alto tienen MET enriquecido sobre fondo en LCT: ratio medio 1.948.
- Vecinos de spots CAF alto también enriquecen MYC y glicólisis en LCT.
- Vecinos de spots HGF alto no enriquecen MET en LCT: ratio medio 0.844.

Interpretación:

- La lectura spatial apoya un nicho CAF-tumor, pero no un modelo simple de co-expresión `HGF~MET` en el mismo spot.
- El modelo queda refinado hacia un programa CAF compuesto: PRELP/MCAM fibroblasts y otros CAF states crean contexto espacial; MET+ tumor y MYC-glicólisis aparecen cerca de zonas CAF altas.
- El siguiente paso no es más descarga, sino síntesis: escribir el modelo refinado y después buscar validación externa en META-PRISM o datasets 2025.

Octavo avance técnico ejecutado: 2026-04-27

- `scripts/analyze_gse225857_spatial.py` extendido con prueba nula por permutaciones.
- Se agregaron argumentos `--permutations` y `--seed` para reproducibilidad.
- Se mantuvieron fijos los spots source-high, vecinos y fondo; se barajo el target dentro de cada muestra.
- Ejecucion principal: 500 permutaciones por combinacion muestra/fuente/target.
- Nueva tabla: `data_manifest/generated/gse225857_spatial_adjacency_permutation.tsv`.
- Reporte actualizado: `data_manifest/generated/gse225857_spatial_report.md`.

Resultados:

- L1 `CAF -> MET`: ratio observado 2.029, media nula 0.998, z 19.177, p empirico 0.002.
- L2 `CAF -> MET`: ratio observado 1.866, media nula 1.009, z 9.992, p empirico 0.002.
- L1/L2 `CAF -> MYC` y `CAF -> glycolysis_score`: p empirico 0.002 en todas las pruebas.
- L1 `HGF -> MET`: ratio 0.874, p empirico 0.994.
- L2 `HGF -> MET`: ratio 0.814, p empirico 0.936.

Decision:

- La hipotesis avanza, pero refinada.
- El foco tecnico pasa de `HGF` aislado a programa espacial `CAF-high`.
- La proxima validacion debe buscar reproducibilidad externa o especificidad CRLM, no acumular mas correlaciones internas del mismo dataset.

## Objetivo
Validar de forma liviana y reproducible si la hipótesis `mCAF-HGF-MET-MYC-glycolysis` merece seguir recibiendo prioridad.

## Preguntas testeables
- ¿`HGF` se concentra en CAF/mCAF?
- ¿`MET` se expresa en células tumorales receptoras?
- ¿`MET` se asocia con `MYC`?
- ¿`MYC` se asocia con glicólisis?
- ¿mCAF y High-M CRC co-localizan espacialmente?
- ¿La señal se observa en más de un dataset?

## Fase 1: preparación de firmas
Crear gene sets mínimos:

- `mCAF_signature`
- `HighM_CRC_signature`
- `HGF_MET_axis`
- `MYC_targets`
- `Glycolysis`
- `MCAM_CAF`
- `CXCL13_Tcell`
- `Lipid_macrophage`

Salida:

- `data_manifest/signatures.yml`
- tabla markdown de genes y fuente

## Fase 2: GEO ligero
Primero usar metadata y matrices accesibles:

- `GSE225857`
- `GSE226997`
- datasets del paper 2025 si están directamente disponibles

Análisis:

- score por célula/spot
- comparación primario vs metástasis
- correlación `MET-MYC`
- co-localización espacial si hay coordenadas

Salida:

- notebook o script reproducible
- reporte markdown con figuras o tablas

## Fase 3: validación bulk
Usar TCGA COAD/READ:

- correlación `MET-MYC`
- asociación score glicólisis con `MYC`
- score `High-M-like` en primarios
- asociación exploratoria con estadio/supervivencia si la metadata lo permite

Limitación:

TCGA no prueba CRLM; sólo aporta señal de plausibilidad.

## Fase 4: validación metastásica externa
Usar META-PRISM u otra cohorte metastásica accesible:

- distinguir señal de metástasis hepática versus metástasis general
- comparar CRC con otros tumores metastásicos
- ver si el eje aparece en tumores refractarios

## Fase 5: TCIA como puente clínico
No descargar imágenes todavía salvo que el análisis molecular dé señales fuertes.

Cuando toque:

- usar dataset CRLM de 197 pacientes
- empezar por metadata clínica
- modelar recurrencia/supervivencia con baseline simple
- considerar radiomics sólo después

## Criterios de avance
La hipótesis avanza si:

- aparece en al menos dos fuentes independientes
- tiene separación primario/metástasis o nicho tumoral/estromal
- tiene lectura espacial o celular clara
- no depende de un único gen aislado

La hipótesis baja prioridad si:

- no hay reproducibilidad
- sólo aparece por batch o composición celular
- no hay célula emisora/receptora plausible
- no hay conexión con agresividad, recurrencia, plasticidad o metabolismo

## Próximo artefacto técnico
Crear:

- `data_manifest/`
- `scripts/`
- `scripts/prepare_signatures.ps1` o un script Python/R si se decide análisis real
- `data_manifest/crlm_sources.md`

La primera ejecución técnica debe ser pequeña: metadata, gene sets y manifest. Nada pesado todavía.
