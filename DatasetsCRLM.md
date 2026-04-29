# Datasets para CRLM y nicho metastásico hepático

Fecha: 2026-04-25 01:06:15 -03:00

## Prioridad alta

### GSE225857
- Tipo: single-cell RNA-seq y spatial transcriptomics.
- Tema: CRC primario, metástasis hepática, tejidos normales adyacentes y sangre periférica.
- Uso: validar heterogeneidad celular, fibroblastos `MCAM+`, células T `CXCL13+`, diferencias primario-metástasis.
- Valor: dataset directamente alineado con CRLM.
- Estado: ya usado para composición celular, expresión single-cell y análisis Visium spot-level.
- Resultado espacial: vecinos de spots CAF alto enriquecen MET/MYC/glicólisis en hígado; HGF alto aislado no explica MET espacial.
- Limitación: pocos pacientes; requiere cuidado con batch y tratamiento. GEO informa un TAR procesado de aproximadamente 607 MB, pero se evitó descargarlo usando archivos individuales por muestra.
- Link: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857

### GSE226997
- Tipo: spatial transcriptomics Visium de CRC.
- Uso: spatial validation en artículos recientes; el estudio 2025 lo usa para mapear `mCAF`, `High-M CRC`, `HGF`, `MET`, `MYC` y glicólisis.
- Valor: permite probar co-localización espacial.
- Limitación: no es por sí solo un atlas grande de CRLM; sirve más como validación espacial. GEO informa un TAR procesado de aproximadamente 41.2 GB, por lo que no entra en la primera fase liviana.
- Estado 2026-04-27: GEO lo describe como Visium de cuatro pacientes con cancer colorrectal primario. No usarlo como validacion CRLM directa sin aclarar esa limitacion. Sigue siendo util como validacion espacial CRC general si se encuentra una ruta liviana para P1/P4.
- Link: https://www.omicsdi.org/dataset/geo/GSE226997

### GSE231559 / GSE234804
- Tipo: scRNA-seq integrado en el estudio 2025 del eje `HGF-MET-MYC`.
- Uso: reconstruir cell states y firmas `High-M CRC`/`mCAF`.
- Valor: forman parte del atlas de 35 datasets del paper líder.
- Limitación: hay que inspeccionar disponibilidad, metadata y consistencia.
- Estado 2026-04-27: triage GEO ejecutado. `GSE234804` tiene H5Seurat individuales manejables y fue analizado en 3 CRC y 6 LM. Resultado sample-level: no aumenta `CAF/MCAM` ni `MYC-glicolisis` en LM; sigue siendo util si se consiguen anotaciones celulares. `GSE231559` queda como candidato secundario por 10x dividido, pero requiere mapeo fenotipico.
- Link de estudio integrador: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/

### GSE245552
- Tipo: scRNA-seq paired primary CRC / liver metastasis / adjacent tissues.
- Tema: CRLM sincrono, EMT e interaccion inmune-tumor.
- Uso: validacion externa pareada de firmas `SPP1/CXCL12`, `HLA-DRB5`, CAF y tumor `MYC/glycolysis`.
- Valor: permite comparar metastasis hepatica contra primario dentro de paciente.
- Estado 2026-04-27: analizado con `scripts/validate_gse245552_paired_scrna.py`. Resultado fuerte en proxies mieloides/CAF: `myeloid SPP1/CXCL12-lite` sube 13/13 pares, `myeloid HLA-DRB5-lite` sube 12/13; tumor `MYC/glycolysis-lite` no sube globalmente.
- Limitacion: se usaron proxies marker-based; falta anotacion celular curada/pseudobulk.
- Link: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE245552

### GSE217414
- Tipo: spatial transcriptomics Visium.
- Tema: 4 metastasis hepaticas de cancer colorrectal.
- Uso: validacion espacial externa del modelo `CAF/SPP1-CXCL12/HLA-DRB5 -> MYC/glycolysis`.
- Valor: dataset CRLM spatial independiente, pequeno y manejable; RAW procesado ~113 MB.
- Estado 2026-04-27: analizado con `scripts/validate_gse217414_spatial_external.py`. Resultado: `CAF -> SPP1/CXCL12-lite`, `CAF -> HLA-DRB5-lite`, `SPP1/CXCL12-lite -> MYC/glycolysis-lite` y `HLA-DRB5-lite -> MYC/glycolysis-lite` positivos en 4/4 muestras.
- Limitacion: Visium mezcla celulas; requiere controles por autocorrelacion espacial.
- Link: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE217414

