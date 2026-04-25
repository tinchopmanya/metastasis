# Resumen de investigación sobre metástasis en cánceres y oportunidades con IA

Fecha: 2026-04-23 03:15:24 -03:00

## Resumen corto
La metástasis es el proceso por el cual células tumorales salen del tumor primario, sobreviven en circulación, llegan a un órgano distante, se adaptan a ese nuevo entorno y logran colonizarlo. No es un solo paso, sino una secuencia completa de eventos biológicos donde el cuello de botella más importante no suele ser la simple diseminación, sino la colonización efectiva, la interacción con el microambiente y, muchas veces, la dormancia. NCI sigue remarcando que la enfermedad metastásica explica la mayoría de las muertes por cáncer y que distintos tumores tienen afinidades distintas por ciertos órganos: por ejemplo, mama suele ir a hueso, cerebro, hígado y pulmón; colon a hígado, pulmón y peritoneo; pulmón a cerebro, hueso, hígado y suprarrenal; próstata a hueso con mucha fuerza.

La oportunidad real de la IA, sin hacer ensayos clínicos ni generar pacientes nuevos, está en el descubrimiento computacional. Hoy se puede trabajar con cohortes públicas metastásicas, imagen médica, histopatología digital, RNA-seq, single-cell, transcriptómica espacial, líneas celulares, organoides y PDX. Con eso, agentes de IA pueden detectar firmas de organotropismo, programas de dormancia y reactivación, subtipos metastásicos, posibles dianas y biomarcadores, además de integrar miles de artículos en grafos de evidencia. Lo importante es no confundir hipótesis fuertes con validación clínica.

Entre todas las líneas posibles, la mejor apuesta inicial parece ser cáncer colorrectal con metástasis hepática. Tiene alta frecuencia clínica, una pregunta biológica clara, buenas posibilidades de validación cruzada y múltiples capas de datos abiertos. La segunda gran apuesta es cáncer de mama con metástasis a cerebro y hueso, especialmente por dormancia y heterogeneidad de subtipos. La tercera, muy fuerte para visión computacional, es cáncer de pulmón con metástasis cerebral. Si el objetivo es maximizar probabilidad de hallazgo útil con agentes de IA, conviene empezar con una pregunta estrecha y órgano-específica, no con un panorama demasiado amplio.

## Resumen extendido
La metástasis es el corazón del problema oncológico avanzado. Aunque el cáncer primario inicia la enfermedad, lo que suele definir el desenlace clínico es la capacidad de algunas células tumorales de desprenderse, viajar y establecerse en órganos distantes. La descripción clásica de NCI sigue siendo útil: invasión local, entrada a vasos sanguíneos o linfáticos, tránsito por la circulación, salida al nuevo tejido, formación de un microfoco y crecimiento sostenido mediante angiogénesis. Sin embargo, esa secuencia es demasiado simple si se la toma de forma literal. En la práctica, la mayor parte de las células que se diseminan fracasa. Las que triunfan lo hacen porque combinan plasticidad celular, adaptación metabólica, evasión inmune, capacidad de remodelar su microambiente y compatibilidad con el órgano receptor.

Por eso, si queremos hacer descubrimiento con IA, la mejor pregunta no es sólo "cómo se mueve una célula", sino "qué permite que una célula metastásica colonice y sobreviva en un órgano concreto". Ahí aparecen los conceptos más potentes del campo actual: organotropismo, dormancia, reactivación, nicho premetastásico, plasticidad transcripcional y evolución clonal bajo tratamiento. El trabajo reciente de NCI sobre dormancia es especialmente importante porque subraya que algunas células diseminadas pueden permanecer meses, años o incluso décadas en estado latente antes de reactivarse. Si una línea de IA lograra aislar firmas robustas de dormancia o de salida de dormancia, el valor sería enorme.

No todos los cánceres se comportan igual. Los patrones clásicos siguen siendo relevantes: mama tiene fuerte relación con hueso, cerebro, hígado y pulmón; colon con hígado, pulmón y peritoneo; pulmón con cerebro, hueso, hígado y suprarrenal; próstata con hueso; melanoma con cerebro, hígado, pulmón y piel. Para IA, esto importa porque permite formular problemas más limpios. La pregunta "qué distingue a un tumor colorrectal que termina colonizando hígado" es más potente que la pregunta "qué es la metástasis en general". Cuanto más concreto es el órgano destino y más claros son los endpoints, mayor probabilidad de producir un hallazgo computacional robusto.

