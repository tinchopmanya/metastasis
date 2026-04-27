# Centro de Investigaciones

Fecha de inicialización: 2026-04-23 03:15:24 -03:00

## Propósito
Este archivo es el log central de la carpeta de investigación. Su función es mantener una vista estable del sistema completo, registrar las olas abiertas y dejar claro el protocolo de trabajo para cada investigación nueva.

## Estructura fija
- `Investigacion.md`: log central y reglas operativas.
- `InvestigacionMapa.md`: mapa cronológico con fecha, hora y links.
- `Conlusion.md`: conclusión dinámica de la ola vigente. No es un log; se reescribe cuando cambia la mejor síntesis.

## Regla por cada investigación nueva
- Crear `InvestigacionSobreTema.md` con la versión extensa.
- Crear `ResumenInvestigacionSobreTema.md` con una síntesis fuerte.
- Actualizar `InvestigacionMapa.md` con fecha, hora y link.
- Actualizar este archivo con estado, foco y próximo paso.
- Reescribir `Conlusion.md` con la mejor lectura vigente del conjunto.

## Formato recomendado para el archivo de resumen
- Un resumen corto de aproximadamente 300 palabras.
- Un resumen extendido de aproximadamente 1000 palabras.
- Una recomendación operativa clara al final.

## Ola activa actual
- Ola 003F: `validacion espacial 2026 del nicho CRLM en capas`

## Olas registradas

### Ola 001
- Fecha de apertura: 2026-04-23 03:15:24 -03:00
- Tema: metástasis en cánceres y oportunidades de descubrimiento con IA sin hacer ensayos clínicos nuevos.
- Estado: cerrada como marco panorámico.
- Archivos asociados:
- [InvestigacionSobreMetastasisEnCanceres.md](./InvestigacionSobreMetastasisEnCanceres.md)
- [ResumenInvestigacionSobreMetastasisEnCanceres.md](./ResumenInvestigacionSobreMetastasisEnCanceres.md)
- [Conlusion.md](./Conlusion.md)
- Resultado: selección de `cáncer colorrectal -> metástasis hepática` como primera línea con mejor equilibrio entre impacto, datos públicos y posibilidad de descubrimiento computacional.

### Ola 002
- Fecha de apertura: 2026-04-23 03:28:33 -03:00
- Tema: cáncer colorrectal y metástasis hepática.
- Estado: cerrada como refinamiento de línea.
- Archivos asociados:
- [InvestigacionSobreCancerColorrectalYMetastasisHepatica.md](./InvestigacionSobreCancerColorrectalYMetastasisHepatica.md)
- [ResumenInvestigacionSobreCancerColorrectalYMetastasisHepatica.md](./ResumenInvestigacionSobreCancerColorrectalYMetastasisHepatica.md)
- [Conlusion.md](./Conlusion.md)
- Resultado: selección del nicho metastásico hepático como sublínea biológica principal, con TCIA/recurrencia post-hepatectomía como sublínea técnica secundaria.

