# Resumen investigacion auditoria de agentes y controles spatial CRLM 2026

Fecha: 2026-04-29 02:47:00 -03:00

## Resumen corto

Se organizo una nueva fase con agente padre como arquitecto, un agente investigador y un agente auditor. El resultado fue util porque aumento la calidad epistemica del proyecto: la hipotesis sigue viva, pero se estrecho de forma importante.

El investigador confirmo que no hay novedad en genes sueltos. `SPP1/CXCL12`, `HLA-DRB5+ macrophages`, mCAFs, `SPP1+ TAM`, T-cell stress/exhaustion y `HGF-MET-MYC-glycolysis` ya estan publicados en CRLM o contexto cercano. La posible novedad no es "descubrir SPP1", sino mostrar una arquitectura multi-dataset donde un modulo estromal/mieloide se acopla localmente a programas tumorales `MYC/glycolysis`.

El auditor detecto riesgos fuertes: el nulo espacial global era debil, habia circularidad parcial porque `MYC/glycolysis-lite` contiene `MYC`, el proxy mieloide scRNA comparte `PTPRC` con `HLA-DRB5-lite`, falta normalizacion por profundidad/UMI, y la firma llamada `SPP1/CXCL12-lite` realmente no contiene `SPP1` despues de desolapar.

Se creo `scripts/consolidate_spatial_niche_effects.py`. La consolidacion bruta fue fuerte: 7/7 efectos clave fueron positivos en 6/6 muestras spatial entre GSE225857 y GSE217414. Pero esa fuerza podia deberse a gradientes regionales.

Se creo `scripts/audit_spatial_signature_specificity.py`. Al quitar genes problematicos, los efectos siguieron mayormente positivos. Sin embargo, no superaron random controls emparejados dentro del panel extraido. Esto baja la especificidad molecular fina y obliga a hablar de programas regionales amplios.

Se creo `scripts/audit_spatial_block_permutation.py`. Bajo permutacion por bloques, el efecto mas robusto fue `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: 6/6 muestras positivas y 6/6 con block p <= 0.05. Tambien sobrevivieron `HLA-DRB5-lite -> MYC/glycolysis-lite` y `SPP1/CXCL12-lite -> MYC` en 5/6. En cambio, `CAF -> MET` solo sobrevivio en 2/6 y debe bajar prioridad.

La formulacion actual mas defendible es:

`Regiones CXCL12/FN1/CD44-like y HLA-DRB5-like en CRLM muestran vecindad reproducible con MYC/glycolysis bajo nulo espacial por bloques, pero la especificidad molecular fina aun necesita controles full-transcriptome.`

## Recomendacion

Seguir, pero con disciplina de reviewer hostil. El siguiente bloque debe ser full-transcriptome random controls, sensibilidad de block-size, residualizacion por UMI/coordenadas, leave-one-gene-out formal e integracion con spFBA/lactate consumption 2026.
