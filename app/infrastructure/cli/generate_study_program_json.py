# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import logging

from sqlmodel import Session

from config import settings
from infrastructure.adapter.external.study_program_agent_parser_provider import (
    StudyProgramAgentParserProvider,
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
        description="Generate JSON for stored study program Markdown."
    )
    parser.add_argument(
        "--markdown-tool",
        default=settings.pdf_converter,
        help="Markdown converter tool used to select source Markdown records.",
    )
    parser.add_argument(
        "--llm-agent-parser",
        choices=("gemini", "ollama"),
        default=settings.llm_agent_parser,
        help="LLM parser used to extract structured JSON.",
    )
    parser.add_argument(
        "--study-program-id",
        type=int,
        help="Process only the study_programs.id value provided.",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Regenerate JSON even when it already exists.",
    )
    args = parser.parse_args()

    from infrastructure.database import engine, init_db

    init_db()

    with Session(engine) as session:
        repository = SqlStudyProgramRepositoryAdapter(session)
        parser_provider = StudyProgramAgentParserProvider(settings)
        agent_parser = parser_provider.get_parser(args.llm_agent_parser)

        generated_count = 0
        for markdown in await repository.list_markdowns(
            args.markdown_tool,
            args.study_program_id,
        ):
            if not markdown.content:
                continue
            existing = await repository.find_json_by_study_program_id_and_tool_name(
                markdown.study_program_id,
                args.llm_agent_parser,
            )
            if existing and not args.refresh:
                continue

            output = await agent_parser.run(markdown.content)
            await repository.save_json(
                markdown.study_program_id,
                output.model_dump(mode="json"),
                args.llm_agent_parser,
            )
            generated_count += 1

    logger.info("Generated JSON for %s study programs.", generated_count)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_cli())
