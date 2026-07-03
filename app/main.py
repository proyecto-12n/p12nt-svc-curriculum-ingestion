import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.infrastructure.database import init_db


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


# Acoplar routers HTTP de los adaptadores

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
