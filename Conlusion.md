# Conclusion dinamica vigente

Fecha de actualizacion: 2026-04-27 17:53:00 -03:00

## Linea activa

La linea activa sigue siendo:

`cancer colorrectal -> metastasis hepatica -> nicho metastasico hepatico`

## Estado real: terreno virgen o no

No estamos en terreno virgen por componentes aislados. `CAF`, `SPP1`, `CXCL12`, `HLA-DRB5`, `MET`, `MYC` y glicolisis ya aparecen con fuerza en la literatura CRLM 2025-2026.

Si estamos en una zona con potencial de hallazgo computacional:

`un modelo multi-dataset donde el modulo estromal-mieloide SPP1/CXCL12/HLA-DRB5 se activa en metastasis hepatica y se acopla espacialmente a programas tumorales MYC/glycolysis.`

La novedad posible no es un gen. Es la arquitectura reproducible.

## Hipotesis vigente

La mejor formulacion actual es:

`CAF-high / SPP1-CXCL12 / HLA-DRB5 layered niche model in CRLM`

En CRLM, nichos `CAF-high` parecen organizar o bordear una interfaz estromal-mieloide `SPP1/CXCL12/HLA-DRB5`, que se aproxima espacialmente a programas tumorales `MYC/glycolysis`. Sin embargo, el brazo tumoral metabolico no sube de forma uniforme en todas las celulas epiteliales metastasicas.

Traduccion biologica prudente:

- La rama mieloide/CAF es el nucleo reproducible actual.
- La rama tumoral `MYC/glycolysis` parece mas local/espacial que global.
- `HGF-MET-MYC` sigue siendo una rama metabolica plausible, pero no explica sola el nicho.

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

## Decision

La hipotesis sube de prioridad.

La formulacion tipo paper seria:

`Paired single-cell and external spatial transcriptomics support a reproducible stromal-myeloid-metabolic niche in colorectal cancer liver metastasis, centered on CAF/SPP1-CXCL12/HLA-DRB5 coupling and local MYC/glycolysis adjacency.`

Todavia no decir:

- que hay causalidad demostrada;
- que tenemos biomarcador clinico validado;
- que `SPP1/CXCL12` o `MET/MYC` son targets probados por este repo;
- que el hallazgo es completamente nuevo por genes individuales.

Si decir:

- que tenemos una hipotesis espacial refinada y falsable;
- que ya tiene soporte en mas de un dataset;
- que el patron mas robusto es estromal-mieloide;
- que la rama tumoral metabolica parece local y espacial.

## Proximo paso tecnico

El siguiente bloque debe ser mas duro, no mas amplio:

1. Agregar controles negativos y firmas aleatorias emparejadas por expresion.
2. Probar nulos espaciales estratificados para controlar autocorrelacion tisular.
3. Mejorar GSE245552 con anotacion celular o pseudobulk por compartimento.
4. Consolidar GSE225857 y GSE217414 en una tabla multi-dataset de efectos.
5. Preparar figuras: mapa conceptual, tabla de reproducibilidad, y heatmap de efectos por muestra.

## Cuidado epistemologico

La frase correcta hoy:

`Estamos cerca de un hallazgo computacional publicable si sobrevive a controles negativos y nulos espaciales mas exigentes.`

No estamos todavia en:

`descubrimiento clinico confirmado`.
