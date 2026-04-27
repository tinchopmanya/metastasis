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
- Ola 003: `nicho metastásico hepático en cáncer colorrectal`

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
- [Conlusion.md](./Conlusion.md)
- Hipótesis de trabajo actual: CAFs/mCAFs del hígado crean nichos metabólicos e inmunomoduladores que favorecen células tumorales colorrectales plásticas, con señalización `HGF-MET`, activación `MYC` y glicólisis local.
- Resultado tecnico vigente: bulk, single-cell, spatial y permutaciones apoyan un nicho `CAF-high -> MET/MYC/glicolisis`; `HGF` aislado no captura por si solo la arquitectura espacial.
- Próximo paso sugerido: buscar validacion independiente/especificidad en otro dataset o cohorte metastasica, manteniendo la hipotesis refinada como programa CAF compuesto.
