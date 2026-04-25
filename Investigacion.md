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
- Ola 002: `cáncer colorrectal -> metástasis hepática`

## Olas registradas

### Ola 001
- Fecha de apertura: 2026-04-23 03:15:24 -03:00
- Tema: metástasis en cánceres y oportunidades de descubrimiento con IA sin hacer ensayos clínicos nuevos.
- Estado: cerrada como marco panorámico.
- Archivos asociados:
- [InvestigacionSobreMetastasisEnCanceres.md](./InvestigacionSobreMetastasisEnCanceres.md)
- [ResumenInvestigacionSobreMetastasisEnCanceres.md](./ResumenInvestigacionSobreMetastasisEnCanceres.md)
- [Conlusion.md](./Conlusion.md)
- Hipótesis de trabajo actual: la mejor combinación entre impacto, datos abiertos y probabilidad de descubrimiento reproducible con IA parece estar en cáncer colorrectal con metástasis hepática. Muy cerca quedan cáncer de mama con metástasis a cerebro o hueso y cáncer de pulmón con metástasis cerebral.
- Próximo paso sugerido: convertir la conclusión actual en una investigación de segunda ola con foco estrecho y datasets concretos.

### Ola 002
- Fecha de apertura: 2026-04-23 03:28:33 -03:00
- Tema: cáncer colorrectal y metástasis hepática.
- Estado: activa.
- Archivos asociados:
- [InvestigacionSobreCancerColorrectalYMetastasisHepatica.md](./InvestigacionSobreCancerColorrectalYMetastasisHepatica.md)
- [ResumenInvestigacionSobreCancerColorrectalYMetastasisHepatica.md](./ResumenInvestigacionSobreCancerColorrectalYMetastasisHepatica.md)
- [Conlusion.md](./Conlusion.md)
- Hipótesis de trabajo actual: la mayor probabilidad de descubrimiento no parece estar en una sola mutación "nueva", sino en un programa de nicho metastásico hepático reproducible que combine plasticidad tumoral, fibroblastos metastásicos, soporte metabólico e inmunorresistencia.
- Subproyecto biológico recomendado: nicho metastásico hepático en CRLM.
- Subproyecto técnico recomendado: predicción de recurrencia post-hepatectomía usando TCIA.
- Próximo paso sugerido: abrir una ola 003 centrada en `nicho metastásico hepático` o, si queremos algo más ingenieril, en `recurrencia post-hepatectomía en CRLM`.
