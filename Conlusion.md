# Conclusion dinamica vigente

Fecha de actualizacion: 2026-04-29 03:23:00 -03:00

## Linea activa

La linea activa sigue siendo:

`cancer colorrectal -> metastasis hepatica -> nicho metastasico hepatico`

La rama que estabamos persiguiendo era:

`HLA-DRB5-like myeloid neighborhoods -> pyruvate/transamination metabolism -> possible non-canonical lactate-carbon handling in CRLM`

Despues de la auditoria robusta, esa rama queda viva solo como hipotesis a validar con flux real, no como hallazgo transcriptomico especifico.

## Estado real

No estamos en terreno virgen por componentes aislados.

Ya existen en la literatura:

- `SPP1+` y `HLA-DRB5+` macrophages en CRLM.
- nichos mCAF/SPP1/T-cell exhaustion.
- `HGF-MET-MYC-glycolysis` en paisajes spatial CRLM.
- lactate uptake y reruteo no canonico de carbono en CRLM por spFBA 2026.

La zona potencialmente novedosa sigue siendo el puente:

`modulo inmune HLA-DRB5-like <-> metabolismo lactato/pyruvato no canonico`

Pero el proxy transcriptomico espacial no lo demuestra todavia.

## Lo que aprendimos hoy

El screen inicial habia encontrado:

- `HLA-DRB5-like -> glutamate_transamination`: positivo 6/6, block p <= 0.05 en 5/6, ratio medio 1.764.
- `HLA-DRB5-like -> pyruvate_mito_entry`: positivo 6/6, block p <= 0.05 en 5/6, ratio medio 1.571.

La auditoria robusta agrego:

- sensibilidad a block-size 8/12/16/20;
- ablation de `PTPRC`, `CD74`, target leave-one-gene-out;
- random controls full-transcriptome emparejados por expresion/dropout;
- residualizacion por profundidad total y coordenadas espaciales.

Resultado honesto:

- La senal sobrevive varios tamanos de bloque.
- La senal sobrevive sacar `PTPRC`.
- La senal no pertenece a `HLA-DRB5` aislado: `HLA-DRB5-only` falla.
- La senal no supera random controls full-transcriptome: 0/6 en pyruvate y transamination, con o sin `PTPRC`.
- La senal desaparece al residualizar por profundidad/coordenadas: 0/6 o 1/6 segun variante.

## Hipotesis vigente revisada

Formulacion anterior, demasiado fuerte:

`HLA-DRB5-like myeloid niches may mark immune-metabolic CRLM regions enriched for non-canonical lactate-carbon routing.`

Formulacion correcta ahora:

`HLA-DRB5-like immune regions co-occur with broad regional metabolic expression programs in CRLM, but transcript proxies do not yet prove a specific lactate/pyruvate niche.`

La pregunta que queda abierta:

`Los mapas reales de flux spFBA/FES muestran lactate uptake/transamination cerca de modulos HLA-DRB5-like, incluso despues de controlar profundidad, coordenadas y region?`

## Evidencia que sigue fuerte

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

Lectura: el patron estromal/mieloide local sigue siendo el mejor nucleo. El brazo metabolico especifico necesita flux real.

## Decision

La rama lactato/HLA-DRB5 no se abandona, pero queda degradada:

`de posible hallazgo -> a hipotesis que solo se puede rescatar con spFBA/FES`

No decir:

- que descubrimos un nicho lactato/HLA-DRB5;
- que HLA-DRB5 regula lactato;
- que los proxies de pyruvato/transaminacion son especificos;
- que hay mecanismo causal.

Si decir:

- que detectamos una co-ocurrencia regional reproducible;
- que esa co-ocurrencia no supera controles transcriptomicos duros;
- que esto obliga a validar con flux, no con mas proxies;
- que el trabajo se volvio mas serio porque ya falsamos la version facil.

## Proximo paso tecnico

Siguiente movimiento:

`spFBA/FES or stop`

Tareas:

1. Buscar/descargar/reconstruir mapas spFBA/FES del paper 2026.
2. Testear lactate uptake, pyruvate/transamination, alphaKG/malate y reductive TCA contra modulos `HLA-DRB5-like`.
3. Aplicar nulo por bloques y residualizacion por profundidad/coordenadas/region.
4. Si FES sobrevive, la rama vuelve a ser candidata a paper.
5. Si FES falla, cerrar lactato/HLA-DRB5 como artefacto regional y volver al nucleo `stromal/myeloid local architecture`.

## Frase final

`Hoy no descubrimos el mecanismo; descubrimos que la version facil no aguanta. Eso es progreso real. El unico camino no recorrido que queda vale la pena solo si pasamos a flux real.`

## Fuentes clave

- spFBA lactate consumption CRLM: https://www.nature.com/articles/s41540-026-00654-x
- SPP1+ y HLA-DRB5+ macrophages CRLM: https://link.springer.com/article/10.1186/s12967-026-07853-4
- Macrophage lipid metabolism CRLM: https://link.springer.com/article/10.1186/s12967-025-07581-1
- HGF-MET-MYC-glycolysis spatial CRLM: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
