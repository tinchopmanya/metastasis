# Resumen de asociacion clinica TCGA-COAD

Fecha: 2026-04-27 02:22:16 -03:00

## Resumen corto

Se agrego una pantalla clinica exploratoria en TCGA-COAD para saber si las firmas del nicho CRLM tienen alguna relacion con agresividad en tumores primarios. Se creo `scripts/analyze_tcga_coad_clinical.py`, que une los scores de firmas previamente calculados con `COAD_clinicalMatrix` de UCSC Xena. El analisis incluye 329 muestras con expresion y clinica.

El resultado no valida metastasis hepatica, porque TCGA-COAD no es una cohorte espacial ni metastasica. Pero si aporta una senal util: las firmas `mcam_caf` y `caf_core` se asocian con rasgos de agresividad. `mcam_caf` fue mas alta en N positivo vs N0 (p=6.95e-04), invasion linfatica positiva vs negativa (p=1.15e-03) y estadio avanzado vs temprano (p=1.24e-02). `caf_core` mostro un patron similar.

En supervivencia exploratoria por mediana, `caf_core` alto tuvo mas eventos de muerte que lo esperado (p=2.03e-02) y `mcam_caf` alto tambien (p=2.70e-02). En cambio, el composite completo `CAF/MET/MYC/glicolisis` no fue significativo (p=0.493) y `HGF-MET` aislado tampoco (p=0.531).

La conclusion es fina: el componente CAF/MCAM tiene senal clinica en bulk primario, pero el mecanismo completo parece requerir contexto espacial/single-cell. Esto encaja con la lectura refinada del proyecto: perseguir `CAF-high spatial niches`, no un biomarcador bulk lineal basado en `HGF` o en un composite simple.

## Resumen extendido

El proyecto ya habia acumulado evidencia de plausibilidad para la hipotesis `CAF-high -> MET/MYC/glicolisis`: bulk TCGA mostro correlaciones `MET-MYC` y `MYC-glycolysis`; GSE225857 single-cell mostro `HGF` en fibroblastos y `MET` en tumor; Visium mostro vecindad entre zonas CAF-altas y senales tumorales/metabolicas; y las permutaciones demostraron que ese patron supera un nulo simple dentro de muestra.

La pregunta ahora fue si esta linea tiene alguna lectura clinica en una cohorte amplia, aunque imperfecta. TCGA-COAD es util para esto porque tiene expresion y anotacion clinica, pero tiene una limitacion fuerte: trabaja sobre tumores primarios y bulk RNA-seq. Por lo tanto, no puede probar el nicho metastasico hepatico ni la interaccion espacial CAF-tumor.

El nuevo script descarga la matriz clinica de UCSC Xena, la une con los scores de firmas y evalua asociaciones con estadio, estado M, estado N, invasion linfatica, invasion venosa y supervivencia global. Los resultados mas consistentes fueron los relacionados con CAF/MCAM. `mcam_caf` fue mayor en N positivo, invasion linfatica y estadio avanzado. `caf_core` siguio el mismo patron. Estas asociaciones sugieren que el componente estromal/CAF captura una dimension de agresividad tumoral en primarios.

La pantalla de supervivencia fue coherente pero exploratoria. Las firmas `caf_core` y `mcam_caf` altas se asociaron con mas eventos de muerte en una division por mediana. Sin embargo, el composite completo `caf_met_myc_glycolysis_composite` no mostro asociacion significativa, y `hgf_met_axis` tampoco. Esta diferencia es importante: lo que parece clinicamente visible en bulk es el componente CAF, no necesariamente el circuito completo.

La mejor lectura es que el nicho no debe reducirse a un score bulk universal. El hallazgo central sigue siendo espacial: regiones CAF-altas se asocian con tumor `MET+`, `MYC` y glicolisis en metastasis hepatica. TCGA agrega que el programa CAF/MCAM tiene relacion con agresividad en primarios, pero no prueba que el eje completo sea prognostico ni causal.

## Recomendacion operativa

Mantener prioridad alta para `CAF-high/MCAM` y tratar `HGF-MET-MYC-glicolisis` como mecanismo espacial dependiente de contexto. El siguiente paso debe buscar especificidad metastasica:

- comparar CRLM contra primario;
- comparar metastasis hepatica contra metastasis no hepatica;
- comparar CRC metastasico contra otros tumores en higado;
- priorizar datasets donde se pueda medir spatial o single-cell, no solo bulk.
