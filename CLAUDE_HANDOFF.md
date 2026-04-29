# Claude handoff: metastasis research repo

Fecha de handoff: 2026-04-25

## Contexto corto
Este repo es un proyecto de investigacion autonoma sobre metastasis. La linea activa no es panoramica: ya se eligio un foco concreto.

Linea activa:

`cancer colorrectal -> metastasis hepatica -> nicho metastasico hepatico`

Hipotesis principal:

`CAFs/mCAFs hepaticos crean nichos metabolicos e inmunomoduladores que favorecen celulas tumorales colorrectales plasticas, con senalizacion HGF-MET, activacion MYC y glicolisis local.`

Abreviatura usada:

`CRLM` = colorectal liver metastasis.

## Estado del repo
Repositorio remoto:

`https://github.com/tinchopmanya/metastasis.git`

Rama activa:

`main`

Ultimos commits relevantes:

- Ultimo: Add TCGA-COAD gene universe and GDC fetch script
- `1dabfc9 Add Claude handoff for CRLM research`
- `877a985 Add CRLM gene availability checker`
- `080fe3d Prepare CRLM signature validation inputs`
- `491e78a Open CRLM niche hypothesis track`
- `478d4ef Add metastasis research roadmap`
- `e203ef3 Initial research workspace setup`

Antes de trabajar:

```powershell
git status --short
```

El estado esperado al recibir este handoff es limpio.

## Archivos principales
- `README.md`: descripcion general del repo.
- `Roadmap.md`: roadmap vivo del proyecto.
- `Investigacion.md`: log central de olas.
- `InvestigacionMapa.md`: mapa cronologico.
- `Conlusion.md`: conclusion dinamica vigente.
- `InvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`: investigacion activa de ola 003.
- `ResumenInvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md`: resumen de ola 003.
- `HipotesisNichoMetastaticoCRLM.md`: matriz de hipotesis priorizadas.
- `DatasetsCRLM.md`: mapa de datasets.
- `SenalesPrioritariasCRLM.md`: senales y genes prioritarios.
- `PlanValidacionCRLM.md`: plan tecnico de validacion.
- `data_manifest/signatures.yml`: firmas genicas iniciales.
- `data_manifest/crlm_sources.md`: manifiesto de fuentes/datasets.
- `scripts/prepare_signatures.py`: prepara firmas.
- `scripts/check_gene_availability.py`: verifica genes contra universos genicos.

## Que ya esta hecho
Se abrieron tres olas:

1. Ola 001: panorama general de metastasis y oportunidades con IA.
2. Ola 002: cancer colorrectal y metastasis hepatica.
3. Ola 003: nicho metastasico hepatico en CRLM, con foco en `mCAF-HGF-MET-MYC-glycolysis`.

Se crearon firmas iniciales:

- `hgf_met_axis`
- `myc_glycolysis_core`
- `caf_core`
- `mcam_caf`
- `cxcl13_t_cells`
- `macrophage_lipid_candidate`
- `plasticity_emt`

Se ejecutaron scripts:

```powershell
python scripts/prepare_signatures.py
python scripts/check_gene_availability.py
```

Resultados actuales:

- 7 firmas.
- 40 filas firma-gen.
- 37 genes unicos.
- 0 advertencias en preparacion de firmas.
- 100% de cobertura contra HGNC aprobado.
- 0 genes faltantes contra HGNC.

Archivos generados:

- `data_manifest/generated/signatures_normalized.tsv`
- `data_manifest/generated/signature_gene_matrix.tsv`
- `data_manifest/generated/signature_report.md`
- `data_manifest/generated/hgnc_approved_symbols.tsv`
- `data_manifest/generated/gene_availability.tsv`
- `data_manifest/generated/gene_availability_report.md`
- `data_manifest/gene_universes/tcga_coad_genes.txt` (59,427 genes desde GDC STAR-Counts)
- `data_manifest/gene_universes/README.md`
- `data_manifest/generated/tcga_coad_expression.tsv` (20,530 genes x 329 muestras, UCSC Xena)
- `data_manifest/generated/tcga_coad_signature_scores.tsv`
- `data_manifest/generated/tcga_coad_correlations.tsv`
- `data_manifest/generated/tcga_coad_bulk_plausibility_report.md`

