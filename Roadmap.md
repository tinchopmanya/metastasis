# Roadmap de investigación: metástasis

Fecha: 2026-04-25 00:53:22 -03:00

## Modo autónomo activo
Actualización: 2026-04-25 01:06:15 -03:00

El proyecto entra en modo de avance autónomo. La línea activa queda fijada como ola 003:

`CAFs/mCAFs hepáticos -> HGF-MET -> MYC/glicólisis -> plasticidad tumoral e inmunomodulación en CRLM`

La prioridad inmediata ya no es decidir qué investigar, sino construir evidencia organizada alrededor de esa hipótesis. El trabajo se ejecuta en este orden:

1. Abrir la ola 003 en `Investigacion.md`, `InvestigacionMapa.md` y `Conlusion.md`.
2. Crear la investigación extensa del nicho metastásico hepático.
3. Crear una matriz de hipótesis priorizadas.
4. Crear un mapa de datasets y señales.
5. Crear un plan de validación computacional.
6. Versionar y subir los avances.

Primer objetivo operativo:

Convertir la hipótesis `mCAF-HGF-MET-MYC-glycolysis` en una hipótesis testeable, con evidencia, datasets, genes, células, predicciones y criterios de falsación.

Primer avance técnico ejecutado:

- `scripts/prepare_signatures.py` creado.
- `data_manifest/generated/signatures_normalized.tsv` generado.
- `data_manifest/generated/signature_gene_matrix.tsv` generado.
- `data_manifest/generated/signature_report.md` generado.
- La preparación inicial de firmas queda sin advertencias.

Segundo avance técnico ejecutado:

- `scripts/check_gene_availability.py` creado.
- `data_manifest/generated/hgnc_approved_symbols.tsv` generado.
- `data_manifest/generated/gene_availability.tsv` generado.
- `data_manifest/generated/gene_availability_report.md` generado.
- Todas las firmas tienen 100% de cobertura contra HGNC aprobado.
- `GSE225857` y `GSE226997` quedan marcados como fuentes que requieren extracción pesada antes de validación dataset-específica.

Tercer avance técnico ejecutado:

- `scripts/fetch_gdc_gene_universe.py` creado: consulta GDC API, descarga un único archivo STAR-Counts TSV y extrae el universo génico.
- `data_manifest/gene_universes/` creado con README y `tcga_coad_genes.txt` (59,427 genes).
- Fuente: archivo STAR-Counts `ff710149-0fc6-464a-93cb-e3b9bdcf3525` de TCGA-COAD via GDC.
- TCGA-READ comparte el mismo pipeline STAR/GENCODE v36; universo génico idéntico.
- `check_gene_availability.py` ejecutado contra HGNC aprobado y TCGA-COAD simultáneamente.
- Resultado: 7/7 firmas, 37/37 genes, 100% cobertura en ambos universos. 0 genes faltantes.
- Las firmas están técnicamente listas para scoring en datos TCGA-COAD bulk.

Cuarto avance técnico ejecutado:

- `scripts/score_signatures_bulk.py` creado.
- Matriz TCGA-COAD descargada desde UCSC Xena (20,530 genes x 329 muestras).
- 7 firmas scored, 22 correlaciones calculadas.
- Resultado clave: `MET-MYC` r = 0.515 (fuerte, significativa), `MYC-glycolysis` r = 0.422, `CAF-HGF` r = 0.675.
- `HGF-MET` r = -0.08 (no significativa): consistente con señalización paracrina.
- Conclusión: el eje es plausible en bulk. Justifica validación single-cell.
- Reporte completo en `data_manifest/generated/tcga_coad_bulk_plausibility_report.md`.

Quinto avance técnico ejecutado:

- GSE225857 tiene archivos individuales por muestra (no requiere el TAR de 607 MB).
- Metadata non-immune descargada (1.9 MB, 41,892 células con anotación de cell type).
- Composición celular analizada: MCAM+ CAFs 83% en hígado (fold 2.86x), CXCL14+ fibroblasts 94% en colon.
- Tu02_DEFA5 es 97% hígado-específico (fold 20.4x).
- Scripts creados: `analyze_gse225857_cellcomp.py`, `download_gse225857.py`.
- Hipótesis MCAM+ CAFs liver-enriched: CONFIRMADA.

Sexto avance técnico ejecutado:

- Count matrix non-immune descargada y parseada (90 MB comprimido, 1.4 GB descomprimido, 17,516 genes x 41,892 células).
- 13/13 genes de interés encontrados en la matriz.
- `scripts/validate_sc_expression.py` creado.
- Validación single-cell ejecutada contra las tres preguntas centrales:

