# -*- coding: utf-8 -*-

# Add 'app' directory to sys.path to resolve 'infrastructure' imports when running tests from root


from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import SQLModel, create_engine, Session

from application.usecase.ingest_curriculum_usecase import (
    IngestCurriculumUseCaseImpl,
)
from domain.model.node import Node
from domain.model.resource_type import ResourceType
from infrastructure.adapter.outbound.db import (
    SqlCurriculumRepositoryAdapter,
    SqlModalityRepositoryAdapter,
    SqlSubjectRepositoryAdapter,
    SqlGradeLevelRepositoryAdapter,
    SqlStudyProgramRefRepositoryAdapter,
    SqlStudyProgramRepositoryAdapter,
)
from infrastructure.cli.ingest_curriculum import run_cli


def mock_get_mock_content(url: str) -> str | bytes:
    if url == "https://www.curriculumnacional.cl/curriculum":
        return """
        <html>
            <body>
                <h1>Curriculum Nacional</h1>
                <div class="menu">
                    <a href="/curriculum/basica"><h3>Educación Regular Básica</h3></a>
                </div>
            </body>
        </html>
        """
    elif url == "https://www.curriculumnacional.cl/curriculum/basica":
        return """
        <html>
            <body>
                <h1>Educación Regular Básica</h1>
                <div class="subject">
                    <a href="/curriculum/basica/matematica"><span class="subject-title">Matemáticas</span></a>
                </div>
            </body>
        </html>
        """
    elif url == "https://www.curriculumnacional.cl/curriculum/basica/matematica":
        return """
        <html>
            <body>
                <h1>Matemáticas</h1>
                <div class="cursos-wrapper">
                    <div class="grade-wrapper">
                        <a href="/curriculum/basica/matematica/1g">1° Básico</a>
                    </div>
                </div>
            </body>
        </html>
        """
    elif url == "https://www.curriculumnacional.cl/curriculum/basica/matematica/1g":
        return """
        <html>
            <body>
                <h1>1° Básico</h1>
                <div class="three-grid-content">
                    <div class="card--content">
                        <span class="badge">Programa de estudio</span>
                        <a href="/curriculum/basica/matematica/1g/ref">Programa de estudio</a>
                    </div>
                </div>
            </body>
        </html>
        """
    elif url == "https://www.curriculumnacional.cl/curriculum/basica/matematica/1g/ref":
        return """
        <html>
            <body>
                <h1>Programa de estudio 1° Básico</h1>
                <a href="/curriculum/basica/matematica/1g/ref/programa.pdf">Descargar PDF</a>
            </body>
        </html>
        """
    elif url.endswith(".pdf") or "programa" in url:
        return b"PDF content"
    return ""


@pytest.mark.skip
@pytest.mark.asyncio
async def test_ingest_curriculum_usecase_with_force_mock():
    # Setup in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    for table in SQLModel.metadata.tables.values():
        table.schema = None
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        curriculum_repo = SqlCurriculumRepositoryAdapter(session)
        modality_repo = SqlModalityRepositoryAdapter(session)
        subject_repo = SqlSubjectRepositoryAdapter(session)
        grade_level_repo = SqlGradeLevelRepositoryAdapter(session)
        study_program_ref_repo = SqlStudyProgramRefRepositoryAdapter(session)
        study_program_repo = SqlStudyProgramRepositoryAdapter(session)

        # Setup mock downloader
        async def mock_download(url, timeout=10.0):
            content = mock_get_mock_content(url)
            res_type = (
                ResourceType.PDF
                if (url.endswith(".pdf") or "programa" in url)
                else ResourceType.HTML
            )
            return Node(url=url, type=res_type, content=content)

        mock_downloader = MagicMock()
        mock_downloader.download = mock_download

        downloader_provider = MagicMock()
        downloader_provider.get_downloader.return_value = mock_downloader

        use_case = IngestCurriculumUseCaseImpl(
            curriculum_repository=curriculum_repo,
            modality_repository=modality_repo,
            subject_repository=subject_repo,
            grade_level_repository=grade_level_repo,
            study_program_ref_repository=study_program_ref_repo,
            study_program_repository=study_program_repo,
            downloader_provider=downloader_provider,
        )

        # Execute
        await use_case.execute()

        # Verify that data was ingested in the database
        curr = await curriculum_repo.find_by_url(
            "https://www.curriculumnacional.cl/curriculum"
        )
        assert curr is not None
        assert curr.title == "Curriculum Nacional"

        # Let's verify modalities were saved
        mod = await modality_repo.find_by_url(
            "https://www.curriculumnacional.cl/curriculum/basica"
        )
        assert mod is not None

        # Check that we can run again and it uses existing records
        await use_case.execute()