## Fuentes clave
Paper lider para la hipotesis:

- Spatially resolved single-cell CRLM landscape / eje `HGF-MET-MYC-glycolysis`: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
- PubMed del mismo estudio: https://pubmed.ncbi.nlm.nih.gov/41234356/

Fuente complementaria:

- `GSE225857`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225857
- Single-cell/spatial CRLM heterogeneity: https://pmc.ncbi.nlm.nih.gov/articles/PMC10275599/

Metabolismo/inmunidad:

- Macrofagos y metabolismo lipidico en CRLM: https://link.springer.com/article/10.1186/s12967-025-07581-1

Linea tecnica secundaria:

- TCIA Colorectal-Liver-Metastases: https://www.cancerimagingarchive.net/collection/colorectal-liver-metastases/
- TCIA/Scientific Data CRLM CT survival dataset: https://pmc.ncbi.nlm.nih.gov/articles/PMC10847495/

## Advertencia importante sobre datos pesados
No arrancar descargando los TAR pesados de GEO.

Estado actual:

- `GSE225857`: TAR procesado de aproximadamente 607 MB.
- `GSE226997`: TAR procesado de aproximadamente 41.2 GB.

Politica actual:

Primero avanzar con metadata, firmas, universos genicos y validacion liviana. Descargar matrices pesadas solo cuando haya una razon concreta y el plan de extraccion este definido.

## Bloque completado: universo genico TCGA-COAD
Este bloque fue completado exitosamente:

- `scripts/fetch_gdc_gene_universe.py` creado y funcional.
- `data_manifest/gene_universes/tcga_coad_genes.txt` generado desde GDC STAR-Counts (59,427 genes).
- `check_gene_availability.py` ejecutado contra HGNC y TCGA-COAD: 100% cobertura, 0 genes faltantes.
- `PlanValidacionCRLM.md` y `Roadmap.md` actualizados.
- TCGA-READ comparte pipeline STAR/GENCODE v36; universo identico a TCGA-COAD.

## Bloque completado: scoring bulk TCGA-COAD

- `scripts/score_signatures_bulk.py` creado y ejecutado.
- Matriz TCGA-COAD de UCSC Xena: 20,530 genes x 329 muestras.
- 7 firmas scored, 22 correlaciones calculadas.
- MET-MYC r=0.515 (fuerte), MYC-glycolysis r=0.422 (moderada), CAF-HGF r=0.675 (fuerte).
- HGF-MET r=-0.08 (no significativa): consistente con paracrinia.
- Conclusion: eje plausible en bulk. Justifica validacion single-cell.

## Bloque completado: composicion celular GSE225857

- Se descubrio que GSE225857 tiene archivos individuales (~1.9 MB metadata vs 607 MB TAR).
- `scripts/download_gse225857.py` creado: descarga selectiva por compartimento.
- `scripts/analyze_gse225857_cellcomp.py` creado.
- Metadata non-immune descargada: 41,892 celulas, 23 cell types, 6 pacientes.
- MCAM+ CAFs: 83% en higado (fold 2.86x). CONFIRMADO.
- CXCL14+ fibroblasts: 94% en colon (fold 0.04x). Patron inverso CONFIRMADO.
- Tu02_DEFA5: 97% en higado (fold 20.4x). Subtipo metastasis-especifico.

## Bloque completado: expresion single-cell GSE225857

- Count matrix non-immune descargada: 90 MB gz, 1.4 GB decompressed, 17,516 genes x 41,892 celulas.
- Extraccion selectiva de 13 genes directamente desde .gz (evita descomprimir 1.4 GB).
- `scripts/validate_sc_expression.py` creado.
- Fix aplicado: cell IDs usan `.` en counts y `-` en metadata. 41,892/41,892 matched.

Resultados clave:

- HGF en fibroblastos: mean=0.674 (30.1%). En tumor: mean=0.004 (0.3%). Ratio 168x. CONFIRMADO.
- MET en tumor: mean=0.399 (27.6%). En fibroblastos: mean=0.009 (0.7%). Ratio 44x. CONFIRMADO.
- MET-MYC en tumor: r=0.1438, n=23,954, p<1e-300. CONFIRMADO.
- MYC-glicolisis: MYC-PGK1 r=0.36, MYC-TPI1 r=0.42. CONFIRMADO.
- Patron paracrino HGF(estroma)->MET(tumor): CONFIRMADO.

