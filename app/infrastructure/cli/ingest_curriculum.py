# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import logging
from sqlmodel import Session

# Import SQLModels to ensure they register in metadata

# Adapters & Use Case
from infrastructure.adapter.outbound.db import (
    SqlCurriculumRepositoryAdapter,
    SqlModalityRepositoryAdapter,
    SqlSubjectRepositoryAdapter,
    SqlGradeLevelRepositoryAdapter,
    SqlStudyProgramRefRepositoryAdapter,
    SqlStudyProgramRepositoryAdapter,
)
from application.usecase.ingest_curriculum_usecase import (
    IngestCurriculumUseCaseImpl,
)

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
        curriculum_repo = SqlCurriculumRepositoryAdapter(session)
        modality_repo = SqlModalityRepositoryAdapter(session)
        subject_repo = SqlSubjectRepositoryAdapter(session)
        grade_level_repo = SqlGradeLevelRepositoryAdapter(session)
        study_program_ref_repo = SqlStudyProgramRefRepositoryAdapter(session)
        study_program_repo = SqlStudyProgramRepositoryAdapter(session)

        from infrastructure.adapter.external.downloader_provider import (
            DownloaderProvider,
        )

        downloader_provider = DownloaderProvider()

        use_case = IngestCurriculumUseCaseImpl(
            curriculum_repository=curriculum_repo,
            modality_repository=modality_repo,
            subject_repository=subject_repo,
            grade_level_repository=grade_level_repo,
            study_program_ref_repository=study_program_ref_repo,
            study_program_repository=study_program_repo,
            downloader_provider=downloader_provider,
        )
        use_case.execute(refresh=args.refresh)

    logger.info("Ingestion completed successfully.")


if __name__ == "__main__":
    run_cli()
