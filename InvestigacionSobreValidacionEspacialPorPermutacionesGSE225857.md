# Investigacion sobre validacion espacial por permutaciones en GSE225857

Fecha: 2026-04-27 00:40:23 -03:00

## Pregunta

Despues de observar que los spots vecinos a zonas `CAF-high` en metastasis hepatica colorrectal tienen mas senal de `MET`, `MYC` y glicolisis, la pregunta critica fue:

`Ese enriquecimiento espacial es real o puede aparecer por azar al redistribuir la expresion dentro de cada muestra?`

La validacion se concentro en las dos muestras Visium de metastasis hepatica de GSE225857:

- `L1`
- `L2`

## Metodo

Se extendio `scripts/analyze_gse225857_spatial.py` para agregar una prueba nula por permutaciones.

El metodo fue:

1. Mantener fijos los spots `source-high`, sus vecinos y el fondo.
2. Barajar los valores del target dentro de la misma muestra.
3. Recalcular el ratio `target_mean_in_neighbors / target_mean_in_background`.
4. Repetir 500 veces por combinacion muestra/fuente/target.
5. Comparar el ratio observado contra la distribucion nula.

Fuentes evaluadas:

- `caf_score`
- `HGF`

Targets evaluados:

- `MET`
- `MYC`
- `glycolysis_score`

El resultado se escribio en:

- `data_manifest/generated/gse225857_spatial_adjacency_permutation.tsv`
- `data_manifest/generated/gse225857_spatial_report.md`

## Resultado principal

En metastasis hepatica, los vecinos de spots `CAF-high` muestran enriquecimiento fuerte y no compatible con azar simple:

| Muestra | Fuente | Target | Ratio observado | Media nula | z | p empirico |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | `caf_score` | `MET` | 2.029 | 0.998 | 19.177 | 0.002 |
| L2 | `caf_score` | `MET` | 1.866 | 1.009 | 9.992 | 0.002 |
| L1 | `caf_score` | `MYC` | 1.355 | 1.000 | 14.167 | 0.002 |
| L2 | `caf_score` | `MYC` | 1.682 | 1.000 | 20.145 | 0.002 |
| L1 | `caf_score` | `glycolysis_score` | 1.624 | 0.999 | 23.389 | 0.002 |
| L2 | `caf_score` | `glycolysis_score` | 1.817 | 1.001 | 24.911 | 0.002 |

La lectura es robusta: cerca de zonas CAF-altas aparecen senales tumorales/metabolicas relevantes para la hipotesis.

## Resultado negativo importante

`HGF` aislado no reproduce el patron espacial. En las mismas muestras de metastasis hepatica:

| Muestra | Fuente | Target | Ratio observado | Media nula | z | p empirico |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | `HGF` | `MET` | 0.874 | 1.000 | -2.661 | 0.994 |
| L2 | `HGF` | `MET` | 0.814 | 0.995 | -1.438 | 0.936 |

Esto no elimina a `HGF` del mecanismo, porque la evidencia single-cell sigue mostrando `HGF` en fibroblastos y `MET` en tumor. Pero si debilita una version simplista:

`HGF-high spot -> MET-high neighbor`

La senal espacial fuerte no es `HGF` como gen unico. La senal espacial fuerte es un programa CAF compuesto.

## Interpretacion

La hipotesis debe refinarse asi:

`PRELP/MCAM fibroblasts y otros estados CAF crean vecindarios CAF-high donde las celulas tumorales MET+ muestran respuesta MYC/glicolisis. HGF forma parte del circuito paracrino, pero no basta como marcador espacial unico del nicho.`

Este refinamiento es valioso porque reduce el riesgo de una historia demasiado lineal. La biologia del nicho parece mas parecida a un contexto estromal organizado que a un unico ligando explicandolo todo.

## Que fortalece

- Fortalece la existencia de arquitectura espacial CAF-tumor en CRLM.
- Fortalece que `MET`, `MYC` y glicolisis aparecen cerca de zonas CAF-altas.
- Fortalece el uso de firmas compuestas por sobre genes individuales.
- Fortalece la necesidad de integrar single-cell y spatial en vez de leer un solo nivel.

## Que debilita

- Debilita la version simple `HGF` como predictor espacial suficiente.
- Debilita una narrativa de causalidad directa desde Visium.
- Debilita la idea de que una correlacion spot-level basta sin vecindad y nulo.

## Limitaciones

- Visium mezcla multiples celulas por spot.
- Solo hay dos muestras de metastasis hepatica Visium en este bloque.
- La prueba permuta valores dentro de muestra, pero no modela toda la autocorrelacion espacial compleja.
- No prueba causalidad; solo refuerza plausibilidad espacial.
- Los p empiricos tienen resolucion limitada por 500 permutaciones; el minimo posible con esta configuracion es 0.001996.

## Decision

Seguir. No estamos ante una prueba clinica ni ante causalidad cerrada, pero si ante una senal computacional coherente y cada vez mas especifica:

1. Bulk: `MET-MYC` y `MYC-glycolysis` son plausibles.
2. Single-cell: `HGF` es fibroblastico y `MET` es tumoral.
3. Spatial: `CAF-high` predice vecindad con `MET/MYC/glycolysis`.
4. Permutacion: esa vecindad supera un nulo simple dentro de muestra.

## Proximo paso recomendado

El siguiente bloque deberia buscar reproducibilidad externa o especificidad:

- Validar un segundo dataset espacial/single-cell si es accesible.
- Buscar si GSE226997 puede aportar una validacion manejable sin descargar 41 GB completos.
- Evaluar META-PRISM para distinguir CRLM de metastasis general.
- Empezar una sintesis de hipotesis publicable: `CAF-high spatial niche in CRLM associates with MET+ MYC/glycolytic tumor neighborhoods`.