Archivos generados:

- `data_manifest/generated/gse225857_sc_expression_report.md`
- `data_manifest/generated/gse225857_gene_expression_summary.tsv`
- `data_manifest/generated/gse225857_sc_correlations.tsv`
- `data_manifest/generated/gse225857_extracted_genes.json`

Refinamiento de hipotesis:

- HGF no viene solo de MCAM+ CAFs. PRELP+ fibroblasts (F01) contribuyen mas HGF total en higado por abundancia.
- En higado: F01_PRELP (5,091 celulas, mean 0.667) + F02_MCAM (3,387 celulas, mean 0.371) = >90% del HGF.
- MYC es 45% mas alto en LCT que CCT, sugiriendo seleccion/induccion en el nicho metastasico.

## Bloque completado: spatial Visium GSE225857

- `scripts/analyze_gse225857_spatial.py` creado y ejecutado.
- Se reviso `filelist.txt` de GEO y se encontro que GSE225857 tiene 6 muestras Visium individuales manejables.
- Se descargaron barcodes, features, matrix.mtx y tissue_positions para `C1-C4` y `L1-L2`.
- No se descargaron imagenes.
- 22,260 spots in-tissue analizados.
- Reporte: `data_manifest/generated/gse225857_spatial_report.md`.

Resultados:

- LCT `caf_score~MET` spot-level promedio r=0.286.
- LCT `MYC~glycolysis_score` spot-level promedio r=0.645.
- Vecinos de spots CAF alto tienen MET enriquecido sobre fondo en LCT: ratio medio 1.948.
- Vecinos de spots HGF alto no enriquecen MET en LCT: ratio medio 0.844.

Interpretacion:

- Se fortalece un modelo de nicho CAF-tumor.
- Se debilita un modelo simplista de co-expresion directa `HGF~MET` en el mismo spot.
- La hipotesis refinada debe formularse como programa CAF compuesto: PRELP/MCAM fibroblasts + CAF-high neighborhoods + tumor MET+ + respuesta MYC/glicolisis.

## Bloque completado: permutaciones espaciales GSE225857

- `scripts/analyze_gse225857_spatial.py` extendido con prueba nula por permutaciones.
- CLI nuevo: `--permutations` y `--seed`.
- Salida nueva: `data_manifest/generated/gse225857_spatial_adjacency_permutation.tsv`.
- Reporte actualizado: `data_manifest/generated/gse225857_spatial_report.md`.
- Documento de investigacion: `InvestigacionSobreValidacionEspacialPorPermutacionesGSE225857.md`.
- Resumen: `ResumenInvestigacionSobreValidacionEspacialPorPermutacionesGSE225857.md`.

Resultados clave en LCT:

- `CAF -> MET`: L1 ratio 2.029 vs null 0.998, p empirico 0.002; L2 ratio 1.866 vs null 1.009, p empirico 0.002.
- `CAF -> MYC` y `CAF -> glycolysis_score`: p empirico 0.002 en L1 y L2.
- `HGF -> MET`: L1 ratio 0.874, p 0.994; L2 ratio 0.814, p 0.936.

Interpretacion actual:

- La senal espacial fuerte es `CAF-high`, no `HGF` aislado.
- `HGF` sigue como parte plausible del circuito paracrino por la evidencia single-cell.
- La tesis refinada es: `CAF-high spatial niches in CRLM associate with MET+ MYC/glycolytic tumor neighborhoods`.
- No afirmar causalidad clinica ni "descubrimiento confirmado"; si afirmar que la hipotesis gano prioridad computacional.

## Bloque completado: asociacion clinica TCGA-COAD

