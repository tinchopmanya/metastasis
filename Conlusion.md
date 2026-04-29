# Conclusion dinamica vigente

Fecha de actualizacion: 2026-04-29 02:58:54 -03:00

## Linea activa

La linea activa sigue siendo:

`cancer colorrectal -> metastasis hepatica -> nicho metastasico hepatico`

Pero el borde mas prometedor cambio. Ya no conviene poner el centro en `CAF -> MET`. La ruta mas interesante ahora es:

`HLA-DRB5-like myeloid neighborhoods -> pyruvate/transamination metabolism -> possible non-canonical lactate-carbon handling in CRLM`

## Terreno virgen o no

No estamos en terreno virgen por piezas aisladas.

Ya existen:

- `SPP1+` y `HLA-DRB5+` macrophages en CRLM.
- nichos mCAF/SPP1/T-cell exhaustion.
- `HGF-MET-MYC-glycolysis` en paisajes spatial CRLM.
- lactate uptake y reruteo no canonico de carbono en CRLM por spFBA 2026.

Si estamos en una zona menos recorrida y potencialmente valiosa:

`conectar espacialmente un estado mieloide HLA-DRB5-like con los programas pyruvate/transamination que podrian reflejar la economia de lactato no canonica descrita por spFBA.`

La novedad posible no es un gen ni una via suelta. Es el puente inmune-metabolico.

## Hipotesis vigente

Formulacion actual:

`Spatial HLA-DRB5-like myeloid niches may mark immune-metabolic regions of colorectal liver metastasis enriched for pyruvate mitochondrial entry and glutamate transamination programs, consistent with non-canonical lactate-carbon routing.`

Traduccion:

En CRLM, los vecindarios `HLA-DRB5-like` no solo podrian representar inmunomodulacion. Tambien podrian marcar zonas donde el tejido tumoral/estromal cercano activa rutas de pyruvato y transaminacion compatibles con el uso no canonico de lactato/pyruvato.

## Evidencia propia acumulada

### GSE245552 paired scRNA

- `myeloid SPP1/CXCL12-lite`: LM/primario 1.844, p = 1.34e-04, positivo 13/13 pares.
- `myeloid HLA-DRB5-lite`: LM/primario 1.478, p = 1.72e-03, positivo 12/13 pares.
- `tumor MYC/glycolysis-lite`: LM/primario 0.967, p = 0.692, positivo 5/13 pares.

Lectura: la rama mieloide sube en metastasis hepatica pareada; el programa tumoral metabolico no sube como promedio global.

### Spatial multi-dataset antes del pivot lactato

- `SPP1/CXCL12-lite -> MYC/glycolysis-lite`: sobrevive nulo por bloques en 6/6 muestras.
- `HLA-DRB5-lite -> MYC/glycolysis-lite`: sobrevive en 5/6 muestras.
- `CAF -> HLA-DRB5-lite`: sobrevive en 5/6 muestras.
- `CAF -> MET`: solo 2/6, por eso baja prioridad como claim central.

Lectura: el patron mas defendible es local y espacial, no bulk ni lineal.

### Nuevo screen lactato/pyruvato spatial

Script:

```powershell
python scripts/analyze_spatial_lactate_axis.py --permutations 500 --block-size 12
```

Dataset combinado:

- `GSE225857`: 2 muestras LCT/CRLM.
- `GSE217414`: 4 muestras CRLM.
- Total: 6 muestras spatial.

Resultados:

- `HLA-DRB5-like -> glutamate_transamination`: positivo 6/6, block p <= 0.05 en 5/6, ratio medio 1.764.
- `HLA-DRB5-like -> pyruvate_mito_entry`: positivo 6/6, block p <= 0.05 en 5/6, ratio medio 1.571.
- `HLA-DRB5-like -> lactate_import_anabolic`: positivo 6/6, block p <= 0.05 en 4/6, ratio medio 1.564.
- `HLA-DRB5-like -> lactate_export_glycolytic`: positivo 6/6, block p <= 0.05 en 4/6, ratio medio 1.375.
- `CXCL12/FN1/CD44-like` tambien da ratios altos, pero sus efectos pyruvato/transaminacion sobreviven solo 2/6 bajo nulo por bloques.

Lectura: la rama `HLA-DRB5-like` es mas interesante para una hipotesis inmune-metabolica especifica que la rama `CXCL12/FN1/CD44-like`, que parece mas vulnerable a gradientes regionales amplios.

## Decision

La mejor apuesta actual para buscar algo digno de paper es:

`HLA-DRB5-like immune-metabolic niche in CRLM lactate-carbon routing`

No decir todavia:

- que hay causalidad;
- que HLA-DRB5 regula lactato;
- que tenemos flux real;
- que el mecanismo esta validado clinicamente;
- que esto es terapeuticamente accionable.

Si decir:

- que encontramos una hipotesis mas novedosa y falsable;
- que la senal aparece en 6 muestras spatial de 2 datasets;
- que los mejores efectos sobreviven permutacion por bloques en 5/6;
- que el siguiente paso ya no es mas correlacion bonita, sino spFBA/FES o flux-like validation.

## Proximo paso tecnico

1. Conseguir o reproducir mapas spFBA/FES de lactate uptake, pyruvate/transamination, alphaKG/malate y reductive TCA.
2. Testear si `HLA-DRB5-like` predice esos mapas en vecinos espaciales.
3. Residualizar por UMI/profundidad, coordenadas, region histologica y tumor/stroma/hepatocyte scores.
4. Crear random controls full-transcriptome emparejados por expresion para los proxies metabolicos.
5. Leave-one-gene-out para `MPC1`, `MPC2`, `PDHA1`, `PDHB`, `GOT1`, `GOT2`, `GLUD1`, `GLS`.
6. Si el puente se sostiene, preparar una figura tipo paper: literatura gap -> spatial proxy -> block null -> spFBA validation.

## Cuidado epistemologico

La frase correcta hoy:

`Estamos cerca de una hipotesis computacional publicable, no de un descubrimiento cerrado. El camino mas virgen es probar si HLA-DRB5-like myeloid niches predicen el metabolismo no canonico de lactato/pyruvato en CRLM.`

La version honesta del entusiasmo:

`Esto huele a borde de hallazgo, pero todavia necesita flux real para convertirse en paper fuerte.`

## Fuentes clave

- spFBA lactate consumption CRLM: https://www.nature.com/articles/s41540-026-00654-x
- SPP1+ y HLA-DRB5+ macrophages CRLM: https://link.springer.com/article/10.1186/s12967-026-07853-4
- Macrophage lipid metabolism CRLM: https://link.springer.com/article/10.1186/s12967-025-07581-1
- HGF-MET-MYC-glycolysis spatial CRLM: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
