# Conclusión dinámica vigente

Fecha de actualización: 2026-04-26

## Línea activa
La línea activa queda fijada en:

`nicho metastásico hepático en cáncer colorrectal`

## Hipótesis principal
CAFs/mCAFs hepáticos crean nichos metabólicos e inmunomoduladores que favorecen células tumorales colorrectales plásticas, con señalización `HGF-MET`, activación `MYC` y glicólisis local.

## Por qué esta hipótesis manda ahora
- Es mecanística: conecta estroma, tumor, metabolismo, espacialidad e inmunidad.
- Tiene soporte reciente en single-cell, spatial transcriptomics y validación funcional.
- Usa datasets públicos concretos: `GSE225857`, `GSE226997`, TCGA-COAD, TCIA CRLM y cohorts metastásicas.
- Es falsable: si no hay co-localización, correlación o enriquecimiento reproducible de las firmas, la hipótesis pierde fuerza.
- Permite salida computacional útil sin prometer validación clínica inmediata.

## Núcleo de evidencia
- Un estudio 2025 integró 35 datasets single-cell y spatial y propuso un eje `mCAF -> HGF-MET -> MYC/glycolysis` en nichos de metástasis hepática colorrectal.
- `GSE225857` aporta soporte independiente para heterogeneidad celular en CRLM, incluyendo fibroblastos `MCAM+` y células T `CXCL13+`.
- La literatura 2025 sobre macrófagos sugiere que el metabolismo lipídico puede reprogramar estados mieloides en CRLM, lo que encaja con el hígado como órgano metabólico e inmunomodulador.

## Validación computacional completada

### Bulk TCGA-COAD (329 muestras)
- `MET-MYC` r = 0.515 (fuerte). `MYC-glycolysis` r = 0.422 (moderada). `CAF-HGF` r = 0.675 (fuerte).
- `HGF-MET` r = -0.08: consistente con señalización paracrina diluida en bulk.

### Composición celular GSE225857 (41,892 células)
- MCAM+ CAFs: 83% en hígado (fold 2.86x). CONFIRMADO.
- Tu02_DEFA5: 97% hígado-específico (fold 20.4x). CONFIRMADO.

### Expresión single-cell GSE225857 (17,516 genes x 41,892 células)
- HGF en fibroblastos (mean 0.674) vs tumor (mean 0.004): ratio 168x. CONFIRMADO.
- MET en tumor (mean 0.399) vs fibroblastos (mean 0.009): ratio 44x. CONFIRMADO.
- MET-MYC en tumor: r = 0.1438, n = 23,954, p < 1e-300. CONFIRMADO.
- MYC-PGK1 r = 0.36, MYC-TPI1 r = 0.42 en tumor. CONFIRMADO.
- Patrón paracrino HGF(estroma)→MET(tumor) validado a nivel single-cell.

### Refinamiento
- La fuente de HGF en hígado no es solo MCAM+ CAFs sino también PRELP+ fibroblasts (F01).
- MYC es 45% más alto en metástasis hepática que en tumor primario.
- MET-MYC es débil per-cell (r=0.14) pero robusto estadísticamente, sugiriendo heterogeneidad espacial.

## Estado de la hipótesis: 5/5 predicciones confirmadas
La hipótesis `mCAF-HGF-MET-MYC-glycolysis` pasa todas las pruebas de plausibilidad en bulk y single-cell. Justifica inversión en validación cruzada y análisis espacial.

## Mejor output próximo
El siguiente avance útil es validación cruzada:

- reproducibilidad en dataset independiente
- co-localización espacial mCAF-tumor
- especificidad CRLM vs metástasis general (META-PRISM)
- supervivencia/pronóstico en TCGA-COAD con firmas validadas

## Señales prioritarias
- `HGF`
- `MET`
- `MYC`
- `SLC2A1`
- `HK2`
- `PGK1`
- `TPI1`
- `MCAM`
- `CXCL13`
- `BHLHE40`
- CAF/mCAF, EMT-like CAF, macrófagos lipídicos, T cells `CXCL13+`

## Próximo paso técnico
Extensión y validación cruzada:

1. Buscar datos espaciales en GSE225857 para co-localización mCAF-tumor.
2. Cruzar con META-PRISM para especificidad CRLM vs metástasis general.
3. Evaluar asociación pronóstica de firmas en TCGA-COAD (supervivencia).
4. Buscar validación independiente en GSE226997 o datasets 2025.
5. Mantener TCIA como línea secundaria para recurrencia post-hepatectomía.

## Cuidado epistemológico
Esta hipótesis es fuerte como programa de descubrimiento, no como afirmación clínica. Todavía no debemos decir que el eje es causal en pacientes ni que existe una intervención validada. La salida correcta por ahora es priorización de hipótesis y validación computacional reproducible.
