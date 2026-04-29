# Investigacion sobre nicho lactato/HLA-DRB5 en CRLM 2026

Fecha: 2026-04-29 02:58:54 -03:00

## Pregunta

La pregunta nueva no es si el cancer colorrectal con metastasis hepatica usa lactato. Eso ya fue propuesto por spFBA en 2026. La pregunta mas fina es:

`los vecindarios mieloides HLA-DRB5-like marcan zonas donde el tejido CRLM muestra programas compatibles con reruteo no canonico de lactato/pyruvato hacia transaminacion y metabolismo biosintetico?`

Esta es una ruta menos transitada que el eje amplio `CAF -> SPP1/CXCL12 -> MYC/glycolysis`. La apuesta es buscar una union entre dos frentes que la literatura todavia trata bastante separados:

- arquitectura inmune espacial de macrophages `SPP1+` y `HLA-DRB5+`;
- consumo de lactato no canonico en CRLM, con pyruvato/transaminacion/reductive TCA.

## Estado de la literatura

El articulo spFBA 2026 reporta que muestras de CRC primario y CRLM muestran lactate uptake y que, en CRLM, el lactato no necesariamente sigue la ruta canonica LDH -> pyruvato -> PDH -> TCA oxidativo. La interpretacion fuerte del paper es que el carbono derivado de lactato puede entrar en rutas de transaminacion con glutamato y sostener circuitos biosinteticos. El mismo articulo tambien observa programas inflamatorios/estres en la muestra metastasica, pero aclara que esa co-ocurrencia no prueba un vinculo funcional o espacial y requiere investigacion dirigida.

En paralelo, Xie et al. 2026 identifican macrophages `SPP1+` y `HLA-DRB5+` como moduladores espaciales importantes del microambiente inmune en CRLM. Ese paper posiciona `HLA-DRB5+` como una rama mieloide con interacciones inmunes diferenciales, especialmente LGALS9-CD45 con celulas T/NK/B. No cierra el puente hacia lactato/flux.

Otro trabajo de 2025 sobre metabolismo lipidico de macrophages en CRLM muestra que los macrophages tienen alta actividad metabolica y que esa actividad aumenta en metastasis hepatica. Esto refuerza que el componente mieloide no debe tratarse solo como "inmune", sino tambien como un posible organizador metabolico del nicho.

Fuentes:

- spFBA lactate consumption CRLM: https://www.nature.com/articles/s41540-026-00654-x
- SPP1+ y HLA-DRB5+ macrophages en CRLM: https://link.springer.com/article/10.1186/s12967-026-07853-4
- Macrophage lipid metabolism en CRLM: https://link.springer.com/article/10.1186/s12967-025-07581-1
- HGF-MET-MYC-glycolysis spatial CRLM: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/

## Datos usados

Se reutilizaron dos datasets spatial ya integrados en el repo:

- `GSE225857`: dos muestras LCT/CRLM Visium (`L1`, `L2`).
- `GSE217414`: cuatro muestras Visium CRLM (`19G081`, `19G0619`, `19G0635`, `19G02977`).

Total: 6 muestras spatial CRLM.

Script nuevo:

```powershell
python scripts/analyze_spatial_lactate_axis.py --permutations 500 --block-size 12
```

Salidas:

- `data_manifest/generated/spatial_lactate_axis_effects.tsv`
- `data_manifest/generated/spatial_lactate_axis_summary.tsv`
- `data_manifest/generated/spatial_lactate_axis_report.md`

## Metodologia

El analisis no hace flux balance real. Es un screen espacial proxy para decidir si vale la pena invertir en spFBA o una aproximacion parecida.

Se extrajeron genes metabolicos disponibles en las matrices Visium y se construyeron proxies:

- `lactate_import_anabolic_proxy`: `SLC16A1`, `MPC1`, `MPC2`, `GOT1`, `GOT2`, `IDH2`, `ACLY`, `ACSS2`.
- `pyruvate_mito_entry_proxy`: `MPC1`, `MPC2`, `PDHA1`, `PDHB`.
- `glutamate_transamination_proxy`: `GOT1`, `GOT2`, `GLUD1`, `GLS`.
- `lactate_export_glycolytic_proxy`: `SLC16A3`, `SLC2A1`, `HK2`, `PGK1`, `ENO1`.

Limitacion importante: `LDHA` y `LDHB` no estaban disponibles en los feature universes probados, asi que las etiquetas de lactato son aproximadas. La parte mas confiable del screen es la direccion pyruvato/transaminacion, no el claim de lactato en si.

Cada efecto se midio como enriquecimiento del score target en vecinos espaciales de spots fuente altos. Despues se comparo contra un nulo por permutacion dentro de bloques espaciales, para reducir el riesgo de que todo sea un gradiente anatomico global.

## Resultados principales