La buena noticia es que hoy existen más recursos públicos de los que había hace pocos años. El Genomic Data Commons del NCI ya reúne decenas de miles de casos y puede ser una base para análisis genómicos y transcriptómicos. Dentro de ese ecosistema, Count Me In aporta cohorts metastásicas reales, incluyendo cáncer de mama metastásico y próstata metastásica. HTAN abre la puerta a estudiar arquitectura tumoral y estados celulares con resoluciones mucho más finas, y su portal ya reporta miles de casos. El Imaging Data Commons y TCIA, por su parte, son especialmente relevantes para metástasis cerebral, donde ya existen colecciones con MRI, segmentaciones, seguimiento y, en algunos casos, patología emparejada. En paralelo, AACR Project GENIE permite usar datos clínico-genómicos de una escala multicéntrica muy valiosa.

Además de cohortes de pacientes, hoy es posible unir datos funcionales. DepMap diferencia líneas de origen primario o metastásico, y MetMap añade potencial metastásico órgano-específico en cientos de líneas. HCMI, PDXNet y PDMR permiten enlazar el descubrimiento computacional con modelos derivados de pacientes, como organoides o PDX. Esto es importante porque un hallazgo serio sobre metástasis rara vez se sostiene sólo con una cohorte retrospectiva; gana fuerza cuando también encaja con evidencia funcional o de modelo.

Entonces, dónde hay más probabilidad de descubrir algo con agentes de IA. Mi lectura actual es la siguiente. En primer lugar, cáncer colorrectal con metástasis hepática. Tiene un trayecto clínico muy conocido, una gran importancia médica, una pregunta órgano-específica potente y espacio real para integrar transcriptómica, espacial, imagen y literatura. En segundo lugar, cáncer de mama con metástasis a cerebro o hueso. Aquí el valor está en la combinación de subtipos moleculares, dormancia, heterogeneidad y disponibilidad de cohorts metastásicas explícitas más datasets de imagen cerebral. En tercer lugar, cáncer de pulmón con metástasis cerebral, una línea muy apta para visión computacional porque ya existe evidencia de que la histopatología del tumor primario contiene señal predictiva del riesgo de metástasis al cerebro.

También hay líneas muy prometedoras, aunque algo más difíciles, como próstata con metástasis ósea, melanoma con neurotropismo y proyectos pan-cáncer centrados en hígado o hueso como órganos de colonización. De hecho, las nuevas atlas single-cell de metástasis hepática y ósea son una señal fuerte de hacia dónde se mueve la frontera del campo: menos análisis puramente descriptivo de bulk tumor y más cartografía fina de estados celulares, interacciones y microambiente.

El mejor uso de agentes de IA en este escenario no es pedirles una teoría universal del cáncer metastásico, sino organizarlos para un pipeline muy concreto. Primero, levantar datasets y metadata. Segundo, leer y estructurar literatura. Tercero, comparar cohorts y detectar programas reproducibles. Cuarto, cruzar esos hallazgos con dependencias, modelos y posibles fármacos. Quinto, producir un ranking de hipótesis listo para validación. Eso sí es una estrategia realista.

Mi conclusión es que la IA tiene alta probabilidad de producir descubrimientos útiles en metástasis si trabaja sobre un problema estrecho, rico en datos y con validación cruzada posible. La mejor puerta de entrada hoy es colorrectal a hígado. Si buscamos una segunda línea de alto valor biológico, mama a cerebro o hueso. Si queremos una línea muy visual y muy compatible con modelos de visión, pulmón a cerebro.

## Recomendación operativa
La próxima investigación debería abandonar el panorama general y enfocarse en una sola ruta metastásica. La recomendación principal es:

`cáncer colorrectal -> metástasis hepática`

La recomendación secundaria es:

`cáncer de mama -> metástasis a cerebro y hueso`

## Fuentes base
- https://www.cancer.gov/types/metastatic-cancer
- https://www.cancer.gov/about-nci/organization/dcb/research-portfolio/tumor-metastasis
- https://www.cancer.gov/news-events/cancer-currents-blog/2025/metastasis-dormant-cancer-cells-immune-system
- https://www.cancer.gov/ccg/research/computational-genomics/genomic-data-commons
- https://gdc.cancer.gov/about-gdc/contributed-genomic-data-cancer-research/count-me-cmi
- https://gdc.cancer.gov/news-and-announcements/browse-data-rare-cancers-data-portal
- https://data.humantumoratlas.org/
- https://datacommons.cancer.gov/repository/imaging-data-commons
- https://www.cancerimagingarchive.net/collection/pretreat-metstobrain-masks/
- https://www.aacr.org/professionals/research/aacr-project-genie/
- https://depmap.org/metmap/data/index.html
- https://pubmed.ncbi.nlm.nih.gov/38433721/
