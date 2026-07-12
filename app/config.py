from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    PROJECT_NAME: str = "p12nt-svc-curriculum-ingestion"
    API_V1_STR: str = "/api/v1"
    P12NT_CURRICULUM_DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost:5432/p12nt_curriculum_ingestion"
    )
    P12NT_CURRICULUM_INIT_DB: bool = True

    # PDF Converter settings
    pdf_converter: str = "pymupdf4llm"

    model_config = SettingsConfigDict(env_file=ENV_FILE, case_sensitive=False)


settings = Settings()
