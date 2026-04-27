# Investigacion sobre validacion externa GSE234804

Fecha: 2026-04-27 03:32:49 -03:00

## Pregunta

Despues de validar en GSE225857 que los vecindarios `CAF-high` se asocian espacialmente con `MET`, `MYC` y glicolisis, la pregunta fue:

`La senal se reproduce en un dataset externo CRLM, aunque sea a nivel muestra?`

La busqueda no intento confirmar a cualquier precio. El objetivo fue poner presion de falsacion sobre la hipotesis refinada:

`CAF-high spatial niches in CRLM associate with MET+ MYC/glycolytic tumor neighborhoods.`

## Triage de datasets externos

Se creo `scripts/triage_geo_external_validation.py` para revisar accesibilidad de datasets GEO sin descargar matrices pesadas.

Resultados:

| Dataset | Resultado de triage | Decision |
| --- | --- | --- |
| `GSE225857` | 607 MB, ya usado, archivos divididos | benchmark interno |
| `GSE226997` | 41.2 GB en TARs Visium de 9-13 GB | evitar por ahora |
| `GSE231559` | 692 MB, 10x dividido | candidato secundario; falta mapeo fenotipo |
| `GSE234804` | 568.8 MB, H5Seurat individuales CRC/LM | mejor candidato externo inmediato |
| `GSE178318` | `filelist.txt` no disponible en ruta GEO esperada | no usable en este bloque |

La decision fue avanzar con `GSE234804` porque contiene archivos individuales moderados:

- `CRC2`, `CRC3`, `CRC4`
- `LM2`, `LM9`, `LM16`, `LM17`, `LM21`, `LM28`

## Metodo GSE234804

Se creo `scripts/validate_gse234804_h5seurat.py`.

El script:

1. Descarga solo archivos `CRC*` y `LM*` `.h5seurat`.
2. Excluye muestras `PC*` en la primera pasada.
3. Lee `/assays/RNA/data`.
4. Extrae genes diana de la hipotesis.
5. Calcula medias por muestra.
6. Calcula scores:
   - `caf_core`
   - `mcam_caf`
   - `hgf_met_axis`
   - `myc_glycolysis_core`
   - `tumor_epithelial`
   - composite `caf_met_myc_glycolysis`
7. Compara LM vs CRC a nivel muestra.

Limitacion importante:

Los archivos H5Seurat inspeccionados no exponen metadata celular rica en `meta.data`. Por lo tanto, este bloque no puede separar fibroblastos de tumor ni probar vecindad espacial. Es una pantalla externa sample-level.

## Resultados

Muestras procesadas:

- CRC: 3 muestras, 8,161 celulas.
- LM: 6 muestras, 24,274 celulas.
- Total: 32,435 celulas.

Comparacion LM vs CRC:

| Metrica | LM mean | CRC mean | LM/CRC | p | Lectura |
| --- | --- | --- | --- | --- | --- |
| `score_mcam_caf` | 0.057 | 0.103 | 0.556 | 0.796 | no sube en LM |
| `score_caf_core` | 0.046 | 0.065 | 0.714 | 0.439 | no sube en LM |
| `score_myc_glycolysis_core` | 2.109 | 3.312 | 0.637 | 0.439 | no sube en LM |
| `score_hgf_met_axis` | 0.178 | 0.166 | 1.072 | 0.796 | casi igual |
| `MET` | 0.341 | 0.236 | 1.443 | 0.796 | modestamente mayor en LM |
| `HGF` | 0.014 | 0.011 | 1.311 | 1.000 | muy bajo/casi igual |
| `MYC` | 0.634 | 1.056 | 0.601 | 0.071 | menor en LM |
| `MCAM` | 0.010 | 0.054 | 0.178 | 0.505 | menor en LM |

## Interpretacion

GSE234804 no reproduce la hipotesis como una firma sample-level simple de LM vs CRC.

Esto importa. Si nuestra hipotesis fuera:

`las metastasis hepaticas tienen globalmente mas CAF/MCAM/MYC-glicolisis que primarios`

entonces este bloque la debilitaria bastante.

Pero esa ya no es la hipotesis mas precisa. La hipotesis actual dice que la senal relevante ocurre en vecindarios espaciales/celulares:

`CAF-high neighborhoods -> tumor MET/MYC/glycolysis`

GSE234804, sin cell-type labels ni coordenadas, no puede probar ni refutar esa arquitectura. Lo que si muestra es que no debemos vender el resultado como un biomarcador promedio de muestra.

## Que fortalece

- Fortalece la prudencia epistemologica del proyecto.
- Fortalece la idea de que necesitamos spatial/cell-type, no solo promedios sample-level.
- `MET` aparece modestamente mayor en LM, aunque sin significancia y con n pequeno.
- El resultado negativo ayuda a definir mejor la contribucion: arquitectura, no bulk.

## Que debilita

- Debilita una lectura simple de `CAF/MCAM` globalmente enriquecido en todas las LM.
- Debilita una lectura simple de `MYC/glicolisis` globalmente enriquecido en todas las LM.
- Debilita la idea de que GSE234804 pueda confirmar rapidamente el modelo sin anotaciones celulares.

## Decision

La linea sigue viva, pero mas estrecha y mas honesta:

- El hallazgo prometedor sigue siendo el resultado espacial/permutacional de GSE225857.
- TCGA-COAD apoya que CAF/MCAM tiene sombra clinica en primarios.
- GSE234804 no confirma un aumento sample-level LM vs CRC.
- La proxima validacion debe ser cell-type-resolved o spatial, no otra comparacion promedio.

## Proximo paso recomendado

Buscar una de estas rutas:

1. Obtener anotaciones celulares para GSE234804 si existen en el paper/suplementos.
2. Usar GSE231559 para validar si hay sample/cell-state mapping suficiente.
3. Encontrar un dataset spatial CRLM manejable, especialmente scCRLM/Cancer Diversity Asia.
4. Reanalizar GSE225857 con un nulo espacial mas estricto o separar tumor-high/CAF-high por regiones.

## Conclusion operativa

No estamos mas cerca de afirmar "descubrimos un biomarcador". Si estamos mas cerca de formular una hipotesis defendible:

`El eje relevante no es un aumento global de CAF/HGF/MYC en metastasis, sino una organizacion espacial especifica donde programas CAF compuestos se asocian localmente con tumor MET+ y respuesta MYC/glicolisis.`
