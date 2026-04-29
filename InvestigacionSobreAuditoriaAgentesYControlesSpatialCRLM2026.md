# Investigacion sobre auditoria de agentes y controles spatial CRLM 2026

Fecha: 2026-04-29 02:47:00 -03:00

## Objetivo

Esta ola transforma el avance anterior en una prueba mas adulta. El usuario pidio que el agente padre actue como arquitecto, lance un agente investigador y un agente auditor, y continue buscando una ruta hacia un hallazgo digno de paper.

Se ejecuto:

- roadmap de agentes: `RoadmapAgentesAutonomosCRLM.md`;
- agente investigador web/literatura/datasets;
- agente auditor metodologico;
- consolidacion multi-dataset spatial;
- auditoria de especificidad por ablacion/random controls;
- auditoria por permutacion espacial en bloques.

## Resultado de los agentes

### Agente investigador

El investigador confirmo que no hay novedad en genes sueltos:

- `SPP1/CXCL12` en CRLM/CAF/inmunorresistencia ya esta publicado.
- `SPP1+ TAM` y estados T stressed/exhausted ya estan publicados.
- `HLA-DRB5+ macrophages` ya son una poblacion relevante en CRLM.
- `mCAF-SPP1+ macrophage-T cell niche` en capas ya existe en la literatura 2026.
- `HGF-MET-MYC-glycolysis` ya fue propuesto como interaccion estroma-tumor.

La posible novedad queda en una formulacion mas fina:

`El nicho CAF/SPP1-CXCL12/HLA-DRB5 no solo es inmunosupresor; podria marcar una arquitectura metabolica local donde programas tumorales MYC/glycolysis aparecen por vecindad, no como aumento global de todas las celulas tumorales metastasicas.`

El investigador tambien marco una ruta importante: spFBA 2026 muestra lactate consumption en CRC/LM y podria convertir nuestro brazo `MYC/glycolysis` en una pregunta metabolica mas fina que la glicolisis clasica.

### Agente auditor

El auditor bajo el entusiasmo de forma sana:

- El nulo espacial global era demasiado debil.
- Habia circularidad parcial: `MYC/glycolysis-lite` incluia `MYC`.
- En scRNA, el proxy mieloide y la firma `HLA-DRB5-lite` comparten `PTPRC`, creando leakage.
- Falta normalizacion por profundidad/UMI.
- La estadistica paired es exploratoria.
- El nombre `SPP1/CXCL12-lite` es mas fuerte que la firma real, porque la version desolapada excluye `SPP1`.

Claims seguros:

- soporte exploratorio multi-dataset para acoplamiento espacial estromal/mieloide-metabolico;
- rama mieloide/CAF sube en paired scRNA;
- brazo tumoral MYC/glycolysis no sube globalmente y parece local;
- la hipotesis merece controles paper-grade.

Claims peligrosos:

- descubrimiento confirmado;
- nicho causal;
- ligando-receptor probado;
- biomarcador clinico;
- target terapeutico;
- terreno virgen por genes individuales.

## Consolidacion multi-dataset spatial

Script:

`scripts/consolidate_spatial_niche_effects.py`

Salidas:

- `data_manifest/generated/spatial_niche_multidataset_effects.tsv`
- `data_manifest/generated/spatial_niche_multidataset_summary.tsv`
- `data_manifest/generated/spatial_niche_multidataset_report.md`

Resultado:

Antes de controles mas duros, los 7 efectos clave fueron positivos en 6/6 muestras spatial combinadas entre GSE225857 y GSE217414:

