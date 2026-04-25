# Investigación sobre metástasis en cánceres y oportunidades de descubrimiento con IA

Fecha: 2026-04-23 03:15:24 -03:00

## Objetivo
Responder tres preguntas:

- Qué es realmente la metástasis y cuáles son sus componentes más importantes a través de distintos tipos de cáncer.
- Qué clase de descubrimientos se pueden perseguir con IA sin hacer ensayos clínicos ni generar datos de pacientes nuevos.
- En qué tipos de cáncer o rutas metastásicas hay hoy más probabilidad de encontrar señales útiles con agentes de IA.

## Respuesta ejecutiva
La metástasis no es un único evento sino una cadena completa de procesos: invasión local, entrada a vasos, supervivencia en circulación, salida al tejido distante, adaptación al nuevo órgano, colonización, crecimiento y, en muchos casos, dormancia seguida de reactivación. NCI remarca que la metástasis causa la mayoría de las muertes por cáncer y que el proceso depende tanto de rasgos intrínsecos de la célula tumoral como del microambiente del órgano receptor.

La oportunidad real para IA no está en prometer curas automáticas, sino en acelerar descubrimiento computacional. Lo más valioso hoy es usar datos públicos para detectar programas metastásicos robustos, biomarcadores de riesgo, subtipos de metástasis, dependencias moleculares y patrones de organotropismo. Esto sí puede generar hipótesis fuertes, priorizar blancos, integrar literatura y preparar validaciones posteriores.

La mejor apuesta inicial para una línea de descubrimiento con agentes de IA parece ser cáncer colorrectal con metástasis hepática. La segunda apuesta más rica es cáncer de mama con metástasis a cerebro o hueso. La tercera, muy fuerte si queremos trabajar con imagen e histopatología, es cáncer de pulmón con metástasis cerebral.

## 1. Qué es la metástasis
Según NCI, el cáncer metastásico es aquel que se disemina desde su sitio primario hacia órganos distantes. Las células metastásicas conservan el nombre y rasgos esenciales del tumor de origen. En la secuencia descrita por NCI, las células tumorales:

- invaden tejido cercano
- atraviesan paredes de vasos linfáticos o sanguíneos
- circulan por el organismo
- se detienen en un sitio distante
- invaden ese nuevo tejido
- forman un microtumor
- inducen angiogénesis y continúan creciendo

Un punto importante es que muchas células diseminadas mueren. Sólo una fracción pequeña logra colonizar de verdad un órgano nuevo. Por eso la colonización metastásica y la dormancia son cuellos de botella biológicos mucho más interesantes que la simple diseminación.

## 2. Ideas biológicas que se repiten entre cánceres

### 2.1 Plasticidad celular
La rama de investigación de metástasis del NCI destaca la plasticidad fenotípica, incluyendo transición epitelio-mesenquimal y procesos relacionados. Esto importa porque la metástasis no depende sólo de mutaciones fijas: también depende de estados celulares reversibles.

### 2.2 Microambiente tumoral y órgano receptor
El NCI enfatiza que células inmunes, estromales y remodelado de matriz extracelular ayudan o frenan invasión y colonización. La metástasis no es sólo propiedad de la célula tumoral; es una interacción entre tumor y nicho.

### 2.3 Dormancia
Una de las áreas más prometedoras hoy es la dormancia metastásica. En abril de 2025, NCI subrayó que células tumorales diseminadas pueden permanecer dormidas durante meses, años o décadas antes de reactivarse. Si la IA puede encontrar firmas de dormancia o de reactivación, esa línea tendría enorme valor preventivo.

### 2.4 Organotropismo
No todos los cánceres metastatizan a los mismos órganos con la misma frecuencia. Hay afinidades preferenciales entre tumores primarios y órganos destino. Esa afinidad emerge de flujo sanguíneo, compatibilidad metabólica, nicho inmune, adhesión celular, estado epigenético y presión terapéutica.

### 2.5 Evolución clonal bajo tratamiento
Los tumores metastásicos suelen estar más moldeados por tratamiento previo, selección clonal y adaptación. Por eso los datasets metastásicos no se deben tratar como simples extensiones de TCGA primario.

## 3. Patrones importantes de metástasis por tipo de cáncer
NCI indica que, en conjunto, los sitios metastásicos más comunes son hueso, hígado y pulmón. También resume rutas frecuentes por tumor primario:

| Tumor primario | Sitios metastásicos frecuentes | Comentario para IA |
| --- | --- | --- |
| Mama | hueso, cerebro, hígado, pulmón | Excelente para estudiar dormancia, subtipos y organotropismo |
| Colon | hígado, pulmón, peritoneo | Muy buena línea por claridad clínica y foco hepático |
| Pulmón | adrenal, hueso, cerebro, hígado, otro pulmón | Ideal para imagen, histopatología y metástasis cerebral |
| Próstata | adrenal, hueso, hígado, pulmón | Muy fuerte para estudiar metástasis ósea |
| Melanoma | hueso, cerebro, hígado, pulmón, piel, músculo | Biología inmune muy rica, pero con cohorts más heterogéneas |
| Páncreas | hígado, pulmón, peritoneo | Altísimo impacto, aunque con mayor dificultad biológica |
| Riñón | adrenal, hueso, cerebro, hígado, pulmón | Interesante para evolución y angiogénesis |

Si pensamos en descubrimiento computacional, conviene priorizar problemas con tres rasgos al mismo tiempo:

- mucha carga clínica
- abundancia de datos abiertos
- una pregunta suficientemente focalizada como para permitir validación cruzada

## 4. Qué puede hacer la IA sin ensayos clínicos nuevos

### 4.1 Minería de literatura y grafos de conocimiento
Los agentes pueden leer miles de papers, extraer genes, vías, órganos destino, tipos celulares, biomarcadores y tratamientos, y construir un grafo de relaciones. Esto sirve para:

- detectar genes repetidos en un órgano metastásico concreto
- encontrar lagunas entre tipos de cáncer
- priorizar combinaciones gen-vía-órgano poco exploradas

### 4.2 Integración de cohortes genómicas metastásicas
Hoy ya existen cohortes metastásicas con exoma, RNA-seq y datos clínicos asociados. La IA puede:

- comparar primario versus metástasis
- comparar metástasis por órgano destino
- encontrar firmas conservadas entre cohortes
- separar señal biológica real de ruido por batch o tratamiento

### 4.3 Histopatología digital
La IA puede extraer patrones de láminas H&E que anticipen riesgo metastásico o sitio futuro de metástasis. Un ejemplo fuerte es el trabajo de 2024 que mostró predicción de metástasis cerebral en cáncer de pulmón a partir de histología del tumor primario.

### 4.4 Imagen y radiogenómica
Metástasis cerebral y metástasis ósea tienen datasets de imagen bastante útiles. Allí la IA puede:

- segmentar lesiones
- predecir evolución
- asociar rasgos de imagen con genómica o pronóstico
- aprender patrones invisibles a simple vista

### 4.5 Single-cell y espacial
Esta es una de las fronteras más interesantes. Los datos de célula única y transcriptómica espacial permiten estudiar:

- qué estados celulares dominan en un órgano metastásico
- qué células del microambiente ayudan a la colonización
- qué programas cambian entre primario y metástasis

### 4.6 Modelos preclínicos y dependencias
Sin tocar pacientes ni hacer clínica nueva, se pueden usar líneas celulares, organoides, PDX y mapas de dependencia genética para priorizar vulnerabilidades. Aquí la IA sirve para unir evidencia de pacientes con evidencia funcional.

## 5. Recursos concretos que hoy habilitan esta investigación

### 5.1 NCI Genomic Data Commons
El GDC de NCI es una pieza central. Según su página institucional, contiene datos genómicos de más de 33,000 pacientes con cáncer y funciona no sólo como repositorio sino como sistema de análisis. Para metástasis, es especialmente relevante porque incluye contribuciones no limitadas a tumores primarios.

### 5.2 Count Me In dentro de GDC
El programa Count Me In ya entregó a GDC datos de cáncer de mama metastásico y cáncer de próstata metastásico, con WES y RNA-seq. Una nota reciente del GDC indica acceso navegable a mutaciones de 200 pacientes de cáncer de mama metastásico y 30 de cáncer de próstata metastásico, además de angiosarcoma. Esto es importante porque son cohortes explícitamente metastásicas, no sólo primarias.

### 5.3 Human Tumor Atlas Network
HTAN es clave para evolución tumoral y estados celulares. En su portal actual reporta 14 atlas, 20 órganos y 2,372 casos. Para IA, esto abre la puerta a estudiar transición desde enfermedad localizada a avanzada, resistencia terapéutica y arquitectura celular.

### 5.4 Imaging Data Commons y TCIA
El Imaging Data Commons de NCI integra colecciones de TCIA, TCGA, CPTAC, HTAN y más. Para metástasis cerebral ya hay al menos varias colecciones útiles:

- `Pretreat-MetsToBrain-Masks`: 200 sujetos, MRI, segmentaciones, demografía, diagnóstico, seguimiento; incluye mama, melanoma y cáncer de pulmón.
- `Yale-Brain-Mets-Longitudinal`: dataset longitudinal de metástasis cerebrales.
- `Brain-Mets-Lung-MRI-Path-Segs`: 103 sujetos con MRI, segmentaciones y láminas patológicas emparejadas de metástasis cerebrales de origen pulmonar.

