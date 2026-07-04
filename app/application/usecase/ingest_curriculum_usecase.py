# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import logging
from typing import Any, AsyncGenerator, Tuple, Optional

from domain.model import (
    Node,
    CurriculumHierarchyType,
)
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from domain.port.inbound import IngestCurriculumUseCase
from domain.port.outbound import (
    DownloaderProvider,
    CurriculumHierarchyRepositoryProvider,
    ScrapResourceParserProvider,
    CurriculumHierarchyMapperProvider,
)

logger = logging.getLogger(__name__)

_ROOT_URL = "https://www.curriculumnacional.cl/curriculum"


class IngestCurriculumUseCaseImpl(IngestCurriculumUseCase):
    def __init__(
        self,
        repository_provider_adapter: CurriculumHierarchyRepositoryProvider,
        resource_parser_provider_adapter: ScrapResourceParserProvider,
        curriculum_hierarchy_mapper_provider: CurriculumHierarchyMapperProvider,
        downloader_provider: DownloaderProvider,
    ):
        self.repository_provider_adapter = repository_provider_adapter
        self.resource_parser_provider_adapter = resource_parser_provider_adapter
        self.curriculum_hierarchy_mapper_provider = curriculum_hierarchy_mapper_provider
        self.downloader_provider = downloader_provider

    async def execute(self, refresh: bool = False) -> None:
        logger.info("Starting ingestion of curriculum data...")

        root_node = Node(
            url=_ROOT_URL,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.CURRICULUM,
        )

        async for node in self._navigator(root_node):
            logger.info(f"Ingesting curriculum data for {node.url}")

    async def _navigator(
        self, node: Node, refresh: bool = False, parent_id: Optional[int] = None
    ) -> AsyncGenerator[Node, Any]:

        # repository = self.repository_provider_adapter.get_repository(node.level)
        cache, resource = await self.__get_resource(node, refresh)
        parser = self.resource_parser_provider_adapter.get_parser(node.hierarchy)

        model, children = await parser.parse(resource, parent_id=parent_id)

        logger.info(f"Ingesting curriculum data for {resource}")

        yield node

    async def __get_resource(
        self, node: Node, refresh: bool = False
    ) -> Tuple[bool, ScrapResource[Any]]:
        repository = self.repository_provider_adapter.get_repository(node.hierarchy)
        cache_node = await repository.find_by_url(node.url) if not refresh else None
        if cache_node is None:
            downloader = self.downloader_provider.get_downloader(node.type)
            return False, await downloader.download(node.url)

        mapper = self.curriculum_hierarchy_mapper_provider.get_mapper(node.hierarchy)
        node = mapper.to_domain_node(cache_node)
        return True, ScrapResource(url=node.url, type=node.type, content=node.content)