- `CAF -> HLA-DRB5-lite`: 6/6 positivo, 6/6 p <= 0.05, ratio medio 1.417.
- `CAF -> MET`: 6/6 positivo, 5/6 p <= 0.05, ratio medio 1.723.
- `CAF -> SPP1/CXCL12-lite`: 6/6 positivo, 5/6 p <= 0.05, ratio medio 1.399.
- `HLA-DRB5-lite -> MYC`: 6/6 positivo, 5/6 p <= 0.05, ratio medio 1.330.
- `HLA-DRB5-lite -> MYC/glycolysis-lite`: 6/6 positivo, 6/6 p <= 0.05, ratio medio 1.357.
- `SPP1/CXCL12-lite -> MYC`: 6/6 positivo, 6/6 p <= 0.05, ratio medio 1.625.
- `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: 6/6 positivo, 6/6 p <= 0.05, ratio medio 1.718.

Lectura:

La reproducibilidad bruta es fuerte. Pero justamente por ser tan fuerte, debia auditarse contra gradientes regionales y firmas random.

## Auditoria 1: ablacion y random controls

Script:

`scripts/audit_spatial_signature_specificity.py`

Salidas:

- `data_manifest/generated/spatial_niche_specificity_audit.tsv`
- `data_manifest/generated/spatial_niche_specificity_summary.tsv`
- `data_manifest/generated/spatial_niche_specificity_report.md`

Controles:

- `SPP1/CXCL12-lite` se redujo a `CXCL12/FN1/CD44`, removiendo `HIF1A/CTNNB1`.
- `HLA-DRB5-lite` se testeo sin `PTPRC`.
- `MYC/glycolysis-lite` se testeo sin `MYC`.
- Se agregaron random controls emparejados por expresion dentro del panel de genes ya extraido.

Resultado:

- `CAF -> CXCL12/FN1/CD44`: queda positivo 5/6, pero no supera random controls.
- `CAF -> HLA-DRB5-no-PTPRC`: positivo 6/6, pero solo 1/6 supera random controls.
- `CXCL12/FN1/CD44 -> glycolysis-no-MYC`: positivo 6/6, pero 0/6 supera random controls.
- `HLA-DRB5-no-PTPRC -> glycolysis-no-MYC`: positivo 6/6, pero 0/6 supera random controls.

Interpretacion:

La senal no desaparece al quitar genes problematicos, lo cual es bueno. Pero no supera random controls dentro del panel extraido, lo cual obliga a decir que el patron puede representar un programa regional amplio y no una especificidad molecular fina. Este control no es definitivo porque el universo random es limitado, pero baja el claim.

## Auditoria 2: permutacion espacial por bloques

Script:

`scripts/audit_spatial_block_permutation.py`

Salidas:

- `data_manifest/generated/spatial_niche_block_permutation.tsv`
- `data_manifest/generated/spatial_niche_block_permutation_summary.tsv`
- `data_manifest/generated/spatial_niche_block_permutation_report.md`

Metodo:

En lugar de permutar targets globalmente, se permutaron dentro de bloques espaciales gruesos. Esto preserva parcialmente gradientes regionales y es mas exigente que el nulo anterior, aunque todavia no reemplaza anotacion histologica manual.

Resultado:

- `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: 6/6 positivo, 6/6 block p <= 0.05, ratio medio 1.718. Es el efecto mas fuerte.
- `SPP1/CXCL12-lite -> MYC`: 6/6 positivo, 5/6 block p <= 0.05, ratio medio 1.625.
- `HLA-DRB5-lite -> MYC/glycolysis-lite`: 6/6 positivo, 5/6 block p <= 0.05, ratio medio 1.357.
- `HLA-DRB5-lite -> MYC`: 6/6 positivo, 5/6 block p <= 0.05, ratio medio 1.330.
- `CAF -> HLA-DRB5-lite`: 6/6 positivo, 5/6 block p <= 0.05, ratio medio 1.417.
- `CAF -> SPP1/CXCL12-lite`: 6/6 positivo, pero solo 4/6 block p <= 0.05. Queda parcial.
- `CAF -> MET`: 6/6 positivo, pero solo 2/6 block p <= 0.05. Esta rama baja prioridad.

Interpretacion:

El nulo por bloques salva lo mas importante: los modulos estromal/mieloide hacia `MYC/glycolysis-lite`. En cambio, `CAF -> MET` parece mucho mas explicable por dominios regionales y debe bajarse como claim central.

## Nueva lectura de la hipotesis

Antes:

`CAF-high organiza SPP1/CXCL12/HLA-DRB5 y MET/MYC/glycolysis.`

Ahora:

`En datasets spatial CRLM, regiones CXCL12/FN1/CD44-like y HLA-DRB5-like muestran vecindad reproducible con MYC/glycolysis, incluso bajo nulo espacial por bloques; pero la especificidad molecular fina aun no supera random controls del panel extraido.`

Esto es menos vistoso, pero mas defendible.

## Decision

La hipotesis sigue viva, pero se estrecha:

- Suben: `SPP1/CXCL12-lite -> MYC/glycolysis-lite`, `HLA-DRB5-lite -> MYC/glycolysis-lite`.
- Queda parcial: `CAF -> SPP1/CXCL12-lite`.
- Baja prioridad: `CAF -> MET` como afirmacion espacial central.
- Debe renombrarse con cuidado `SPP1/CXCL12-lite`, porque la firma desolapada es realmente `CXCL12/FN1/CD44/HIF1A/CTNNB1`.

## Proximo paso

1. Full-transcriptome random controls, no solo panel extraido.
2. Sensibilidad a tamano de bloque: 8, 12, 16, 20.
3. Residualizacion por profundidad/UMI y coordenadas.
4. Ablation leave-one-gene-out formal.
5. Integracion spFBA/lactate consumption si los datos 2026 son accesibles.
6. Anotacion/pseudobulk real en GSE245552 para evitar proxies con leakage.

## Fuentes externas clave

- mCAF-SPP1+ macrophage-T cell niche 2026: https://link.springer.com/article/10.1186/s12967-026-07978-6
- SPP1/CXCL12 e inmunorresistencia CRLM: https://pmc.ncbi.nlm.nih.gov/articles/PMC12757724/
- SPP1+ y HLA-DRB5+ macrophages: https://pubmed.ncbi.nlm.nih.gov/41715121/
- HGF-MET-MYC-glycolysis: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
- spFBA lactate consumption CRC/LM 2026: https://www.nature.com/articles/s41540-026-00654-x
- GSE206552 spatial senescence CRLM: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE206552
