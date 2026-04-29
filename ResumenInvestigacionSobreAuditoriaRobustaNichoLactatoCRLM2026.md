# Resumen investigacion: auditoria robusta del nicho lactato/HLA-DRB5 en CRLM

Fecha: 2026-04-29 03:23:00 -03:00

## Resumen corto

Se ejecuto una auditoria dura sobre el eje mas prometedor del bloque anterior: `HLA-DRB5-like -> pyruvate/transamination`. El objetivo fue actuar como reviewer hostil y preguntar si la senal seguia siendo especifica despues de controles mas fuertes.

El resultado es mixto y muy importante. La senal sobrevive sensibilidad a block-size y ablations: `HLA-DRB5-like -> pyruvate_mito_entry` se mantiene positivo en 6/6 muestras y significativo en 4/6 a 6/6 segun block-size; `HLA-DRB5-like -> glutamate_transamination` tambien es positivo en 6/6 y significativo en 2/6 a 5/6 segun block-size. Al sacar `PTPRC`, el efecto sigue: `hla_drb5_no_ptprc -> pyruvate_mito_entry` y `hla_drb5_no_ptprc -> glutamate_transamination` quedan positivos en 6/6 y significativos en 5/6.

Pero los controles mas duros bajan la hipotesis. El gen `HLA-DRB5` solo no reproduce el efecto: apenas 1/6 muestras positivas y 0/6 significativas. Esto indica que la senal no es de `HLA-DRB5` aislado, sino de un modulo inmune mas amplio (`HLA-DRB5/CD74/CXCR4/LGALS9`, con o sin `PTPRC`). Mas grave: los efectos no superan random controls full-transcriptome emparejados por expresion/dropout; 0/6 en todos los casos. Y al residualizar por profundidad total y coordenadas espaciales, el efecto desaparece casi por completo.

Conclusion: no podemos vender esto como descubrimiento de nicho lactato/HLA-DRB5. La lectura honesta es que hay una co-ocurrencia regional entre modulo inmune HLA-DRB5-like y programas metabolicos, pero la especificidad metabolica no esta demostrada por transcript proxies. El siguiente paso solo vale si usamos mapas reales spFBA/FES.

## Resumen extendido

El bloque anterior habia encontrado una senal atractiva: vecindarios `HLA-DRB5-like` enriquecian proxies de entrada de pyruvato y transaminacion en 6 muestras spatial CRLM. Eso parecia una posible conexion entre la literatura 2026 sobre macrophages `HLA-DRB5+` y el paper spFBA que propone consumo no canonico de lactato en CRLM. Pero antes de convertirlo en narrativa de paper, habia que intentar romperlo.

Se creo `scripts/audit_lactate_axis_robustness.py`, que ejecuta cuatro controles. Primero, sensibilidad a tamanos de bloque 8, 12, 16 y 20. Segundo, ablations del source `HLA-DRB5-like`, sacando `PTPRC`, sacando `CD74/PTPRC`, o usando `HLA-DRB5` solo. Tercero, leave-one-gene-out de targets metabolicos. Cuarto, random controls desde el universo completo de features de cada muestra, emparejados por expresion/dropout. Quinto, residualizacion por profundidad total y coordenadas espaciales.

La parte positiva: la senal no depende de un unico block-size ni de un unico gen target. Tambien sobrevive al retiro de `PTPRC`, lo cual reduce el riesgo de leakage inmune obvio. Esto significa que hay una arquitectura regional real: zonas `HLA-DRB5/CD74/CXCR4/LGALS9-like` suelen estar cerca de zonas con scores pyruvato/transaminacion mas altos.

La parte negativa: esa arquitectura no es especifica todavia. `HLA-DRB5` solo falla, asi que el nombre debe ser modulo inmune y no gen aislado. Peor aun, los random controls full-transcriptome no son superados en ninguna muestra de forma significativa. Eso sugiere que genes con expresion y dropout parecidos pueden producir enriquecimientos espaciales similares. Ademas, cuando se residualizan source y target por profundidad/captura y coordenadas, el efecto deja de ser significativo. Esto indica que una parte sustancial del patron podria ser dominio histologico/espacial o gradiente de captura, no metabolismo especifico.

La decision es clara: no abandonar la rama, pero dejar de avanzar con proxies transcriptomicos simples. La unica forma de rescatar esta hipotesis es ir a flux real: spFBA/FES de lactate uptake, pyruvate/transamination, alphaKG/malate y reductive TCA. Si los mapas de flux muestran que los vecindarios HLA-DRB5-like predicen esas rutas incluso despues de residualizacion y controles espaciales, la historia vuelve a ponerse fuerte. Si no, esta rama debe cerrarse como co-ocurrencia regional no especifica.

## Recomendacion operativa

El siguiente paso debe ser `spFBA/FES or stop`. No mas proxies bonitos. Buscar o reconstruir los mapas spFBA 2026 y testear directamente si el modulo inmune HLA-DRB5-like predice lactate-carbon routing real.
