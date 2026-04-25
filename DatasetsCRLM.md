# Datasets para CRLM y nicho metastásico hepático

Fecha: 2026-04-25 01:06:15 -03:00

## Prioridad alta

### GSE225857
- Tipo: single-cell RNA-seq y spatial transcriptomics.
- Tema: CRC primario, metástasis hepática, tejidos normales adyacentes y sangre periférica.
- Uso: validar heterogeneidad celular, fibroblastos `MCAM+`, células T `CXCL13+`, diferencias primario-metástasis.
- Valor: dataset directamente alineado con CRLM.
- Limitación: pocos pacientes; requiere cuidado con batch y tratamiento.
- Link: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857

### GSE226997
- Tipo: spatial transcriptomics Visium de CRC.
- Uso: spatial validation en artículos recientes; el estudio 2025 lo usa para mapear `mCAF`, `High-M CRC`, `HGF`, `MET`, `MYC` y glicólisis.
- Valor: permite probar co-localización espacial.
- Limitación: no es por sí solo un atlas grande de CRLM; sirve más como validación espacial.
- Link: https://www.omicsdi.org/dataset/geo/GSE226997

### GSE231559 / GSE234804
- Tipo: scRNA-seq integrado en el estudio 2025 del eje `HGF-MET-MYC`.
- Uso: reconstruir cell states y firmas `High-M CRC`/`mCAF`.
- Valor: forman parte del atlas de 35 datasets del paper líder.
- Limitación: hay que inspeccionar disponibilidad, metadata y consistencia.
- Link de estudio integrador: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/

### TCGA COAD/READ vía GDC
- Tipo: bulk multi-omics de tumor primario.
- Uso: validación débil de firmas, correlación `MET-MYC`, asociación con pronóstico o estado.
- Valor: gran baseline de CRC primario.
- Limitación: no es cohorte CRLM pura; etiquetas metastásicas no son ideales.
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
