# Investigacion sobre validacion externa paired y spatial CRLM 2026

Fecha: 2026-04-27 17:53:00 -03:00

## Pregunta

Queremos saber donde estamos parados despues de mirar la literatura 2026 y si el proyecto esta cerca de un hallazgo digno de paper.

La pregunta operativa fue:

`El modelo CAF-high layered niche en CRLM se reproduce fuera de GSE225857, o era solo una historia bonita armada sobre un unico dataset?`

## Respuesta corta

No estamos en terreno virgen si la afirmacion es que `CAF`, `SPP1`, `CXCL12`, `HLA-DRB5`, `MET`, `MYC` o glicolisis importan en CRLM. Eso ya esta muy activo en 2025-2026.

Si hay terreno interesante en una formulacion mas precisa:

`En CRLM, el acoplamiento espacial CAF/SPP1-CXCL12/HLA-DRB5 parece formar un modulo estromal-mieloide que se aproxima a programas tumorales MYC/glycolysis, pero la activacion MYC/glycolysis no aparece como aumento uniforme de todas las celulas tumorales metastasicas.`

Esa diferencia es importante. El aporte posible no es "descubrimos SPP1"; es una triangulacion reproducible entre literatura 2026, GSE225857 spatial, GSE245552 paired scRNA y GSE217414 external spatial.

## Donde esta el campo en 2026

La web/literatura reciente muestra que el frente esta lleno de senales convergentes:

- `HGF-MET-MYC-glycolysis` ya fue propuesto como interaccion estroma-tumor en CRLM con single-cell/spatial transcriptomics.
- Un trabajo 2026 en Journal of Translational Medicine describe un nicho mCAF - macrofago `SPP1+` - T cell stress/exhaustion, con organizacion espacial en capas y ejes `SPP1-CD44`, `FN1-CD44`, `MIF/CXCL12`.
- Otro trabajo 2026 propone `SPP1/CXCL12` como eje funcional de CRLM e inmunorresistencia, con CAFs como productores de CXCL12.
- Otro trabajo 2026 identifica macrofagos `SPP1+` y `HLA-DRB5+` como moduladores inmunes en CRLM mediante single-cell y spatial.

Conclusion: el campo esta caliente, no vacio. Eso es bueno y malo. Malo porque no se puede vender novedad por genes sueltos. Bueno porque nos da un andamiaje fuerte para hacer una contribucion computacional integrativa si somos estrictos.

## Validacion 1: GSE245552 paired scRNA

Dataset:

- GEO: `GSE245552`.
- 39 muestras scRNA-seq.
- Incluye primarios CRC, metastasis hepaticas, colon adyacente y higado adyacente.
- GEO describe mas de 160,000 celulas y muestras de 18 pacientes sincronos CRLM.
- Para el test paired util se obtuvieron 13 pacientes con primario y metastasis hepatica.

Script:

`scripts/validate_gse245552_paired_scrna.py`

Salidas:

- `data_manifest/generated/gse245552_sample_manifest.tsv`
- `data_manifest/generated/gse245552_sample_signature_scores.tsv`
- `data_manifest/generated/gse245552_lm_vs_primary_comparisons.tsv`
- `data_manifest/generated/gse245552_paired_deltas.tsv`
- `data_manifest/generated/gse245552_external_validation_report.md`

Metodo resumido:

- Descarga los archivos 10x split desde GEO.
- Extrae solo genes de interes para no cargar matrices completas gigantes en memoria.
- Calcula scores log1p por muestra.
- Asigna proxies gruesos de compartimento: tumor epithelial, CAF, myeloid, T cell.
- Compara metastasis hepatica vs primario, incluyendo deltas pareados por paciente.

## Resultado GSE245552

Lo fuerte:

- `myeloid_proxy__score_spp1_cxcl12_axis_desoverlap_2026`: LM/primario 1.844, p = 1.34e-04, delta positivo 13/13 pares, sign p = 2.44e-04.
- `myeloid_proxy__score_hla_drb5_macrophage_axis_desoverlap_2026`: LM/primario 1.478, p = 1.72e-03, delta positivo 12/13 pares, sign p = 0.0034.
- `caf_proxy__score_spp1_cxcl12_axis_desoverlap_2026`: LM/primario 1.361, p = 0.0307, delta positivo 11/13 pares, sign p = 0.0225.

Lo debil o correctivo:

- `tumor_epithelial_proxy__score_myc_glycolysis_desoverlap_2026`: LM/primario 0.967, p = 0.692, delta positivo solo 5/13 pares.
- `fraction_caf_proxy`: LM/primario 0.526, p = 0.130; no parece una historia simple de "hay mas CAFs en promedio".
- El score whole-sample `SPP1/CXCL12-lite` sube poco: ratio 1.140, p = 0.368, 7/13 pares.

Lectura:

GSE245552 no apoya una version burda del modelo donde toda metastasis hepatica tiene mas CAF o mas tumor MYC/glycolysis en promedio. Apoya algo mas fino: dentro de proxies mieloides y CAF, los programas `SPP1/CXCL12-lite` y `HLA-DRB5-lite` estan mas altos en metastasis hepatica que en primario.

Esto encaja con una arquitectura de nicho y con la literatura 2026, pero todavia no prueba espacialidad.

## Validacion 2: GSE217414 external spatial

Dataset:

- GEO: `GSE217414`.
- 4 secciones Visium de metastasis hepaticas de cancer colorrectal.
- RAW procesado de GEO: ~113 MB, manejable.
- Muestras: `19G081`, `19G0619`, `19G0635`, `19G02977`.

