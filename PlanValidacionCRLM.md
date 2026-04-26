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

Siguiente paso técnico:

- Descargar una matriz de expresión bulk TCGA-COAD (e.g. HTSeq counts aggregados) para calcular scores de firma y correlaciones `MET-MYC`.
- Alternativa: usar `TCGAbiolinks` o el endpoint GDC para obtener una matriz compacta sin descargar archivos crudos.
- Antes de descargar matrices pesadas de GEO, validar primero con TCGA bulk como señal de plausibilidad.

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

## Fase 4: validación metastásica ext