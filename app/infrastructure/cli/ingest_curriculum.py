# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import logging
from sqlmodel import Session, SQLModel

# Import SQLModels to ensure they register in metadata

# Adapters & Use Case
from app.infrastructure.adapter.outbound.db.sql_curriculum_repository_adapter import (
    SqlCurriculumRepositoryAdapter,
)
from app.application.usecase.ingest_curriculum_usecase import (
    IngestCurriculumUseCaseImpl,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def run_cli():
    # Database setup
    from app.infrastructure.database import engine

    db_url = str(engine.url)
    logger.info("Using database configuration from app/infrastructure/database.py")

    # In PostgreSQL, we must ensure schema exists before creating tables
    if "postgresql" in db_url:
        from sqlalchemy import text

        with engine.connect() as conn:
            conn.execute(text('CREATE SCHEMA IF NOT EXISTS "curriculum-ingestion"'))
            conn.commit()

    # Create tables
    SQLModel.metadata.create_all(engine)
    logger.info("Database schema and tables initialized.")

    with Session(engine) as session:
        repository = SqlCurriculumRepositoryAdapter(session)
        from app.infrastructure.adapter.external.downloader_provider import (
            DownloaderProvider,
        )

        downloader_provider = DownloaderProvider()

        use_case = IngestCurriculumUseCaseImpl(repository, downloader_provider)
        use_case.execute()

    logger.info("Ingestion completed successfully.")


if __name__ == "__main__":
    run_cli()
