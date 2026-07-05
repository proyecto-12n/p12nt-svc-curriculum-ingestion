import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from infrastructure.database import init_db
from infrastructure.adapter.inbound.web.routers.curriculum_router import (
    router as curriculum_router,
)
from infrastructure.adapter.inbound.web.routers.data_quality_kpi_router import (
    router as data_quality_kpi_router,
)
from infrastructure.adapter.inbound.web.routers.modality_router import (
    router as modality_router,
)
from infrastructure.adapter.inbound.web.routers.subject_router import (
    router as subject_router,
)
from infrastructure.adapter.inbound.web.routers.grade_level_router import (
    router as grade_level_router,
)
from infrastructure.adapter.inbound.web.routers.study_program_ref_router import (
    router as study_program_ref_router,
)
from infrastructure.adapter.inbound.web.routers.study_program_router import (
    router as study_program_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database and create tables if they do not exist
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Configurar CORS para el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modificar en produccion
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Healthcheck
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}


app.include_router(curriculum_router, prefix=settings.API_V1_STR)
app.include_router(data_quality_kpi_router, prefix=settings.API_V1_STR)
app.include_router(modality_router, prefix=settings.API_V1_STR)
app.include_router(subject_router, prefix=settings.API_V1_STR)
app.include_router(grade_level_router, prefix=settings.API_V1_STR)
app.include_router(study_program_ref_router, prefix=settings.API_V1_STR)
app.include_router(study_program_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