@pytest.mark.skip
@pytest.mark.asyncio
async def test_ingest_curriculum_usecase_downloader_failure_fallback():
    engine = create_engine("sqlite:///:memory:")
    for table in SQLModel.metadata.tables.values():
        table.schema = None
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        curriculum_repo = SqlCurriculumRepositoryAdapter(session)
        modality_repo = SqlModalityRepositoryAdapter(session)
        subject_repo = SqlSubjectRepositoryAdapter(session)
        grade_level_repo = SqlGradeLevelRepositoryAdapter(session)
        study_program_ref_repo = SqlStudyProgramRefRepositoryAdapter(session)
        study_program_repo = SqlStudyProgramRepositoryAdapter(session)

        # Mock downloader provider to raise an error when PDF download is called
        async def mock_download(url, timeout=10.0):
            if url.endswith(".pdf") or "programa" in url:
                raise Exception("Connection reset by peer")
            content = mock_get_mock_content(url)
            return Node(url=url, type=ResourceType.HTML, content=content)

        mock_downloader = MagicMock()
        mock_downloader.download = mock_download

        mock_downloader_provider = MagicMock()
        mock_downloader_provider.get_downloader.return_value = mock_downloader

        use_case = IngestCurriculumUseCaseImpl(
            curriculum_repository=curriculum_repo,
            modality_repository=modality_repo,
            subject_repository=subject_repo,
            grade_level_repository=grade_level_repo,
            study_program_ref_repository=study_program_ref_repo,
            study_program_repository=study_program_repo,
            downloader_provider=mock_downloader_provider,
        )

        await use_case.execute()

        # Verify fallback still populated database structures
        curr = await curriculum_repo.find_by_url(
            "https://www.curriculumnacional.cl/curriculum"
        )
        assert curr is not None

        # Verify empty placeholder program was saved on PDF failure
        prog = await study_program_repo.find_by_url(
            "https://www.curriculumnacional.cl/curriculum/basica/matematica/1g/ref/programa.pdf"
        )
        assert prog is not None
        assert prog.content == b""


def test_run_cli_postgresql_dialect():
    with (
        patch("infrastructure.cli.ingest_curriculum.Session") as mock_session_class,
        patch("infrastructure.database.init_db") as mock_init_db,
        patch(
            "infrastructure.cli.ingest_curriculum.IngestCurriculumUseCaseImpl"
        ) as mock_usecase_class,
        patch("argparse.ArgumentParser.parse_args") as mock_parse_args,
    ):
        mock_args = MagicMock()
        mock_args.refresh = False
        mock_parse_args.return_value = mock_args

        mock_engine = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        mock_usecase = MagicMock()

        async def mock_execute(*args, **kwargs):
            pass

        mock_usecase.execute = MagicMock(side_effect=mock_execute)
        mock_usecase_class.return_value = mock_usecase

        with patch("infrastructure.database.engine", new=mock_engine):
            run_cli()

            mock_init_db.assert_called_once()
            mock_usecase.execute.assert_called_once_with(refresh=False)


def test_init_db_postgresql():
    mock_engine = MagicMock()
    mock_engine.url = "postgresql://localhost:5432/test"

    with (
        patch("infrastructure.database.engine", new=mock_engine),
        patch("sqlalchemy.text") as mock_text,
        patch("sqlmodel.SQLModel.metadata.create_all") as mock_create_all,
    ):
        from infrastructure.database import init_db

        init_db()

        mock_engine.connect.assert_called_once()
        mock_create_all.assert_called_once_with(mock_engine)
        mock_text.assert_called_once_with(
            'CREATE SCHEMA IF NOT EXISTS "curriculum-ingestion"'
        )


def test_init_db_sqlite():
    mock_engine = MagicMock()
    mock_engine.url = "sqlite:///:memory:"

    with (
        patch("infrastructure.database.engine", new=mock_engine),
        patch("sqlalchemy.text") as mock_text,
        patch("sqlmodel.SQLModel.metadata.create_all") as mock_create_all,
    ):
        from infrastructure.database import init_db

        init_db()

        mock_engine.connect.assert_not_called()
        mock_create_all.assert_called_once_with(mock_engine)
        mock_text.assert_not_called()