Resultado 1 — HGF en fibroblastos:

- HGF mean en fibroblastos: 0.674 (30.1% expressing). En tumor: 0.004 (0.3%). Ratio 168x. CONFIRMADO.
- Dentro de fibroblastos: CXCL14+ tiene mayor expresión per-cell (mean 1.664), pero MCAM+ CAFs son la fuente dominante en hígado por abundancia (3,387 células en LCT, mean 0.371).

Resultado 2 — MET en tumor:

- MET mean en tumor: 0.399 (27.6% expressing). En fibroblastos: 0.009 (0.7%). Ratio 44x. CONFIRMADO.
- Patrón paracrino HGF(estroma)→MET(tumor) validado a nivel single-cell.

Resultado 3 — MET-MYC en tumor:

- Pearson r = 0.1438 en 23,954 células tumorales (p < 1e-300). CONFIRMADO (débil pero robustamente significativo).
- MYC-PGK1 r = 0.36, MYC-TPI1 r = 0.42: el eje MYC-glicólisis es el enlace más fuerte.

Reporte completo en `data_manifest/generated/gse225857_sc_expression_report.md`.

Conclusión de validación single-cell:

Las 5 predicciones de expresión de la hipótesis se confirman:
1. HGF en fibroblastos >> tumor (168x).
2. MET en tumor >> fibroblastos (44x).
3. MET-MYC correlación positiva en tumor (r=0.14, p<1e-300).
4. MYC-glicólisis fuerte en tumor (MYC-TPI1 r=0.42).
5. Patrón paracrino no-solapante confirmado.

Próximo avance técnico pendiente:

- Evaluar co-localización espacial mCAF-tumor si hay datos de coordenadas en GSE225857.
- Cruzar con META-PRISM para verificar especificidad CRLM vs metástasis general.
- Considerar validación en dataset independiente (GSE226997 o papers 2025).

Séptimo avance técnico ejecutado:

- `scripts/analyze_gse225857_spatial.py` creado y ejecutado.
- 6 muestras Visium de GSE225857 procesadas (`C1-C4`, `L1-L2`), 22,260 spots.
- Se descargaron matrices y coordenadas, sin imágenes.
- En LCT: `caf_score~MET` promedio r = 0.286.
- En LCT: `MYC~glycolysis_score` promedio r = 0.645.
- Vecinos de CAF alto tienen MET casi 2x sobre fondo en LCT (ratio 1.948).
- Vecinos de HGF alto no enriquecen MET (ratio 0.844).

Lectura estratégica:

La hipótesis se fortalece, pero se refina. No conviene seguir diciendo "HGF solo explica el nicho". La señal fuerte es un programa CAF espacial compuesto, donde CAF alto predice proximidad a MET/MYC/glicólisis. HGF sigue siendo parte del mecanismo, pero no captura por sí solo toda la arquitectura espacial.

Octavo avance técnico ejecutado:

- `scripts/analyze_gse225857_spatial.py` extendido con permutaciones espaciales.
- Nueva salida: `data_manifest/generated/gse225857_spatial_adjacency_permutation.tsv`.
- Reporte espacial actualizado con seccion de permutaciones.
- En LCT, `CAF -> MET` supera el nulo en L1 y L2: ratios 2.029 y 1.866, p empirico 0.002 en ambas muestras.
- En LCT, `CAF -> MYC` y `CAF -> glycolysis_score` tambien superan el nulo con p empirico 0.002.
- En LCT, `HGF -> MET` no supera el nulo: ratios 0.874 y 0.814, p empirico 0.994 y 0.936.

Lectura estrategica:

El resultado mejora la calidad de la evidencia porque compara contra una redistribucion aleatoria dentro de muestra. La apuesta actual debe ser `CAF-high spatial niche`, no `HGF` como marcador unico. El siguiente avance con mayor retorno es validacion independiente o especificidad CRLM/metastasis general.

Noveno avance tecnico ejecutado:

- `scripts/analyze_tcga_coad_clinical.py` creado.
- Clinica TCGA-COAD descargada desde UCSC Xena `COAD_clinicalMatrix`.
- 329 muestras unidas con scores de firmas.
- Nuevas salidas: `tcga_coad_clinical_signature_associations.tsv`, `tcga_coad_signature_survival.tsv`, `tcga_coad_clinical_association_report.md`.
- `mcam_caf` y `caf_core` se asocian con N positivo, invasion linfatica y estadio avanzado.
- `caf_core` alto y `mcam_caf` alto muestran peor supervivencia exploratoria por mediana.
- El composite completo `CAF/MET/MYC/glicolisis` no es significativo en supervivencia bulk.

