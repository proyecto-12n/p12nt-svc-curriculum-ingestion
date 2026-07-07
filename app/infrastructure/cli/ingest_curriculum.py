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
from application.usecase.convert_pdf_to_markdown_usecase import (
    ConvertPDFToMarkdownUseCaseImpl,
)
from infrastructure.adapter.external.pdf_converter.pdf_converter_provider import (
    PDFConverterProvider,
)
from infrastructure.adapter.outbound.db import (
    SqlCurriculumHierarchyRepositoryProviderAdapter,
)
from infrastructure.adapter.outbound.http.scrap_resource_parser_provider_adapter import (
    ScrapResourceParserProviderAdapter,
)
from infrastructure.mapper import CurriculumHierarchyMapperProviderAdapter
from config import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


async def run_cli():
    import argparse

    parser = argparse.ArgumentParser(
        description="Ingest curriculum national data into the database."
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force the update of elements even if they already exist in the database.",
    )

    parser.add_argument(
        "--pdf-converter",
        choices=("pymupdf4llm", "markitdown"),
        default=settings.pdf_converter,
        help="PDF converter used to generate stored Markdown.",
    )

    parser.add_argument(
        "--ignore-pdf-resources",
        action="store_true",
        help="Skip PDF resource download, persistence, and Markdown generation.",
    )

    args = parser.parse_args()

    # Database setup
    from infrastructure.database import engine, init_db

    init_db()

    with Session(engine) as session:
        from infrastructure.adapter.external.downloader.downloader_provider import (
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
        pdf_to_markdown_use_case = ConvertPDFToMarkdownUseCaseImpl(
            PDFConverterProvider()
        )

        use_case = IngestCurriculumUseCaseImpl(
            repository_provider_adapter=repository_provider_adapter,
            resource_parser_provider_adapter=node_parser_provider_adapter,
            curriculum_hierarchy_mapper_provider=curriculum_hierarchy_mapper_provider,
            downloader_provider=downloader_provider,
            pdf_to_markdown_use_case=pdf_to_markdown_use_case,
            markdown_tool_name=args.pdf_converter,
        )
        await use_case.execute(
            refresh=args.refresh,
            ignore_pdf_resources=args.ignore_pdf_resources,
        )

    logger.info("Ingestion completed successfully.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_cli())
