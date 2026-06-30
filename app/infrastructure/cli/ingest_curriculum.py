# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import argparse
import logging
from sqlmodel import Session, SQLModel, create_engine

# Import SQLModels to ensure they register in metadata

# Adapters & Use Case
from app.infrastructure.adapter.outbound.db.sql_curriculum_repository_adapter import (
    SqlCurriculumRepositoryAdapter,
)
from app.infrastructure.adapter.outbound.http.http_curriculum_scraper_adapter import (
    HttpCurriculumScraperAdapter,
)
from app.application.usecase.ingest_curriculum_usecase import (
    IngestCurriculumUseCaseImpl,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def run_cli():
    parser = argparse.ArgumentParser(description="P12NT Curriculum Ingestion CLI")
    parser.add_argument(
        "--db-url", default=None, help="Database URL connection string."
    )
    parser.add_argument(
        "--sqlite",
        action="store_true",
        help="Force the use of a local SQLite database (curriculum_cache.db).",
    )
    args = parser.parse_args()

    # Database setup
    if args.sqlite:
        db_url = "sqlite:///curriculum_cache.db"
        logger.info(f"Using database: {db_url}")
        engine = create_engine(db_url)
    elif args.db_url:
        db_url = args.db_url
        logger.info(f"Using database: {db_url}")
        engine = create_engine(db_url)
    else:
        from app.infrastructure.database import engine

        db_url = str(engine.url)
        logger.info("Using API database connection")

    # In PostgreSQL, we must ensure schema exists before creating tables
    if "postgresql" in db_url:
        from sqlalchemy import text

        with engine.connect() as conn:
            conn.execute(text('CREATE SCHEMA IF NOT EXISTS "curriculum-ingestion"'))
            conn.commit()

    # For SQLite, remove schema attribute to prevent errors
    if engine.dialect.name == "sqlite":
        for table in SQLModel.metadata.tables.values():
            table.schema = None

    # Create tables
    SQLModel.metadata.create_all(engine)
    logger.info("Database schema and tables initialized.")

    with Session(engine) as session:
        repository = SqlCurriculumRepositoryAdapter(session)
        scraper = HttpCurriculumScraperAdapter()

        use_case = IngestCurriculumUseCaseImpl(repository, scraper)
        use_case.execute()

    logger.info("Ingestion completed successfully.")


if __name__ == "__main__":
    run_cli()
