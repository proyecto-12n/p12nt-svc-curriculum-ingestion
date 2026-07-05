from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from application.usecase.ingest_curriculum_usecase import IngestCurriculumUseCaseImpl
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource


class TestIngestCurriculumUseCaseImpl:
    async def test_given_uncached_root_when_execute_then_downloads_parses_maps_and_saves(
        self,
    ):
        repository = AsyncMock()
        repository.find_by_url.return_value = None
        repository_provider = SimpleNamespace(
            get_repository=MagicMock(return_value=repository)
        )
        parser = MagicMock()
        parser.get_title = AsyncMock(return_value="Curriculum")

        async def no_children(_resource):
            if False:
                yield None

        parser.get_children = no_children
        parser_provider = SimpleNamespace(get_parser=MagicMock(return_value=parser))
        mapper = MagicMock()
        mapper.to_model.return_value = "model"
        mapper_provider = SimpleNamespace(get_mapper=MagicMock(return_value=mapper))
        downloader = AsyncMock()
        downloader.download.return_value = ScrapResource(
            url="https://www.curriculumnacional.cl/curriculum",
            type=ResourceType.HTML,
            content="<h1>Curriculum</h1>",
        )
        downloader_provider = SimpleNamespace(
            get_downloader=MagicMock(return_value=downloader)
        )
        use_case = IngestCurriculumUseCaseImpl(
            repository_provider_adapter=repository_provider,
            resource_parser_provider_adapter=parser_provider,
            curriculum_hierarchy_mapper_provider=mapper_provider,
            downloader_provider=downloader_provider,
        )

        await use_case.execute()

        repository.find_by_url.assert_awaited_once_with(
            "https://www.curriculumnacional.cl/curriculum"
        )
        downloader.download.assert_awaited_once_with(
            "https://www.curriculumnacional.cl/curriculum"
        )
        repository.save.assert_awaited_once_with("model")

    async def test_given_pdf_download_failure_when_get_resource_then_returns_empty_pdf_placeholder(
        self,
    ):
        repository = AsyncMock()
        repository.find_by_url.return_value = None
        repository_provider = SimpleNamespace(
            get_repository=MagicMock(return_value=repository)
        )
        downloader = AsyncMock()
        downloader.download.side_effect = Exception("Connection reset by peer")
        downloader_provider = SimpleNamespace(
            get_downloader=MagicMock(return_value=downloader)
        )
        use_case = IngestCurriculumUseCaseImpl(
            repository_provider_adapter=repository_provider,
            resource_parser_provider_adapter=MagicMock(),
            curriculum_hierarchy_mapper_provider=MagicMock(),
            downloader_provider=downloader_provider,
        )
        edge = Edge(
            url="https://example.test/program.pdf",
            type=ResourceType.PDF,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
        )

        cache, resource = await use_case._IngestCurriculumUseCaseImpl__get_resource(
            False, edge
        )

        assert cache is False
        assert resource.type == ResourceType.PDF
        assert resource.content == b""
