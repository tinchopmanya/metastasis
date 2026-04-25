# Investigación sobre cáncer colorrectal y metástasis hepática

Fecha: 2026-04-23 03:28:33 -03:00

## Objetivo
Responder cuatro preguntas:

- Por qué la metástasis hepática del cáncer colorrectal es una línea tan fuerte para investigar.
- Qué sabemos hoy, con suficiente respaldo, sobre la biología de esta ruta metastásica.
- Qué datos públicos permiten estudiarla sin generar clínica nueva.
- En qué subproyectos concretos los agentes de IA tienen más probabilidad de producir hallazgos útiles.

## Respuesta ejecutiva
Sí, esta es probablemente la mejor línea para una investigación computacional seria sobre metástasis. El cáncer colorrectal sigue siendo uno de los cánceres más comunes: SEER estima 154,270 casos nuevos y 52,900 muertes en 2025 en Estados Unidos. Además, el NCI señala que aproximadamente el 50% de los pacientes con cáncer de colon desarrollarán metástasis hepáticas al diagnóstico o por recurrencia. Esa frecuencia convierte al hígado en el órgano más importante para entender el fracaso clínico del cáncer colorrectal.

La ruta `cáncer colorrectal -> hígado` no es valiosa sólo por frecuencia. También tiene una ventaja metodológica: el problema está bien delimitado. Hay una pregunta anatómica clara, una historia natural conocida, datasets de imagen específicos, cohorts transcriptómicas, estudios single-cell y espaciales, y hasta organoides emparejados entre tumor primario y metástasis hepática. Eso permite validación cruzada real, que es exactamente lo que necesita una estrategia con agentes de IA.

Mi lectura actual es que dentro de esta línea hay dos apuestas distintas:

- Si queremos la mayor probabilidad de descubrimiento biológico, la mejor sublínea es estudiar el nicho metastásico hepático, especialmente los programas fibroblasto-macrófago-metabolismo-inmunidad que sostienen colonización, fibrosis e inmunorresistencia.
- Si queremos construir algo más rápido y verificable con un dataset muy claro, la mejor sublínea es predecir recurrencia o supervivencia post-hepatectomía usando el dataset de TCIA de 197 pacientes con metástasis hepáticas colorrectales resecadas.

## 1. Por qué esta línea importa tanto

### 1.1 Carga clínica
SEER estima para 2025:

- 154,270 casos nuevos de cáncer colorrectal
- 52,900 muertes

El PDQ del NCI sobre cáncer de colon indica que aproximadamente la mitad de los pacientes presentarán metástasis hepáticas ya sea al inicio o en la recurrencia. El mismo PDQ remarca que, para enfermedad localmente recurrente y/o metástasis limitadas a hígado o pulmón, la resección quirúrgica, cuando es factible, es la única opción potencialmente curativa.

### 1.2 El hígado no es sólo un destino frecuente, es el cuello de botella clínico
En esta enfermedad, muchas decisiones terapéuticas reales giran alrededor del hígado:

- resecabilidad
- conversión de irresecable a resecable
- riesgo de recurrencia intrahepática
- respuesta a quimioterapia
- interacción entre lesión, parénquima hepático y sistema inmune

Eso vuelve a CRLM un problema ideal para IA: hay endpoints claros, biología rica y señales medibles en múltiples capas de datos.

## 2. Qué sabemos hoy sobre la biología de CRLM

### 2.1 La diseminación puede ocurrir muy temprano
El NCI resumió en julio de 2019 un estudio de Nature Genetics mostrando que muchos cánceres colorrectales metastásicos probablemente diseminan células muy temprano en la evolución tumoral. En la cohorte analizada, 17 de 21 pacientes mostraban evidencia de siembra metastásica temprana. El artículo también sugirió que combinaciones concretas de mutaciones tempranas podrían marcar tumores con alto potencial metastásico.

Esto importa mucho para IA porque cambia la pregunta. Ya no se trata sólo de buscar eventos tardíos exclusivos de la metástasis; también hay que buscar programas tempranos que ya estén presentes en el tumor primario y predisponen a colonizar el hígado.

### 2.2 El problema no es sólo llegar al hígado, sino colonizarlo
La anatomía portal ayuda a explicar por qué el hígado es un destino frecuente, pero no basta. La colonización hepática requiere:

- adaptación metabólica
- evasión inmune
- remodelado de matriz extracelular
- cooperación con fibroblastos, macrófagos y células del nicho hepático
- tolerancia a tratamiento y, a veces, dormancia

