# Investigacion sobre analisis spFBA/FES de lactato en CRLM 2026

Fecha: 2026-04-29 08:23:44 -03:00

## Pregunta

Venimos de una rama que parecia prometedora:

`HLA-DRB5-like myeloid neighborhoods -> pyruvate/transamination programs -> possible non-canonical lactate-carbon handling in CRLM`

La auditoria robusta anterior bajo esa rama de categoria: los proxies transcriptomicos espaciales mostraban co-ocurrencia regional, pero fallaban random controls full-transcriptome y residualizacion por profundidad/coordenadas. La pregunta tecnica quedo muy clara:

`El flux real spFBA/FES rescata la hipotesis metabolica o la cerramos como artefacto regional?`

Para responder, descargamos y analizamos el archivo pesado `output.tar.gz` del deposito Zenodo asociado al paper spFBA 2026. El archivo no se versiona en git: queda en `downloads/spfba/output.tar.gz`, ruta ignorada por `.gitignore`.

## Fuente primaria

Paper:

- `Spatial FBA reveals heterogeneous Warburg niches in renal tumors and lactate consumption in colorectal cancer`, npj Systems Biology and Applications, publicado el 2026-01-27.
- URL: https://www.nature.com/articles/s41540-026-00654-x

Repositorio:

- https://github.com/CompBtBs/spFBA

Datos:

- Zenodo record 13988866.
- Archivo descargado: `output.tar.gz`, aproximadamente 2.8 GB.

## Metodo ejecutado

Se extrajeron selectivamente los archivos:

`output/*/sampling/CBS/flux_statistics.h5ad`

No se expandio todo el archivo al repo. Los `.h5ad` quedaron bajo:

`downloads/spfba/extracted/output/.../sampling/CBS/flux_statistics.h5ad`

Se creo un script reproducible:

```powershell
python scripts/summarize_spfba_flux_statistics.py
```

El script lee directamente HDF5/AnnData con `h5py`, sin requerir `scanpy`, y resume reacciones seleccionadas:

- `EX_lac__L_e`: intercambio de lactato.
- `PYRt2m`: transporte mitocondrial de pyruvato.
- `PDHm`: piruvato deshidrogenasa mitocondrial.
- `ASPTA` y `ASPTAm`: transaminacion de aspartato citosolica y mitocondrial.
- `AKGMALtm`: transporte alphaKG/malato.
- `MDHm`: malato deshidrogenasa mitocondrial.
- `Biomass`: crecimiento/proliferacion estimada.
- Reacciones auxiliares de glucosa, oxigeno, glutamina, glutamato, TCA y ATP.

Salidas generadas:

- `data_manifest/generated/spfba_flux_summary_report.md`
- `data_manifest/generated/spfba_flux_selected_reaction_summary.tsv`
- `data_manifest/generated/spfba_flux_lm_vs_pt_comparisons.tsv`
- `data_manifest/generated/spfba_lactate_uptake_correlation_summary.tsv`

## Convencion de signos

En estos `flux_statistics.h5ad`, `.X` corresponde a `meanNormalized`: el promedio de flux sampleado normalizado por el rango FVA.

Para `EX_lac__L_e`:

- valor negativo = consumo/uptake de lactato;
- valor positivo = export/secrecion de lactato.

Para reacciones internas, el signo depende de la definicion de la reaccion. Por eso las comparaciones se interpretan con cuidado y no como causalidad directa.

## Resultado principal

El analisis confirma que existe un fenotipo de consumo de lactato en muestras colorrectales/metastasis hepatica del dataset spFBA, pero no confirma que sea especifico de metastasis ni que este ligado a `HLA-DRB5`.

En SC087 Stereo-seq:

- `LM4`: `EX_lac__L_e` medio -0.083, 92.6% de spots negativos.
- `LM4r`: `EX_lac__L_e` medio -0.165, 99.5% de spots negativos.
- `LM7`: `EX_lac__L_e` medio -0.153, 98.2% de spots negativos.
- `PT`: `EX_lac__L_e` medio -0.175, 99.0% de spots negativos.

Lectura: las metastasis hepaticas tienen lactate uptake extendido, pero el primario pareado tambien, incluso con media mas negativa. Por lo tanto, el claim correcto no es:

`lactate uptake es exclusivo de metastasis hepatica`

El claim correcto es:

`lactate uptake es un fenotipo recurrente en regiones colorrectales primarias y metastasicas modeladas por spFBA; dentro de algunas metastasis se acopla a rutas de transaminacion/malato/PDH.`

## Comparacion LM vs PT en SC087

Promedios `meanNormalized`:

- `EX_lac__L_e`: PT -0.175, LM -0.133, LM-PT +0.041.
- `PDHm`: PT 0.043, LM 0.051, LM-PT +0.008.
- `ASPTA`: PT 0.125, LM 0.132, LM-PT +0.007.
- `ASPTAm`: PT 0.129, LM 0.138, LM-PT +0.009.
- `MDHm`: PT 0.138, LM 0.160, LM-PT +0.022.
- `AKGMALtm`: PT 0.215, LM 0.065, LM-PT -0.150.
- `Biomass`: PT 0.013, LM 0.008, LM-PT -0.005.

