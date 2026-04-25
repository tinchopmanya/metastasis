# Roadmap de investigación: metástasis

Fecha: 2026-04-25 00:53:22 -03:00

## Modo autónomo activo
Actualización: 2026-04-25 01:06:15 -03:00

El proyecto entra en modo de avance autónomo. La línea activa queda fijada como ola 003:

`CAFs/mCAFs hepáticos -> HGF-MET -> MYC/glicólisis -> plasticidad tumoral e inmunomodulación en CRLM`

La prioridad inmediata ya no es decidir qué investigar, sino construir evidencia organizada alrededor de esa hipótesis. El trabajo se ejecuta en este orden:

1. Abrir la ola 003 en `Investigacion.md`, `InvestigacionMapa.md` y `Conlusion.md`.
2. Crear la investigación extensa del nicho metastásico hepático.
3. Crear una matriz de hipótesis priorizadas.
4. Crear un mapa de datasets y señales.
5. Crear un plan de validación computacional.
6. Versionar y subir los avances.

Primer objetivo operativo:

Convertir la hipótesis `mCAF-HGF-MET-MYC-glycolysis` en una hipótesis testeable, con evidencia, datasets, genes, células, predicciones y criterios de falsación.

Primer avance técnico ejecutado:

- `scripts/prepare_signatures.py` creado.
- `data_manifest/generated/signatures_normalized.tsv` generado.
- `data_manifest/generated/signature_gene_matrix.tsv` generado.
- `data_manifest/generated/signature_report.md` generado.
- La preparación inicial de firmas queda sin advertencias.

## Decisión estratégica
La dirección más prometedora ahora no es seguir ampliando el panorama general de metástasis. Ya hay suficiente señal para avanzar con una línea concreta:

`cáncer colorrectal -> metástasis hepática -> nicho metastásico hepático`

La meta de las próximas horas debe ser producir algo verificable: una matriz de hipótesis, datasets, señales moleculares/celulares y rutas de validación. La pregunta no es "qué es la metástasis", sino:

Qué estados celulares e interacciones del microambiente hepático hacen que una metástasis colorrectal pueda colonizar, resistir tratamiento y recurrir.

## Por qué esta línea
- Tiene alto impacto clínico.
- Tiene datasets públicos útiles: TCIA, GEO, TCGA/GDC, META-PRISM, scRNA-seq y spatial.
- Tiene señales recientes concretas: `HGF-MET-MYC-glycolysis`, fibroblastos metastásicos, macrófagos, estados T `CXCL13+`, metabolismo lipídico, EMT/plasticidad.
- Permite que agentes de IA aporten de verdad: leer papers, cruzar datasets, detectar convergencias, construir hipótesis y proponer validaciones.

## Qué haría ahora
Haría una ola 003 con foco estrecho:

`InvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`

El objetivo no sería escribir otro resumen bonito, sino construir una base de trabajo accionable:

- hipótesis priorizadas
- evidencia a favor y en contra
- datasets donde probar cada hipótesis
- biomarcadores o genes candidatos
- rutas de validación computacional
- riesgos metodológicos

## Entregables de las próximas horas

### 1. Matriz de hipótesis
Archivo sugerido:

`HipotesisNichoMetastaticoCRLM.md`

Columnas o secciones:

- hipótesis
- mecanismo propuesto
- células implicadas
- genes/vías
- evidencia principal
- datasets donde se puede validar
- nivel de novedad
- riesgo de sesgo
- próximo experimento computacional

Hipótesis candidatas iniciales:

- `HGF-MET-MYC-glycolysis`: CAFs y tumor cooperan metabólicamente en nichos espaciales.
- `MCAM+ CAFs`: fibroblastos metastásicos podrían modular estados T vía señalización Notch.
- `CXCL13+ T cells`: subpoblaciones T enriquecidas en metástasis hepática podrían marcar nichos inmunes específicos.
- `macrófagos y metabolismo lipídico`: heterogeneidad mieloide vinculada a progresión y soporte hepático.
- `BHLHE40/EMT`: plasticidad y transición fenotípica como programa metastásico.
- `firma temprana del primario`: señal de tropismo hepático ya presente antes de la metástasis visible.

### 2. Mapa de datasets
Archivo sugerido:

`DatasetsCRLM.md`

Contenido:

- `GSE225857`: single-cell y spatial de CRC primario y metástasis hepática.
- `TCIA Colorectal-Liver-Metastases`: CT, segmentaciones, clínica y supervivencia en 197 pacientes.
- `TCGA COAD/READ`: baseline multi-omics de tumor primario.
- `META-PRISM`: cohorte metastásica pan-cáncer con hígado como sitio frecuente de biopsia.
- `scCRLM`: recurso espacial usado en artículos recientes.
- `PDMR/HCMI/organoides`: puente hacia validación preclínica.

