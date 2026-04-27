# Resumen de investigacion sobre literatura 2026 del nicho CRLM

Fecha: 2026-04-27 16:22:03 -03:00

## Resumen corto
La busqueda PubMed 2025-2026 confirma que nuestra linea no esta perdida, pero debe refinarse. El eje original `mCAF-HGF-MET-MYC-glycolysis` sigue siendo plausible como componente metabolico del nicho, especialmente porque nuestros analisis en GSE225857 ya mostraron `CAF-high -> MET/MYC/glicolisis` con soporte espacial y permutaciones. Sin embargo, el frente mas caliente de 2026 en CRLM parece moverse hacia nichos espaciales inmunosupresores construidos por CAFs, macrofagos y T cells, con `SPP1`, `CXCL12`, `MIF`, `CD44`, `FN1`, `HLA-DRB5`, `CD74`, `CXCR4` y `LGALS9` como senales repetidas.

Los papers mas importantes de 2026 describen una arquitectura en capas: mCAF en la zona externa, macrofagos `SPP1+` en zonas internas y bandas de T cells estresadas/exhaustas. Otro paper muestra que `SPP1` induce `CXCL12` en CAFs y genera inmunoresistencia, EMT y exclusion CD8. Un tercer trabajo ubica macrofagos `SPP1+` y `HLA-DRB5+` como moduladores espaciales del microambiente inmune. En paralelo, la literatura metabolica 2026 agrega proteogenomica, one-carbon metabolism (`SHMT1`), `PIM/NDRG1`, `GLUT1` por compartimento y `MORF4L1` en radioresistencia.

Conclusion fuerte: no estamos en terreno virgen si decimos "SPP1/CAF importa"; eso ya esta publicado. La oportunidad esta en integrar nuestra evidencia `CAF-high -> MET/MYC/glicolisis` con el nuevo frente `CAF/mieloide/T-cell immunosuppressive niche`. La pregunta con mas chance de aporte es si los nichos `CAF-high` forman una arquitectura bifasica: una interfaz tumoral metabolica y otra interfaz inmunosupresora mieloide/T. El proximo paso debe ser reanalizar GSE225857 spatial con firmas 2026 y buscar capas/vecindades, no solo promedios por muestra.

## Resumen extendido
La ola de literatura 2026 cambia la lectura estrategica del proyecto. Hasta ahora, la hipotesis principal se habia refinado hacia un modelo espacial donde los nichos `CAF-high` en CRLM se asocian a tumor `MET+`, activacion `MYC` y glicolisis local. Esa idea se fortalecio con TCGA-COAD como plausibilidad bulk, GSE225857 single-cell como evidencia paracrina `HGF` fibroblastico y `MET` tumoral, y GSE225857 spatial/permutaciones como evidencia de vecindad `CAF-high -> MET/MYC/glycolysis`. Pero GSE234804 no confirmo la hipotesis como promedio sample-level LM-vs-CRC, lo que ya nos habia obligado a formularla como arquitectura local, no como biomarcador global.

La busqueda PubMed 2025-2026 refuerza esa decision. Los conteos muestran que la literatura reciente en CRLM esta dominada por inmunidad mieloide, metabolismo, resistencia terapeutica, single-cell y spatial. El eje `HGF-MET-MYC` aparece, pero no domina. El nuevo centro gravitatorio es `CAF + SPP1/CXCL12 + macrofagos + T-cell exclusion/exhaustion`, con metabolismo como capa transversal.

El paper mas transformador para nuestro plan es el de mCAF-SPP1 macrophage-T cell crosstalk en CRC-LM ([PMID 41807965](https://pubmed.ncbi.nlm.nih.gov/41807965/)). Describe un nicho inmunosupresor espacial con tres capas: cinturones mCAF, zonas ricas en macrofagos `SPP1+` y bandas de T cells estresadas o exhaustas. Sus ejes dominantes son `SPP1-CD44`, `FN1-CD44` y `MIF/CXCL12`, y ademas propone una firma minima `KLF2/ZBTB20/ARL4C` con valor pronostico. Esto encaja muy bien con nuestro resultado `CAF-high`, pero sugiere que el CAF no solo empuja metabolismo tumoral; tambien organiza una arquitectura inmune que puede confinar o agotar T cells.

El segundo paper clave ([PMID 41051794](https://pubmed.ncbi.nlm.nih.gov/41051794/)) muestra que `SPP1` puede estimular `CXCL12` en CAFs mediante beta-catenin/HIF1A, promoviendo EMT, reduciendo infiltracion CD8 y generando resistencia a anti-PD-1. Esto convierte a `SPP1/CXCL12` en una firma prioritaria para el repo. Un tercer paper ([PMID 41715121](https://pubmed.ncbi.nlm.nih.gov/41715121/)) separa macrofagos `SPP1+` y `HLA-DRB5+`, vinculando el primer grupo con `MIF-(CD74+CXCR4)` y el segundo con `LGALS9-CD45`. Estos ejes son ideales para scoring spatial/cell-type, porque no son simples genes aislados sino circuitos de comunicacion.

El componente metabolico tampoco desaparece. Un estudio proteogenomico 2026 ([PMID 41195591](https://pubmed.ncbi.nlm.nih.gov/41195591/)) apunta a disrupcion del metabolismo de carbono, `SHMT1`, formate/AMPK y `PIM/NDRG1`. Otro trabajo sobre `GLUT1` en margen invasivo ([PMID 41940986](https://pubmed.ncbi.nlm.nih.gov/41940986/)) advierte que la glicolisis depende del compartimento: tumor-core e invasive margin pueden tener significados opuestos. Esto es importante porque evita una lectura ingenua de `SLC2A1` como "siempre agresivo". La biologia espacial manda.

La conclusion operativa es que el proyecto debe pivotear de un eje lineal a un modelo en capas:

`CAF-high layered niche model in CRLM`

Ese modelo dice que los nichos `CAF-high` podrian organizar dos respuestas acopladas: una interfaz metabolica tumoral `MET/MYC/glycolysis/one-carbon metabolism` y una interfaz inmunosupresora `SPP1/CXCL12/MIF/CD44/HLA-DRB5`. Esta formulacion es mas fuerte que la anterior porque explica por que `HGF` aislado no funciono tan bien en spatial, por que el promedio sample-level fallo en GSE234804 y por que la literatura 2026 insiste en macrofagos/T cells.

Recomendacion: ampliar firmas, regenerar disponibilidad y correr una segunda pasada espacial en GSE225857. Hay que medir vecindades entre CAF-high, SPP1/CXCL12, macrofagos HLA-DRB5, CD8/exhaustion y MET/MYC/glicolisis. Si aparece una arquitectura reproducible de capas, ahi si podemos estar cerca de un aporte interesante. No seria "descubrimos SPP1"; seria "integramos el nicho metabolico y el nicho inmunosupresor en un modelo espacial computacional falsable".

## Recomendacion operativa
Continuar con una validacion espacial 2026 sobre GSE225857. El siguiente bloque debe crear scores nuevos, probar co-localizacion/vecindad y actualizar la hipotesis segun resultado. No conviene volver a bulk ni a sample-level promedios como prueba principal.