- `scripts/analyze_tcga_coad_clinical.py` creado.
- Clinica descargada desde UCSC Xena `TCGA.COAD.sampleMap/COAD_clinicalMatrix`.
- 329 muestras unidas con scores de firmas.
- Reporte: `data_manifest/generated/tcga_coad_clinical_association_report.md`.
- Tablas: `tcga_coad_clinical_signature_associations.tsv`, `tcga_coad_signature_survival.tsv`.
- Documentos: `InvestigacionSobreAsociacionClinicaTCGACOAD.md`, `ResumenInvestigacionSobreAsociacionClinicaTCGACOAD.md`.

Resultados clave:

- `mcam_caf` en N positivo vs N0: p=6.95e-04.
- `caf_core` en N positivo vs N0: p=8.57e-04.
- `mcam_caf` en invasion linfatica positiva: p=1.15e-03.
- `caf_core` en invasion linfatica positiva: p=2.27e-03.
- Supervivencia exploratoria: `caf_core` p=0.020, `mcam_caf` p=0.027.
- Composite `CAF/MET/MYC/glycolysis` no significativo en supervivencia bulk: p=0.493.

Interpretacion:

- El componente CAF/MCAM tiene senal clinica en primarios.
- El mecanismo completo no funciona como biomarcador bulk simple.
- Mantener la tesis como nicho espacial y buscar especificidad metastasica externa.

## Bloque completado: triage externo y GSE234804

- `scripts/triage_geo_external_validation.py` creado.
- Triage GEO ejecutado para `GSE225857`, `GSE226997`, `GSE231559`, `GSE234804`, `GSE178318`.
- Salidas: `geo_external_filelist.tsv`, `geo_external_validation_triage.tsv`, `geo_external_validation_triage_report.md`.
- `GSE234804` quedo como mejor candidato externo inmediato: H5Seurat individuales CRC/LM, 568.8 MB total.
- `GSE226997` queda como baja prioridad ahora: 41.2 GB y CRC primario, no CRLM directa.
- `scripts/validate_gse234804_h5seurat.py` creado.
- Se procesaron 3 CRC y 6 LM de GSE234804, 32,435 celulas.
- Salidas: `gse234804_sample_signature_scores.tsv`, `gse234804_lm_vs_crc_comparisons.tsv`, `gse234804_external_validation_report.md`.

Resultados GSE234804:

- `score_mcam_caf`: LM 0.057 vs CRC 0.103.
- `score_caf_core`: LM 0.046 vs CRC 0.065.
- `score_myc_glycolysis_core`: LM 2.109 vs CRC 3.312.
- `MET`: LM 0.341 vs CRC 0.236.
- `HGF`: LM 0.014 vs CRC 0.011.

Interpretacion:

- GSE234804 no replica el modelo como firma sample-level LM-vs-CRC.
- Esto no mata la hipotesis espacial, pero elimina una lectura demasiado amplia.
- La tesis defendible ahora es arquitectura espacial/cell-state-specific, no biomarcador promedio.
- Proxima validacion debe tener anotaciones celulares o coordenadas espaciales.

## Proximo objetivo recomendado
Validacion cruzada y extension.

Ruta recomendada:

1. Buscar validacion independiente con cell-type labels o spatial real.
2. Explorar si GSE234804 tiene anotaciones celulares recuperables en suplementos/paper.
3. Revisar GSE231559 para mapeo fenotipo/cell-state.
4. Buscar scCRLM/Cancer Diversity Asia como ruta spatial externa manejable.

## Criterios de exito del proximo bloque
El bloque cuenta como exitoso si deja:

- Evidencia de reproducibilidad en un segundo dataset independiente.
- O: analisis espacial que confirme co-localizacion.
- O: documento de limitaciones y plan alternativo claro.
- Actualizacion en documentos vivos.
- Commit y push.

## Reglas de trabajo
- Trabajar autonomamente, sin pedir permiso para pasos razonables.
- Mantener el foco en `mCAF-HGF-MET-MYC-glycolysis`.
- No abrir nuevas lineas de cancer salvo que aparezcan como validacion comparativa.
- No afirmar causalidad clinica.
- No afirmar utilidad terapeutica sin validacion.
- No borrar ni revertir cambios del usuario.
- Mantener `.env` fuera de git.
- Preferir archivos markdown y scripts reproducibles simples.
- Despues de cada bloque util: `git status`, commit y push.

## Comandos utiles
Preparar firmas:

```powershell
python scripts/prepare_signatures.py
```

Verificar disponibilidad contra HGNC:

```powershell
python scripts/check_gene_availability.py
```

Verificar contra universo local:

```powershell
python scripts/check_gene_availability.py --universe nombre=data_manifest/gene_universes/archivo_genes.txt
```

Chequeo de diff:

```powershell
git diff --check
```

Commit/push:

```powershell
git add .
git commit -m "Short useful message"
git push
```

## Si hay que decidir
Decidir asi:

1. Priorizar validacion liviana.
2. Priorizar reproducibilidad.
3. Priorizar hipotesis falsables.
4. Evitar descargas pesadas hasta que una pregunta concreta lo justifique.
5. Mantener documentos vivos actualizados.

## Mensaje para continuar
La siguiente accion ideal es:

`Buscar validacion independiente o especificidad del patron CAF-high -> MET/MYC/glycolysis, empezando por una revision liviana de GSE226997, datasets 2025 o META-PRISM.`

Si eso se bloquea, documentar el bloqueo y crear un plan alternativo reproducible.

## Actualizacion para Claude: ola 003E literatura 2026

Fecha: 2026-04-27 16:22:03 -03:00

Se hizo una busqueda PubMed reproducible 2025-2026:

```powershell
python scripts/search_pubmed_crlm_latest.py --retmax 80
```

Archivos nuevos:

- `scripts/search_pubmed_crlm_latest.py`
- `data_manifest/generated/pubmed_crlm_latest_2025_2026.tsv`
- `data_manifest/generated/pubmed_crlm_latest_2025_2026_report.md`
- `InvestigacionSobreLiteratura2026NichoCRLM.md`
- `ResumenInvestigacionSobreLiteratura2026NichoCRLM.md`

Resultado estrategico:

La hipotesis ya no debe presentarse como `HGF-MET-MYC-glycolysis` lineal. La formulacion vigente es:

`CAF-high layered niche model in CRLM`

En palabras:

`Niches CAF-high in CRLM may coordinate a tumor metabolic interface (MET/MYC/glycolysis/one-carbon metabolism) and an immunosuppressive myeloid/T-cell interface (SPP1/CXCL12/MIF/CD44/FN1/HLA-DRB5/CD74/CXCR4/LGALS9).`

Papers 2026 clave:

- PMID 41807965: mCAF - SPP1+ macrophage - T-cell stress/exhaustion spatial niche.
- PMID 41051794: SPP1 induces CXCL12 in CAFs and drives immunotherapy resistance.
- PMID 41715121: SPP1+ and HLA-DRB5+ macrophages as spatial immune modulators.
- PMID 41655559: SPP1+ macrophage - FADS1+ tumor crosstalk via PDGFB-PDGFRB.
- PMID 41195591: proteogenomic CRLM metabolism, SHMT1/formate/AMPK and PIM/NDRG1.
- PMID 41940986: compartment-specific GLUT1 at invasive margin.

Firmas nuevas agregadas a `data_manifest/signatures.yml`:

- `spp1_cxcl12_caf_myeloid_axis`
- `spp1_macrophage_fads1_pdgfb_axis`
- `hla_drb5_macrophage_axis`
- `stromal_myeloid_risk_2026`
- `sema3c_nrp2_lmic_axis`
- `crlm_metabolic_vulnerabilities_2026`
- `radioresistance_morf4l1`
- `marco_cash_macrophage_axis`
- `glut1_invasive_margin_axis`

Proxima accion ideal:

1. Ejecutar `python scripts/prepare_signatures.py`.
2. Ejecutar `python scripts/check_gene_availability.py --universe tcga_coad=data_manifest/gene_universes/tcga_coad_genes.txt`.
3. Extender `scripts/analyze_gse225857_spatial.py` para scorear firmas dinamicas desde `signatures_normalized.tsv`.
4. Probar si `CAF-high` se asocia espacialmente con `SPP1/CXCL12` y `HLA-DRB5` ademas de `MET/MYC/glycolysis`.
5. Buscar arquitectura en capas, no solo correlaciones.

Regla interpretativa:

No decir "descubrimos SPP1"; eso ya esta publicado. El posible aporte es integrar el nicho metabolico y el nicho inmunosupresor en un modelo espacial reproducible.

## Actualizacion para Claude: ola 003F validacion espacial 2026

Fecha: 2026-04-27 16:50:00 -03:00

Se ejecuto la primera validacion tecnica del pivot 2026.

Nuevo script:

```powershell
python scripts/analyze_gse225857_spatial_2026.py --permutations 500
```

Salidas:

- `data_manifest/generated/gse225857_spatial_2026_signature_availability.tsv`
- `data_manifest/generated/gse225857_spatial_2026_spot_scores.tsv`
- `data_manifest/generated/gse225857_spatial_2026_correlations.tsv`
- `data_manifest/generated/gse225857_spatial_2026_adjacency_permutation.tsv`
- `data_manifest/generated/gse225857_spatial_2026_report.md`

Documentos:

- `InvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md`
- `ResumenInvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md`

Resultados LCT principales:

- `CAF -> SPP1/CXCL12`: L1 ratio 1.497, L2 ratio 1.522, p empirico 0.002.
- `CAF -> HLA-DRB5-like`: L1 ratio 1.564, L2 ratio 1.403, p empirico 0.002.
- `SPP1/CXCL12 -> MYC/glycolysis`: L1 ratio 1.578, L2 ratio 1.932, p empirico 0.002.
- `HLA-DRB5-like -> MYC/glycolysis`: L1 ratio 1.548, L2 ratio 1.563, p empirico 0.002.

Interpretacion:

Hay evidencia de un macro-nicho estromal-inmune-metabolico `CAF-high` en GSE225857 LCT. Todavia no decir que hay capas microscopicas separadas ni causalidad. Visium mezcla celulas y las firmas 2026 tienen overlap de genes.

Proxima accion recomendada:

Se crearon firmas desolapadas 2026 y se repitio el analisis.

Resultado del control:

- `CAF -> SPP1/CXCL12-lite`: ratio medio LCT 1.513.
- `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: ratio medio LCT 1.602.
- `CAF -> HLA-DRB5-lite`: ratio medio 1.470, pero impulsado por L1; L2 queda debil/no robusto.
- `HLA-DRB5-lite -> MYC/glycolysis-lite`: ratio medio 1.137.

Interpretacion actual:

La rama `SPP1/CXCL12` es robusta aun sin genes compartidos. La rama `HLA-DRB5` es realista como candidata secundaria, pero lesion-dependiente. Priorizar SPP1/CXCL12 para el siguiente bloque.

## Actualizacion para Claude: ola 003G validacion externa paired y spatial

Fecha: 2026-04-27 17:53:00 -03:00

Se busco el estado web/literatura 2026 y se avanzo con dos validaciones externas.

Nuevos scripts:

```powershell
python scripts/validate_gse245552_paired_scrna.py
python scripts/validate_gse217414_spatial_external.py --permutations 500
```

Nuevos documentos:

- `InvestigacionSobreValidacionExternaPairedYSpatialCRLM2026.md`
- `ResumenInvestigacionSobreValidacionExternaPairedYSpatialCRLM2026.md`

Nuevas salidas GSE245552:

- `data_manifest/generated/gse245552_sample_manifest.tsv`
- `data_manifest/generated/gse245552_sample_signature_scores.tsv`
- `data_manifest/generated/gse245552_lm_vs_primary_comparisons.tsv`
- `data_manifest/generated/gse245552_paired_deltas.tsv`
- `data_manifest/generated/gse245552_external_validation_report.md`

Nuevas salidas GSE217414:

- `data_manifest/generated/gse217414_spatial_signature_availability.tsv`
- `data_manifest/generated/gse217414_spatial_correlations.tsv`
- `data_manifest/generated/gse217414_spatial_adjacency_permutation.tsv`
- `data_manifest/generated/gse217414_spatial_spot_scores.tsv`
- `data_manifest/generated/gse217414_spatial_external_report.md`

Resultado GSE245552:

- `myeloid SPP1/CXCL12-lite`: LM/primario 1.844, p = 1.34e-04, positivo 13/13 pares.
- `myeloid HLA-DRB5-lite`: LM/primario 1.478, p = 1.72e-03, positivo 12/13 pares.
- `CAF SPP1/CXCL12-lite`: LM/primario 1.361, p = 0.0307, positivo 11/13 pares.
- `tumor MYC/glycolysis-lite`: LM/primario 0.967, p = 0.692, positivo 5/13 pares.

Resultado GSE217414:

- 4 muestras Visium CRLM, 10,674 spots.
- `CAF -> SPP1/CXCL12-lite`: positivo 4/4, ratio medio 1.346.
- `CAF -> HLA-DRB5-lite`: positivo 4/4, ratio medio 1.391.
- `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: positivo 4/4, ratio medio 1.776.
- `HLA-DRB5-lite -> MYC/glycolysis-lite`: positivo 4/4, ratio medio 1.467.

