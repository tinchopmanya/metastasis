# Resumen de investigación sobre cáncer colorrectal y metástasis hepática

Fecha: 2026-04-23 03:28:33 -03:00

## Resumen corto
El cáncer colorrectal con metástasis hepática es, probablemente, la mejor línea disponible para una investigación seria con agentes de IA sobre metástasis. La razón principal es que combina tres ventajas a la vez: alta relevancia clínica, una pregunta biológica muy concreta y un ecosistema de datos públicos bastante mejor que en otras rutas metastásicas. En 2025, SEER estima 154,270 casos nuevos y 52,900 muertes por cáncer colorrectal en Estados Unidos. Además, el PDQ del NCI indica que aproximadamente el 50% de los pacientes con cáncer de colon desarrollarán metástasis hepáticas ya sea al diagnóstico o por recurrencia. Esto vuelve al hígado el gran punto crítico de la enfermedad avanzada.

La biología de esta ruta también la hace especialmente atractiva. La evidencia actual sugiere que, en muchos casos, la siembra metastásica ocurre temprano y que el verdadero cuello de botella no es sólo que células tumorales lleguen al hígado, sino que logren colonizarlo, remodelar el nicho, escapar del sistema inmune y sostener crecimiento o recurrencia. Los trabajos recientes de single-cell y spatial transcriptomics muestran que las metástasis hepáticas colorrectales no son una masa uniforme: contienen subestados tumorales, fibroblastos específicos, macrófagos y programas metabólicos particulares que parecen cooperar entre sí.

Hoy ya existen recursos concretos para trabajar esto sin hacer clínica nueva: TCGA COAD/READ vía GDC para baseline de primario; el dataset `Colorectal-Liver-Metastases` de TCIA con 197 pacientes, CT preoperatorio, segmentaciones y supervivencia; `GSE225857` para single-cell y spatial en muestras emparejadas; atlas espaciales usados desde `scCRLM`; cohorts metastásicas como META-PRISM; y modelos derivados de pacientes como organoides y PDX. Dentro de esta ruta, la mejor apuesta biológica para agentes de IA es estudiar el nicho metastásico hepático, especialmente ejes fibroblasto-macrófago-metabolismo-inmunidad. La mejor apuesta técnica rápida, en cambio, es construir modelos de recurrencia post-hepatectomía sobre TCIA. Si la meta es descubrir algo realmente interesante, empezaría por el nicho metastásico.

## Resumen extendido
El cáncer colorrectal con metástasis hepática merece una ola propia porque reúne, mejor que casi cualquier otra ruta metastásica, impacto clínico, claridad conceptual y posibilidad real de descubrimiento computacional. No es sólo una línea importante: es una de las pocas donde se puede pasar de revisión panorámica a una agenda de trabajo concreta apoyada en datos abiertos relativamente maduros. El punto de partida es fuerte por sí solo. Según SEER, para 2025 se estiman 154,270 casos nuevos de cáncer colorrectal y 52,900 muertes en Estados Unidos. El PDQ del NCI añade que aproximadamente el 50% de los pacientes con cáncer de colon presentarán metástasis hepáticas ya sea en la presentación inicial o como recurrencia. El hígado, entonces, no es un destino secundario anecdótico; es el órgano donde se juega gran parte del fracaso terapéutico del cáncer colorrectal.

También es importante que el mismo PDQ del NCI recuerde que la resección quirúrgica, cuando la enfermedad está limitada y es factible, es la única opción potencialmente curativa para enfermedad localmente recurrente o para metástasis limitadas a hígado y/o pulmón. Eso ordena la investigación: si un proyecto ayuda a entender por qué algunos pacientes recaen, por qué algunas lesiones son resecables y otras no, o qué programas biológicos sostienen colonización hepática, el resultado puede tener relevancia clínica real. No necesariamente inmediata, pero sí muy directa.

Desde el lado biológico, esta ruta es más rica de lo que parece. Durante años se pensó que las metástasis aparecían más tarde, después de mucha evolución tumoral. Pero el NCI resumió en 2019 un estudio de Nature Genetics que sugiere lo contrario para muchos casos de cáncer colorrectal metastásico: la diseminación puede empezar bastante temprano. En esa cohorte, 17 de 21 pacientes mostraban evidencia de siembra temprana. Además, el estudio sugirió que ciertas combinaciones de mutaciones aparecen con más frecuencia en tumores metastásicos que en tumores no metastásicos. Esto cambia el enfoque de investigación. Ya no basta con preguntar qué aparece sólo en la metástasis; también hay que buscar qué señales tempranas del primario predisponen a tropismo hepático.

Ahora bien, llegar al hígado no es suficiente. El gran cuello de botella parece ser la colonización exitosa. Para que eso ocurra, las células tumorales deben adaptarse a un microambiente hepático muy particular, evitar o desviar la respuesta inmune, remodelar matriz y cooperar con células locales. Esa es precisamente la zona donde la IA tiene más potencial para producir hallazgos útiles. Porque los hallazgos interesantes hoy no suelen ser listas de genes aislados, sino programas funcionales y relaciones entre tipos celulares.

