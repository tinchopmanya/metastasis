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

Noveno avance tecnico ejecutado: 2026-04-27

- `scripts/analyze_tcga_coad_clinical.py` creado.
- Se descargo/uso UCSC Xena `TCGA.COAD.sampleMap/COAD_clinicalMatrix`.
- Se unieron 329 muestras con `tcga_coad_signature_scores.tsv`.
- Se evaluaron estadio avanzado, M positivo, N positivo, invasion linfatica, invasion venosa y supervivencia global.

Resultados:

- `mcam_caf` en N positivo vs N0: diferencia media 0.332, p = 6.95e-04.
- `caf_core` en N positivo vs N0: diferencia media 0.301, p = 8.57e-04.
- `mcam_caf` en invasion linfatica positiva: diferencia media 0.358, p = 1.15e-03.
- `caf_core` en invasion linfatica positiva: diferencia media 0.312, p = 2.27e-03.
- Supervivencia por mediana: `caf_core` p = 0.020, `mcam_caf` p = 0.027.
- `caf_met_myc_glycolysis_composite` no fue significativo en supervivencia bulk: p = 0.493.

Decision:

- El componente `CAF-high/MCAM` sube prioridad.
- El eje completo debe seguir analizandose como mecanismo espacial dependiente de contexto.
- TCGA-COAD aporta plausibilidad clinica, no validacion CRLM.

Decimo avance tecnico ejecutado: 2026-04-27

- `scripts/triage_geo_external_validation.py` creado para evitar descargas pesadas sin plan.
- `GSE234804` priorizado como mejor ruta externa inmediata por H5Seurat individuales CRC/LM.
- `scripts/validate_gse234804_h5seurat.py` creado.
- Se usaron `h5py` y `numpy` para leer H5Seurat desde Python.
- Se procesaron 3 CRC y 6 LM de GSE234804, excluyendo `PC*`.
- Tablas: `gse234804_sample_signature_scores.tsv`, `gse234804_lm_vs_crc_comparisons.tsv`.
- Reporte: `gse234804_external_validation_report.md`.

Resultado:

- `score_mcam_caf`: LM 0.057 vs CRC 0.103.
- `score_caf_core`: LM 0.046 vs CRC 0.065.
- `score_myc_glycolysis_core`: LM 2.109 vs CRC 3.312.
- `MET`: LM 0.341 vs CRC 0.236.
- `HGF`: LM 0.014 vs CRC 0.011.

Decision:

- GSE234804 no valida el modelo como firma sample-level LM-vs-CRC.
- Este resultado fuerza a mantener la hipotesis como arquitectura espacial/cell-state-specific.
- La siguiente validacion debe tener anotaciones celulares o coordenadas; no alcanza con promedios por muestra.

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

## Fase 6: validacion espacial del modelo en capas 2026

Actualizacion: 2026-04-27 16:22:03 -03:00

La literatura 2026 cambia la proxima validacion. Ya no basta con repetir `CAF -> MET/MYC/glycolysis`; ahora hay que testear si el mismo nicho `CAF-high` contiene o bordea una capa inmunosupresora mieloide/T-cell.

Firmas agregadas para esta fase:

- `spp1_cxcl12_caf_myeloid_axis`
- `spp1_macrophage_fads1_pdgfb_axis`
- `hla_drb5_macrophage_axis`
- `stromal_myeloid_risk_2026`
- `sema3c_nrp2_lmic_axis`
- `crlm_metabolic_vulnerabilities_2026`
- `radioresistance_morf4l1`
- `marco_cash_macrophage_axis`
- `glut1_invasive_margin_axis`

Preguntas testeables:

- Los spots `CAF-high` tienen vecinos altos en `SPP1/CXCL12/MIF/CD44/FN1`?
- Los scores mieloides `SPP1/HLA-DRB5` aparecen junto a `MET/MYC/glycolysis` o en una capa separada?
- El score `stromal_myeloid_risk_2026` se ubica en interfaz tumor-estroma?
- El componente `SLC2A1/GLUT1` se comporta como tumor-core, immune-margin o ambos?
- Las firmas metabolicas 2026 (`SHMT1`, `PIM/NDRG1`, etc.) se asocian con tumor `MET/MYC` o con otro compartimento?

Analisis recomendado:

