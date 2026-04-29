# Roadmap de agentes autonomos CRLM

Fecha: 2026-04-29 00:00:00 -03:00

## Objetivo de la fase

Convertir la hipotesis actual en una linea paper-grade:

`CAF/SPP1-CXCL12/HLA-DRB5 stromal-myeloid niche spatially couples to MYC/glycolysis tumor programs in colorectal liver metastasis.`

La prioridad no es acumular mas narrativa. La prioridad es tensionar la hipotesis con controles, evidencia externa, auditoria metodologica y lectura continua del estado 2026.

## Rol del agente padre

El agente padre actua como arquitecto:

- decide la direccion tecnica;
- divide tareas;
- integra resultados;
- mantiene los documentos centrales;
- evita sobreclaims;
- ejecuta o coordina commits/push;
- prioriza evidencia falsable por encima de entusiasmo biologico.

## Agente 1: investigador web/literatura/datasets

Mision:

Buscar continuamente evidencia nueva o no incorporada sobre CRLM, CAFs, SPP1/CXCL12, HLA-DRB5, macrofagos, MET/MYC/glycolysis, spatial transcriptomics y datasets publicos.

Preguntas:

1. Hay papers 2026/early online que contradigan o fortalezcan la hipotesis?
2. Hay datasets CRLM spatial/single-cell adicionales manejables?
3. Hay marcadores mejores para distinguir CAF, macrophage, tumor glycolysis y T-cell exhaustion?
4. Hay controles metodologicos publicados para evitar falsas asociaciones spatial por autocorrelacion?
5. Que claims ya estan publicados y no debemos vender como novedad?

Salida esperada:

- lista de fuentes con links;
- 5-10 hallazgos accionables;
- datasets priorizados por costo/valor;
- riesgos de novedad;
- recomendaciones para el siguiente experimento computacional.

## Agente 2: auditor metodologico

Mision:

Auditar la evidencia ya generada como si fuera un revisor hostil pero constructivo.

Preguntas:

1. Donde puede haber leakage por genes compartidos?
2. Donde las firmas son demasiado amplias o circulares?
3. El nulo espacial actual controla autocorrelacion, composicion tisular y profundidad/UMI?
4. Las comparaciones paired scRNA dependen de proxies demasiado gruesos?
5. Que controles negativos son minimos antes de hablar de paper?
6. Que resultados deberian bajar de prioridad o reescribirse?

Salida esperada:

- hallazgos ordenados por severidad;
- mejoras concretas;
- tests de falsacion;
- lista de claims permitidos/no permitidos.

## Trabajo local inmediato del agente padre

Mientras los agentes trabajan:

1. Consolidar GSE225857 y GSE217414 en una tabla comun de efectos espaciales.
2. Crear controles negativos iniciales: housekeeping/targets no relacionados y firmas aleatorias emparejadas por tamano si es viable.
3. Documentar un plan de nulos espaciales mas estrictos.
4. Actualizar `Conlusion.md`, `PlanValidacionCRLM.md` y `Roadmap.md` con lo que sobreviva.

## Criterios de avance

La linea avanza si:

- el patron aparece en al menos dos datasets spatial;
- los controles negativos no reproducen la misma fuerza;
- el efecto sobrevive a firmas desolapadas;
- la rama paired scRNA refuerza la parte mieloide/CAF;
- el claim se puede formular sin causalidad exagerada.

La linea baja prioridad si:

- controles negativos muestran efectos iguales;
- el patron desaparece con nulos espaciales estratificados;
- todo depende de `SPP1` o de genes muy expresados;
- no hay forma de separar composicion celular de arquitectura local;
- la literatura ya publico exactamente el mismo modelo multi-dataset.

## Entregable deseado de esta fase

Un paquete reproducible con:

- investigacion nueva;
- resumen fuerte;
- tabla multi-dataset de efectos;
- reporte de controles;
- auditoria de riesgos;
- proximo roadmap paper-grade.
