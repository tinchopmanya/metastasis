# Resumen de investigación sobre nicho metastásico hepático en cáncer colorrectal

Fecha: 2026-04-25 01:06:15 -03:00

## Resumen corto
La ola 003 se enfoca en una hipótesis concreta: CAFs/mCAFs del hígado podrían crear nichos metabólicos e inmunomoduladores que favorecen células tumorales colorrectales plásticas mediante señalización `HGF-MET`, activación `MYC` y glicólisis local. Esta línea es atractiva porque deja de tratar la metástasis hepática colorrectal como un simple destino anatómico y la convierte en un ecosistema espacial: tumor, estroma, metabolismo e inmunidad interactuando en regiones específicas.

La evidencia principal viene de un estudio 2025 que integró 35 datasets single-cell RNA-seq y spatial transcriptomics. Ese trabajo describió células tumorales `High-M CRC`, enriquecidas en metástasis hepáticas, con stemness, actividad `MYC` y glicólisis, además de CAFs/mCAFs que podrían activar el eje `HGF-MET-MYC`. `GSE225857` aporta una segunda capa de evidencia: fibroblastos `MCAM+` enriquecidos en metástasis hepática y células T `CXCL13+`, con posible comunicación vía Notch. Una tercera línea reciente apunta a macrófagos con metabolismo lipídico elevado en CRLM, compatible con la idea de que el hígado metastásico funciona como nicho metabólico e inmunomodulador.

La salida correcta por ahora no es afirmar causalidad clínica. La salida útil es construir una matriz de hipótesis priorizadas y preparar validación computacional: gene sets para `mCAF`, `High-M CRC`, `HGF-MET`, `MYC`, glicólisis, `MCAM+ CAFs`, `CXCL13+ T cells` y macrófagos lipídicos; luego probar si esas señales se reproducen en GEO, TCGA/META-PRISM y eventualmente TCIA.

## Resumen extendido
La pregunta de esta ola es deliberadamente estrecha: qué hace que el hígado sea un nicho fértil para la metástasis colorrectal, y qué parte de ese proceso puede investigarse con IA y datos públicos. La hipótesis elegida es que CAFs/mCAFs hepáticos crean nichos donde células tumorales colorrectales de alta plasticidad reciben señales `HGF-MET`, activan `MYC` y adoptan un programa glicolítico que favorece invasión, proliferación, adaptación y quizás recurrencia.

Esta hipótesis tiene buen sabor científico porque no depende de un único gen aislado. Une estroma, tumor, metabolismo y arquitectura espacial. En cáncer metastásico eso importa mucho: una célula tumoral puede llegar al hígado por anatomía vascular, pero sólo una fracción logra colonizar. La colonización exige cooperación con el microambiente. Por eso el foco se mueve desde "qué mutación tiene el tumor" hacia "qué nicho permite que ese tumor prospere".

La evidencia principal viene de un estudio 2025 disponible en PMC y PubMed. El trabajo integró 35 datasets single-cell RNA-seq y spatial transcriptomics de tumores colorrectales, metástasis hepáticas y tejidos normales. Identificó una subpoblación de alta malignidad, `High-M CRC`, enriquecida en metástasis hepáticas, con actividad `MYC`, mayor stemness y reprogramación glicolítica. También describió CAFs, especialmente mCAFs, como posibles productores de `HGF`, y células tumorales receptoras con `MET`, formando un eje `HGF-MET-MYC`. La parte espacial es clave: el estudio reporta co-localización entre mCAFs, señalización HGF-MET, MYC y actividad glicolítica en regiones metastásicas. Además, incluye validación funcional in vitro, donde la señal derivada de CAFs aumenta invasión/proliferación de células CRC y el knockdown de `MET` revierte parte del efecto.

La evidencia complementaria viene de `GSE225857` y el artículo de Science Advances asociado. Ese recurso analiza CRC primario y metástasis hepática mediante single-cell y spatial transcriptomics. Sus hallazgos no son exactamente los mismos, pero son compatibles con la idea de nicho: fibroblastos `MCAM+` enriquecidos en metástasis hepática, células T `CD8_CXCL13` y `CD4_CXCL13`, y posible señalización Notch entre estroma y células inmunes. Esto amplía la hipótesis: el nicho no sería sólo metabólico, sino también inmunomodulador.

Una tercera capa viene de trabajos recientes sobre macrófagos y metabolismo lipídico en CRLM. El hígado es un órgano metabólico; por eso tiene sentido observar macrófagos con actividad lipídica alterada, comunicación VEGF/complemento/integrinas y estados inmunes reprogramados durante progresión metastásica. Esto sugiere que una validación seria debe incluir no sólo `HGF`, `MET`, `MYC` y glicólisis, sino también macrófagos, lípidos, fibrosis y estados T.

La forma correcta de avanzar es convertir la hipótesis en predicciones falsables. `HGF` debería aparecer principalmente en CAF/mCAF o estroma. `MET` debería aparecer en células tumorales receptoras. `MYC` y genes glicolíticos como `SLC2A1`, `HK2`, `PGK1`, `TPI1` y `LDHA` deberían enriquecerse en células tumorales de alta malignidad. En datos espaciales, las firmas `mCAF`, `HGF`, `MET`, `MYC` y glicólisis deberían co-localizar o al menos mostrar proximidad. En datos bulk, debería haber alguna señal pronóstica o de agresividad, aunque con cuidado porque TCGA no es una cohorte metastásica pura.

La IA puede aportar mucho aquí si trabaja como sistema de integración: extraer relaciones desde papers, armar gene sets, construir matrices de evidencia, comparar datasets y priorizar hipótesis. El objetivo no es decir "encontramos la cura", sino "esta interacción aparece de forma convergente y merece validación". Esa diferencia es sana y nos mantiene en terreno serio.

La recomendación operativa es clara: avanzar primero con la matriz de hipótesis y el mapa de datasets. Luego, en una segunda fase, preparar scripts para extraer matrices GEO y probar scores de `mCAF`, `High-M CRC`, `HGF-MET`, `MYC` y glicólisis. TCIA queda como línea secundaria: útil para recurrencia y supervivencia, pero más pesada por imágenes. El eje principal ahora es biología espacial reproducible.

## Recomendación operativa
Prioridad inmediata:

`HipotesisNichoMetastaticoCRLM.md`

Luego:

`PlanValidacionCRLM.md`

Meta técnica próxima:

Preparar un primer script reproducible que descargue metadata y permita probar firmas en GEO/TCGA sin descargar imágenes pesadas.

## Fuentes
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
- https://pubmed.ncbi.nlm.nih.gov/41234356/
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10275599/
- https://link.springer.com/article/10.1186/s12967-025-07581-1
- https://www.cancerimagingarchive.net/collection/colorectal-liver-metastases/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10847495/
