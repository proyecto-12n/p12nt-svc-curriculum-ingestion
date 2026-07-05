# p12nt-svc-curriculum-ingestion

Servicio backend de ingestion del Curriculum Nacional para la plataforma 12NT.

El servicio descarga, parsea y persiste la jerarquia curricular: curriculums,
modalities, subjects, grade levels, study program references y study programs.

## Arquitectura

El proyecto sigue arquitectura hexagonal:

- `app/domain`: entidades puras y puertos. No depende de FastAPI, Pydantic,
  SQLModel ni drivers de base de datos.
- `app/application`: casos de uso que orquestan reglas de negocio mediante
  puertos.
- `app/infrastructure`: adaptadores externos: FastAPI, SQLModel/PostgreSQL,
  descarga de contenido, conversion de PDF y parsing HTML.

Reglas importantes del proyecto:

- Los puertos son `typing.Protocol`.
- La programacion de casos de uso y adaptadores es asincrona.
- Los modelos SQLModel viven solo en infraestructura.
- El codigo de dominio y aplicacion no debe importar frameworks externos.

## Requisitos

- Python 3.14 o superior.
- `uv`.
- PostgreSQL.

## Configuracion

La configuracion se lee desde variables de entorno o `.env`.

Variables principales:

```env
PROJECT_NAME=p12nt-svc-curriculum_ingestion-service
API_V1_STR=/api/v1
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/p12nt_curriculum_ingestion

LLM_AGENT_PARSER=gemini
GEMINI_API_KEY=
GEMINI_LLM_MODEL_NAME=gemini-1.5-flash

OLLAMA_LLM_BASE_URL=http://localhost:11434
OLLAMA_LLM_MODEL_NAME=llama3

PDF_CONVERTER=pymupdf4llm
```

## Instalacion

```powershell
uv sync
```

Activar entorno en Windows:

```powershell
.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "app"
```

Activar entorno en Linux/macOS:

```bash
source .venv/bin/activate
export PYTHONPATH=app
```

## Ejecutar API

```powershell
python app/main.py
```

Endpoints utiles:

- Healthcheck: `GET /health`
- OpenAPI JSON: `/api/v1/openapi.json`
- Swagger UI: `/docs`

Recursos expuestos bajo `/api/v1`:

- `/curriculums`
- `/modalities`
- `/subjects`
- `/grade-levels`
- `/study-program-refs`
- `/study-programs`

## Ejecutar ingesta

```powershell
python -m infrastructure.cli.ingest_curriculum
```

Forzar refresco de datos existentes:

```powershell
python -m infrastructure.cli.ingest_curriculum --refresh
```

La ingesta inicializa el esquema de base de datos, descarga los recursos del
Curriculum Nacional, parsea la jerarquia y persiste los registros.

## Tests

Ejecutar suite completa:

```powershell
.venv\Scripts\pytest
```

Ejecutar con cobertura:

```powershell
.venv\Scripts\pytest --cov=app --cov-report=term-missing
```

Estado actual de referencia: la suite pasa con cobertura total cercana al 96%.

## Calidad

Ejecutar hooks locales:

```powershell
.venv\Scripts\pre-commit.exe run --all-files
```

Si un ejecutable no esta disponible globalmente, usa siempre el binario dentro
de `.venv\Scripts\` en Windows o `.venv/bin/` en Linux/macOS.
