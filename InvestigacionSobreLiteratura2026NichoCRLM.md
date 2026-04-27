# Investigacion sobre literatura 2026 del nicho CRLM

Fecha: 2026-04-27 16:22:03 -03:00

## Pregunta
La pregunta de esta ola fue practica: que dice lo mas reciente de 2026 sobre metastasis hepatica colorrectal (CRLM), y como deberia cambiar nuestro plan autonomo?

La hipotesis previa era:

`CAF-high spatial niches in CRLM associate with MET+ MYC/glycolytic tumor neighborhoods.`

La busqueda 2026 obliga a ampliarla. El eje `HGF-MET-MYC-glycolysis` sigue siendo biologicamente plausible, pero ya no parece el centro unico del frente. El frente mas activo combina estroma, macrofagos, exclusion/agotamiento T, metabolismo y arquitectura espacial.

## Metodo reproducible
Se creo y ejecuto:

`scripts/search_pubmed_crlm_latest.py --retmax 80`

El script consulta PubMed via NCBI E-utilities para cinco bloques:

- CRLM + spatial/single-cell.
- CRLM + CAF/fibroblast.
- colorectal liver metastasis + HGF/MET/MYC/glycolysis.
- CRLM + macrophage/myeloid/immune/SPP1.
- CRLM + metabolism/proteomics/phosphoproteomics.

Salidas:

- `data_manifest/generated/pubmed_crlm_latest_2025_2026.tsv`
- `data_manifest/generated/pubmed_crlm_latest_2025_2026_report.md`

Snapshot:

- 185 PMIDs unicos detectados.
- 184 articulos con detalle recuperado.
- Tags dominantes: `immune_myeloid` 88 articulos, `glycolysis_metabolism` 87, `therapy_resistance` 72, `single_cell` 55, `hgf_met_myc` 27, `caf` 25, `spatial` 22.

Nota temporal: PubMed ya indexa al menos un articulo con fecha de issue `2026-May`; al estar hoy en 2026-04-27, debe leerse como articulo indexado/early publication con metadata de issue futura, no como observacion posterior al dia de hoy.

## Papers que cambian el mapa

### mCAF-SPP1 macrophage-T cell niche