### spFBA CRC/LM 2026
- Tipo: spatial transcriptomics + spatial Flux Balance Analysis.
- Tema: metabolismo espacial en tumores primarios colorrectales y metastasis hepaticas.
- Uso: validar si las regiones `MYC/glycolysis` del repo corresponden a lactate consumption, crecimiento/proliferacion o metabolismo Warburg no canonico.
- Valor: puede convertir el brazo metabolico de una firma expresional a una pregunta de flujo/metabolismo espacial.
- Estado 2026-04-29: priorizado por agente investigador como siguiente dataset/metodo de alto valor.
- Limitacion: hay que localizar/validar los datos Zenodo/procesados y mapearlos a nuestra logica de nicho.
- Link: https://www.nature.com/articles/s41540-026-00654-x

### GSE206552
- Tipo: spatial transcriptomics CRLM.
- Tema: dinamica de senescencia celular en metastasis hepatica colorrectal.
- Uso: candidato externo adicional para validar si el patron stromal/myeloid-metabolic se observa en otro spatial CRLM.
- Valor: pequeno y manejable; GEO informa RAW ~100.4 MB.
- Estado 2026-04-29: detectado en busqueda web; no analizado todavia.
- Limitacion: parece custom CSV/H5/JSON/imagenes, requiere inspeccion de formato.
- Link: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE206552

### TCGA COAD/READ vía GDC
- Tipo: bulk multi-omics de tumor primario.
- Uso: validación débil de firmas, correlación `MET-MYC`, asociación con pronóstico o estado.
- Valor: gran baseline de CRC primario.
- Limitación: no es cohorte CRLM pura; etiquetas metastásicas no son ideales.
- Estado 2026-04-27: usado para plausibilidad bulk y clinica exploratoria. `mcam_caf`/`caf_core` se asocian con N positivo e invasion linfatica; el composite completo no fue prognostico en bulk.
- Link: https://portal.gdc.cancer.gov/

### TCIA Colorectal-Liver-Metastases
- Tipo: CT preoperatorio, segmentaciones, clínica y supervivencia.
- Tamaño: 197 pacientes.
- Uso: línea secundaria para recurrencia/supervivencia post-hepatectomía; posible puente entre biología y radiomics.
- Valor: endpoint clínico claro.
- Limitación: pesado en imagen; no arrancar por aquí si el objetivo inmediato es biología molecular.
- Link: https://www.cancerimagingarchive.net/collection/colorectal-liver-metastases/

## Prioridad media

### META-PRISM
- Tipo: exoma/transcriptoma de tumores metastásicos refractarios.
- Uso: distinguir señal CRLM de señal metastásica general.
- Valor: cohorte metastásica amplia.
- Limitación: heterogeneidad de tumor, tratamiento y sitio biopsiado.
- Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC10157368/

### scCRLM / Cancer Diversity Asia
- Tipo: recurso spatial usado en papers recientes.
- Uso: validación espacial adicional si los datos son accesibles.
- Valor: útil para contrastar nichos.
- Limitación: disponibilidad y formato pueden requerir exploración manual.

### PDMR / HCMI / organoides
- Tipo: modelos derivados de pacientes.
- Uso: priorización de targets y plausibilidad funcional.
- Valor: puente preclínico.
- Limitación: no todos los modelos tienen metadata CRLM perfecta.
- Links:
- https://dctd.cancer.gov/drug-discovery-development/reagents-materials/pdmr/models
- https://www.cancer.gov/ccg/research/functional-genomics/hcmi

## Regla operativa
Primero se trabaja con datasets ligeros y metadata accesible. La descarga pesada de imágenes TCIA queda para una fase técnica posterior.