Lectura estrategica:

El componente `CAF-high/MCAM` tiene una sombra clinica en primarios TCGA-COAD. Eso fortalece el foco en CAF/MCAM, pero tambien advierte que el mecanismo completo no debe venderse como biomarcador bulk lineal. La proxima prioridad sigue siendo especificidad metastasica externa.

Decimo avance tecnico ejecutado:

- `scripts/triage_geo_external_validation.py` creado.
- Se hizo triage de `GSE225857`, `GSE226997`, `GSE231559`, `GSE234804` y `GSE178318`.
- `GSE234804` quedo como mejor candidato externo inmediato: 13 H5Seurat individuales, 568.8 MB total.
- `scripts/validate_gse234804_h5seurat.py` creado.
- Se procesaron 9 muestras externas: 3 CRC y 6 LM, 32,435 celulas.
- Resultado: `mcam_caf`, `caf_core` y `myc_glycolysis_core` no aumentan en LM a nivel muestra.
- `MET` sube modestamente en LM, pero sin soporte fuerte; `HGF` permanece muy bajo.

Lectura estrategica:

GSE234804 no confirma la hipotesis como firma sample-level. Esto no mata el modelo espacial, pero lo estrecha: si hay aporte importante, esta en la organizacion local/celular, no en un promedio global LM-vs-CRC. Proxima prioridad: validacion externa con cell-type labels o spatial real.

## Decisión estratégica
La dirección más prometedora ahora no es seguir ampliando el panorama general de metástasis. Ya hay suficiente señal para avanzar con una línea concreta:

`cáncer colorrectal -> metástasis hepática -> nicho metastásico hepático`

La meta de las próximas horas debe ser producir algo verificable: una matriz de hipótesis, datasets, señales moleculares/celulares y rutas de validación. La pregunta no es "qué es la metástasis", sino:

Qué estados celulares e interacciones del microambiente hepático hacen que una metástasis colorrectal pueda colonizar, resistir tratamiento y recurrir.

## Por qué esta línea
- Tiene alto impacto clínico.
- Tiene datasets públicos útiles: TCIA, GEO, TCGA/GDC, META-PRISM, scRNA-seq y spatial.
- Tiene señales recientes concretas: `HGF-MET-MYC-glycolysis`, fibroblastos metastásicos, macrófagos, estados T `CXCL13+`, metabolismo lipídico, EMT/plasticidad.
- Permite que agentes de IA aporten de verdad: leer papers, cruzar datasets, detectar convergencias, construir hipótesis y proponer validaciones.

## Qué haría ahora
Haría una ola 003 con foco estrecho:

`InvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`

El objetivo no sería escribir otro resumen bonito, sino construir una base de trabajo accionable:

- hipótesis priorizadas
- evidencia a favor y en contra
- datasets donde probar cada hipótesis
- biomarcadores o genes candidatos
- rutas de validación computacional
- riesgos metodológicos

## Entregables de las próximas horas

### 1. Matriz de hipótesis
Archivo sugerido:

`HipotesisNichoMetastaticoCRLM.md`

Columnas o secciones:

- hipótesis
- mecanismo propuesto
- células implicadas
- genes/vías
- evidencia principal
- datasets donde se puede validar
- nivel de novedad
- riesgo de sesgo
- próximo experimento computacional

Hipótesis candidatas iniciales:

- `HGF-MET-MYC-glycolysis`: CAFs y tumor cooperan metabólicamente en nichos espaciales.
- `MCAM+ CAFs`: fibroblastos metastásicos podrían modular estados T vía señalización Notch.
- `CXCL13+ T cells`: subpoblaciones T enriquecidas en metástasis hepática podrían marcar nichos inmunes específicos.
- `macrófagos y metabolismo lipídico`: heterogeneidad mieloide vinculada a progresión y soporte hepático.
- `BHLHE40/EMT`: plasticidad y transición fenotípica como programa metastásico.
- `firma temprana del primario`: señal de tropismo hepático ya presente antes de la metástasis visible.

### 2. Mapa de datasets
Archivo sugerido:

`DatasetsCRLM.md`

Contenido:

- `GSE225857`: single-cell y spatial de CRC primario y metástasis hepática.
- `TCIA Colorectal-Liver-Metastases`: CT, segmentaciones, clínica y supervivencia en 197 pacientes.
- `TCGA COAD/READ`: baseline multi-omics de tumor primario.
- `META-PRISM`: cohorte metastásica pan-cáncer con hígado como sitio frecuente de biopsia.
- `scCRLM`: recurso espacial usado en artículos recientes.
- `PDMR/HCMI/organoides`: puente hacia validación preclínica.