1. Extender `scripts/analyze_gse225857_spatial.py` para aceptar firmas dinamicas desde `signatures_normalized.tsv`.
2. Calcular scores por spot para las nuevas firmas.
3. Reutilizar el modulo de vecindad/permutaciones con fuentes `CAF-high`, `SPP1/CXCL12-high`, `HLA-DRB5-high` y targets `MET`, `MYC`, `glycolysis`, `CD8/T`.
4. Exportar tabla de resultados por muestra y un reporte markdown.
5. Si el patron sale fuerte, buscar dataset spatial externo; si sale debil, documentar falsacion parcial.

Criterio de avance:

La hipotesis avanza si las nuevas firmas muestran estructura espacial no aleatoria y consistente con capas o interfaces. Baja prioridad si las senales son solo composicion celular global, batch o ruido de genes muy escasos.

Nota historica: la primera ejecucion tecnica ya fue completada con metadata, gene sets y manifest; mantener la misma filosofia de validacion liviana antes de descargar datos pesados.

## Fase 6A completada: primera pasada espacial 2026

Actualizacion: 2026-04-27 16:50:00 -03:00

Se ejecuto la fase 6A con `scripts/analyze_gse225857_spatial_2026.py`.

Resultado:

- 22,260 spots Visium scoreados.
- 17 firmas 2026 evaluadas, incluyendo controles desolapados.
- 500 permutaciones por prueba en LCT.
- `CAF -> SPP1/CXCL12` y `CAF -> HLA-DRB5-like` positivos en L1/L2.
- `SPP1/CXCL12 -> MYC/glycolysis` y `HLA-DRB5-like -> MYC/glycolysis` positivos en L1/L2.

Siguiente fase:

1. Profundizar la rama `SPP1/CXCL12-lite`, que sobrevivio al control desolapado.
2. Refinar la rama `HLA-DRB5-lite`, que quedo lesion-dependiente.
3. Agregar controles negativos o targets no relacionados.
4. Evaluar deconvolucion espacial si hay marcadores suficientes.
5. Buscar validacion espacial externa.

## Fase 6B completada: validacion externa paired y spatial

Actualizacion: 2026-04-27 17:53:00 -03:00

Se ejecutaron dos validaciones externas:

- `scripts/validate_gse245552_paired_scrna.py`
- `scripts/validate_gse217414_spatial_external.py`

GSE245552 paired scRNA:

- 39 muestras procesadas.
- 13 pares primario/metastasis hepatica utiles.
- `myeloid SPP1/CXCL12-lite`: ratio LM/primario 1.844, p = 1.34e-04, 13/13 pares positivos.
- `myeloid HLA-DRB5-lite`: ratio 1.478, p = 1.72e-03, 12/13 pares positivos.
- `CAF SPP1/CXCL12-lite`: ratio 1.361, p = 0.0307, 11/13 pares positivos.
- `tumor MYC/glycolysis-lite`: ratio 0.967, p = 0.692, 5/13 pares positivos.

GSE217414 external spatial:

