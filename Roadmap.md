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

Próximo avance técnico pendiente:

- Descargar count matrix non-immune (86 MB) con `python scripts/download_gse225857.py --non-immune`.
- Validar expresión celular HGF→mCAF, MET→tumor.
- Evaluar correlación MET-MYC dentro del compartimento tumoral.

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
- No descargaría imágenes pesadas antes de tener clara la hipó