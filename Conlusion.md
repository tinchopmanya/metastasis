# Conclusion dinamica vigente

Fecha de actualizacion: 2026-04-27 16:50:00 -03:00

## Linea activa
La linea activa sigue siendo:

`cancer colorrectal -> metastasis hepatica -> nicho metastasico hepatico`

## Hipotesis principal refinada
La hipotesis vigente ya no es un eje lineal `HGF -> MET -> MYC`. La mejor formulacion ahora es:

`CAF-high layered niche model in CRLM`

En CRLM, nichos `CAF-high` pueden organizar dos respuestas acopladas:

- una interfaz tumoral metabolica: `MET/MYC/glycolysis/one-carbon metabolism`;
- una interfaz inmunosupresora mieloide/T: `SPP1/CXCL12/MIF/CD44/FN1/HLA-DRB5/CD74/CXCR4/LGALS9`.

`HGF-MET-MYC-glycolysis` sigue siendo una rama importante, pero no debe presentarse como explicacion completa del nicho. El centro operativo pasa a ser la arquitectura espacial: quien esta cerca de quien, en que compartimento y con que respuesta biologica.

## Que cambio con la literatura 2026
La busqueda PubMed 2025-2026 encontro 184 articulos recuperados y mostro que el frente mas activo en CRLM combina inmunidad mieloide, metabolismo, resistencia terapeutica, single-cell y spatial transcriptomics.

Lectura fuerte:

- No estamos en terreno virgen si decimos que `CAF`, `SPP1`, `CXCL12` o macrofagos importan en CRLM.
- Si puede haber una oportunidad relevante en integrar dos capas que suelen analizarse por separado: el nicho metabolico tumoral `MET/MYC/glycolysis` y el nicho inmunosupresor `SPP1/CXCL12/myeloid/T-cell`.
- El aporte computacional posible es un modelo espacial falsable de capas o interfaces, no una afirmacion clinica.

Papers 2026 que empujan el pivot:

- [PMID 41807965](https://pubmed.ncbi.nlm.nih.gov/41807965/): nicho mCAF - macrofago `SPP1+` - T cell stress/exhaustion, con ejes `SPP1-CD44`, `FN1-CD44`, `MIF/CXCL12` y firma `KLF2/ZBTB20/ARL4C`.
- [PMID 41051794](https://pubmed.ncbi.nlm.nih.gov/41051794/): `SPP1` induce `CXCL12` en CAFs, favorece EMT, exclusion CD8 e inmunoresistencia.
- [PMID 41715121](https://pubmed.ncbi.nlm.nih.gov/41715121/): macrofagos `SPP1+` y `HLA-DRB5+` con comunicacion `MIF-(CD74+CXCR4)` y `LGALS9-CD45`.
- [PMID 41195591](https://pubmed.ncbi.nlm.nih.gov/41195591/): proteogenomica CRLM con metabolismo de carbono, `SHMT1`, `PIM/NDRG1`, `FTCD/GPD1/SOD2/EIF4B`.
- [PMID 41940986](https://pubmed.ncbi.nlm.nih.gov/41940986/): `GLUT1/SLC2A1` depende del compartimento; margen invasivo y tumor-core pueden significar cosas distintas.

## Evidencia computacional propia

### TCGA-COAD bulk
- `MET-MYC` r = 0.515.
- `MYC-glycolysis` r = 0.422.
- `CAF-HGF` r = 0.675.
- `HGF-MET` no fue significativo, consistente con paracrinia diluida en bulk.
- `mcam_caf` y `caf_core` se asocian con N positivo, invasion linfatica y supervivencia exploratoria por mediana.

### GSE225857 single-cell
- `HGF` se concentra en fibroblastos, no en tumor.
- `MET` se concentra en tumor, no en fibroblastos.
- `MET-MYC` es debil per-cell pero robusto estadisticamente.
- `MYC-PGK1` y `MYC-TPI1` son enlaces tumorales mas fuertes.
- La fuente de `HGF` no es solo MCAM+ CAFs; PRELP+ fibroblasts tambien contribuyen fuerte.

### GSE225857 spatial
- En LCT, `caf_score~MET` promedio r = 0.286.
- En LCT, `MYC~glycolysis_score` promedio r = 0.645.
- Vecinos de spots `CAF-high` tienen `MET` casi 2x sobre fondo.
- Contra 500 permutaciones por test, `CAF -> MET`, `CAF -> MYC` y `CAF -> glycolysis_score` conservan p empirico 0.002 en L1 y L2.
- `HGF-high -> MET` no supera el nulo.

### GSE225857 spatial 2026 layered niche
- Se creo `scripts/analyze_gse225857_spatial_2026.py`.
- Se scorearon 17 firmas 2026 en 22,260 spots Visium, incluyendo controles desolapados.
- En LCT, `caf_core -> spp1_cxcl12_caf_myeloid_axis`: ratios 1.497 y 1.522, p empirico 0.002 en L1 y L2.
- En LCT, `caf_core -> hla_drb5_macrophage_axis`: ratios 1.564 y 1.403, p empirico 0.002 en L1 y L2.
- En LCT, `caf_core -> myc_glycolysis_core`: ratios 1.423 y 1.847, p empirico 0.002.
- En LCT, `spp1_cxcl12_axis -> myc_glycolysis_core`: ratios 1.578 y 1.932, p empirico 0.002.
- En LCT, `hla_drb5_axis -> myc_glycolysis_core`: ratios 1.548 y 1.563, p empirico 0.002.
- La rama T `CXCL13` fue heterogenea: fuerte en L1, debil/no significativa en varias pruebas L2.
- Control desolapado: `CAF -> SPP1/CXCL12-lite` conserva ratio medio 1.513 y `SPP1/CXCL12-lite -> MYC/glycolysis-lite` ratio medio 1.602.
- Control desolapado: `HLA-DRB5-lite` se vuelve mas heterogeneo; `CAF -> HLA-DRB5-lite` es fuerte en L1 pero debil/no robusto en L2, y `HLA-DRB5-lite -> MYC/glycolysis-lite` queda mas bajo (media 1.137).
- Interpretacion: el resultado apoya un macro-nicho espacial estromal-inmune-metabolico; todavia no prueba capas microscopicas separadas.

### GSE234804 externo
- No valida una firma sample-level LM-vs-CRC para `mcam_caf`, `caf_core` ni `myc_glycolysis_core`.
- Esto restringe la tesis a arquitectura local/cell-state-specific.

## Estado de la hipotesis
La hipotesis esta viva y mejor enfocada, pero no es un descubrimiento clinico confirmado.

Lo fuerte:

- Hay evidencia propia de que `CAF-high` tiene vecindad espacial con `MET/MYC/glycolysis`.
- La literatura 2026 aporta una capa independiente y muy activa: `SPP1/CXCL12/myeloid/T-cell`.
- La union de ambas capas ya tiene una primera validacion en GSE225857 LCT: `CAF-high` se acopla a `SPP1/CXCL12` y `MYC/glycolysis` incluso con controles desolapados.
- La rama `HLA-DRB5-like` queda interesante pero mas lesion-dependiente tras remover genes compartidos.

Lo debil:

- El promedio sample-level no replica.
- `HGF` aislado no explica la arquitectura espacial.
- La novedad no esta en genes sueltos, sino en organizacion espacial reproducible.

## Proximo paso tecnico
El siguiente paso ya no es probar si existe acoplamiento bruto; eso salio positivo. Ahora hay que endurecer la prueba:

1. Crear firmas 2026 desolapadas, removiendo genes compartidos como `SPP1` y `MIF` cuando sea necesario.
2. Ya repetida la primera prueba desolapada, refinar la rama HLA-DRB5 con marcadores mas especificos.
3. Intentar deconvolucion espacial o scorear marcadores mas especificos de tumor, CAF, macrofago y T cell.
4. Buscar dataset spatial externo CRLM para validar el macro-nicho.
5. Si no hay dataset externo manejable, usar GSE225857 para mapa de regiones y dejar claro el limite de muestra.

## Cuidado epistemologico
La frase correcta hoy es:

`Tenemos una hipotesis espacial refinada y falsable que conecta evidencia propia con literatura 2026.`

No decir todavia:

- que hay causalidad clinica demostrada;
- que existe un biomarcador validado;
- que SPP1/CXCL12 o MET/MYC son targets terapeuticos probados para este repo;
- que estamos solos en el tema.

El objetivo inmediato es producir una validacion computacional reproducible del modelo en capas.