PMID: [41807965](https://pubmed.ncbi.nlm.nih.gov/41807965/)

Este articulo 2026 integra single-cell, spatial transcriptomics, CellChat/NicheNet, deconvolucion espacial y validacion funcional con CAR-T. La observacion clave es una arquitectura de tres capas en CRC-LM:

- cinturones externos de mCAF;
- zonas internas ricas en TAM `SPP1+`;
- bandas intermedias de T cells estresadas/exhaustas.

Los ejes dominantes no son `HGF-MET`, sino `SPP1-CD44`, `FN1-CD44` y `MIF/CXCL12`. Recombinant SPP1 y MIF reducen killing tumoral en modelo CAR-T, y una firma `KLF2/ZBTB20/ARL4C` estratifica recurrencia y disease-free survival.

Lectura para nosotros: esto se pega directamente a nuestro resultado espacial `CAF-high`, pero desplaza el mecanismo de "CAF alimenta tumor glicolitico" hacia "CAF organiza una barrera mieloide/T". Es una expansion natural, no una contradiccion.

### SPP1 estimula CXCL12 en CAFs e inmunoresistencia

PMID: [41051794](https://pubmed.ncbi.nlm.nih.gov/41051794/)

Este paper de Cancer Research 2026 propone un circuito muy concreto: SPP1 induce `CXCL12` en CAFs mediante activacion beta-catenin/HIF1A. CXCL12 promueve EMT en celulas tumorales y reduce infiltracion CD8. El bloqueo de SPP1 o CXCL12 receptor mejora respuesta anti-PD-1 en modelos.

Lectura para nosotros: `SPP1/CXCL12` merece subir a firma prioritaria. Ademas une tres piezas que ya nos importaban: CAF, EMT/plasticidad tumoral e inmunomodulacion.

### SPP1+ y HLA-DRB5+ macrophages

PMID: [41715121](https://pubmed.ncbi.nlm.nih.gov/41715121/)

Este articulo 2026 integra single-cell, spatial y bulk para mapear diversidad mieloide. Identifica macrofagos `SPP1+` y `HLA-DRB5+` enriquecidos en metastasis hepatica, con localizaciones distintas y comunicaciones inferidas:

- `SPP1+` macrophages con B cells/Tregs via `MIF-(CD74+CXCR4)`.
- `HLA-DRB5+` macrophages con T/NK via `LGALS9-CD45`.

Lectura para nosotros: no alcanza con scorear CAF/tumor. Hay que introducir al menos dos ejes mieloides en el modelo.

### SPP1+ fibroblasts y heterogeneidad metabolica

PMID: [40340245](https://pubmed.ncbi.nlm.nih.gov/40340245/)

Aunque es 2025, encaja con la ola 2026 porque anticipa el mismo vocabulario: regiones dominadas por fibroblastos, `SPP1+ fibroblasts`, interaccion con tumor `CD44+`, inmunosupresion y componentes metabolicos espaciales.

Lectura para nosotros: `SPP1` aparece tanto en fibroblasto como en macrofago. El hallazgo posible no es "SPP1 existe", sino distinguir que compartimento lo expresa, donde se ubica y que respuesta tumoral/immune se asocia.

### SPP1+ macrophage-FADS1+ tumor via PDGFB-PDGFRB

PMID: [41655559](https://pubmed.ncbi.nlm.nih.gov/41655559/)

Este paper 2026 propone que macrofagos `SPP1+` secretan `PDGFB`, activando `PDGFRB` en tumor `FADS1+`, disparando EMT y favoreciendo metastasis hepatica.

Lectura para nosotros: se suma una posible rama `SPP1+ myeloid -> PDGFB/PDGFRB -> FADS1+ tumor/EMT`. Esto se puede testear en matrices single-cell si hay expresion y anotacion.

### GLUT1 en margen invasivo

PMID: [41940986](https://pubmed.ncbi.nlm.nih.gov/41940986/)

Estudio 2026 de 192 pacientes resecados por CRLM. `GLUT1/SLC2A1` en tumor se asocia a proliferacion, pero `GLUT1` en margen invasivo se asocia con mejor outcome en enfermedad solitaria y parece co-localizar con CD8+ cells.

Lectura para nosotros: la glicolisis no es automaticamente "mala" ni puramente tumoral. El compartimento importa. Esto refuerza la necesidad de separar tumor-core, invasive margin, CAF y immune.

### Proteogenomica y vulnerabilidades metabolicas

PMID: [41195591](https://pubmed.ncbi.nlm.nih.gov/41195591/)

Estudio proteogenomico/phosphoproteomico 2026 en 102 muestras de 34 pacientes CRLM naive a tratamiento. Reporta disrupcion de metabolismo de carbono, rol de `SHMT1`/formate/AMPK y `PIM` kinases sobre `NDRG1`, mas subtipos proteomicos con pronostico distinto.

Lectura para nosotros: si seguimos la rama metabolica, no debe limitarse a glicolisis Hallmark. Hay que abrir one-carbon metabolism, AMPK/formate, PIM/NDRG1 y marcadores `FTCD/GPD1/SOD2/EIF4B`.

### MORF4L1 y radioresistencia

PMID: [41751172](https://pubmed.ncbi.nlm.nih.gov/41751172/)

Paper 2026 que integra single-cell/spatial y machine learning para resistencia a radioterapia en CRLM. `MORF4L1-high` tumor cells se asocian con DNA damage response, vias metabolicas pro-supervivencia e inmunoevasion; espacialmente se colocalizan con Tregs/TAMs.

Lectura para nosotros: todavia secundaria, pero util si luego conectamos nicho con tratamiento local/radioterapia.

### MARCO+ macrophages en CASH

PMID: [41274349](https://pubmed.ncbi.nlm.nih.gov/41274349/)

Articulo con fecha de issue 2026-May ya indexado por PubMed. En pacientes CRLM con chemotherapy-associated steatohepatitis (CASH), macrofagos `MARCO+` aparecen como red inmunosupresora asociada a recurrencia, con T cells `TOX+` agotadas y NK `DNAJB1+` estresadas.

Lectura para nosotros: hay una version "higado lesionado por tratamiento" del nicho. No es prioridad inmediata, pero puede ser muy relevante para recurrencia post-hepatectomia o pacientes tratados con irinotecan.

## Sintesis: que cambia

Antes:

`CAF/mCAF -> HGF-MET -> MYC/glycolysis -> plasticidad tumoral`

Ahora:

`CAF-high spatial niche -> dos interfaces acopladas`

Interfaz metabolica tumoral:

`CAF-high / ECM / MCAM-PRELP states -> tumor MET+ -> MYC/glycolysis/one-carbon metabolism`

Interfaz inmunosupresora:

`mCAF/SPP1+ fibroblast -> SPP1+ or HLA-DRB5+ macrophage -> CXCL12/MIF/CD44/LGALS9/CD74/CXCR4 -> T cell exclusion/exhaustion`

La novedad computacional posible no es afirmar que `SPP1`, `CXCL12` o `CAF` son nuevos. Eso ya esta muy publicado. La oportunidad esta en probar si, en datos publicos reanalizados, los nichos `CAF-high` se dividen en subzonas:

- una subzona tumor-metabolica `MET/MYC/glycolysis`;
- una subzona mieloide-inmunosupresora `SPP1/CXCL12/MIF/CD44/HLA-DRB5`;
- o una capa tripartita donde ambas conviven alrededor de interfaces tumor-estroma.

Ese angulo si es interesante porque conecta nuestra evidencia propia en GSE225857 con el frente 2026, y permite una validacion computacional sin vender causalidad clinica.

## Estamos en terreno virgen?

No en el sentido bruto. `CAF`, `SPP1`, `CXCL12`, macrofagos `SPP1+`, spatial transcriptomics y nicho inmunosupresor en CRLM ya son terreno concurrido en 2026.

Pero si hay terreno aun poco explotado en una pregunta mas fina:

`La misma arquitectura CAF-high que predice MET/MYC/glicolisis tumoral tambien organiza, o se separa de, el circuito SPP1/CXCL12/MIF/HLA-DRB5 que confina T cells?`

Si el analisis espacial muestra que ambas capas se ordenan de forma reproducible, eso podria ser un aporte real: un modelo computacional integrado de "nicho bifasico" o "nicho en capas" en CRLM.

## Acciones tecnicas derivadas

1. Ampliar `data_manifest/signatures.yml` con firmas `SPP1/CXCL12`, `HLA-DRB5 macrophage`, `KLF2/ZBTB20/ARL4C`, `SEMA3C/NRP2`, `SHMT1/PIM/NDRG1`, `MORF4L1` y `MARCO`.
2. Recalcular disponibilidad de genes contra HGNC y TCGA-COAD.
3. Reanalizar GSE225857 spatial con nuevos scores:
   - `caf_score`
   - `spp1_cxcl12_axis`
   - `hla_drb5_macrophage_axis`
   - `myc_glycolysis_core`
   - `metabolic_vulnerability_2026`
4. En spatial, probar no solo correlaciones, sino capas:
   - CAF-high vecinos de SPP1/CXCL12.
   - SPP1/CXCL12 vecinos de CD8/T exhaustion.
   - CAF-high vecinos de MET/MYC/glycolysis.
   - Distancia o vecindad entre interface metabolica e interface inmune.
5. Buscar dataset espacial externo donde validar el patron de capas.

## Decision
La mejor continuacion no es buscar "otro cancer" ni hacer mas bulk. La mejor continuacion es una segunda pasada espacial en GSE225857 incorporando el frente 2026.

Nombre operativo del modelo refinado:

`CAF-high layered niche model in CRLM`

Formulacion:

`En CRLM, nichos CAF-high pueden organizar dos respuestas acopladas: una tumoral metabolica MET/MYC/glycolysis y otra inmunosupresora mieloide/T mediada por SPP1/CXCL12/MIF/CD44/HLA-DRB5.`

