# Investigacion sobre auditoria robusta del nicho lactato/HLA-DRB5 en CRLM 2026

Fecha: 2026-04-29 03:23:00 -03:00

## Pregunta

Despues del screen positivo `HLA-DRB5-like -> pyruvate/transamination`, la pregunta critica fue:

`la senal sobrevive controles de reviewer hostil o es un gradiente regional/transcripcional amplio?`

Esta auditoria intenta romper la hipotesis antes de avanzar hacia spFBA o manuscrito.

## Script nuevo

```powershell
python scripts/audit_lactate_axis_robustness.py --permutations 200 --ablation-permutations 100 --random-controls 100 --block-sizes 8,12,16,20
```

Salidas:

- `data_manifest/generated/lactate_axis_robustness_report.md`
- `data_manifest/generated/lactate_axis_robustness_blocksize.tsv`
- `data_manifest/generated/lactate_axis_robustness_blocksize_summary.tsv`
- `data_manifest/generated/lactate_axis_robustness_ablation.tsv`
- `data_manifest/generated/lactate_axis_robustness_ablation_summary.tsv`
- `data_manifest/generated/lactate_axis_robustness_random_controls.tsv`
- `data_manifest/generated/lactate_axis_robustness_random_controls_summary.tsv`
- `data_manifest/generated/lactate_axis_robustness_residualized.tsv`
- `data_manifest/generated/lactate_axis_robustness_residualized_summary.tsv`

## Controles aplicados

1. Sensibilidad a tamanos de bloque espacial: 8, 12, 16 y 20.
2. Ablation del source `HLA-DRB5-like`:
   - `hla_drb5_original`: `HLA-DRB5`, `CD74`, `CXCR4`, `LGALS9`, `PTPRC`.
   - `hla_drb5_no_ptprc`: saca `PTPRC`.
   - `hla_drb5_no_cd74_ptprc`: saca `CD74` y `PTPRC`.
   - `hla_drb5_only`: solo `HLA-DRB5`.
3. Leave-one-gene-out de targets:
   - `pyruvate_mito_entry`: `MPC1`, `MPC2`, `PDHA1`, `PDHB`.
   - `glutamate_transamination`: `GOT1`, `GOT2`, `GLUD1`, `GLS`.
4. Random controls desde el universo completo de features de cada muestra, emparejados aproximadamente por expresion y dropout.
5. Residualizacion por profundidad total (`log_total_counts`) y coordenadas espaciales (`array_row`, `array_col`, terminos cuadraticos e interaccion).

## Resultado 1: block-size sensitivity

La senal bruta sigue existiendo con varios tamanos de bloque:

| Efecto | Block 8 | Block 12 | Block 16 | Block 20 |
| --- | ---: | ---: | ---: | ---: |
| `HLA-DRB5 -> pyruvate_mito_entry` | 4/6 | 5/6 | 4/6 | 6/6 |
| `HLA-DRB5 -> glutamate_transamination` | 2/6 | 5/6 | 4/6 | 5/6 |
| `HLA-DRB5 -> lactate_import_anabolic` | 2/6 | 4/6 | 3/6 | 5/6 |
| `HLA-DRB5 -> lactate_export_glycolytic` | 3/6 | 4/6 | 4/6 | 4/6 |

Lectura: el patron no era un accidente de un unico block-size. Eso mantiene viva la senal como fenomeno espacial regional.

## Resultado 2: ablation

El source `hla_drb5_no_ptprc` mantiene la senal:

- `hla_drb5_no_ptprc -> glutamate_transamination`: positivo 6/6, block p <= 0.05 en 5/6, ratio medio 1.705.
- `hla_drb5_no_ptprc -> pyruvate_mito_entry`: positivo 6/6, block p <= 0.05 en 5/6, ratio medio 1.557.

Los leave-one-gene-out de targets tambien retienen senal en la mayoria de variantes, especialmente para `pyruvate_mito_entry`.

Pero hay una correccion importante:

- `hla_drb5_only` falla: solo 1/6 positivo y 0/6 significativo.

Lectura: el efecto no pertenece al gen `HLA-DRB5` aislado. Pertenece a un estado inmune/antigen-presentation/chemokine mas amplio (`HLA-DRB5/CD74/CXCR4/LGALS9`, con o sin `PTPRC`). Hay que nombrarlo como `HLA-DRB5-like immune module`, no como `HLA-DRB5 gene effect`.

## Resultado 3: random controls full-transcriptome

Este fue el golpe fuerte.

Ningun efecto supero random controls emparejados por expresion/dropout desde el universo completo de cada muestra:

| Source | Target | Beats random p<=0.05 |
| --- | ---: | ---: |
| `hla_drb5_original` | `pyruvate_mito_entry` | 0/6 |
| `hla_drb5_original` | `glutamate_transamination` | 0/6 |
| `hla_drb5_no_ptprc` | `pyruvate_mito_entry` | 0/6 |
| `hla_drb5_no_ptprc` | `glutamate_transamination` | 0/6 |

Lectura: genes con expresion/dropout parecidos pueden mostrar enriquecimientos espaciales similares. Eso baja la especificidad del proxy metabolico.

## Resultado 4: residualizacion por profundidad y coordenadas

Al residualizar source y target por `log_total_counts` y coordenadas espaciales, la senal practicamente desaparece:

- `hla_drb5_original -> glutamate_transamination`: 4/6 deltas positivas, 0/6 significativas.
- `hla_drb5_original -> pyruvate_mito_entry`: 4/6 deltas positivas, 0/6 significativas.
- `hla_drb5_no_ptprc -> glutamate_transamination`: 4/6 positivas, 0/6 significativas.
- `hla_drb5_no_ptprc -> pyruvate_mito_entry`: 4/6 positivas, 1/6 significativa.

Lectura: parte grande del patron parece explicarse por profundidad/captura y coordenadas/region. El proxy transcriptomico espacial no alcanza para claim paper-grade.

## Conclusion

La auditoria no mata la intuicion biologica, pero si mata el claim fuerte basado solo en transcript proxies.

Nueva lectura:

`El eje HLA-DRB5-like -> pyruvate/transamination existe como senal regional robusta, pero no demuestra especificidad metabolica tras random controls full-transcriptome ni residualizacion por profundidad/coordenadas.`

Eso significa que no debemos avanzar diciendo "descubrimos nicho lactato/HLA-DRB5". La formulacion correcta es:

`HLA-DRB5-like immune regions co-occur with broad metabolic/regional expression programs; spFBA/FES real is required to decide whether there is a lactate-carbon routing niche.`

## Decision operativa

No abandonar todavia. Pero el siguiente paso ya no puede ser otro proxy.

La unica ruta que vale ahora es:

1. Conseguir o reconstruir mapas spFBA/FES.
2. Probar directamente lactate uptake, pyruvate/transamination, alphaKG/malate y reductive TCA.
3. Mantener residualizacion por UMI/coordenadas/region.
4. Si FES tambien falla, cerrar la rama lactato/HLA-DRB5 como artefacto regional.
5. Si FES sobrevive, ahi si hay una historia potencialmente fuerte: el proxy transcriptomico era confuso, pero el flux real revela el nicho.

## Frase honesta

`Estamos mas lejos de un hallazgo cerrado, pero mas cerca de una investigacion seria: ya sabemos que la version facil de la hipotesis no aguanta reviewer hostil.`
