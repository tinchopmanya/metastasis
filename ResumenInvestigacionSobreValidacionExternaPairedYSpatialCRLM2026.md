# Resumen investigacion validacion externa paired y spatial CRLM 2026

Fecha: 2026-04-27 17:53:00 -03:00

## Resumen corto

La conclusion honesta es: no estamos en terreno virgen por genes o ejes individuales, pero si estamos entrando en una zona con potencial de hallazgo computacional defendible. La literatura 2025-2026 ya tiene trabajos fuertes sobre `HGF-MET-MYC-glycolysis`, `SPP1/CXCL12`, mCAFs, macrofagos `SPP1+`, macrofagos `HLA-DRB5+` y nichos inmunosupresores en CRLM. Por eso no conviene decir "descubrimos SPP1" ni "descubrimos CAFs". La posible novedad esta en integrar esas piezas en un modelo reproducible de nicho espacial.

Se ejecutaron dos validaciones externas nuevas. En `GSE245552`, una cohorte scRNA pareada con primarios CRC y metastasis hepaticas, la senal mas fuerte no fue el tumor `MYC/glycolysis`, sino el compartimento mieloide/CAF. El proxy mieloide `SPP1/CXCL12-lite` aumento en metastasis hepatica vs primario en 13/13 pares, con ratio 1.844 y p = 1.34e-04. El proxy mieloide `HLA-DRB5-lite` aumento en 12/13 pares, ratio 1.478 y p = 0.0017. El proxy CAF `SPP1/CXCL12-lite` tambien aumento en 11/13 pares. En cambio, el proxy tumoral `MYC/glycolysis-lite` no aumento; ratio 0.967 y solo 5/13 pares positivos.

En `GSE217414`, dataset externo Visium con 4 metastasis hepaticas CRLM, el patron espacial fue fuerte: `CAF -> SPP1/CXCL12-lite` fue positivo en 4/4 muestras, `CAF -> HLA-DRB5-lite` positivo en 4/4, `SPP1/CXCL12-lite -> MYC/glycolysis-lite` positivo en 4/4, y `HLA-DRB5-lite -> MYC/glycolysis-lite` positivo en 4/4. Todas estas pruebas usaron 500 permutaciones in-sample por test.

La nueva tesis queda asi: el modulo estromal-mieloide `CAF/SPP1-CXCL12/HLA-DRB5` parece reproducirse en metastasis hepatica y acercarse espacialmente al programa tumoral `MYC/glycolysis`, pero el brazo tumoral no se comporta como aumento uniforme por celula tumoral. Eso apunta a nicho local, no a una firma global de metastasis.

## Resumen extendido

La ola se inicio con una pregunta directa: "estamos en terreno virgen o cerca de un hallazgo importante?". La respuesta actual es mas interesante que un si/no. El terreno no es virgen si miramos componentes aislados. En 2025-2026 ya hay literatura solida sobre CRLM, single-cell, spatial transcriptomics, mCAFs, macrofagos `SPP1+`, `HLA-DRB5+`, `SPP1/CXCL12`, inmunorresistencia y programas tumorales `MET/MYC/glycolysis`. Esto obliga a no sobreactuar la novedad. La oportunidad real es demostrar una arquitectura reproducible y falsable que conecte esas piezas de forma multi-dataset.

El primer bloque nuevo fue `GSE245552`, una cohorte scRNA con 39 muestras, incluyendo primarios, metastasis hepaticas y tejidos adyacentes. El script `scripts/validate_gse245552_paired_scrna.py` descarga archivos 10x, extrae genes de interes, calcula scores de firmas 2026 y compara metastasis hepatica vs primario. Para evitar depender de anotaciones inexistentes o dificiles, se usaron proxies gruesos de compartimento: tumor epithelial, CAF, myeloid y T cell.

El resultado de `GSE245552` fue una correccion valiosa. Si el modelo fuera simplemente "las metastasis hepaticas tienen mas CAF y mas tumor glicolitico", deberiamos ver una subida limpia de CAF fraction y tumor `MYC/glycolysis`. No ocurrio. La fraccion CAF proxy no subio y el score tumoral `MYC/glycolysis-lite` fue practicamente igual o menor en metastasis. En cambio, el compartimento mieloide mostro una senal muy fuerte: `SPP1/CXCL12-lite` subio en 13/13 pares y `HLA-DRB5-lite` en 12/13. Tambien subio el `SPP1/CXCL12-lite` dentro del proxy CAF. Esto sugiere que la diferencia metastasica no es cantidad bruta de CAFs o glicolisis tumoral uniforme, sino activacion de estados inmuno-estromales especificos.

El segundo bloque fue `GSE217414`, una validacion espacial externa mucho mas cercana a un argumento de paper. GEO muestra cuatro secciones Visium de metastasis hepaticas de CRC, con raw procesado de tamano manejable. Se creo `scripts/validate_gse217414_spatial_external.py`, que descarga los H5 filtrados y los archivos de coordenadas, scorea firmas desolapadas 2026 y mide si los vecinos de spots source-high tienen targets enriquecidos contra un nulo por permutacion dentro de muestra.

El resultado fue fuerte: el acoplamiento `CAF -> SPP1/CXCL12-lite` fue positivo en las cuatro muestras, con ratio medio 1.346. `CAF -> HLA-DRB5-lite` tambien fue positivo en 4/4, ratio medio 1.391. Mas importante: los programas `SPP1/CXCL12-lite` y `HLA-DRB5-lite` predijeron vecinos altos en `MYC/glycolysis-lite` en 4/4 muestras, con ratios medios 1.776 y 1.467 respectivamente. Esto reproduce, en un dataset externo, la idea de un macro-nicho estromal-inmune-metabolico.

La lectura integrada es esta: `GSE245552` dice que la rama mieloide/CAF sube en metastasis hepatica de manera pareada; `GSE217414` dice que esa rama se acopla espacialmente al programa tumoral `MYC/glycolysis`; `GSE225857` ya habia mostrado un patron similar. La convergencia no prueba causalidad, pero si construye un caso computacional coherente.

El camino hacia un paper no es escribir mas narrativa, sino endurecer los controles. Hay que agregar firmas negativas y aleatorias, permutaciones espaciales estratificadas, pseudobulk por paciente y compartimento, anotacion celular curada para GSE245552, y una tabla comun de efectos espaciales GSE225857/GSE217414. Si esas pruebas sobreviven, la historia podria presentarse como un modelo computacional reproducible de nicho CRLM en capas.

## Recomendacion operativa

Seguir. Pero seguir como si fueramos revisores hostiles de nuestro propio hallazgo. El proximo bloque debe ser controles negativos y consolidacion multi-dataset, no otra busqueda panoramica.

Frase guia:

`No descubrimos SPP1; estamos intentando demostrar que SPP1/CXCL12/HLA-DRB5 define una interfaz estromal-mieloide reproducible que se acopla espacialmente a MYC/glycolysis en CRLM.`