### Ola 003
- Fecha de apertura: 2026-04-25 01:06:15 -03:00
- Tema: nicho metastásico hepático en cáncer colorrectal.
- Estado: activa.
- Archivos asociados:
- [InvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md](./InvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md)
- [ResumenInvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md](./ResumenInvestigacionSobreNichoMetastaticoHepaticoEnCancerColorrectal.md)
- [HipotesisNichoMetastaticoCRLM.md](./HipotesisNichoMetastaticoCRLM.md)
- [DatasetsCRLM.md](./DatasetsCRLM.md)
- [SenalesPrioritariasCRLM.md](./SenalesPrioritariasCRLM.md)
- [PlanValidacionCRLM.md](./PlanValidacionCRLM.md)
- [InvestigacionSobreValidacionEspacialPorPermutacionesGSE225857.md](./InvestigacionSobreValidacionEspacialPorPermutacionesGSE225857.md)
- [ResumenInvestigacionSobreValidacionEspacialPorPermutacionesGSE225857.md](./ResumenInvestigacionSobreValidacionEspacialPorPermutacionesGSE225857.md)
- [InvestigacionSobreAsociacionClinicaTCGACOAD.md](./InvestigacionSobreAsociacionClinicaTCGACOAD.md)
- [ResumenInvestigacionSobreAsociacionClinicaTCGACOAD.md](./ResumenInvestigacionSobreAsociacionClinicaTCGACOAD.md)
- [InvestigacionSobreValidacionExternaGSE234804.md](./InvestigacionSobreValidacionExternaGSE234804.md)
- [ResumenInvestigacionSobreValidacionExternaGSE234804.md](./ResumenInvestigacionSobreValidacionExternaGSE234804.md)
- [InvestigacionSobreLiteratura2026NichoCRLM.md](./InvestigacionSobreLiteratura2026NichoCRLM.md)
- [ResumenInvestigacionSobreLiteratura2026NichoCRLM.md](./ResumenInvestigacionSobreLiteratura2026NichoCRLM.md)
- [InvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md](./InvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md)
- [ResumenInvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md](./ResumenInvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md)
- [Conlusion.md](./Conlusion.md)
- Hipotesis de trabajo actual: nichos `CAF-high` en CRLM pueden organizar dos interfaces acopladas: una tumoral metabolica `MET/MYC/glycolysis` y otra inmunosupresora `SPP1/CXCL12/MIF/CD44/HLA-DRB5`.
- Resultado tecnico vigente: GSE225857 apoya `CAF-high -> MET/MYC/glicolisis` y ahora tambien `CAF-high -> SPP1/CXCL12/HLA-DRB5-like` con 500 permutaciones en LCT; TCGA apoya sombra clinica CAF/MCAM; GSE234804 descarta una lectura sample-level simple.
- Proximo paso sugerido: repetir la prueba con firmas 2026 desolapadas y buscar validacion spatial externa o deconvolucion.

### Ola 003E
- Fecha de apertura: 2026-04-27 16:22:03 -03:00
- Tema: literatura 2026 y pivot a nicho CRLM en capas.
- Estado: abierta como refinamiento estrategico y preparacion de nueva validacion espacial.
- Archivos asociados:
- [InvestigacionSobreLiteratura2026NichoCRLM.md](./InvestigacionSobreLiteratura2026NichoCRLM.md)
- [ResumenInvestigacionSobreLiteratura2026NichoCRLM.md](./ResumenInvestigacionSobreLiteratura2026NichoCRLM.md)
- [data_manifest/generated/pubmed_crlm_latest_2025_2026_report.md](./data_manifest/generated/pubmed_crlm_latest_2025_2026_report.md)
- [data_manifest/generated/pubmed_crlm_latest_2025_2026.tsv](./data_manifest/generated/pubmed_crlm_latest_2025_2026.tsv)
- Resultado: el frente 2026 no reemplaza el eje metabolico, lo encaja dentro de un modelo mas amplio `CAF-high layered niche`: interfaz `MET/MYC/glycolysis` + interfaz `SPP1/CXCL12/myeloid/T-cell`.

### Ola 003F
- Fecha de apertura: 2026-04-27 16:50:00 -03:00
- Tema: validacion espacial 2026 del nicho CRLM en capas en GSE225857.
- Estado: abierta como primera validacion tecnica del pivot 2026.
- Archivos asociados:
- [InvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md](./InvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md)
- [ResumenInvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md](./ResumenInvestigacionSobreValidacionEspacial2026NichoEnCapasGSE225857.md)
- [data_manifest/generated/gse225857_spatial_2026_report.md](./data_manifest/generated/gse225857_spatial_2026_report.md)
- [data_manifest/generated/gse225857_spatial_2026_adjacency_permutation.tsv](./data_manifest/generated/gse225857_spatial_2026_adjacency_permutation.tsv)
- [scripts/analyze_gse225857_spatial_2026.py](./scripts/analyze_gse225857_spatial_2026.py)
- Resultado: el macro-nicho `CAF-high` se acopla espacialmente a `SPP1/CXCL12`, `HLA-DRB5-like` y `MYC/glycolysis` en LCT, con p empirico 0.002 en las pruebas principales. El control desolapado mantiene fuerte `SPP1/CXCL12-lite` y debilita `HLA-DRB5-lite`, que queda como rama secundaria.