- 4 CRLM Visium sections.
- 10,674 spots in-tissue.
- 500 permutaciones por test.
- `CAF -> SPP1/CXCL12-lite`: ratio medio 1.346, positivo 4/4.
- `CAF -> HLA-DRB5-lite`: ratio medio 1.391, positivo 4/4.
- `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: ratio medio 1.776, positivo 4/4.
- `HLA-DRB5-lite -> MYC/glycolysis-lite`: ratio medio 1.467, positivo 4/4.

Decision:

La validacion externa apoya una historia de nicho local estromal-mieloide-metabolico. El siguiente paso no debe ser sumar mas datasets sin controles, sino endurecer la evidencia existente.

## Fase 6C siguiente: controles paper-grade

Objetivo:

Probar si el patron es especifico del modelo o si solo refleja autocorrelacion espacial/alta expresion regional.

Tareas:

1. Agregar firmas negativas emparejadas por tamano y nivel de expresion.
2. Agregar genes housekeeping y targets no relacionados como controles.
3. Implementar permutaciones estratificadas por bins de UMI/expresion total o regiones espaciales.
4. Consolidar GSE225857 y GSE217414 en una tabla unica de efectos por muestra.
5. En GSE245552, pasar de proxies marker-based a pseudobulk por anotacion celular curada.

## Fase 6C parcial ejecutada: auditoria inicial y nulo por bloques

Actualizacion: 2026-04-29 02:47:00 -03:00

Se lanzaron dos agentes:

- Investigador web/literatura/datasets.
- Auditor metodologico.

Conclusiones de agentes:

- No hay novedad en genes sueltos; la novedad posible es una arquitectura multi-dataset local y metabolica.
- El nulo global era debil y habia circularidad/leakage en firmas/proxies.
- Prioridad tecnica: controles negativos, nulos espaciales mas duros, spFBA/lactate consumption y pseudobulk real.

Scripts nuevos:

- `scripts/consolidate_spatial_niche_effects.py`
- `scripts/audit_spatial_signature_specificity.py`
- `scripts/audit_spatial_block_permutation.py`

Resultados:

- Consolidacion bruta: 7/7 efectos positivos en 6/6 muestras spatial.
- Ablacion/random controls: los efectos sobreviven ablacion, pero no superan random controls dentro del panel extraido.
- Nulo por bloques: `SPP1/CXCL12-lite -> MYC/glycolysis-lite` sobrevive 6/6; `HLA-DRB5-lite -> MYC/glycolysis-lite` sobrevive 5/6; `CAF -> MET` sobrevive solo 2/6.

Decision:

- Bajar prioridad de `CAF -> MET` como claim central.
- Mantener como eje lider `stromal/myeloid-like regions -> MYC/glycolysis local adjacency`.
- Renombrar con cuidado `SPP1/CXCL12-lite`: la firma desolapada debe describirse como `CXCL12/FN1/CD44/HIF1A/CTNNB1-like` hasta validar SPP1 directamente.

## Fase 6D siguiente: controles de reviewer hostil

Objetivo:

Convertir controles iniciales en controles paper-grade.

Tareas:

1. Construir random controls desde universo full-transcriptome de cada spatial dataset.
2. Repetir nulo por bloques con varios tamanos: 8, 12, 16, 20.
3. Residualizar scores por profundidad/UMI y coordenadas.
4. Hacer leave-one-gene-out formal por firma.
5. Probar spFBA/lactate consumption 2026 como puente metabolico.
6. Rehacer paired scRNA con anotacion celular/pseudobulk para eliminar leakage de proxies.

## Fase 6E abierta: puente HLA-DRB5/lactato-pyruvato

Actualizacion: 2026-04-29 02:58:54 -03:00

Se ejecuto un primer screen proxy del puente metabolico recomendado por los agentes:

```powershell
python scripts/analyze_spatial_lactate_axis.py --permutations 500 --block-size 12
```

Objetivo:

Probar si vecindarios `HLA-DRB5-like` o `CXCL12/FN1/CD44-like` se asocian espacialmente con proxies de lactate import/anabolism, pyruvate mitochondrial entry y glutamate transamination.

Resultado:

- `HLA-DRB5-like -> glutamate_transamination`: 6/6 positivo, 5/6 sobrevive nulo por bloques, ratio medio 1.764.
- `HLA-DRB5-like -> pyruvate_mito_entry`: 6/6 positivo, 5/6 sobrevive, ratio medio 1.571.
- `HLA-DRB5-like -> lactate_import_anabolic`: 6/6 positivo, 4/6 sobrevive, ratio medio 1.564.
- `CXCL12/FN1/CD44-like` muestra ratios altos pero menor supervivencia bajo bloques, sugiriendo gradiente regional amplio.

Decision:

La hipotesis mas prometedora se estrecha a:

`HLA-DRB5-like immune-metabolic niches may mark non-canonical lactate/pyruvate carbon routing in CRLM.`

Siguiente validacion dura:

1. Conseguir o reconstruir mapas spFBA/FES para lactate uptake, pyruvate/transamination y reductive TCA.
2. Testear si los vecinos de `HLA-DRB5-like` predicen esos FES.
3. Residualizar por UMI, coordenadas, region histologica y tumor/stroma/hepatocyte score.
4. Generar random controls full-transcriptome para proxies metabolicos.
5. Leave-one-gene-out para `MPC1`, `MPC2`, `PDHA1`, `PDHB`, `GOT1`, `GOT2`, `GLUD1`, `GLS`.
