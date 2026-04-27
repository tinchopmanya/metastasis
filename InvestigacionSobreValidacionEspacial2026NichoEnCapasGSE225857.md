# Investigacion sobre validacion espacial 2026 del nicho en capas en GSE225857

Fecha: 2026-04-27 16:50:00 -03:00

## Pregunta
Tras la busqueda de literatura 2026, la pregunta inmediata fue:

`El nicho CAF-high que ya asociamos con MET/MYC/glicolisis tambien se acopla espacialmente con los ejes inmunosupresores 2026 SPP1/CXCL12/HLA-DRB5?`

Esto prueba una version mas rica de la hipotesis:

`CAF-high layered niche model in CRLM`

Formulacion operativa:

`Niches CAF-high in CRLM may coordinate a tumor metabolic interface (MET/MYC/glycolysis) and an immunosuppressive myeloid/T-cell interface (SPP1/CXCL12/MIF/CD44/HLA-DRB5).`

## Metodo
Se creo:

`scripts/analyze_gse225857_spatial_2026.py`

El script reutiliza los archivos Visium ya descargados de GSE225857 y calcula scores por spot para firmas 2026 derivadas de la ola bibliografica.

Entrada:

- 6 muestras Visium: `C1-C4` primario colon, `L1-L2` metastasis hepatica.
- 22,260 spots in-tissue.
- `data_manifest/generated/signatures_normalized.tsv` con 16 firmas.
- 17 firmas usadas en esta pasada espacial 2026, incluyendo controles desolapados.

Salidas:

- `data_manifest/generated/gse225857_spatial_2026_signature_availability.tsv`
- `data_manifest/generated/gse225857_spatial_2026_spot_scores.tsv`
- `data_manifest/generated/gse225857_spatial_2026_correlations.tsv`
- `data_manifest/generated/gse225857_spatial_2026_adjacency_permutation.tsv`
- `data_manifest/generated/gse225857_spatial_2026_report.md`

Control agregado despues de la primera corrida:

- Se crearon firmas desolapadas para reducir inflado por genes compartidos.
- `caf_core_desoverlap_2026`: remueve `PDGFRB`.
- `spp1_cxcl12_axis_desoverlap_2026`: remueve `SPP1` y `MIF`.
- `hla_drb5_macrophage_axis_desoverlap_2026`: remueve `SPP1` y `MIF`.
- `myc_glycolysis_desoverlap_2026`: remueve `SLC2A1` para no confundir con GLUT1/margen.

Prueba de vecindad:

- Se definieron spots source-high por percentil 75 de cada score.
- Se calcularon vecinos hexagonales Visium.
- Se comparo target mean en vecinos vs background.
- Se corrieron 500 permutaciones por test en LCT, barajando el target dentro de muestra.

## Disponibilidad de firmas en LCT
Las firmas principales fueron mayormente utilizables:

- `caf_core`: 7/7 genes.
- `mcam_caf`: 4/4.
- `spp1_cxcl12_caf_myeloid_axis`: 7/7.
- `spp1_macrophage_fads1_pdgfb_axis`: 6/6.
- `hla_drb5_macrophage_axis`: 6/7; falta `LGALS9`.
- `stromal_myeloid_risk_2026`: 2/3; falta `KLF2`.
- `myc_glycolysis_core`: 5/7; faltan `TPI1` y `LDHA`.
- `crlm_metabolic_vulnerabilities_2026`: 8/9; falta `SHMT1`.
- `glut1_invasive_margin_axis`: 5/5.

Interpretacion: las firmas son suficientemente testeables para una primera pasada, pero algunas ramas 2026 quedan incompletas en este Visium.

## Resultados de correlacion LCT
En las dos metastasis hepaticas, los scores 2026 se acoplan fuertemente a CAF:

| Par | L1 r | L2 r | Lectura |
| --- | ---: | ---: | --- |
| `caf_core ~ spp1_cxcl12_axis` | 0.756 | 0.674 | CAF y eje SPP1/CXCL12 co-varian fuerte |
| `mcam_caf ~ spp1_cxcl12_axis` | 0.739 | 0.668 | MCAM-CAF tambien se acopla al eje 2026 |
| `caf_core ~ hla_drb5_macrophage_axis` | 0.748 | 0.530 | CAF se acopla a rama mieloide |
| `spp1_cxcl12_axis ~ hla_drb5_axis` | 0.886 | 0.689 | las dos ramas inmunes se superponen fuerte |
| `spp1_cxcl12_axis ~ myc_glycolysis_core` | 0.702 | 0.630 | eje inmune/estromal se acopla a metabolismo tumoral |
| `hla_drb5_axis ~ myc_glycolysis_core` | 0.652 | 0.458 | rama mieloide se acopla a metabolismo tumoral |

Pero los pares de ligando individual fueron mas debiles:

- `SPP1~CXCL12`: L1 r = -0.197, L2 r = -0.012.
- `SPP1~CD44`: L1 r = 0.247, L2 r = 0.128.
- `MIF~CXCR4`: L1 r = 0.207, L2 r = 0.037.
- `HLA-DRB5~LGALS9`: no evaluable porque `LGALS9` no esta disponible.

Lectura: la senal fuerte esta en programas/firma de nicho, no en pares de genes aislados. Esto coincide con lo que vimos antes con `HGF`: un solo ligando no captura toda la arquitectura.

## Resultados de vecindad y permutacion
Los resultados LCT mas importantes:

| Fuente | Target | L1 ratio | L2 ratio | p empirico |
| --- | --- | ---: | ---: | --- |
| `caf_core` | `spp1_cxcl12_axis` | 1.497 | 1.522 | 0.002 en ambas |
| `caf_core` | `hla_drb5_axis` | 1.564 | 1.403 | 0.002 en ambas |
| `caf_core` | `myc_glycolysis_core` | 1.423 | 1.847 | 0.002 en ambas |
| `mcam_caf` | `spp1_cxcl12_axis` | 1.495 | 1.522 | 0.002 en ambas |
| `mcam_caf` | `hla_drb5_axis` | 1.557 | 1.420 | 0.002 en ambas |
| `spp1_cxcl12_axis` | `myc_glycolysis_core` | 1.578 | 1.932 | 0.002 en ambas |
| `hla_drb5_axis` | `myc_glycolysis_core` | 1.548 | 1.563 | 0.002 en ambas |
| `caf_core` | `glut1_invasive_margin_axis` | 1.720 | 2.022 | 0.002 en ambas |
| `caf_core` | `crlm_metabolic_vulnerabilities_2026` | 1.634 | 1.645 | 0.002 en ambas |

Medias LCT:

- `CAF -> SPP1/CXCL12 axis`: ratio medio 1.509.
- `CAF -> HLA-DRB5 macrophage axis`: ratio medio 1.484.
- `SPP1/CXCL12 axis -> MYC/glycolysis`: ratio medio 1.755.
- `HLA-DRB5 macrophage axis -> MYC/glycolysis`: ratio medio 1.556.

## Control desolapado
El control desolapado fue clave para separar senal biologica de posible inflado por overlap tecnico.

Resultados principales:

| Fuente | Target | L1 ratio | L2 ratio | Lectura |
| --- | --- | ---: | ---: | --- |
| `caf_core_desoverlap` | `spp1_cxcl12_lite` | 1.599 | 1.426 | sobrevive fuerte en ambas lesiones |
| `caf_core_desoverlap` | `hla_drb5_lite` | 1.894 | 1.045 | fuerte en L1, debil/no robusto en L2 |
| `spp1_cxcl12_lite` | `myc_glycolysis_lite` | 1.471 | 1.734 | sobrevive fuerte en ambas lesiones |
| `hla_drb5_lite` | `myc_glycolysis_lite` | 1.222 | 1.052 | mas debil; lesion-dependiente |

Medias LCT:

- `CAF -> SPP1/CXCL12-lite`: ratio medio 1.513.
- `CAF -> HLA-DRB5-lite`: ratio medio 1.470, pero impulsado por L1.
- `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: ratio medio 1.602.
- `HLA-DRB5-lite -> MYC/glycolysis-lite`: ratio medio 1.137.

Decision tras control:

- La rama `SPP1/CXCL12` queda robusta incluso sin `SPP1` y `MIF`.
- La rama `HLA-DRB5` queda como candidata secundaria, heterogenea por lesion.
- El macro-nicho CAF/SPP1-CXCL12/metabolismo tumoral es mas fuerte que la afirmacion especifica CAF/HLA-DRB5.

Esto es un resultado importante: el eje 2026 no solo aparece en la literatura, tambien se acopla espacialmente en GSE225857 al mismo territorio donde ya veiamos `CAF -> MET/MYC/glicolisis`.

## Senales no tan consistentes
La rama T `CXCL13` no fue tan estable:

- `caf_core -> cxcl13_t_cells`: L1 ratio 2.265, p 0.002; L2 ratio 1.084, p 0.246.
- `mcam_caf -> cxcl13_t_cells`: L1 ratio 2.230, p 0.002; L2 ratio 1.146, p 0.122.
- `spp1_cxcl12_axis -> cxcl13_t_cells`: L1 ratio 1.823, p 0.002; L2 ratio 0.994, p 0.493.
- `hla_drb5_axis -> cxcl13_t_cells`: L1 ratio 2.109, p 0.002; L2 ratio 1.409, p 0.004.

Lectura: la capa T puede ser heterogenea entre lesiones. El acoplamiento CAF/mieloide/metabolico parece mas robusto que CAF/T `CXCL13`.

## Interpretacion
Esta pasada fortalece el modelo en capas, pero con una precision importante:

La evidencia no demuestra todavia capas microscopicas separadas. Lo que demuestra es un `macro-nicho` espacial superpuesto en Visium: regiones CAF-high en LCT enriquecen simultaneamente senales metabolicas tumorales y senales inmunosupresoras/mieloides 2026.

Esto puede significar tres cosas:

1. Un nicho real en capas, pero Visium no tiene suficiente resolucion para separarlas.
2. Una region tumor-estroma amplia donde multiples programas coexisten.
3. Una mezcla de composicion celular y programas biologicos, amplificada por firmas broad y genes compartidos.

Por eso el resultado es prometedor, no definitivo.

## Terreno virgen o cerca de hallazgo?
No estamos en terreno virgen respecto a `SPP1`, `CXCL12`, CAFs o macrofagos. Pero este resultado nos acerca a un aporte mas especifico:

`Integrar CAF-high -> MET/MYC/glycolysis con CAF/myeloid -> SPP1/CXCL12/HLA-DRB5 dentro de un mismo macro-nicho espacial CRLM.`

Si logramos separar capas con deconvolucion, subspots, histologia o dataset espacial externo, el aporte podria ser interesante. Hoy estamos cerca de una hipotesis fuerte de segundo nivel, no de un descubrimiento clinico.

## Limitaciones
- Visium mezcla celulas; no prueba causalidad ni direccion ligand-receptor.
- Varias firmas 2026 son amplias y comparten genes; esto puede inflar correlaciones.
- `SPP1~CXCL12` como par individual no correlaciona fuerte.
- Algunos genes faltan en este universo espacial: `LGALS9`, `KLF2`, `SHMT1`, `TPI1`, `LDHA`.
- Solo hay dos muestras LCT Visium; la validacion externa sigue siendo critica.

## Decision
La hipotesis sube prioridad.

Nuevo enunciado operativo:

`En GSE225857, los nichos CAF-high de CRLM se acoplan no solo a MET/MYC/glicolisis, sino tambien a un programa SPP1/CXCL12 robusto y a una rama HLA-DRB5-like mas heterogenea; esto sugiere un macro-nicho estromal-inmune-metabolico que merece validacion espacial externa.`

Proximo paso:

1. Intentar separar capa tumoral, CAF y mieloide con deconvolucion/cell2location-like si es viable.
2. Buscar dataset spatial externo CRLM con coordenadas y/o anotaciones.
3. Refinar la rama HLA-DRB5 con marcadores menos solapados y mas especificos.
4. Buscar si la rama SPP1/CXCL12-lite predice CD8/T-cell exclusion o exhaustion mejor que las firmas amplias.
