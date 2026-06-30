from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "p12nt-svc-curriculum-ingestion-service"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost:5432/p12nt_curriculum-ingestion"
    )

    # LLM Settings for external study program parsing agent
    llm_agent_parser: str = "gemini"
    gemini_api_key: str | None = None
    llm_model_name_gemini: str = "gemini-1.5-flash"
    llm_base_url_ollama: str = "http://localhost:11434"
    llm_model_name_ollama: str = "llama3"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
