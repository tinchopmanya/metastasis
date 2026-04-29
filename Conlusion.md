# Conclusion dinamica vigente

Fecha de actualizacion: 2026-04-29 02:47:00 -03:00

## Linea activa

La linea activa sigue siendo:

`cancer colorrectal -> metastasis hepatica -> nicho metastasico hepatico`

## Estado real: terreno virgen o no

No estamos en terreno virgen por componentes aislados. `CAF`, `SPP1`, `CXCL12`, `HLA-DRB5`, `MET`, `MYC` y glicolisis ya aparecen con fuerza en la literatura CRLM 2025-2026.

Si estamos en una zona con potencial de hallazgo computacional, pero mas estrecha de lo que parecia antes de los controles:

`un modelo multi-dataset donde regiones CXCL12/FN1/CD44-like y HLA-DRB5-like se acoplan espacialmente a programas tumorales MYC/glycolysis en CRLM.`

La novedad posible no es un gen. Es la arquitectura reproducible y su relacion con metabolismo local. La especificidad molecular fina todavia no esta demostrada.

## Hipotesis vigente

La mejor formulacion actual es:

`CXCL12/FN1/CD44 - HLA-DRB5 - MYC/glycolysis spatial niche model in CRLM`

En CRLM, regiones estromal-mieloides `CXCL12/FN1/CD44-like` y `HLA-DRB5-like` se aproximan espacialmente a programas tumorales `MYC/glycolysis`. Sin embargo, el brazo tumoral metabolico no sube de forma uniforme en todas las celulas epiteliales metastasicas, y los controles random iniciales sugieren que parte del patron puede ser un gradiente regional amplio.

Traduccion biologica prudente:

- La rama mieloide/CAF es el nucleo reproducible actual.
- La rama tumoral `MYC/glycolysis` parece mas local/espacial que global.
- `HGF-MET-MYC` queda como rama plausible pero ya no debe ser el claim central; `CAF -> MET` bajo nulo por bloques sobrevivio solo en 2/6 muestras.

## Evidencia propia acumulada

### TCGA-COAD bulk

- `MET-MYC` r = 0.515.
- `MYC-glycolysis` r = 0.422.
- `CAF-HGF` r = 0.675.
- `HGF-MET` no fue significativo, consistente con paracrinia diluida.
- `mcam_caf` y `caf_core` se asocian con N positivo, invasion linfatica y supervivencia exploratoria por mediana.

### GSE225857 single-cell y spatial

- `HGF` se concentra en fibroblastos.
- `MET` se concentra en tumor.
- `MYC-glycolysis` es fuerte en tumor.
- En spatial LCT, vecinos de `CAF-high` enriquecen `MET`, `MYC` y `glycolysis_score` contra 500 permutaciones.
- Con firmas 2026, `CAF-high` se acopla a `SPP1/CXCL12`, `HLA-DRB5-like` y `MYC/glycolysis`.
- El control desolapado mantiene fuerte la rama `SPP1/CXCL12-lite`; `HLA-DRB5-lite` queda mas heterogenea.

### GSE234804 externo

- No valida una firma sample-level simple LM-vs-CRC para `mcam_caf`, `caf_core` ni `myc_glycolysis_core`.
- Esto obliga a formular la hipotesis como arquitectura local/cell-state-specific.

### GSE245552 paired scRNA externo

- 39 muestras procesadas.
- 13 pares utiles primario/metastasis hepatica.
- `myeloid_proxy__score_spp1_cxcl12_axis_desoverlap_2026`: LM/primario 1.844, p = 1.34e-04, positivo 13/13 pares.
- `myeloid_proxy__score_hla_drb5_macrophage_axis_desoverlap_2026`: LM/primario 1.478, p = 1.72e-03, positivo 12/13 pares.
- `caf_proxy__score_spp1_cxcl12_axis_desoverlap_2026`: LM/primario 1.361, p = 0.0307, positivo 11/13 pares.
- `tumor_epithelial_proxy__score_myc_glycolysis_desoverlap_2026`: LM/primario 0.967, p = 0.692, positivo 5/13 pares.

Lectura: la rama mieloide/CAF sube pareada; el tumor `MYC/glycolysis` no sube como promedio global.

### GSE217414 external spatial

