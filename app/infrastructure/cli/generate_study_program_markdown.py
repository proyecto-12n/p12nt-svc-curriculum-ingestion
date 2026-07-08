# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import logging

from sqlmodel import Session

from application.usecase.convert_pdf_to_markdown_usecase import (
    ConvertPDFToMarkdownUseCaseImpl,
)
from config import settings
from domain.model.pdf_resource import PDFResource
from infrastructure.adapter.external.pdf_converter.pdf_converter_provider import (
    PDFConverterProvider,
)
from infrastructure.adapter.outbound.db.impl.sql_study_program_repository_adapter import (
    SqlStudyProgramRepositoryAdapter,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


async def run_cli():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Markdown for stored study program PDFs."
    )
    parser.add_argument(
        "--pdf-converter",
        choices=("pymupdf4llm", "markitdown"),
        default=settings.pdf_converter,
        help="PDF converter used to generate stored Markdown.",
    )
    parser.add_argument(
        "--study-program-id",
        type=int,
        help="Process only the study_programs.id value provided.",
    )
    args = parser.parse_args()

    from infrastructure.database import engine, init_db

    init_db()

    with Session(engine) as session:
        repository = SqlStudyProgramRepositoryAdapter(session)
        use_case = ConvertPDFToMarkdownUseCaseImpl(PDFConverterProvider())

        if args.study_program_id is not None:
            study_program = await repository.find_by_id(args.study_program_id)
            study_programs = [study_program] if study_program else []
        else:
            study_programs = await repository.list()

        generated_count = 0
        for study_program in study_programs:
            if not study_program.content:
                continue
            existing = await repository.find_markdown_by_study_program_id_and_tool_name(
                study_program.id,
                args.pdf_converter,
            )
            if existing:
                continue

            markdown = await use_case.execute(
                PDFResource(
                    content=study_program.content,
                    source_name=study_program.url,
                ),
                args.pdf_converter,
            )
            await repository.save_markdown(
                study_program,
                markdown,
                args.pdf_converter,
            )
            generated_count += 1

    logger.info("Generated Markdown for %s study programs.", generated_count)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_cli())
