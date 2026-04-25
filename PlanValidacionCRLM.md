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
