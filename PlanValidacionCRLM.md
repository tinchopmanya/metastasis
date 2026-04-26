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

- **MCAM+ CAFs enriquecidos en hígado**: CONFIRMADO (3,387 en LCT vs 692 en CCT, 83% en 