Lectura para seguir:

No decir que el terreno es virgen. La oportunidad es una historia multi-dataset:

`stromal-myeloid SPP1/CXCL12/HLA-DRB5 states are enriched in liver metastasis and spatially couple to tumor MYC/glycolysis programs.`

Siguiente paso recomendado:

1. Crear controles negativos y firmas aleatorias emparejadas por expresion.
2. Implementar nulos espaciales estratificados para GSE217414 y GSE225857.
3. Consolidar ambos datasets spatial en una tabla unica de efectos por muestra.
4. Mejorar GSE245552 con anotacion celular/pseudobulk.
5. Preparar figuras de manuscrito.

## Actualizacion para Claude: ola 003H agentes y controles spatial

Fecha: 2026-04-29 02:47:00 -03:00

Se actuo como agente padre/arquitecto y se lanzaron dos agentes:

- Investigador web/literatura/datasets.
- Auditor metodologico.

Roadmap nuevo:

- `RoadmapAgentesAutonomosCRLM.md`

Investigador:

- Confirmo que no hay novedad en genes sueltos: `SPP1/CXCL12`, `HLA-DRB5`, mCAF, `SPP1+ TAM`, T-cell stress/exhaustion, `HGF-MET-MYC-glycolysis` ya estan publicados.
- Recomendo foco en arquitectura local/metabolica y spFBA/lactate consumption 2026.

Auditor:

- Critico nulo espacial global, circularidad por `MYC`, leakage `PTPRC`, falta normalizacion por UMI y proxies scRNA gruesos.
- Recomendo ablation, random controls, nulos por bloques/estratificados y pseudobulk.

Scripts nuevos:

```powershell
python scripts/consolidate_spatial_niche_effects.py
python scripts/audit_spatial_signature_specificity.py --permutations 200 --random-controls 200
python scripts/audit_spatial_block_permutation.py --permutations 500 --block-size 12
```

Resultados:

- `spatial_niche_multidataset_report.md`: 7/7 efectos positivos en 6/6 muestras spatial.
- `spatial_niche_specificity_report.md`: los efectos sobreviven ablation, pero no superan random controls dentro del panel extraido.
- `spatial_niche_block_permutation_report.md`: `SPP1/CXCL12-lite -> MYC/glycolysis-lite` sobrevive 6/6 bajo nulo por bloques; `HLA-DRB5-lite -> MYC/glycolysis-lite` sobrevive 5/6; `CAF -> MET` solo 2/6.

Nueva decision:

- Subir prioridad: `stromal/myeloid-like regions -> MYC/glycolysis local adjacency`.
- Bajar prioridad: `CAF -> MET` como claim central.
- Cuidar nombre: `SPP1/CXCL12-lite` desolapado realmente es `CXCL12/FN1/CD44/HIF1A/CTNNB1-like` porque no contiene `SPP1`.

Siguiente trabajo ideal:

1. Random controls full-transcriptome.
2. Sensibilidad block-size 8/12/16/20.
3. Residualizar por UMI/coordenadas.
4. Leave-one-gene-out.
5. Integrar spFBA/lactate consumption.
6. GSE245552 pseudobulk con anotacion celular real.

## Actualizacion para Claude: ola 003I nicho lactato/HLA-DRB5

Fecha: 2026-04-29 02:58:54 -03:00

Se abrio una ruta mas novedosa que el eje `CAF -> MET`: conectar `HLA-DRB5-like` macrophage neighborhoods con metabolismo no canonico de lactato/pyruvato en CRLM.