Por eso, una lista simple de genes diferencialmente expresados rara vez alcanza. La señal más interesante está en interacciones celulares y estados funcionales.

### 2.3 El microambiente hepático parece ser decisivo
La literatura reciente enfatiza el nicho premetastásico e inmunosupresor del hígado. Las revisiones sobre CRLM describen al hígado como un órgano con una ecología inmune propia, capaz de favorecer tolerancia y apagar respuestas antitumorales. Esto ayuda a explicar por qué muchas metástasis hepáticas de colorrectal, en especial MSS, son difíciles para inmunoterapia.

### 2.4 El frente actual está en single-cell y espacial
Las capas de mayor valor hoy no son sólo bulk RNA-seq o mutaciones. Son:

- scRNA-seq
- spatial transcriptomics
- multi-omics integradas
- modelos derivados de pacientes

Un ejemplo especialmente útil es `GSE225857`, un estudio público cuyo título en GEO es "Single-cell and spatial transcriptome analysis reveals the cellular heterogeneity of liver metastatic colorectal cancer". Allí se describen 27 muestras de 6 pacientes con tejido primario, metástasis hepática, tejidos normales adyacentes y sangre periférica. La propia ficha GEO resume hallazgos muy accionables:

- aumento de subpoblaciones `CD8_CXCL13` y `CD4_CXCL13` en metástasis hepática
- perfiles fibroblásticos distintos entre tumor primario y metástasis
- enriquecimiento de fibroblastos `MCAM+` en metástasis hepática, con posible promoción de estados T específicos vía señalización Notch

Más recientemente, un atlas integrado de 2025 describió una interacción espacialmente resuelta entre estroma y tumor basada en señalización glicolítica, destacando un eje `HGF-MET-MYC-glycolysis` como posible mecanismo de soporte metastásico.

### 2.5 Heterogeneidad real, no ruido
CRLM no es una entidad homogénea. La heterogeneidad aparece en varios niveles:

- lado del tumor primario
- KRAS y otros drivers
- exposición previa a tratamiento
- resecabilidad
- inmunofenotipo
- estados fibroblásticos
- estados macrófago/mieloides
- arquitectura espacial dentro de la lesión

La consecuencia práctica es importante: los agentes de IA no deberían buscar "el gen maestro de la metástasis hepática", sino subtipos, programas y nichos reproducibles.

## 3. Datasets y recursos públicos que hoy sí permiten trabajar

### 3.1 GDC / TCGA COAD-READ
El GDC del NCI sigue siendo la base para bulk multi-omics en colorrectal. La publicación clásica de TCGA COAD/READ, accesible desde GDC, analizó 276 muestras con exoma, copy number, metilación, mRNA y miRNA.

Uso real para esta investigación:

- establecer baseline de tumor primario
- validar firmas transcriptómicas
- contrastar genes o vías encontradas en metástasis
- entrenar modelos de riesgo desde tumor primario, con la limitación de que TCGA no es una cohorte metastásica pura

### 3.2 TCIA Colorectal-Liver-Metastases
Este es el dataset más importante para la vía imagen-radiomics:

- 197 pacientes
- CT preoperatorio
- segmentaciones DICOM
- variables demográficas, de medición y tratamiento
- datos clínicos y de supervivencia

La página de TCIA y el artículo de Scientific Data 2024 lo describen como el dataset más grande de su tipo para desarrollar biomarcadores de imagen y modelos de aprendizaje automático orientados a recurrencia y supervivencia después de resección.

Uso real para esta investigación:

- predicción de recurrencia hepática post-resección
- segmentación automática de metástasis
- estimación de remanente hepático
- integración imagen-clínica

### 3.3 GEO GSE225857
Ya mencionado, es uno de los recursos más valiosos para preguntas de ecología tumoral. Tiene:

- single-cell
- spatial
- pares primario/metástasis
- tejidos normales asociados

Uso real:

- reconstrucción de estados celulares metastásicos
- ligand-receptor analysis
- identificación de nichos fibroblasto-inmune-tumor
- priorización de firmas para validar en bulk o imagen

### 3.4 scCRLM / Cancer Diversity Asia
Varios trabajos recientes usan el portal `scCRLM` de Cancer Diversity Asia como recurso de spatial transcriptomics para CRC y CRLM. Distintos artículos lo describen como un atlas web con al menos cuatro muestras tumorales espaciales de CRC utilizadas para análisis espaciales y validación.

Uso real:

