# Conclusión dinámica vigente

Fecha de actualización: 2026-04-25 01:06:15 -03:00

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

## Mejor output próximo
El siguiente avance útil no es un paper narrativo más. Es una matriz priorizada:

- hipótesis
- genes/vías
- células implicadas
- evidencia
- datasets
- validación computacional
- criterio de falsación

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
Preparar una validación liviana y reproducible:

1. Extraer metadata y matrices accesibles de GEO.
2. Definir gene sets para `mCAF`, `High-M CRC`, `HGF-MET`, `MYC` y glicólisis.
3. Calcular enriquecimiento/co-expresión cuando los datos lo permitan.
4. Cruzar contra evidencia externa de TCGA-COAD/META-PRISM.
5. Mantener TCIA como línea secundaria para supervivencia/recurrencia.

## Cuidado epistemológico
Esta hipótesis es fuerte como programa de descubrimiento, no como afirmación clínica. Todavía no debemos decir que el eje es causal en pacientes ni que existe una intervención validada. La salida correcta por ahora es priorización de hipótesis y validación computacional reproducible.
