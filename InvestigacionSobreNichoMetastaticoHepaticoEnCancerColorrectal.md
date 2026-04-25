# Investigación sobre nicho metastásico hepático en cáncer colorrectal

Fecha: 2026-04-25 01:06:15 -03:00

## Objetivo
Convertir la línea `cáncer colorrectal -> metástasis hepática` en una hipótesis operativa y testeable:

`CAFs/mCAFs hepáticos crean nichos metabólicos e inmunomoduladores que favorecen células tumorales colorrectales plásticas, con señalización HGF-MET, activación MYC y glicólisis local.`

## Tesis actual
La oportunidad más fuerte no está en buscar una mutación aislada. El foco debe estar en el ecosistema espacial del hígado metastásico: células tumorales de alta plasticidad, fibroblastos asociados a cáncer, macrófagos reprogramados, células T particulares y metabolismo local.

La hipótesis `mCAF-HGF-MET-MYC-glycolysis` es especialmente atractiva porque une cuatro capas:

- célula tumoral: subpoblación de alta malignidad o alta plasticidad
- estroma: CAFs/mCAFs como productores de señales
- metabolismo: activación de MYC y glicólisis
- espacialidad: co-localización física de estados celulares y señales

## Evidencia central
Un artículo de 2025, publicado en Frontiers in Cell and Developmental Biology y disponible en PMC, integró 35 datasets single-cell RNA-seq y spatial transcriptomics de CRC, tejido normal, metástasis hepática y tejido hepático normal. El estudio propuso una subpoblación `High-M CRC`, enriquecida en metástasis hepáticas, con stemness, actividad `MYC` y reprogramación glicolítica. También describió que CAFs, particularmente mCAFs, podrían promover progresión mediante `HGF-MET-MYC`.

Lo importante para nosotros no es aceptar el paper como verdad final, sino usarlo como hipótesis generadora:

- si `mCAFs` producen `HGF`
- si células `High-M CRC` expresan `MET`
- si `MET` se asocia con actividad `MYC`
- si `MYC` se asocia con glicólisis
- si esas señales co-localizan espacialmente
- entonces puede existir un nicho metabólico-estromal que favorece colonización hepática

## Evidencia complementaria
`GSE225857` y el artículo de Science Advances asociado describen el paisaje single-cell y spatial de CRC primario y metástasis hepática. Allí aparecen señales importantes:

- fibroblastos `MCAM+` enriquecidos en metástasis hepática
- células T `CD8_CXCL13` y `CD4_CXCL13`
- posible señalización Notch entre fibroblastos `MCAM+` y estados T
- diferencias de composición entre tumor primario y metástasis hepática

Esto no prueba directamente el eje `HGF-MET-MYC`, pero sí refuerza la idea de que el nicho hepático tiene una arquitectura estromal-inmune específica.

Una línea 2025 de Journal of Translational Medicine agrega otra pieza: macrófagos con metabolismo lipídico elevado en CRLM. Esto encaja con el hígado como órgano metabólico y sugiere que la inmunomodulación no debe entenderse sólo como checkpoints o linfocitos, sino también como reprogramación mieloide y metabolismo local.

## Modelo de trabajo

### Paso 1: nicho estromal
Los mCAFs/CAFs del hígado podrían actuar como organizadores del nicho. Sus funciones esperadas:

- secreción de `HGF`
- remodelado de matriz extracelular
- soporte metabólico
- modulación de células inmunes
- creación de fronteras o interfaces tumor-estroma

### Paso 2: célula tumoral receptora
Las células tumorales colorrectales de alta malignidad/plasticidad podrían expresar `MET`, responder a `HGF` y activar `MYC`.

Predicción:

- mayor co-expresión o co-actividad `MET-MYC` en subpoblaciones tumorales enriquecidas en metástasis
- mayor score de stemness/plasticidad en células con actividad de glicólisis
- enriquecimiento de genes de invasión, EMT parcial o proliferación

### Paso 3: metabolismo
`MYC` puede favorecer programa glicolítico. Genes de interés:

- `SLC2A1`
- `HK2`
- `PGK1`
- `TPI1`
- `LDHA`
- `ENO1`

Predicción:

- regiones con alto score `High-M CRC` deben mostrar score glicolítico mayor
- regiones con mCAF alto deben estar cerca o correlacionadas con score glicolítico tumoral

### Paso 4: inmunomodulación
La hipótesis se vuelve más fuerte si el nicho no sólo alimenta tumor, sino que también modula inmunidad.

Señales a seguir:

- `CXCL13+ T cells`
- macrófagos de alto metabolismo lipídico
- VEGF/complement/integrinas en macrófagos
- Notch en interacción fibroblasto-linfocito
- TGF-beta y fibrosis

## Qué puede aportar IA de forma concreta
- Lectura sistemática de papers y extracción de relaciones célula-gen-vía.
- Construcción de matriz de hipótesis con evidencia y falsación.
- Generación de gene sets para mCAF, High-M CRC, MYC/glicólisis y macrófagos lipídicos.
- Validación cruzada entre GEO, TCGA, META-PRISM y TCIA.
- Priorización de targets no por fama, sino por convergencia entre datasets.

## Primeras predicciones falsables
- `HGF` debe concentrarse en CAF/mCAF o estroma, no en cualquier célula de forma inespecífica.
- `MET` debe ser detectable en células tumorales receptoras.
- `MYC` y genes glicolíticos deben aumentar en subpoblaciones tumorales de mayor malignidad/plasticidad.
- En spatial, `mCAF score`, `HGF`, `MET`, `MYC` y glicólisis deben mostrar proximidad o co-localización parcial.
- Si el eje es real, debería haber alguna señal pronóstica o de agresividad en TCGA/META-PRISM, aunque TCGA no sea una cohorte metastásica ideal.

## Criterios para bajar prioridad
La hipótesis debería perder prioridad si:

- `HGF` no aparece consistentemente ligado a CAF/mCAF
- `MET-MYC` no se correlaciona en células tumorales o bulk
- la glicólisis no se enriquece en subpoblaciones malignas
- spatial no muestra proximidad entre estroma productor y tumor receptor
- la señal sólo aparece en un estudio y desaparece en datasets independientes

## Resultado esperado de esta ola
La ola 003 debe producir una base de trabajo para pasar a análisis:

- matriz de hipótesis
- mapa de datasets
- tabla de señales prioritarias
- plan de validación computacional
- conclusión dinámica actualizada

## Fuentes
- Frontiers/PMC 2025, HGF-MET-MYC-glycolysis: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
- PubMed del mismo estudio: https://pubmed.ncbi.nlm.nih.gov/41234356/
- GSE225857: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857
- Science Advances, single-cell/spatial CRLM: https://pmc.ncbi.nlm.nih.gov/articles/PMC10275599/
- Macrófagos y metabolismo lipídico en CRLM: https://link.springer.com/article/10.1186/s12967-025-07581-1
- TCIA Colorectal-Liver-Metastases: https://www.cancerimagingarchive.net/collection/colorectal-liver-metastases/
- TCIA/Scientific Data CRLM CT survival dataset: https://pmc.ncbi.nlm.nih.gov/articles/PMC10847495/