- validar organización espacial de nichos
- comparar bordes invasivos frente a regiones centrales
- estudiar co-localización de fibroblastos, macrófagos y subpoblaciones tumorales

### 3.5 META-PRISM
El cohort META-PRISM analizó 1,031 tumores metastásicos refractarios con exoma y transcriptoma. El sitio metastásico biopsiado con mayor frecuencia fue hígado, con 37% de los casos. Además, el artículo destaca que biomarcadores estándar de resistencia estaban clínicamente validados sólo en pocos tumores, incluyendo colon.

Uso real:

- comparar firmas metastásicas de colon con otros tumores avanzados
- verificar si una señal encontrada en CRLM es específica o pan-metastásica
- distinguir programas de resistencia asociados a tratamiento

### 3.6 PDMR / HCMI / organoides emparejados
El ecosistema de modelos del NCI, especialmente PDMR y HCMI, aporta modelos derivados de pacientes. Además, trabajos recientes han construido:

- organoides pareados primario-hígado
- biobancos vivos de CRLM
- perfiles multi-ómicos con screening de fármacos

Un trabajo de 2025 sobre organoides pareados reportó que modelos y análisis de machine learning resaltaron señalización `KRAS` y `TGF-beta` como reguladores importantes del comportamiento metastásico.

Uso real:

- validar hipótesis computacionales
- hacer priorización de vulnerabilidades
- conectar signatures con sensibilidad a drogas

## 4. Dónde los agentes de IA tienen más probabilidad de descubrir algo

### 4.1 Mejor apuesta biológica: nicho metastásico hepático
Pregunta:

Qué programas celulares y espaciales sostienen colonización, fibrosis, inmunorresistencia y recurrencia en CRLM.

Por qué es fuerte:

- hay señal biológica rica
- hay datos single-cell y spatial
- permite hipótesis nuevas, no sólo clasificación
- se puede validar en bulk, imagen y modelos derivados de pacientes

Salida esperable:

- subtipos de nicho metastásico
- genes y vías candidatas
- ejes ligand-receptor reproducibles
- ranking de targets para validación

Mi lectura:

Esta es la mejor sublínea si la meta es un hallazgo interesante y potencialmente publicable.

### 4.2 Mejor apuesta técnica rápida: recurrencia post-hepatectomía con CT
Pregunta:

Podemos predecir recurrencia hepática temprana o supervivencia usando CT preoperatorio, segmentaciones y clínica básica.

Por qué es fuerte:

- dataset muy claro
- endpoint concreto
- benchmarking posible contra trabajos recientes
- relativamente fácil de operacionalizar

Salida esperable:

- pipeline reproducible
- modelo base
- mapa de variables de mayor valor
- comparación entre radiomics clásico y modelos más modernos

Mi lectura:

Esta es la mejor sublínea si la meta es construir rápido y medir bien.

### 4.3 Mejor apuesta translacional: organoides + multi-omics + priorización de drogas
Pregunta:

Qué vulnerabilidades se mantienen entre tumor primario, metástasis hepática y modelos derivados de pacientes.

Por qué es fuerte:

- acerca el trabajo a validación experimental
- obliga a priorizar targets más robustos
- permite filtrar hallazgos débiles

Salida esperable:

- shortlist de vías
- hipótesis de reposicionamiento
- targets ligados a KRAS, TGF-beta, MET o metabolismo

Mi lectura:

Muy interesante, pero más dependiente de integrar papers y recursos dispersos.

### 4.4 Apuesta de riesgo medio: firma temprana de tropismo hepático desde el primario
Pregunta:

Existe una firma en el tumor primario que anticipe con robustez riesgo de metástasis hepática.

Por qué es valiosa:

- clínicamente muy potente
- conectada con la evidencia de siembra temprana

Riesgo:

- las cohorts primarias abiertas no siempre tienen etiquetas metastásicas limpias
- el confounding clínico es mayor

Mi lectura:

Vale la pena, pero no como primer paso.

## 5. Plan de investigación recomendado dentro de esta línea

### Ruta A: descubrimiento biológico
Secuencia sugerida:

1. Integrar `GSE225857`, `scCRLM`, y literatura single-cell/spatial reciente.
2. Definir estados tumorales, fibroblásticos y mieloides enriquecidos en hígado.
3. Construir una tabla de interacciones candidatas.
4. Validar en bulk TCGA COAD/READ y en cohorts metastásicas públicas.
5. Ver si alguna firma se asocia con recurrencia o mal pronóstico en TCIA y estudios externos.