Razon:

- spFBA 2026 reporta lactate uptake en CRC/CRLM y reruteo no canonico hacia pyruvato/transaminacion/reductive TCA.
- Xie et al. 2026 reportan `SPP1+` y `HLA-DRB5+` macrophages como moduladores espaciales inmunes en CRLM.
- La grieta no cerrada es el puente espacial entre estado mieloide y metabolismo/flux.

Nuevo script:

```powershell
python scripts/analyze_spatial_lactate_axis.py --permutations 500 --block-size 12
```

Salidas:

- `data_manifest/generated/spatial_lactate_axis_effects.tsv`
- `data_manifest/generated/spatial_lactate_axis_summary.tsv`
- `data_manifest/generated/spatial_lactate_axis_report.md`

Documentos:

- `InvestigacionSobreNichoLactatoSpatialCRLM2026.md`
- `ResumenInvestigacionSobreNichoLactatoSpatialCRLM2026.md`

Resultados clave:

- `HLA-DRB5-like -> glutamate_transamination`: positivo 6/6, block p <= 0.05 en 5/6, ratio medio 1.764.
- `HLA-DRB5-like -> pyruvate_mito_entry`: positivo 6/6, block p <= 0.05 en 5/6, ratio medio 1.571.
- `HLA-DRB5-like -> lactate_import_anabolic`: positivo 6/6, block p <= 0.05 en 4/6, ratio medio 1.564.
- La rama `CXCL12/FN1/CD44-like` es positiva pero menos especifica bajo nulo por bloques.

Nueva hipotesis:

`Spatial HLA-DRB5-like myeloid niches may mark immune-metabolic CRLM regions enriched for pyruvate mitochondrial entry and glutamate transamination programs, consistent with non-canonical lactate-carbon routing.`

Advertencia:

No es flux real. `LDHA/LDHB` no estaban disponibles en los feature universes probados. El claim debe formularse como proxy spatial y priorizacion de hipotesis.

Siguiente accion ideal:

1. Obtener o reproducir mapas spFBA/FES de lactate uptake, pyruvate/transamination y reductive TCA.
2. Probar `HLA-DRB5-like -> FES` con nulo por bloques.
3. Residualizar por UMI/coordenadas/region histologica.
4. Hacer random controls full-transcriptome emparejados por expresion.
5. Preparar una figura que conecte literatura gap, spatial proxy y flux validation.

## Actualizacion para Claude: ola 003J auditoria robusta lactato/HLA-DRB5

Fecha: 2026-04-29 03:23:00 -03:00

Se ejecuto la auditoria reviewer-hostile del eje `HLA-DRB5-like -> pyruvate/transamination`.

Nuevo script:

```powershell
python scripts/audit_lactate_axis_robustness.py --permutations 200 --ablation-permutations 100 --random-controls 100 --block-sizes 8,12,16,20
```

Salidas clave:

- `data_manifest/generated/lactate_axis_robustness_report.md`
- `data_manifest/generated/lactate_axis_robustness_blocksize_summary.tsv`
- `data_manifest/generated/lactate_axis_robustness_ablation_summary.tsv`
- `data_manifest/generated/lactate_axis_robustness_random_controls_summary.tsv`
- `data_manifest/generated/lactate_axis_robustness_residualized_summary.tsv`

Resultado:

- Sobrevive block-size y ablation sin `PTPRC`.
- Falla `HLA-DRB5-only`; no es un gen aislado.
- Falla random controls full-transcriptome: 0/6 en pyruvate/transamination, original y no-PTPRC.
- Falla residualizacion por profundidad/coordenadas: 0/6 o 1/6 significativo.

Nueva decision:

No vender nicho lactato/HLA-DRB5 con proxies transcriptomicos. La rama queda como co-ocurrencia regional interesante.

Siguiente trabajo ideal:

`spFBA/FES or stop`

Si los mapas de flux reales rescatan lactate uptake/transamination cerca de `HLA-DRB5-like`, vuelve a ser candidato fuerte. Si no, cerrar esta rama como artefacto regional y volver al nucleo estromal/mieloide local.
