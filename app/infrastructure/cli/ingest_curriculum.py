# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import logging

from sqlmodel import Session

from application.usecase.ingest_curriculum_usecase import (
    IngestCurriculumUseCaseImpl,
)
from infrastructure.adapter.outbound import ScrapResourceParserProviderAdapter
from infrastructure.adapter.outbound.db import (
    SqlCurriculumHierarchyRepositoryProviderAdapter,
)
from infrastructure.mapper import CurriculumHierarchyMapperProviderAdapter


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def run_cli():
    import argparse

    parser = argparse.ArgumentParser(
        description="Ingest curriculum national data into the database."
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force the update of elements even if they already exist in the database.",
    )
    args = parser.parse_args()

    # Database setup
    from infrastructure.database import engine, init_db

    init_db()

    with Session(engine) as session:
        from infrastructure.adapter.external.downloader_provider import (
            DownloaderProvider,
        )

        repository_provider_adapter = SqlCurriculumHierarchyRepositoryProviderAdapter(
            session
        )
        node_parser_provider_adapter = ScrapResourceParserProviderAdapter()
        curriculum_hierarchy_mapper_provider = (
            CurriculumHierarchyMapperProviderAdapter()
        )
        downloader_provider = DownloaderProvider()

        use_case = IngestCurriculumUseCaseImpl(
            repository_provider_adapter=repository_provider_adapter,
            resource_parser_provider_adapter=node_parser_provider_adapter,
            curriculum_hierarchy_mapper_provider=curriculum_hierarchy_mapper_provider,
            downloader_provider=downloader_provider,
        )
        import asyncio

        asyncio.run(use_case.execute(refresh=args.refresh))

    logger.info("Ingestion completed successfully.")


if __name__ == "__main__":
    run_cli()