### Ruta B: sistema reproducible rápido
Secuencia sugerida:

1. Tomar `TCIA Colorectal-Liver-Metastases`.
2. Reproducir segmentaciones y features básicos.
3. Construir baseline clínico-radiomics.
4. Probar modelos modernos y comparar.
5. Evaluar si zonas peritumorales o parénquima hepático aportan señal extra.

### Ruta C: terapia y vulnerabilidades
Secuencia sugerida:

1. Extraer vías repetidas en CRLM: MET, TGF-beta, fibrosis, glicólisis, inmunorresistencia.
2. Cruzarlas con organoides pareados y recursos de sensibilidad a fármacos.
3. Priorizar combinaciones plausibles para validación.

## 6. Lo que me parece más prometedor hoy
Mi hipótesis central actual es esta:

La mejor probabilidad de descubrimiento con IA en CRLM no está en encontrar una sola mutación nueva, sino en identificar un programa metastásico de nicho hepático reproducible, compuesto por:

- subestado tumoral de alta plasticidad
- fibroblastos metastáticos específicos
- soporte metabólico local
- supresión inmune o desvío inmune

Los candidatos que más llaman la atención en la literatura reciente son:

- señalización `HGF-MET`
- activación `MYC`
- glicólisis y metabolismo del nicho
- fibrosis/hepatic remodeling
- ejes fibroblasto-T cell o fibroblasto-macrófago

Esto no quiere decir que esos ejes ya estén "demostrados" como causa única. Sí quiere decir que son un muy buen punto de partida para una investigación computacional seria.

## 7. Riesgos metodológicos

- Muchos datasets metastásicos son pequeños.
- Muchas muestras vienen de pacientes ya tratados.
- Resección hepática introduce sesgo de selección hacia enfermedad más favorable.
- TCGA sirve más como baseline de primario que como cohorte metastásica directa.
- Los modelos de IA pueden aprender señal del hospital o del protocolo en vez de biología.
- Correlación no equivale a mecanismo causal.

## 8. Recomendación final
Para una siguiente ola ya no panorámica, recomiendo empezar por:

`nicho metastásico hepático en cáncer colorrectal`

Nombre sugerido:

`InvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`

Objetivo sugerido:

Definir qué estados tumorales, fibroblásticos, mieloides e interacciones espaciales distinguen la metástasis hepática colorrectal y cuáles de esas señales son reproducibles en datos públicos independientes.

Si en cambio queremos una línea más ingenieril y rápida de verificar:

`InvestigacionSobreRecurrenciaPostHepatectomiaEnCRLM.md`

## Fuentes base
- SEER Cancer Stat Facts: Colorectal Cancer: https://seer.cancer.gov/statfacts/html/colorect.html
- NCI Common Cancer Types: https://www.cancer.gov/types/common-cancers
- NCI PDQ Colon Cancer Treatment: https://www.cancer.gov/types/colorectal/hp/colon-treatment-pdq
- NCI blog, early spread in metastatic colorectal cancer: https://www.cancer.gov/news-events/cancer-currents-blog/2019/early-metastasis-colorectal-cancer
- Nature Genetics, early metastatic seeding in colorectal cancer: https://www.nature.com/articles/s41588-019-0423-x
- TCIA Colorectal-Liver-Metastases: https://www.cancerimagingarchive.net/collection/colorectal-liver-metastases/
- Scientific Data 2024, preoperative CT and survival data for CRLM: https://www.nature.com/articles/s41597-024-02981-2
- GEO GSE225857: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857
- Science Advances / GEO-linked single-cell and spatial study of liver metastatic CRC: https://pmc.ncbi.nlm.nih.gov/articles/PMC10275599/
- 2025 integrated spatial/single-cell atlas with stromal-tumor glycolytic signaling: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
- META-PRISM metastatic cohort: https://pmc.ncbi.nlm.nih.gov/articles/PMC10157368/
- Review on AI in CRLM: https://pubmed.ncbi.nlm.nih.gov/40240167/
- Review on immune landscape and therapy in CRLM: https://pubmed.ncbi.nlm.nih.gov/37480104/
- PDMR models: https://dctd.cancer.gov/drug-discovery-development/reagents-materials/pdmr/models
- HCMI: https://www.cancer.gov/ccg/research/functional-genomics/hcmi
- Multi-omics paired organoids in primary CRC and liver metastasis: https://pmc.ncbi.nlm.nih.gov/articles/PMC12637260/
