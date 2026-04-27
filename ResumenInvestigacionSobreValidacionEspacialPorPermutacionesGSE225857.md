# Resumen de validacion espacial por permutaciones en GSE225857

Fecha: 2026-04-27 00:40:23 -03:00

## Resumen corto

Se agrego una prueba de permutaciones al analisis spatial Visium de GSE225857 para responder una pregunta clave: si los spots vecinos a zonas `CAF-high` realmente enriquecen senales tumorales/metabolicas o si ese patron podria emerger por azar al redistribuir la expresion dentro de cada muestra.

El resultado fortalece la hipotesis central, pero tambien la refina. En las dos muestras de metastasis hepatica (`L1`, `L2`), los vecinos de spots `CAF-high` muestran enriquecimiento fuerte de `MET`, `MYC` y `glycolysis_score`. Para `CAF -> MET`, los ratios observados fueron 2.029 en L1 y 1.866 en L2, contra medias nulas cercanas a 1.0. Los p empiricos fueron 0.002 en ambas muestras usando 500 permutaciones.

El hallazgo negativo importante es que `HGF` aislado no reproduce ese patron espacial. Los vecinos de spots `HGF-high` no enriquecen `MET` en metastasis hepatica; de hecho los ratios fueron menores a 1.0. Esto no contradice la evidencia single-cell donde `HGF` aparece en fibroblastos y `MET` en tumor, pero si muestra que el nicho no se explica bien con un unico gen.

La mejor lectura actual es: el nicho relevante parece ser un programa CAF espacial compuesto, probablemente con fibroblastos PRELP/MCAM y otros estados CAF, que se asocia con vecindarios tumorales `MET+`, `MYC+` y glicoliticos. `HGF` sigue siendo parte posible del circuito paracrino, pero no basta como marcador espacial unico.

## Resumen extendido

La validacion espacial anterior habia mostrado que, en GSE225857, las muestras Visium de metastasis hepatica colorrectal tienen una asociacion positiva entre `caf_score` y `MET`, y una asociacion fuerte entre `MYC` y `glycolysis_score`. Tambien habia aparecido un patron de vecindad: los spots cercanos a zonas con alto score CAF tenian casi el doble de senal `MET` que el fondo. Sin embargo, una correlacion o un ratio observado no es suficiente para saber si estamos viendo una arquitectura biologica o solo un efecto esperable de la distribucion espacial de expresion.

Por eso se implemento una prueba nula por permutaciones. La estrategia fue mantener fija la geometria de la muestra: los spots source-high, sus vecinos y el fondo no cambian. Lo unico que se baraja es el valor del target dentro de la misma muestra. Si el enriquecimiento observado sobrevive contra este nulo, entonces no depende solamente de la cantidad global de expresion del target, sino de su ubicacion relativa respecto a las zonas fuente.

La prueba se corrio con 500 permutaciones por combinacion muestra/fuente/target. En las dos muestras hepaticas (`L1`, `L2`), los vecinos de `CAF-high` enriquecieron `MET`, `MYC` y glicolisis con p empirico 0.002. Para `CAF -> MET`, el ratio observado fue 2.029 en L1 y 1.866 en L2, mientras que la media nula fue cercana a 1.0. Esto sugiere que la proximidad entre regiones CAF-altas y senal tumoral `MET+` no es una consecuencia trivial de redistribuir la expresion al azar.

La misma prueba produjo un resultado negativo muy informativo: `HGF-high` no enriquecio `MET` en vecinos de metastasis hepatica. En L1 el ratio `HGF -> MET` fue 0.874 y en L2 fue 0.814, con p empiricos altos. Esta parte es crucial para no sobreinterpretar. El eje `HGF-MET` sigue siendo plausible porque la validacion single-cell encontro `HGF` concentrado en fibroblastos y `MET` concentrado en tumor. Pero espacialmente, el gen `HGF` aislado no captura el nicho. El mejor predictor de vecindarios tumorales `MET/MYC/glycolysis` fue el estado CAF compuesto.

La hipotesis queda entonces refinada: no deberia formularse como una flecha simple `HGF -> MET`, sino como un sistema de vecindario: fibroblastos PRELP/MCAM y otros CAF states crean regiones CAF-high donde aparecen celulas tumorales `MET+` con respuesta `MYC` y glicolitica. Este matiz es importante porque acerca el proyecto a un hallazgo mas serio: no una lista de genes, sino una arquitectura espacial reproducible en dos muestras hepaticas.

Todavia no se puede afirmar causalidad ni relevancia clinica directa. Visium mezcla celulas, solo hay dos muestras hepaticas en este bloque y el nulo de permutacion es simple. Pero la convergencia entre bulk, single-cell, spatial y permutacion convierte esta linea en la prioridad mas fuerte del repo.

## Recomendacion operativa

Seguir con esta apuesta, pero no como "HGF solo". La formulacion que conviene perseguir es:

`CAF-high spatial niches in CRLM associate with MET+ MYC/glycolytic tumor neighborhoods.`

El proximo paso de mayor valor es buscar validacion independiente o especificidad metastasica:

- segundo dataset spatial/single-cell manejable
- evaluacion de META-PRISM para especificidad CRLM
- revision de GSE226997 sin descargar archivos gigantes si hay subset util
- sintesis formal de la hipotesis refinada con predicciones falsables
