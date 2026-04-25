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

## Proximo objetivo recomendado
Crear el primer universo genico dataset-especifico liviano.

Ruta recomendada:

1. Empezar con TCGA/GDC antes que GEO pesado.
2. Crear `data_manifest/gene_universes/`.
3. Crear un script para obtener o construir un universo de genes de `TCGA-COAD` y luego `TCGA-READ`.
4. Usar ese universo con:

```powershell
python scripts/check_gene_availability.py --universe tcga_coad=data_manifest/gene_universes/tcga_coad_genes.txt
```

5. Generar un reporte nuevo en `data_manifest/generated/`.
6. Actualizar `PlanValidacionCRLM.md` y `Roadmap.md`.
7. Commit y push.

## Proximo bloque tecnico exacto
Crear:

- `scripts/fetch_gdc_gene_universe.py`
- `data_manifest/gene_universes/README.md`
- `data_manifest/gene_universes/tcga_coad_genes.txt` si se logra obtener datos livianos.

Objetivo del script:

- Consultar GDC/TCGA de forma liviana.
- Obtener una lista de genes disponibles para TCGA-COAD, preferentemente desde metadata o un archivo de expresion manejable.
- No descargar BAM/FASTQ ni archivos pesados.
- Guardar solo el universo genico.
- Reusar `scripts/check_gene_availability.py` para comparar las firmas.

Si GDC resulta incomodo:

- Crear primero un universo manual/provisional desde HGNC subset o desde un recurso oficial de GENCODE/HGNC.
- Documentar claramente que es un universo provisional, no validacion TCGA real.

## Criterios de exito del proximo bloque
El bloque cuenta como exitoso si deja:

- Un script reproducible.
- Un archivo de universo genico dataset-especifico o un reporte claro de bloqueo.
- Un reporte de disponibilidad de firmas contra ese universo.
- Actualizacion en `PlanValidacionCRLM.md`.
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

`Crear el primer universo genico TCGA/GDC liviano y correr check_gene_availability.py contra ese universo.`

Si eso se bloquea, documentar el bloqueo y crear un plan alternativo reproducible.