Esto sugiere una imagen mixta:

- el primario no es menos lactate-consuming;
- las metastasis si muestran elevacion ligera de `PDHm`, `ASPTA`, `ASPTAm` y `MDHm`;
- `Biomass` baja en metastasis, consistente con que el fenotipo no es simplemente proliferacion;
- `AKGMALtm` baja fuerte en metastasis, por lo que la historia alphaKG/malato debe formularse con cuidado.

## Acoplamientos dentro de muestra

La variable operativa fue:

`lactate_uptake_score = -EX_lac__L_e`

Un Spearman positivo significa: mas uptake de lactato co-ocurre con mayor FES de la reaccion objetivo dentro de la misma muestra.

Seales fuertes:

- `LM7`: lactate uptake vs `ASPTA`, Spearman 0.776.
- `LM7`: lactate uptake vs `MDHm`, Spearman 0.643.
- `LM4r`: lactate uptake vs `ASPTA`, Spearman 0.520.
- `LM4r`: lactate uptake vs `MDHm`, Spearman 0.489.
- `LM4r`: lactate uptake vs `PDHm`, Spearman 0.404.
- `LM4`: lactate uptake vs `AKGMALtm`, Spearman 0.575.

En CRC VisiumHD:

- `P2`: lactate uptake vs `PDHm`, Spearman 0.615.
- `P2`: lactate uptake vs `ASPTA`, Spearman 0.529.
- `P2`: lactate uptake vs `MDHm`, Spearman 0.511.
- `P5`: lactate uptake vs `PDHm`, Spearman 0.527.
- `P5`: lactate uptake vs `ASPTA`, Spearman 0.504.

Esto es la parte mas interesante: aunque la media LM-vs-PT no da un efecto metastasis-especifico simple, dentro de varias muestras el lactate uptake se acopla con transaminacion, malato y PDH. Eso sostiene la mitad metabolica de la hipotesis.

## Lo que NO queda probado

Este analisis no prueba el puente inmune `HLA-DRB5`.

Razones:

- Los FES de spFBA analizados no son las mismas secciones que nuestras validaciones spatial GSE225857/GSE217414.
- Los archivos `flux_statistics.h5ad` contienen FES y ratios, pero no bastan para re-scorear `HLA-DRB5-like` en los mismos spots.
- Para probar el puente se necesita la expresion/metadata de los mismos samples spFBA, probablemente desde `data.tar.gz` o archivos procesados equivalentes.
- Sin ese puente, esto es triangulacion metabolica independiente, no validacion espacial inmune-metabolica.

## Decision

La rama no muere, pero cambia de estado.

Antes:

`HLA-DRB5-like -> pyruvate/transamination podria ser un nicho metabolico especifico`

Despues de la auditoria robusta:

`HLA-DRB5-like -> pyruvate/transamination es co-ocurrencia regional no especifica`

Despues de spFBA/FES:

`el fenotipo lactate uptake/transamination existe en datos de flux independientes; el puente con HLA-DRB5 sigue sin demostrar`

Eso significa que el camino digno de paper no es todavia un claim biologico cerrado. Es un programa de validacion con una grieta concreta:

`conectar el estado inmune espacial HLA-DRB5-like con FES de lactate uptake/transamination en los mismos spots o regiones`

## Siguiente movimiento recomendado

No seguir agregando proxies transcriptomicos de lactato. Ya sabemos que fallan controles duros.

El siguiente movimiento correcto es:

1. Descargar o extraer selectivamente los datos procesados de expresion/anotacion de spFBA (`data.tar.gz`, probablemente mas pesado que `output.tar.gz`).
2. Localizar `SC087_C03445G5_PT`, `SC087_A02991A2_LM4`, `SC087_A03389C5_LM4r`, `SC087_C03445C6_LM7`, `CRC_P1`, `CRC_P2`, `CRC_P5`.
3. Ver si tienen genes/metadata/coords compatibles con los FES.
4. Calcular `HLA-DRB5-like`, `SPP1/CXCL12-like`, CAF, tumor/metabolic scores en esos mismos spots.
5. Testear vecinos espaciales o region-level:

`HLA-DRB5-like -> EX_lac__L_e uptake / ASPTA / ASPTAm / PDHm / MDHm`

6. Aplicar nulos por bloques, residualizacion por profundidad/coordenadas y random controls full-transcriptome.

Si eso sobrevive, el hallazgo vuelve a ser fuerte. Si no sobrevive, cerrar la rama `HLA-DRB5/lactate` y concentrarse en el eje mas robusto:

`stromal/myeloid local architecture -> MYC/glycolysis-like adjacency`

## Frase honesta

No encontramos todavia un descubrimiento cerrado. Encontramos algo mejor que una ilusion: una parte metabolica real, computacionalmente independiente, y una frontera tecnica muy precisa donde el descubrimiento podria vivir o morir.
