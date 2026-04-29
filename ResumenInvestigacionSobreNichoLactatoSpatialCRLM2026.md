# Resumen investigacion: nicho lactato/HLA-DRB5 en CRLM 2026

Fecha: 2026-04-29 02:58:54 -03:00

## Resumen corto

La nueva ruta mas prometedora no es insistir en `CAF -> MET`. La evidencia acumulada empuja hacia una pregunta menos recorrida: si los vecindarios mieloides `HLA-DRB5-like` se conectan espacialmente con el metabolismo no canonico de lactato/pyruvato en metastasis hepatica de cancer colorrectal.

La literatura 2026 ya reporto dos piezas por separado. Primero, spFBA mostro que CRLM puede consumir lactato y rerutear carbono hacia pyruvato, transaminacion, alphaKG/malato y biosintesis, en lugar de usar una ruta Warburg canonica simple. Segundo, Xie et al. 2026 identificaron macrophages `SPP1+` y `HLA-DRB5+` como moduladores espaciales del microambiente inmune en CRLM. Lo que no queda cerrado en esos trabajos es el puente entre la arquitectura inmune y el estado metabolico/flux.

Se creo `scripts/analyze_spatial_lactate_axis.py` y se ejecuto sobre 6 muestras spatial CRLM: 2 de `GSE225857` y 4 de `GSE217414`. El analisis es proxy, no spFBA real. Como `LDHA/LDHB` no estaban disponibles, la lectura mas fuerte no es "lactato" directo, sino los programas vecinos de entrada de pyruvato y transaminacion.

Resultado: `HLA-DRB5-like -> glutamate_transamination` fue positivo en 6/6 y sobrevivio nulo por bloques en 5/6, ratio medio 1.764. `HLA-DRB5-like -> pyruvate_mito_entry` fue positivo en 6/6 y sobrevivio en 5/6, ratio medio 1.571. En cambio, la rama `CXCL12/FN1/CD44-like` tuvo ratios altos pero se explico mas por estructura espacial global.

Conclusion: no es un descubrimiento cerrado, pero si una hipotesis nueva y testeable con potencial de paper: `HLA-DRB5-like myeloid neighborhoods may mark immune-metabolic CRLM niches linked to non-canonical lactate-carbon handling`.

## Resumen extendido

El proyecto venia sosteniendo una arquitectura `stromal/myeloid-like regions -> MYC/glycolysis local adjacency` en CRLM. Esa linea sobrevivio varios controles, pero los ultimos nulos tambien bajaron la confianza en claims demasiado especificos como `CAF -> MET`. Por eso se abrio una ruta mas fina, inspirada por el trabajo spFBA 2026: buscar no solo glicolisis tumoral, sino una economia local de lactato/pyruvato.

La literatura revisada ubica la oportunidad con bastante precision. El paper spFBA 2026 reporta lactate uptake en CRC primario y metastasis hepatica, y propone que en CRLM el carbono de lactato puede desviarse hacia transaminacion y metabolismo biosintetico no canonico. A la vez, el paper sobre `SPP1+` y `HLA-DRB5+` macrophages en CRLM identifica estados mieloides con localizacion espacial e interacciones inmunes diferenciales. La grieta es que el primer trabajo no liga su mapa metabolico con una poblacion inmune concreta, y el segundo no prueba una funcion metabolica de los estados mieloides. Nuestro nuevo analisis se mete justo ahi.

El script nuevo extrae genes metabolicos disponibles en Visium y construye proxies para `lactate_import_anabolic`, `pyruvate_mito_entry`, `glutamate_transamination` y `lactate_export_glycolytic`. Luego pregunta si los vecinos de spots altos en `HLA-DRB5-like` o `CXCL12/FN1/CD44-like` enriquecen esos proxies, usando permutacion por bloques para controlar gradientes espaciales amplios. El analisis combino 6 muestras CRLM spatial de dos datasets independientes.

La senal mas interesante aparece en `HLA-DRB5-like`, no en `CXCL12/FN1/CD44-like`. `HLA-DRB5-like -> glutamate_transamination` y `HLA-DRB5-like -> pyruvate_mito_entry` sobreviven bloque en 5/6 muestras. Las ramas de import/export lactato son parciales, y la conexion proxy lactato -> MYC/glycolysis parece mas regional que especifica. Esto sugiere que el hallazgo potencial no es "mas glicolisis", sino una vecindad mieloide-metabolica compatible con transaminacion/pyruvato.

El nivel de evidencia actual es exploratorio pero valioso. No se puede afirmar flux ni causalidad, porque faltan spFBA real, LDHA/LDHB, deconvolucion por tipo celular y controles full-transcriptome. Pero el resultado si prioriza una hipotesis mas novedosa que las anteriores: una rama `HLA-DRB5-like immune-metabolic niche` que podria conectar tolerancia/inmunomodulacion con metabolismo no canonico de carbono en CRLM.

## Recomendacion operativa

Seguir por esta ruta. El siguiente paso debe ser conseguir o reproducir mapas spFBA/FES y probar directamente si `HLA-DRB5-like` predice lactate uptake, pyruvate/transamination y reductive TCA en spots vecinos. Si esa validacion funciona, estaremos mas cerca de una contribucion tipo paper que con el eje `CAF -> MET`.

Fuentes principales:

- https://www.nature.com/articles/s41540-026-00654-x
- https://link.springer.com/article/10.1186/s12967-026-07853-4
- https://link.springer.com/article/10.1186/s12967-025-07581-1

## Nota post-auditoria

La auditoria robusta posterior bajo la prioridad de este resultado: la senal no supera random controls full-transcriptome y desaparece al residualizar por profundidad/coordenadas. Mantener como hipotesis para spFBA/FES, no como claim de descubrimiento.
