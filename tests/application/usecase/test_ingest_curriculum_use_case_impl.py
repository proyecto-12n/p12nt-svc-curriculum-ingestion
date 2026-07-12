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

    async def test_given_edge_with_title_when_navigate_then_preserves_link_title(self):
        repository = AsyncMock()
        repository.find_by_url.return_value = None
        repository_provider = SimpleNamespace(
            get_repository=MagicMock(return_value=repository)
        )
        parser = MagicMock()
        parser.get_title = AsyncMock(return_value="Page Title")

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
            url="https://example.test/linked",
            type=ResourceType.HTML,
            content="<h1>Page Title</h1>",
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
        edge = Edge(
            url="https://example.test/linked",
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.CURRICULUM,
            title="Link Title",
        )

        await use_case._IngestCurriculumUseCaseImpl__navigator(False, edge)

        mapper.to_model.assert_called_once()
        assert mapper.to_model.call_args.args[0].title == "Link Title"
        parser.get_title.assert_not_awaited()

    async def test_given_cached_edge_when_reprocess_titles_then_parses_title_and_saves(
        self,
    ):
        cached_model = SimpleNamespace(
            id=1,
            url="https://example.test/linked",
            title="Old Link Title",
            content="<h1>Clean Page Title</h1>",
        )
        repository = AsyncMock()
        repository.find_by_url.return_value = cached_model
        repository_provider = SimpleNamespace(
            get_repository=MagicMock(return_value=repository)
        )
        parser = MagicMock()
        parser.get_title = AsyncMock(return_value="Clean Page Title")

        async def no_children(_resource):
            if False:
                yield None

        parser.get_children = no_children
        parser_provider = SimpleNamespace(get_parser=MagicMock(return_value=parser))
        mapper = MagicMock()
        mapper.to_edge.return_value = Edge(
            url=cached_model.url,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.CURRICULUM,
            title=cached_model.title,
            content=cached_model.content,
        )
        mapper.to_model.return_value = "updated-model"
        mapper_provider = SimpleNamespace(get_mapper=MagicMock(return_value=mapper))
        downloader_provider = SimpleNamespace(get_downloader=MagicMock())
        use_case = IngestCurriculumUseCaseImpl(
            repository_provider_adapter=repository_provider,
            resource_parser_provider_adapter=parser_provider,
            curriculum_hierarchy_mapper_provider=mapper_provider,
            downloader_provider=downloader_provider,
        )
        edge = Edge(
            url=cached_model.url,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.CURRICULUM,
            title="Old Link Title",
        )

        await use_case._IngestCurriculumUseCaseImpl__navigator(
            False, edge, reprocess_titles=True
        )

        parser.get_title.assert_awaited_once()
        assert mapper.to_model.call_args.args[0].title == "Clean Page Title"
        repository.save.assert_awaited_once_with("updated-model")
        downloader_provider.get_downloader.assert_not_called()

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

    async def test_given_ignore_pdf_resources_when_navigate_pdf_then_skips_processing(
        self,
    ):
        repository_provider = SimpleNamespace(get_repository=MagicMock())
        downloader_provider = SimpleNamespace(get_downloader=MagicMock())
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

        await use_case._IngestCurriculumUseCaseImpl__navigator(
            False, edge, ignore_pdf_resources=True
        )

        repository_provider.get_repository.assert_not_called()
        downloader_provider.get_downloader.assert_not_called()

    async def test_given_cached_study_program_when_get_resource_then_returns_cached_pdf(
        self,
    ):
        cached_model = SimpleNamespace(
            id=1,
            parent_id=2,
            url="https://example.test/program.pdf",
            title="Program",
            content=b"pdf",
            checksum="abc",
        )
        repository = AsyncMock()
        repository.find_by_url.return_value = cached_model
        repository_provider = SimpleNamespace(
            get_repository=MagicMock(return_value=repository)
        )
        mapper = MagicMock()
        mapper.to_edge.return_value = Edge(
            url=cached_model.url,
            type=ResourceType.PDF,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
            content=cached_model.content,
        )
        mapper_provider = SimpleNamespace(get_mapper=MagicMock(return_value=mapper))
        use_case = IngestCurriculumUseCaseImpl(
            repository_provider_adapter=repository_provider,
            resource_parser_provider_adapter=MagicMock(),
            curriculum_hierarchy_mapper_provider=mapper_provider,
            downloader_provider=MagicMock(),
        )
        edge = Edge(
            url=cached_model.url,
            type=ResourceType.PDF,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
        )

        cache, resource = await use_case._IngestCurriculumUseCaseImpl__get_resource(
            False, edge
        )

        assert cache is True
        assert resource.content == b"pdf"
        repository.save.assert_not_awaited()
        repository.save_markdown.assert_not_awaited()