### 3. Tabla de señales priorizadas
Archivo sugerido:

`SenalesPrioritariasCRLM.md`

Señales iniciales:

- `HGF`
- `MET`
- `MYC`
- genes de glicólisis: `SLC2A1`, `PGK1`, `TPI1`
- `MCAM`
- genes T `CXCL13+`
- marcadores CAF/mCAF
- marcadores macrófago/lípidos
- `BHLHE40`
- ejes `TGF-beta`, `KRAS`, fibrosis, matriz extracelular

### 4. Plan de validación computacional
Archivo sugerido:

`PlanValidacionCRLM.md`

Validaciones posibles:

- comprobar si los genes/vías aparecen en múltiples papers y datasets
- validar firmas en TCGA COAD/READ como señal temprana o pronóstica
- cruzar con META-PRISM para distinguir señal específica de CRLM versus metástasis general
- usar TCIA para preguntar si señales biológicas se conectan con recurrencia/supervivencia por imagen
- cruzar con organoides/PDMR/HCMI para priorizar targets más plausibles

## Orden recomendado de trabajo

### Bloque 1: dos a tres horas
Crear la matriz de hipótesis y datasets. Este es el bloque de mayor retorno porque convierte literatura dispersa en una base de decisión.

Resultado esperado:

- `HipotesisNichoMetastaticoCRLM.md`
- `DatasetsCRLM.md`
- actualización de `Conlusion.md`

### Bloque 2: tres a seis horas
Profundizar en las tres hipótesis más fuertes. Para cada una:

- paper principal
- evidencia independiente
- genes centrales
- células implicadas
- qué dataset permite probarla
- qué resultado computacional la fortalecería o debilitaría

Resultado esperado:

- `InvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`
- `ResumenInvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`

### Bloque 3: seis a doce horas
Empezar trabajo técnico. Prioridad conservadora:

1. Descargar metadata y tablas disponibles.
2. Construir manifest de datasets.
3. Preparar scripts de análisis exploratorio.
4. Intentar una primera validación de firmas en datos públicos accesibles.

Resultado esperado:

- carpeta `data_manifest/`
- carpeta `scripts/`
- primer script reproducible de extracción/validación
- un reporte de hallazgos y bloqueos

### Bloque 4: línea técnica paralela
Usar TCIA para recurrencia post-hepatectomía. Esta línea es valiosa, pero la pondría como segunda prioridad porque se vuelve más pesada en datos e infraestructura.

Resultado esperado:

- manifest del dataset TCIA
- revisión del paper base
- plan de pipeline radiomics/deep learning

## Qué no haría todavía
- No intentaría prometer descubrimiento clínico.
- No descargaría imágenes pesadas antes de tener clara la hipótesis.
- No haría un modelo predictivo primero si todavía no sabemos qué queremos validar.
- No abriría diez tipos de cáncer a la vez.
- No convertiría esto en una lista gigante de genes sin mecanismo.

## Mi apuesta concreta
Si tengo varias horas para avanzar, empezaría por una ola 003 y construiría una matriz de hipótesis del nicho metastásico hepático.

La hipótesis que hoy parece más fuerte como punto de partida es:

`CAFs/mCAFs en el hígado crean nichos metabólicos e inmunomoduladores que favorecen células tumorales colorrectales de alta plasticidad, con señalización HGF-MET, activación MYC y glicólisis local.`

Por qué esta hipótesis:

- es concreta
- conecta célula tumoral y microambiente
- tiene soporte single-cell y spatial reciente
- se puede validar con datasets públicos
- apunta a mecanismos, no sólo predicción

## Próxima acción recomendada
Abrir la ola 003:

`nicho metastásico hepático en cáncer colorrectal`

Primeros archivos a crear:

- `InvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`
- `ResumenInvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`
- `HipotesisNichoMetastaticoCRLM.md`
- `DatasetsCRLM.md`

## Fuentes clave para arrancar
- GSE225857: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857
- Single-cell and spatial transcriptome analysis of liver metastatic colorectal cancer: https://pmc.ncbi.nlm.nih.gov/articles/PMC10275599/
- Spatially resolved single-cell landscape with HGF-MET-MYC-glycolysis axis: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
- TCIA Colorectal-Liver-Metastases: https://www.cancerimagingarchive.net/collection/colorectal-liver-metastases/
- Preoperative CT and survival data for CRLM: https://pmc.ncbi.nlm.nih.gov/articles/PMC10847495/
- NCI PDQ Colon Cancer Treatment: https://www.cancer.gov/types/colorectal/hp/colon-treatment-pdq
- SEER Colorectal Cancer Stat Facts: https://seer.cancer.gov/statfacts/html/colorect.html
- AI in CRLM review: https://pubmed.ncbi.nlm.nih.gov/40240167/

