from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "p12nt-svc-curriculum_ingestion-service"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost:5432/p12nt_curriculum_ingestion"
    )

    # LLM Settings for external study program parsing agent
    llm_agent_parser: str = "gemini"
    gemini_api_key: str | None = None
    gemini_llm_model_name: str = "gemini-1.5-flash"

    ollama_llm_base_url: str = "http://localhost:11434"
    ollama_llm_model_name: str = "llama3"

    # PDF Converter settings
    pdf_converter: str = "pymupdf4llm"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