### 3. Tabla de señales priorizadas
Archivo sugerido:

`SenalesPrioritariasCRLM.md`

Señales iniciales:

- `HGF`
- `MET`
- `MYC`
- genes de glicólisis: `SLC2A1`, `PGK1`, `TPI1`
- `MCAM`
- genes T `CXCL13+`
- marcadores CAF/mCAF
- marcadores macrófago/lípidos
- `BHLHE40`
- ejes `TGF-beta`, `KRAS`, fibrosis, matriz extracelular

### 4. Plan de validación computacional
Archivo sugerido:

`PlanValidacionCRLM.md`

Validaciones posibles:

- comprobar si los genes/vías aparecen en múltiples papers y datasets
- validar firmas en TCGA COAD/READ como señal temprana o pronóstica
- cruzar con META-PRISM para distinguir señal específica de CRLM versus metástasis general
- usar TCIA para preguntar si señales biológicas se conectan con recurrencia/supervivencia por imagen
- cruzar con organoides/PDMR/HCMI para priorizar targets más plausibles

## Orden recomendado de trabajo

### Bloque 1: dos a tres horas
Crear la matriz de hipótesis y datasets. Este es el bloque de mayor retorno porque convierte literatura dispersa en una base de decisión.

Resultado esperado:

- `HipotesisNichoMetastaticoCRLM.md`
- `DatasetsCRLM.md`
- actualización de `Conlusion.md`

### Bloque 2: tres a seis horas
Profundizar en las tres hipótesis más fuertes. Para cada una:

- paper principal
- evidencia independiente
- genes centrales
- células implicadas
- qué dataset permite probarla
- qué resultado computacional la fortalecería o debilitaría

Resultado esperado:

- `InvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`
- `ResumenInvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`

### Bloque 3: seis a doce horas
Empezar trabajo técnico. Prioridad conservadora:

1. Descargar metadata y tablas disponibles.
2. Construir manifest de datasets.
3. Preparar scripts de análisis exploratorio.
4. Intentar una primera validación de firmas en datos públicos accesibles.

Resultado esperado:

- carpeta `data_manifest/`
- carpeta `scripts/`
- primer script reproducible de extracción/validación
- un reporte de hallazgos y bloqueos

### Bloque 4: línea técnica paralela
Usar TCIA para recurrencia post-hepatectomía. Esta línea es valiosa, pero la pondría como segunda prioridad porque se vuelve más pesada en datos e infraestructura.

Resultado esperado:

- manifest del dataset TCIA
- revisión del paper base
- plan de pipeline radiomics/deep learning

## Qué no haría todavía
- No intentaría prometer descubrimiento clínico.
- No descargaría imágenes pesadas antes de tener clara la hipótesis.
- No haría un modelo predictivo primero si todavía no sabemos qué queremos validar.
- No abriría diez tipos de cáncer a la vez.
- No convertiría esto en una lista gigante de genes sin mecanismo.

## Mi apuesta concreta
Si tengo varias horas para avanzar, empezaría por una ola 003 y construiría una matriz de hipótesis del nicho metastásico hepático.

La hipótesis que hoy parece más fuerte como punto de partida es:

`CAFs/mCAFs en el hígado crean nichos metabólicos e inmunomoduladores que favorecen células tumorales colorrectales de alta plasticidad, con señalización HGF-MET, activación MYC y glicólisis local.`

Por qué esta hipótesis:

- es concreta
- conecta célula tumoral y microambiente
- tiene soporte single-cell y spatial reciente
- se puede validar con datasets públicos
- apunta a mecanismos, no sólo predicción

## Próxima acción recomendada
Abrir la ola 003:

`nicho metastásico hepático en cáncer colorrectal`

Primeros archivos a crear:

- `InvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`
- `ResumenInvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`
- `HipotesisNichoMetastaticoCRLM.md`
- `DatasetsCRLM.md`

## Fuentes clave para arrancar
- GSE225857: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857
- Single-cell and spatial transcriptome analysis of liver metastatic colorectal cancer: https://pmc.ncbi.nlm.nih.gov/articles/PMC10275599/
- Spatially resolved single-cell landscape with HGF-MET-MYC-glycolysis axis: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
- TCIA Colorectal-Liver-Metastases: https://www.cancerimagingarchive.net/collection/colorectal-liver-metastases/
- Preoperative CT and survival data for CRLM: https://pmc.ncbi.nlm.nih.gov/articles/PMC10847495/
- NCI PDQ Colon Cancer Treatment: https://www.cancer.gov/types/colorectal/hp/colon-treatment-pdq
- SEER Colorectal Cancer Stat Facts: https://seer.cancer.gov/statfacts/html/colorect.html
- AI in CRLM review: https://pubmed.ncbi.nlm.nih.gov/40240167/
