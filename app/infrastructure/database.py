from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

db_url = settings.DATABASE_URL
if db_url.startswith("postgresql+asyncpg://"):
    db_url = db_url.replace("postgresql+asyncpg://", "postgresql://", 1)

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database schema and tables."""
    import logging
    from sqlmodel import SQLModel

    # Import all models to ensure they register in SQLModel.metadata
    import infrastructure.models  # noqa: F401

    logger = logging.getLogger(__name__)
    db_url_str = str(engine.url)
    logger.info("Using database configuration from app/infrastructure/database.py")

    # In PostgreSQL, we must ensure schema exists before creating tables
    if "postgresql" in db_url_str:
        from sqlalchemy import text

        with engine.connect() as conn:
            conn.execute(text('CREATE SCHEMA IF NOT EXISTS "curriculum_ingestion"'))
            conn.commit()

    # Create tables
    SQLModel.metadata.create_all(engine)
    logger.info("Database schema and tables initialized.")