### 5.5 AACR Project GENIE
GENIE es un registro clínico-genómico público ensamblado por 20 centros oncológicos internacionales. Aunque no es exclusivo de metástasis, es muy útil para capturar enfermedad avanzada y validar asociaciones.

### 5.6 DepMap y MetMap
DepMap aporta metadata de origen primario o metastásico de líneas celulares. MetMap, desde Broad, ofrece un mapa de potencial metastásico órgano-específico en cientos de líneas y recursos de cohorte basal de mama con órganos como cerebro, pulmón, hígado, riñón y hueso. Esto es oro para generar hipótesis funcionales.

### 5.7 HCMI, PDXNet y PDMR
El Human Cancer Models Initiative y el ecosistema PDXNet/PDMR permiten conectar descubrimiento computacional con modelos derivados de pacientes, incluyendo PDX, organoides, cultivos y fibroblastos asociados al cáncer. Esto ayuda a priorizar hallazgos que luego puedan ser probados por un equipo experimental.

## 6. Líneas de descubrimiento donde la IA tiene mejor relación riesgo-recompensa

### 6.1 Predicción de organotropismo
Pregunta: dado un tumor primario, qué probabilidad hay de que metastatice a hígado, cerebro, hueso o pulmón.

Valor:
- clínicamente relevante
- técnicamente abordable
- fácil de plantear en cohorts retrospectivas

Riesgo:
- muchos modelos capturan sesgos del tejido de origen y del tratamiento, no causalidad

### 6.2 Dormancia y reactivación
Pregunta: qué programas permiten que una célula diseminada sobreviva dormida y luego se reactive.

Valor:
- altísimo impacto biológico
- hoy sigue siendo una frontera abierta

Riesgo:
- etiquetas imperfectas
- datos longitudinales todavía escasos

### 6.3 Subtipos metastásicos transversales
Ya existen trabajos que proponen subtipos pan-cáncer de metástasis basados en transcriptómica. Un buen proyecto con agentes sería revisar si esos subtipos se sostienen al integrar cohorts nuevas, single-cell y espacial.

### 6.4 Predicción desde histología o imagen
El trabajo de 2024 sobre metástasis cerebral en pulmón muestra que esta dirección ya produce resultados concretos. La ventaja es que las imágenes son abundantes. La desventaja es que un modelo puede ser preciso pero poco interpretable.

### 6.5 Priorización de blancos y reposicionamiento
La IA puede unir literatura, expresión, dependencia genética, redes de proteínas y metástasis órgano-específica para priorizar genes o combinaciones terapéuticas. Esto no reemplaza validación, pero sí reduce el espacio de búsqueda.

## 7. Qué tipos de cáncer o problemas conviene investigar primero

| Prioridad | Línea | Probabilidad de descubrimiento con IA | Motivo principal |
| --- | --- | --- | --- |
| 1 | Colorrectal -> hígado | Muy alta | Fenotipo claro, alto volumen clínico, problema bien acotado, buena validación cruzada |
| 2 | Mama -> cerebro/hueso | Muy alta | Subtipos ricos, dormancia, datasets metastásicos y de imagen disponibles |
| 3 | Pulmón -> cerebro | Alta | Muy buena combinación de histopatología, MRI y problema clínico fuerte |
| 4 | Próstata -> hueso | Alta | Organotropismo muy marcado y biología ósea muy específica |
| 5 | Pan-cáncer -> metástasis hepática | Alta | Permite descubrir programas comunes entre tejidos de origen distintos |
| 6 | Melanoma -> cerebro | Media-alta | Interesantísimo en inmunología, pero más fragmentado en datos |
| 7 | Páncreas -> hígado/peritoneo | Media | Gran impacto pero más difícil por heterogeneidad y menor abundancia de cohorts abiertas de calidad homogénea |

## 8. Mi recomendación concreta
Si el criterio es "dónde tengo más probabilidad de descubrir algo útil con agentes de IA", empezaría por una de estas dos:

### Opción A
`cáncer colorrectal con metástasis hepática`

Por qué:
- la pregunta es limpia
- la metástasis al hígado es central en la historia natural del tumor
- hay valor clínico inmediato en entender riesgo, colonización y microambiente
- permite unir transcriptómica, espacial, imagen e incluso reposicionamiento

### Opción B
`cáncer de mama con metástasis a cerebro y hueso`

Por qué:
- enorme riqueza biológica
- subtipos bien definidos
- relación fuerte con dormancia y reactivación
- hay cohorts metastásicas explícitas y datasets de imagen útiles

Si quisiéramos una tercera línea especializada en visión computacional:

### Opción C
`cáncer de pulmón con metástasis cerebral`

Por qué:
- ya existe evidencia de que H&E del tumor primario contiene señal predictiva
- hay datasets de MRI y patología emparejada
- permite una línea muy compatible con agentes de IA orientados a imagen