Script:

`scripts/validate_gse217414_spatial_external.py`

Salidas:

- `data_manifest/generated/gse217414_spatial_signature_availability.tsv`
- `data_manifest/generated/gse217414_spatial_correlations.tsv`
- `data_manifest/generated/gse217414_spatial_adjacency_permutation.tsv`
- `data_manifest/generated/gse217414_spatial_spot_scores.tsv`
- `data_manifest/generated/gse217414_spatial_external_report.md`

Metodo resumido:

- Descarga matrices H5 filtradas y archivos `spatial.tar.gz`.
- Extrae coordenadas `tissue_positions_list.csv`.
- Scorea firmas 2026 desolapadas.
- Define spots source-high por percentil 75.
- Compara los vecinos de esos spots contra el fondo de la misma muestra.
- Usa 500 permutaciones por test para un nulo in-sample.

## Resultado GSE217414

Resultados medios externos:

- `CAF -> SPP1/CXCL12-lite`: ratio medio 1.346; positivo 4/4 muestras; p <= 0.05 en 3/4.
- `CAF -> HLA-DRB5-lite`: ratio medio 1.391; positivo 4/4; p <= 0.05 en 4/4.
- `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: ratio medio 1.776; positivo 4/4; p <= 0.05 en 4/4.
- `HLA-DRB5-lite -> MYC/glycolysis-lite`: ratio medio 1.467; positivo 4/4; p <= 0.05 en 4/4.
- `CAF -> MET`: ratio medio 1.627; positivo 4/4; p <= 0.05 en 3/4.

Lectura:

Esta es la pieza mas fuerte del dia. GSE217414 no es el mismo dataset que GSE225857 y aun asi reproduce la logica espacial central: regiones CAF-high se acoplan a programas `SPP1/CXCL12-lite` y `HLA-DRB5-lite`, y esos programas se acoplan a `MYC/glycolysis-lite`.

La muestra `19G0619` debilita especificamente `CAF -> SPP1/CXCL12-lite`, pero mantiene fuerte `CAF -> HLA-DRB5-lite` y las relaciones hacia MYC/glycolysis. Esa heterogeneidad no destruye la hipotesis; la vuelve mas realista.

## Sintesis: terreno virgen o no?

No es terreno virgen por componentes. Si decimos "SPP1/CXCL12 importa", llegamos tarde. Si decimos "CAFs/macrofagos/tumor interactuan", tambien.

La ventana de aporte esta en:

`un modelo reproducible, multi-dataset, de nicho CRLM donde el eje estromal-mieloide SPP1/CXCL12/HLA-DRB5 se acerca espacialmente al brazo tumoral MYC/glycolysis, pero el componente tumoral no se comporta como aumento uniforme por celula tumoral en paired scRNA.`

Eso es un hallazgo computacional defendible si se endurece con controles.

## Que haria ahora para ir hacia paper

1. Repetir GSE217414 con controles negativos: firmas aleatorias emparejadas por expresion, genes housekeeping, targets no relacionados y fuentes no-CAF.
2. Cambiar el nulo espacial: ademas de permutar target globalmente, probar permutaciones estratificadas por region/expresion total para controlar autocorrelacion tisular.
3. Mejorar GSE245552 con anotacion celular curada: no quedarse en proxies gruesos.
4. Hacer pseudobulk por paciente y compartimento: macrophage-like, CAF-like, epithelial-like.
5. Probar ligand-receptor solo en ejes con soporte externo: `SPP1-CD44`, `CXCL12-CXCR4`, `MIF-CD74/CXCR4`, `FN1-CD44`.
6. Consolidar GSE225857 + GSE217414 en una tabla comun de efectos espaciales por muestra.
7. Crear una figura conceptual: `CAF belt -> SPP1/CXCL12/HLA-DRB5 myeloid zone -> MYC/glycolysis tumor response`.

## Riesgos

- Visium mezcla celulas; no prueba contacto celular directo.
- Las firmas comparten genes o vias biologicas, aunque usamos controles desolapados.
- Los p empiricos salen del nulo in-sample y no reemplazan validacion estadistica jerarquica por paciente.
- GSE245552 uso proxies marker-based, no anotaciones curadas.
- Puede haber autocorrelacion espacial general: muchos programas biologicos suben juntos en regiones tumorales densas.

## Decision

La linea sigue viva y sube de calidad.

Antes de esta ola, el proyecto tenia una hipotesis razonable. Despues de esta ola, tiene un esqueleto de paper computacional:

`paired scRNA muestra que la rama mieloide/CAF sube en metastasis hepatica; spatial externo muestra que esa rama se acopla localmente a MYC/glycolysis; spatial inicial GSE225857 ya habia mostrado el mismo macro-nicho.`

La frase prudente:

`Estamos cerca de un hallazgo publicable como modelo computacional exploratorio, no de una verdad clinica cerrada.`

## Fuentes web usadas

- GSE245552 GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE245552
- GSE217414 GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE217414
- HGF-MET-MYC-glycolysis CRLM: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
- mCAF-SPP1 macrophage-T cell niche 2026: https://link.springer.com/article/10.1186/s12967-026-07978-6
- SPP1/CXCL12 CRLM immunotherapy resistance: https://pmc.ncbi.nlm.nih.gov/articles/PMC12757724/
- SPP1+ and HLA-DRB5+ macrophages in CRLM: https://link.springer.com/article/10.1186/s12967-026-07853-4