## Undecimo avance tecnico ejecutado

Actualizacion: 2026-04-27 16:22:03 -03:00

- `scripts/search_pubmed_crlm_latest.py` creado y robustecido con reintentos/lotes chicos para PubMed E-utilities.
- Se genero `data_manifest/generated/pubmed_crlm_latest_2025_2026.tsv`.
- Se genero `data_manifest/generated/pubmed_crlm_latest_2025_2026_report.md`.
- Snapshot: 185 PMIDs unicos detectados, 184 con detalle recuperado.
- Tags dominantes: `immune_myeloid` 88, `glycolysis_metabolism` 87, `therapy_resistance` 72, `single_cell` 55, `hgf_met_myc` 27, `caf` 25, `spatial` 22.
- La literatura 2026 empuja el foco hacia `SPP1/CXCL12`, macrofagos `SPP1+`/`HLA-DRB5+`, T-cell exclusion/exhaustion, metabolismo de carbono y respuestas terapeuticas.
- Se crearon `InvestigacionSobreLiteratura2026NichoCRLM.md` y `ResumenInvestigacionSobreLiteratura2026NichoCRLM.md`.
- `data_manifest/signatures.yml` fue ampliado con firmas 2026 para la proxima pasada espacial.

Lectura estrategica nueva:

`HGF-MET-MYC-glycolysis` sigue como rama metabolica tumoral, pero el roadmap pasa a un modelo `CAF-high layered niche`.

Proximo bloque autonomo:

1. Regenerar firmas y disponibilidad.
2. Reanalizar GSE225857 spatial con scores 2026.
3. Probar si los nichos `CAF-high` separan o acoplan una interfaz metabolica tumoral y una interfaz inmunosupresora mieloide/T-cell.
4. Solo despues buscar validacion espacial externa.

## Duodecimo avance tecnico ejecutado

Actualizacion: 2026-04-27 16:50:00 -03:00

- `scripts/analyze_gse225857_spatial_2026.py` creado.
- Se reutilizaron los archivos Visium de GSE225857.
- 6 muestras procesadas, 22,260 spots in-tissue.
- 17 firmas 2026 scoreadas por spot, incluyendo controles desolapados.
- 500 permutaciones por prueba en LCT.
- Nuevas salidas:
- `data_manifest/generated/gse225857_spatial_2026_signature_availability.tsv`
- `data_manifest/generated/gse225857_spatial_2026_spot_scores.tsv`
- `data_manifest/generated/gse225857_spatial_2026_correlations.tsv`
- `data_manifest/generated/gse225857_spatial_2026_adjacency_permutation.tsv`
- `data_manifest/generated/gse225857_spatial_2026_report.md`
- Documento nuevo: `InvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md`.
- Resumen nuevo: `ResumenInvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md`.

Resultado clave:

- `CAF -> SPP1/CXCL12`: ratio medio LCT 1.509, p empirico 0.002 en L1/L2.
- `CAF -> HLA-DRB5-like`: ratio medio LCT 1.484, p empirico 0.002 en L1/L2.
- `SPP1/CXCL12 -> MYC/glycolysis`: ratio medio LCT 1.755, p empirico 0.002 en L1/L2.
- `HLA-DRB5-like -> MYC/glycolysis`: ratio medio LCT 1.556, p empirico 0.002 en L1/L2.

Lectura estrategica:

El proyecto ya tiene una primera evidencia propia que conecta el frente 2026 con el resultado espacial anterior. No es causalidad ni capa celular fina; es un macro-nicho `CAF-high` con acoplamiento estromal-inmune-metabolico. El siguiente avance debe ser endurecer la prueba: firmas desolapadas, deconvolucion o validacion espacial externa.

Control desolapado agregado:

- Se agregaron `caf_core_desoverlap_2026`, `spp1_cxcl12_axis_desoverlap_2026`, `hla_drb5_macrophage_axis_desoverlap_2026` y `myc_glycolysis_desoverlap_2026`.
- El control mantiene fuerte la rama `SPP1/CXCL12-lite`: `CAF -> SPP1/CXCL12-lite` ratio medio 1.513; `SPP1/CXCL12-lite -> MYC/glycolysis-lite` ratio medio 1.602.
- La rama `HLA-DRB5-lite` se debilita y queda lesion-dependiente: fuerte en L1, debil/marginal en L2.
- Decision: priorizar `SPP1/CXCL12` como eje 2026 robusto; mantener `HLA-DRB5` como candidato secundario hasta nueva validacion.