- 4 muestras Visium CRLM.
- 10,674 spots in-tissue.
- 500 permutaciones por prueba.
- `CAF -> SPP1/CXCL12-lite`: ratio medio 1.346, positivo 4/4, p <= 0.05 en 3/4.
- `CAF -> HLA-DRB5-lite`: ratio medio 1.391, positivo 4/4, p <= 0.05 en 4/4.
- `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: ratio medio 1.776, positivo 4/4, p <= 0.05 en 4/4.
- `HLA-DRB5-lite -> MYC/glycolysis-lite`: ratio medio 1.467, positivo 4/4, p <= 0.05 en 4/4.
- `CAF -> MET`: ratio medio 1.627, positivo 4/4, p <= 0.05 en 3/4.

Lectura: esta es la primera validacion espacial externa fuerte del macro-nicho.

### Auditoria de agentes y controles 2026

Se lanzo un agente investigador y un agente auditor.

El investigador confirmo que no hay novedad en genes sueltos: `SPP1/CXCL12`, `HLA-DRB5+ macrophages`, mCAFs, `SPP1+ TAM`, T-cell stress/exhaustion y `HGF-MET-MYC-glycolysis` ya estan activos en la literatura 2026. La oportunidad real es una integracion espacial/metabolica, posiblemente conectable a spFBA/lactate consumption.

El auditor marco riesgos fuertes: nulo espacial global debil, circularidad por `MYC` dentro de `MYC/glycolysis-lite`, leakage `PTPRC` entre proxy mieloide y `HLA-DRB5-lite`, falta normalizacion por UMI, y nombre excesivo de `SPP1/CXCL12-lite` porque la version desolapada no contiene `SPP1`.

Se crearon tres scripts:

- `scripts/consolidate_spatial_niche_effects.py`
- `scripts/audit_spatial_signature_specificity.py`
- `scripts/audit_spatial_block_permutation.py`

Resultado consolidado:

- Antes de controles duros, 7/7 efectos clave fueron positivos en 6/6 muestras spatial combinadas.
- Con ablacion y random controls dentro del panel extraido, los efectos siguen positivos pero no superan random controls. Esto baja la especificidad molecular fina.
- Con permutacion espacial por bloques, `SPP1/CXCL12-lite -> MYC/glycolysis-lite` sobrevive en 6/6 muestras, ratio medio 1.718, block p <= 0.05 en 6/6.
- Con permutacion por bloques, `HLA-DRB5-lite -> MYC/glycolysis-lite` sobrevive en 5/6, ratio medio 1.357.
- Con permutacion por bloques, `CAF -> HLA-DRB5-lite` sobrevive en 5/6, ratio medio 1.417.
- `CAF -> SPP1/CXCL12-lite` queda parcial: 4/6.
- `CAF -> MET` baja prioridad: 2/6.

Lectura: el patron mas defendible ya no es `CAF -> MET`, sino `stromal/myeloid-like regions -> MYC/glycolysis local adjacency`.

## Decision

La hipotesis sigue viva, pero queda mas estrecha y mas honesta.

La formulacion tipo paper seria:

`Exploratory paired single-cell and spatial transcriptomics support a reproducible stromal-myeloid/metabolic architecture in colorectal liver metastasis, where CXCL12/FN1/CD44-like and HLA-DRB5-like regions show local adjacency to MYC/glycolysis programs.`

Todavia no decir:

- que hay causalidad demostrada;
- que tenemos biomarcador clinico validado;
- que `SPP1/CXCL12` o `MET/MYC` son targets probados por este repo;
- que el hallazgo es completamente nuevo por genes individuales.
- que `CAF -> MET` es el eje espacial central.

Si decir:

- que tenemos una hipotesis espacial refinada y falsable;
- que ya tiene soporte en mas de un dataset;
- que el patron mas robusto es estromal-mieloide;
- que la rama tumoral metabolica parece local y espacial.
- que los controles iniciales obligan a validar especificidad full-transcriptome.

## Proximo paso tecnico

El siguiente bloque debe ser mas duro:

1. Full-transcriptome random controls, no solo panel extraido.
2. Sensibilidad a block-size: 8, 12, 16, 20.
3. Residualizacion por UMI/profundidad y coordenadas espaciales.
4. Leave-one-gene-out formal para `MYC`, `PTPRC`, `CD74`, `FN1`, `HIF1A`, `CD44`.
5. Integrar spFBA/lactate consumption 2026 si los datos son accesibles.
6. Mejorar GSE245552 con anotacion celular o pseudobulk por compartimento.

## Cuidado epistemologico

La frase correcta hoy:

`Estamos cerca de una hipotesis computacional publicable, pero todavia no de un hallazgo cerrado; la prioridad es demostrar que el patron supera controles full-transcriptome e histologia/deconvolucion-aware.`

No estamos todavia en:

`descubrimiento clinico confirmado`.