| Efecto | Muestras positivas | Sobrevive bloque p<=0.05 | Ratio medio | Lectura |
| --- | ---: | ---: | ---: | --- |
| `hla_drb5_to_glutamate_transamination` | 6/6 | 5/6 | 1.764 | Senal mas interesante |
| `hla_drb5_to_pyruvate_mito_entry` | 6/6 | 5/6 | 1.571 | Senal mas interesante |
| `hla_drb5_to_lactate_import_anabolic` | 6/6 | 4/6 | 1.564 | Parcial, plausible |
| `hla_drb5_to_lactate_export_glycolytic` | 6/6 | 4/6 | 1.375 | Parcial, menos especifica |
| `cxcl12_fn1_cd44_to_lactate_import_anabolic` | 6/6 | 2/6 | 1.871 | Positiva pero explicable por bloques |
| `cxcl12_fn1_cd44_to_pyruvate_mito_entry` | 6/6 | 2/6 | 1.893 | Positiva pero explicable por bloques |
| `lactate_import_anabolic_to_myc_glycolysis` | 6/6 | 1/6 | 1.630 | Regional, no suficiente |

La sorpresa util es que el eje `CXCL12/FN1/CD44-like`, aunque da ratios altos, pierde fuerza con el nulo por bloques. En cambio, el eje `HLA-DRB5-like` conserva vecindad con `pyruvate_mito_entry` y `glutamate_transamination` en 5/6 muestras.

## Interpretacion

Esto no prueba un descubrimiento biologico cerrado. Pero si abre una grieta prometedora:

`HLA-DRB5-like myeloid neighborhoods may mark spatial immune-metabolic niches where CRLM tissue activates pyruvate/transamination programs consistent with non-canonical lactate-carbon handling.`

La novedad no seria "HLA-DRB5 existe" ni "CRLM consume lactato". Ambas cosas ya existen en la literatura. La novedad posible seria conectar esas dos piezas en un modelo spatial y falsable:

- spFBA muestra lactate consumption y transaminacion, pero no vincula espacialmente ese flux con nichos mieloides concretos.
- La literatura HLA-DRB5 muestra modulacion inmune y localizacion espacial, pero no lo conecta con el reruteo metabolico de lactato/pyruvato.
- Nuestro screen sugiere que el puente mas prometedor podria estar en `HLA-DRB5-like -> pyruvate/transamination`, no en `CAF -> MET` ni solo en `SPP1/CXCL12`.

## Donde estamos parados

No estamos en terreno virgen por componentes. Estamos en un borde interesante por integracion.

La frase prudente hoy:

`Tenemos una hipotesis computacional nueva y testeable: los vecindarios HLA-DRB5-like podrian organizar o marcar zonas de metabolismo no canonico de lactato/pyruvato en CRLM.`

La frase que todavia no podemos decir:

`Descubrimos un mecanismo causal de lactato regulado por HLA-DRB5 macrophages.`

## Camino hacia algo digno de paper

El proximo bloque de mayor valor es convertir este proxy en una prueba de flux:

1. Obtener o reconstruir mapas spFBA/FES para las muestras CRC/CRLM del paper 2026.
2. Testear si spots/vecinos `HLA-DRB5-like` predicen lactate uptake FES, alanine/alphaKG/transamination FES y reductive TCA FES.
3. Residualizar por UMI, coordenadas, tumor/stroma/hepatocyte region y scores de proliferacion.
4. Usar random controls full-transcriptome emparejados por expresion para los proxies metabolicos.
5. Hacer leave-one-gene-out para `MPC1`, `MPC2`, `PDHA1`, `PDHB`, `GOT1`, `GOT2`, `GLUD1`, `GLS`.
6. Validar si el efecto aparece en tumor-adjacent versus stroma/hepatocyte-adjacent neighborhoods.

Si ese bloque sale positivo, el titulo tentativo de paper podria ser:

`Spatial HLA-DRB5-like myeloid niches associate with non-canonical lactate-carbon routing in colorectal liver metastasis.`

Si sale negativo, igual habremos aprendido algo importante: el puente inmune-metabolico no esta en HLA-DRB5 sino que el lactato CRLM es un programa tumoral/organ-specific independiente del nicho mieloide.

## Actualizacion post-auditoria robusta

Fecha: 2026-04-29 03:23:00 -03:00

Se ejecuto una auditoria mas dura en `InvestigacionSobreAuditoriaRobustaNichoLactatoCRLM2026.md`.

Resultado correctivo:

- La senal `HLA-DRB5-like -> pyruvate/transamination` sobrevive block-size y ablation sin `PTPRC`.
- `HLA-DRB5-only` falla, por lo que no debe presentarse como efecto del gen aislado.
- Los random controls full-transcriptome no son superados.
- La residualizacion por profundidad/coordenadas elimina la significancia.

Por lo tanto, esta investigacion queda como generadora de hipotesis, no como evidencia suficiente. La unica ruta valida para continuar es `spFBA/FES or stop`.
