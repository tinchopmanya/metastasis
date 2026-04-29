# Conclusion dinamica vigente

Fecha de actualizacion: 2026-04-29 08:23:44 -03:00

## Linea activa

La linea activa sigue siendo:

`cancer colorrectal -> metastasis hepatica -> nicho metastasico hepatico`

La rama que estamos probando con mas dureza es:

`HLA-DRB5-like myeloid neighborhoods -> lactate uptake / pyruvate-transamination FES -> possible immune-metabolic CRLM niche`

## Estado real

No estamos en terreno virgen por componentes aislados.

Ya existen:

- `SPP1+` y `HLA-DRB5+` macrophages en CRLM.
- Nichos mCAF/SPP1/T-cell exhaustion.
- `HGF-MET-MYC-glycolysis` en paisajes spatial CRLM.
- Lactate uptake y reruteo no canonico de carbono en CRC/CRLM por spFBA 2026.

La zona potencialmente novedosa sigue siendo el puente:

`estado inmune HLA-DRB5-like <-> mapas reales de flux lactate uptake / pyruvate-transamination`

Pero ese puente todavia no esta demostrado.

## Lo nuevo del analisis spFBA/FES

Se descargo `output.tar.gz` del deposito spFBA 2026, aproximadamente 2.8 GB, fuera de git en:

`downloads/spfba/output.tar.gz`

Se extrajeron selectivamente los `flux_statistics.h5ad` y se resumieron con:

```powershell
python scripts/summarize_spfba_flux_statistics.py
```

Resultado central:

- Las metastasis hepaticas SC087 tienen lactate uptake extendido: `EX_lac__L_e < 0` en 92.6% a 99.5% de spots.
- El primario pareado SC087 tambien tiene lactate uptake fuerte: 99.0% de spots negativos y media mas negativa que el promedio LM.
- Por tanto, lactate uptake no es metastasis-especifico en promedio.
- Dentro de varias muestras, lactate uptake se acopla con transaminacion/malato/PDH.

Acoplamientos fuertes:

- `LM7`: lactate uptake vs `ASPTA`, Spearman 0.776.
- `LM7`: lactate uptake vs `MDHm`, Spearman 0.643.
- `LM4r`: lactate uptake vs `ASPTA`, Spearman 0.520.
- `LM4r`: lactate uptake vs `MDHm`, Spearman 0.489.
- `CRC_P2`: lactate uptake vs `PDHm`, Spearman 0.615.
- `CRC_P5`: lactate uptake vs `PDHm`, Spearman 0.527.

## Interpretacion

La mitad metabolica de la historia queda mejor parada:

`lactate uptake + transamination/malate/PDH coupling`

Eso aparece en FES independientes y no depende de nuestros proxies transcriptomicos anteriores.

Pero la mitad inmune sigue abierta:

`HLA-DRB5-like -> FES lactate/transamination`

No queda probada porque los FES analizados no estan todavia alineados con expression/metadata/coords que permitan scorear `HLA-DRB5-like` en los mismos spots.

## Decision vigente

No decir:

- que descubrimos un nicho lactato/HLA-DRB5;
- que HLA-DRB5 regula lactato;
- que lactate uptake es especifico de metastasis hepatica;
- que los proxies transcriptomicos ya validaron flux.

Si decir:

- que el fenotipo lactate-consuming existe en mapas spFBA/FES de CRC/CRLM;
- que en varias muestras lactate uptake se acopla con transaminacion/malato/PDH;
- que el puente inmune-metabolico todavia exige datos de expresion/anotacion de los mismos samples spFBA;
- que la rama esta viva solo si pasamos de triangulacion a colocalizacion FES-expression.

## Proximo paso tecnico

Siguiente movimiento:

`spFBA expression/metadata alignment or stop`

Tareas:

1. Extraer selectivamente de `data.tar.gz` o equivalente los datos procesados de `SC087_*` y `CRC_P*`.
2. Confirmar si hay expresion, coordenadas, anotaciones y spots compatibles con los `flux_statistics.h5ad`.
3. Calcular scores `HLA-DRB5-like`, `SPP1/CXCL12-like`, CAF, tumor/metabolic controls.
4. Probar `HLA-DRB5-like -> EX_lac__L_e uptake / ASPTA / ASPTAm / PDHm / MDHm` en los mismos spots o regiones.
5. Aplicar nulo por bloques, residualizacion por profundidad/coordenadas y random controls full-transcriptome.

Si sobrevive, la rama vuelve a ser candidata fuerte a paper.

Si falla, cerrar `HLA-DRB5/lactate` y volver al nucleo mas robusto:

`stromal/myeloid local architecture -> MYC/glycolysis-like adjacency`

## Frase final

`No tenemos todavia el hallazgo cerrado. Tenemos una mitad metabolica real, una mitad inmune no probada y un proximo experimento computacional muy claro. La frontera del descubrimiento esta en alinear FES y expresion en los mismos spots.`

## Fuentes clave

- spFBA lactate consumption CRC/CRLM: https://www.nature.com/articles/s41540-026-00654-x
- Repositorio spFBA: https://github.com/CompBtBs/spFBA
- Zenodo spFBA record 13988866: https://zenodo.org/records/13988866
- HGF-MET-MYC-glycolysis spatial CRLM: https://pmc.ncbi.nlm.nih.gov/articles/PMC12605286/
