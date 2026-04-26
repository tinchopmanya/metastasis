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

## Proximo objetivo recomendado
Validar expresion gen-especifica en single-cell.

Ruta recomendada:

1. Evaluar GSE225857 como fuente de datos single-cell accesible (~607 MB).
2. Si se descarga, verificar que HGF se expresa en CAF/mCAF y MET en tumor.
3. Evaluar correlacion MET-MYC dentro del compartimento tumoral.
4. Evaluar co-localizacion mCAF-tumor si hay datos espaciales.
5. Si GSE225857 es demasiado pesado, buscar matrices procesadas o subsets.

## Criterios de exito del proximo bloque
El bloque cuenta como exitoso si deja:

- Un plan claro de extraccion de GSE225857 o alternativa.
- Si se logra acceso: localización celular de HGF y MET confirmada o refutada.
- Si no: un documento de bloqueo con alternativas.
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
- Preferir archiv