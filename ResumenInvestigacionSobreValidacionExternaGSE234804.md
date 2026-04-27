# Resumen de validacion externa GSE234804

Fecha: 2026-04-27 03:32:49 -03:00

## Resumen corto

Se hizo un triage reproducible de datasets GEO para buscar una validacion externa liviana de la hipotesis `CAF-high -> MET/MYC/glicolisis`. El mejor candidato inmediato fue `GSE234804`, porque ofrece archivos `.h5seurat` individuales para muestras `CRC` y `LM` de tamano moderado. `GSE226997`, aunque espacialmente relevante, queda descartado por ahora porque sus archivos Visium individuales pesan 9-13 GB y ademas corresponden a CRC primario, no CRLM directa.

Se creo `scripts/validate_gse234804_h5seurat.py`, que descarga solo muestras `CRC*` y `LM*`, extrae genes diana desde `/assays/RNA/data` y calcula scores de `caf_core`, `mcam_caf`, `hgf_met_axis`, `myc_glycolysis_core` y un composite. Se procesaron 9 muestras: 3 CRC y 6 LM, con 32,435 celulas en total.

El resultado fue negativo para la version sample-level simple: `mcam_caf`, `caf_core` y `myc_glycolysis_core` no suben en LM frente a CRC. `MET` fue modestamente mayor en LM, pero sin significancia; `HGF` fue muy bajo/casi igual. Esto no confirma el modelo como firma promedio de metastasis hepatica.

La interpretacion importante es que la hipotesis queda mas estrecha: el posible hallazgo no es "LM tiene mas CAF/MCAM/MYC-glicolisis en promedio", sino "vecindarios espaciales CAF-high se asocian localmente con tumor MET+ y respuesta MYC/glicolisis". GSE234804 no tiene metadata celular rica ni coordenadas en este formato, por lo que no puede probar esa arquitectura.

## Resumen extendido

El proyecto venia acumulando evidencia fuerte dentro de GSE225857: composicion celular, expresion single-cell, Visium spot-level y permutaciones espaciales apoyaban una organizacion donde los spots vecinos a regiones `CAF-high` tienen mas `MET`, `MYC` y glicolisis. Ademas, `HGF-high` por si solo no explicaba la vecindad con `MET`, refinando la hipotesis hacia un programa CAF compuesto.

La pregunta siguiente era si esa senal podia sobrevivir fuera de GSE225857. Para no entrar en descargas enormes sin plan, se construyo un triage GEO. Ese triage mostro que `GSE234804` era la mejor ruta externa inmediata: 13 archivos `.h5seurat`, de los cuales 9 corresponden a CRC y LM. En cambio, `GSE226997` requiere archivos Visium gigantes y no sirve como CRLM directa; `GSE231559` es manejable pero necesita mapeo fenotipico; `GSE178318` no tenia `filelist.txt` disponible en la ruta esperada.

La validacion externa con GSE234804 fue deliberadamente conservadora. Como los archivos no exponian anotaciones celulares utiles en `meta.data`, el analisis se hizo a nivel muestra. Esto es una limitacion importante: no podemos distinguir fibroblastos de celulas tumorales ni medir vecindad espacial.

Los resultados no replicaron la historia como una firma promedio LM-vs-CRC. `score_mcam_caf` fue menor en LM que en CRC, `score_caf_core` tambien fue menor, y `score_myc_glycolysis_core` bajo de 3.312 en CRC a 2.109 en LM. `MET` subio modestamente en LM, pero sin soporte estadistico fuerte, y `HGF` permanecio muy bajo.

Este resultado es valioso porque evita una conclusion exagerada. Si la apuesta fuera un biomarcador bulk o sample-level, GSE234804 la debilitaria. Pero la hipotesis actual es mas especifica: arquitectura local, no promedio global. Por eso GSE234804 no mata la linea, pero si obliga a ser mas precisos y mas exigentes.

## Recomendacion operativa

No seguir acumulando promedios sample-level. El proximo paso debe ser cell-type-resolved o spatial:

- buscar anotaciones celulares para GSE234804;
- mapear GSE231559 si tiene fenotipos suficientes;
- encontrar scCRLM/Cancer Diversity Asia u otro spatial CRLM manejable;
- fortalecer el nulo espacial en GSE225857.

La frase correcta ahora es:

`La evidencia apunta a una arquitectura espacial CAF-high, no a una firma promedio universal de metastasis hepatica.`