## 9. Qué puede descubrir realmente un sistema de agentes
Un sistema de agentes bien organizado puede:

- levantar y comparar cohorts
- limpiar metadata
- generar hipótesis y someterlas a validación cruzada
- construir tablas de evidencia gen-vía-órgano
- revisar cientos de papers y producir síntesis reproducibles
- detectar contradicciones entre estudios
- sugerir un ranking de blancos o biomarcadores

Lo que no puede hacer solo es demostrar beneficio clínico. La salida correcta de este trabajo no es "hemos curado la metástasis", sino "hemos aislado una hipótesis prioritaria, reproducible, explicable y lista para validación experimental o clínica".

## 10. Propuesta de siguiente ola
La siguiente ola debería ser estrecha y no panorámica. Recomiendo una investigación dedicada a:

`Cancer colorrectal -> metástasis hepática`

La pregunta operativa podría ser:

"Qué programas transcriptómicos, espaciales y microambientales distinguen a los tumores colorrectales que colonizan hígado, y qué targets o biomarcadores aparecen de manera consistente en datasets independientes."

## Fuentes base
- NCI, Metastatic Cancer: When Cancer Spreads: https://www.cancer.gov/types/metastatic-cancer
- NCI, Tumor Metastasis Research: https://www.cancer.gov/about-nci/organization/dcb/research-portfolio/tumor-metastasis
- NCI, Expanding Research on Dormant Cancer Cells Aims to Prevent Metastasis: https://www.cancer.gov/news-events/cancer-currents-blog/2025/metastasis-dormant-cancer-cells-immune-system
- NCI, What Is Cancer?: https://www.cancer.gov/cancertopics/cancerlibrary/what-is-cancer
- NCI GDC overview: https://www.cancer.gov/ccg/research/computational-genomics/genomic-data-commons
- GDC, Count Me In: https://gdc.cancer.gov/about-gdc/contributed-genomic-data-cancer-research/count-me-cmi
- GDC, Browse Data from Rare Cancers in the Data Portal: https://gdc.cancer.gov/news-and-announcements/browse-data-rare-cancers-data-portal
- NCI HTAN: https://www.cancer.gov/about-nci/organization/dcb/research-programs/htan
- HTAN Data Portal: https://data.humantumoratlas.org/
- NCI Imaging Data Commons: https://datacommons.cancer.gov/repository/imaging-data-commons
- NCI note on TCIA metastasis dataset updates: https://www.cancer.gov/about-nci/organization/cbiit/news-events/news/2024/cancer-imaging-archive-updates-data-set-collections
- TCIA Pretreat-MetsToBrain-Masks: https://www.cancerimagingarchive.net/collection/pretreat-metstobrain-masks/
- TCIA Yale-Brain-Mets-Longitudinal: https://www.cancerimagingarchive.net/collection/yale-brain-mets-longitudinal/
- TCIA Brain-Mets-Lung-MRI-Path-Segs: https://www.cancerimagingarchive.net/collection/brain-mets-lung-mri-path-segs/
- AACR Project GENIE: https://www.aacr.org/professionals/research/aacr-project-genie/
- DepMap metadata: https://depmap.org/rnai/data/index
- MetMap data: https://depmap.org/metmap/data/index.html
- Human Cancer Models Initiative: https://www.cancer.gov/ccg/research/functional-genomics/hcmi
- PDXNet: https://dctd.cancer.gov/research/networks/precision-medicine-oncology/pdxnet
- PDMR models: https://dctd.cancer.gov/drug-discovery-development/reagents-materials/pdmr/models
- Nature, Pan-cancer whole-genome analyses of metastatic solid tumours (2019): https://www.nature.com/articles/s41586-019-1689-y
- Cell Reports Medicine, Pan-cancer molecular subtypes of metastasis reveal distinct and evolving transcriptional programs (2023): https://pmc.ncbi.nlm.nih.gov/articles/PMC9975284/
- Single-cell atlas of pan-cancer liver metastasis (2026): https://pmc.ncbi.nlm.nih.gov/articles/PMC13010057/
- Cell Reports Medicine, A pan-cancer single-cell transcriptomic atlas of human bone metastases (2026): https://www.sciencedirect.com/science/article/pii/S2666379125006561
- Journal of Pathology, AI-guided histopathology predicts brain metastasis in lung cancer patients (2024): https://pubmed.ncbi.nlm.nih.gov/38433721/
- Cancers, Artificial Intelligence in Detection, Management, and Prognosis of Bone Metastasis: A Systematic Review (2024): https://pmc.ncbi.nlm.nih.gov/articles/PMC11311270/
- BioScience Trends, Artificial intelligence in colorectal cancer liver metastases: From classification to precision medicine (2025): https://pubmed.ncbi.nlm.nih.gov/40240167/
