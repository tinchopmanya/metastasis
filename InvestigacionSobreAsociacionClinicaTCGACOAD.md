# Investigacion sobre asociacion clinica TCGA-COAD

Fecha: 2026-04-27 02:22:16 -03:00

## Pregunta

Despues de validar la arquitectura espacial `CAF-high -> MET/MYC/glicolisis` en GSE225857, la siguiente pregunta fue:

`Las firmas del nicho tienen alguna sombra clinica en tumores primarios TCGA-COAD?`

Esta no es una validacion directa de metastasis hepatica. TCGA-COAD contiene principalmente tumores primarios y no resuelve espacialidad ni nichos hepaticos. Aun asi, puede servir como filtro de plausibilidad clinica:

- si las firmas CAF se asocian con estadio avanzado, invasion o supervivencia, la linea gana relevancia;
- si no se asocian, la hipotesis puede seguir siendo valida como fenomeno espacial/metastasico, pero no como biomarcador bulk de primario.

## Metodo

Se creo `scripts/analyze_tcga_coad_clinical.py`.

Entradas:

- `data_manifest/generated/tcga_coad_signature_scores.tsv`
- UCSC Xena `TCGA.COAD.sampleMap/COAD_clinicalMatrix`

Salida:

- `data_manifest/generated/tcga_coad_clinicalMatrix.tsv`
- `data_manifest/generated/tcga_coad_clinical_signature_associations.tsv`
- `data_manifest/generated/tcga_coad_signature_survival.tsv`
- `data_manifest/generated/tcga_coad_clinical_association_report.md`

El script une 329 muestras con scores de firmas y anotacion clinica. Evalua:

- estadio avanzado vs temprano;
- `M1` vs `M0`;
- `N1/N2` vs `N0`;
- invasion linfatica;
- invasion venosa;
- supervivencia global por mediana de score.

Los tests son exploratorios, sin ajuste por multiples comparaciones.

## Resultados principales

Las asociaciones mas claras aparecen en firmas CAF/MCAM:

| Comparacion | Firma | Diferencia media | Cohen d | p |
| --- | --- | --- | --- | --- |
| N positivo vs N0 | `mcam_caf` | 0.332 | 0.382 | 6.95e-04 |
| N positivo vs N0 | `caf_core` | 0.301 | 0.357 | 8.57e-04 |
| Invasion linfatica si vs no | `mcam_caf` | 0.358 | 0.418 | 1.15e-03 |
| Invasion linfatica si vs no | `caf_core` | 0.312 | 0.374 | 2.27e-03 |
| Estadio avanzado vs temprano | `mcam_caf` | 0.259 | 0.298 | 1.24e-02 |
| Estadio avanzado vs temprano | `caf_core` | 0.228 | 0.269 | 1.64e-02 |

Lectura:

- Las firmas CAF/MCAM son mas altas en tumores con ganglios positivos.
- Tambien son mas altas en tumores con invasion linfatica.
- Tienen senal moderada/debil hacia estadio avanzado.

## Supervivencia

Pantalla por mediana:

| Firma | Eventos bajo | Eventos alto | p log-rank |
| --- | --- | --- | --- |
| `caf_core` | 33/157 | 46/158 | 2.03e-02 |
| `mcam_caf` | 33/157 | 46/158 | 2.70e-02 |
| `caf_met_myc_glycolysis_composite` | 39/157 | 40/158 | 4.93e-01 |
| `hgf_met_axis` | 45/157 | 34/158 | 5.31e-01 |
| `plasticity_emt` | 42/157 | 37/158 | 9.34e-01 |

Lectura:

- `caf_core` y `mcam_caf` altos muestran mas eventos de muerte que lo esperado por log-rank exploratorio.
- El composite completo `CAF/MET/MYC/glicolisis` no muestra supervivencia significativa en bulk.
- `HGF-MET` aislado tampoco muestra supervivencia.

## Interpretacion

Este bloque fortalece especificamente el componente CAF/MCAM, no el eje completo como biomarcador bulk.

La lectura actual es:

`En tumores primarios TCGA-COAD, las firmas CAF/MCAM se asocian con rasgos de agresividad como N positivo, invasion linfatica y peor supervivencia exploratoria. El circuito completo MET/MYC/glicolisis no aparece como predictor clinico simple en bulk.`

Esto encaja con la hipotesis refinada: la arquitectura importante podria ser contextual y espacial. El componente CAF tiene una sombra clinica detectable incluso en bulk, pero la interaccion CAF-tumor completa requiere datos spatial/single-cell.

## Que fortalece

- El componente `CAF-high` no parece una rareza exclusivamente espacial; tambien se asocia con agresividad clinica en primarios.
- `mcam_caf` aparece repetidamente entre las firmas mas asociadas a N positivo, invasion linfatica y supervivencia.
- Esto apoya mantener `MCAM/CAF` como eje prioritario junto a PRELP/CAF states.

## Que no demuestra

- No demuestra metastasis hepatica.
- No demuestra causalidad.
- No demuestra que `HGF-MET-MYC-glycolysis` sea prognostico como score bulk.
- No reemplaza validacion externa en cohortes metastasicas.

## Decision

La hipotesis sigue avanzando, con un matiz importante:

- `CAF-high/MCAM` gana prioridad como componente robusto y clinicamente asociado.
- `HGF-MET-MYC-glycolysis` debe mantenerse como mecanismo espacial/nicho, no como score bulk simple.
- El proximo salto debe ser especificidad metastasica: META-PRISM, GSE226997 si se encuentra ruta liviana util, o datasets CRLM 2025.

## Proximo paso recomendado

Buscar una cohorte donde se pueda preguntar:

`CAF-high/MCAM alto distingue metastasis hepatica colorrectal de primario, de metastasis no hepatica o de metastasis de otros tumores?`

Esa pregunta seria mas valiosa ahora que seguir acumulando asociaciones dentro de TCGA.
