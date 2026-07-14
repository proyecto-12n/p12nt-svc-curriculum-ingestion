# Requirements - p12nt-svc-curriculum-ingestion

Fuente: `../p12nt-doc-technical-design/microservices.md`

Microservicio asociado en la arquitectura: `p12nt-svc-ingestion` - Curriculum Ingestion & Document Processing Service.

## Responsabilidad

Descargar, almacenar, convertir y preparar documentos oficiales o normativos para extraccion estructurada, manteniendo artefactos auditables.

## Requerimientos funcionales

| ID | Asociacion |
| --- | --- |
| RF-001 | Ingesta de documentos MINEDUC en PDF, HTML y Markdown. |
| RF-002 | Extraccion automatizada inicial de nodos mediante IA sobre chunks curriculares. |
| RF-034 | Monitoreo automatizado de fuentes oficiales MINEDUC y Diario Oficial. |
| RF-035 | Preprocesamiento de documentos normativos para analisis de impacto. |

## Reglas de negocio

RN-002, RN-035, RN-036.

## Requerimientos no funcionales con mayor impacto

RNF-002, RNF-004, RNF-005, RNF-006, RNF-012.

## Colaboradores

- Publica documentos y eventos para `p12nt-svc-academic`.
- Publica documentos y eventos para `p12nt-svc-alignment-ai`.

## Eventos de integracion

| Evento | Rol |
| --- | --- |
| `document.scraped` | Publica documentos descargados desde fuentes oficiales. |
| `document.parsed.to.markdown` | Publica documentos convertidos a Markdown canonico. |