Los recursos más prometedores para esto son single-cell y spatial transcriptomics. Un recurso clave es `GSE225857`, cuyo resumen en GEO describe un estudio que trazó el paisaje celular de cáncer colorrectal y metástasis hepática emparejada. Allí se generaron perfiles single-cell y espaciales a partir de seis pacientes, y se reportaron hallazgos como el aumento de subpoblaciones `CD8_CXCL13` y `CD4_CXCL13` en muestras metastásicas hepáticas, además de diferencias claras entre perfiles fibroblásticos del primario y de la metástasis. La misma ficha GEO menciona fibroblastos `MCAM+` enriquecidos en metástasis hepática, con un posible papel en la generación de estados T a través de señalización Notch. Ese tipo de resultado es ideal para una estrategia con agentes: no es todavía una conclusión definitiva, pero sí una hipótesis estructurada y validable.

La literatura de 2025 empuja todavía más en esa dirección. Un atlas integrado de scRNA y spatial describe una interacción estroma-tumor basada en un eje `HGF-MET-MYC-glycolysis`, sugiriendo que parte del éxito metastásico podría depender de cooperación metabólica y espacial entre células tumorales y fibroblastos del nicho. Esta línea es especialmente interesante porque une varias capas que suelen aparecer por separado en la literatura: plasticidad tumoral, metabolismo, soporte estromal y progresión metastásica. Si una firma así se reprodujera en otros cohorts, pasaría rápidamente a ser una de las hipótesis más valiosas del proyecto.

La otra gran ventaja de esta línea es el ecosistema de datos. Para bulk multi-omics de tumor primario, GDC y TCGA COAD/READ siguen siendo la base. No son cohorts metastásicas puras, así que no sirven para todo, pero son muy útiles para validar si una firma derivada de metástasis ya estaba insinuada en el primario o si se asocia con pronóstico. Para imagen, el dataset `Colorectal-Liver-Metastases` de TCIA es central: 197 pacientes, CT preoperatorio, segmentaciones, variables clínicas y supervivencia. Scientific Data lo presenta como el mayor dataset de su tipo para CRLM y como un recurso diseñado para el desarrollo de biomarcadores cuantitativos y modelos de aprendizaje automático orientados a recurrencia o supervivencia tras resección.

Aquí aparece una distinción importante. Si lo que buscamos es producir hallazgo biológico, la mejor sublínea es el nicho metastásico hepático. Si lo que queremos es construir algo rápido, sólido y fácilmente medible, entonces la mejor entrada es recurrencia post-hepatectomía con imagen preoperatoria. Ese segundo camino es menos ambicioso biológicamente, pero mucho más limpio desde el punto de vista ingenieril. Y además puede servir como plataforma de validación cruzada: si una firma espacial o transcriptómica parece importante, después podemos preguntar si también deja huella radiológica.

Hay una tercera línea muy interesante, más translacional, que combina organoides y multi-omics. Trabajos recientes ya generaron organoides emparejados entre tumor colorrectal primario y metástasis hepática, incluso biobancos vivos relativamente grandes. Un estudio de 2025 destacó que modelos de machine learning sobre organoides y multi-omics apuntaban a señalización `KRAS` y `TGF-beta` como reguladores importantes del comportamiento metastásico. Eso no significa que ya tengamos un target listo para clínica, pero sí que existe una vía concreta para conectar hallazgos computacionales con modelos que pueden validar sensibilidad a drogas.

La conclusión más útil para avanzar es simple: dentro de `cáncer colorrectal -> metástasis hepática`, la mayor probabilidad de descubrimiento real con agentes de IA está en mapear el nicho metastásico hepático, no en hacer una simple clasificación. La mejor pregunta para una próxima ola es cuáles estados tumorales, fibroblásticos, mieloides e interacciones espaciales distinguen a la metástasis hepática colorrectal y cuáles de esas señales se sostienen en cohorts independientes. Si en lugar de eso queremos un proyecto más rápido y más cuantificable, entonces conviene ir por predicción de recurrencia post-resección en TCIA. Las dos líneas son buenas, pero si la meta es descubrir algo importante, empezaría por el nicho.

## Recomendación operativa
Recomendación principal:

`InvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`

Recomendación secundaria:

`InvestigacionSobreRecurrenciaPostHepatectomiaEnCRLM.md`

## Fuentes base
- https://seer.cancer.gov/statfacts/html/colorect.html
- https://www.cancer.gov/types/common-cancers
- https://www.cancer.gov/types/colorectal/hp/colon-treatment-pdq
- https://www.cancer.gov/news-events/cancer-currents-blog/2019/early-metastasis-colorectal-cancer
- https://www.nature.com/articles/s41588-019-0423-x
- https://www.cancerimagingarchive.net/collection/colorectal-liver-metastases/
- https://www.nature.com/articles/s41597-024-02981-2
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10275599/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10157368/
- https://pubmed.ncbi.nlm.nih.gov/40240167/
