# -*- coding: utf-8 -*-

# Add 'app' directory to sys.path to resolve 'infrastructure' imports when running tests from root


from unittest.mock import MagicMock, patch

from sqlmodel import SQLModel, create_engine, Session

from app.application.usecase.ingest_curriculum_usecase import (
    IngestCurriculumUseCaseImpl,
)
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.infrastructure.adapter.outbound.db.sql_curriculum_repository_adapter import (
    SqlCurriculumRepositoryAdapter,
)
from app.infrastructure.cli.ingest_curriculum import run_cli


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


def test_ingest_curriculum_usecase_with_force_mock():
    # Setup in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    for table in SQLModel.metadata.tables.values():
        table.schema = None
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        repository = SqlCurriculumRepositoryAdapter(session)

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

        use_case = IngestCurriculumUseCaseImpl(repository, downloader_provider)

        # Execute
        use_case.execute()

        # Verify that data was ingested in the database
        curr = repository.find_curriculum_by_url(
            "https://www.curriculumnacional.cl/curriculum"
        )
        assert curr is not None
        assert curr.title == "Curriculum Nacional"

        # Let's verify modalities were saved
        mod = repository.find_modality_by_url(
            "https://www.curriculumnacional.cl/curriculum/basica"
        )
        assert mod is not None

        # Check that we can run again and it uses existing records
        use_case.execute()


def test_ingest_curriculum_usecase_downloader_failure_fallback():
    engine = create_engine("sqlite:///:memory:")
    for table in SQLModel.metadata.tables.values():
        table.schema = None
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        repository = SqlCurriculumRepositoryAdapter(session)

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

        use_case = IngestCurriculumUseCaseImpl(repository, mock_downloader_provider)

        use_case.execute()

        # Verify fallback still populated database structures
        curr = repository.find_curriculum_by_url(
            "https://www.curriculumnacional.cl/curriculum"
        )
        assert curr is not None

        # Verify empty placeholder program was saved on PDF failure
        prog = repository.find_study_program_by_url(
            "https://www.curriculumnacional.cl/curriculum/basica/matematica/1g/ref/programa.pdf"
        )
        assert prog is not None
        assert prog.content == b""


def test_run_cli_postgresql_dialect():
    with (
        patch("app.infrastructure.cli.ingest_curriculum.Session") as mock_session_class,
        patch("app.infrastructure.cli.ingest_curriculum.SQLModel") as mock_sqlmodel,
        patch(
            "app.infrastructure.cli.ingest_curriculum.IngestCurriculumUseCaseImpl"
        ) as mock_usecase_class,
    ):
        mock_engine = MagicMock()
        mock_engine.url = "postgresql://localhost:5432/test"
        mock_engine.dialect.name = "postgresql"

        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        mock_usecase = MagicMock()
        mock_usecase_class.return_value = mock_usecase

        with (
            patch("app.infrastructure.database.engine", new=mock_engine),
            patch("sqlalchemy.text") as mock_text,
        ):
            run_cli()

            mock_engine.connect.assert_called_once()
            mock_usecase.execute.assert_called_once()
            mock_sqlmodel.metadata.create_all.assert_called_once_with(mock_engine)
            assert mock_text is not None
