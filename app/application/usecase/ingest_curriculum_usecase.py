# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import logging
from dataclasses import replace
from typing import Tuple, Any
from urllib.parse import urljoin

from domain.model import (
    Edge,
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


class IngestCurriculumUseCaseImpl(IngestCurriculumUseCase):
    BASE_URL = "https://www.curriculumnacional.cl"
    ROOT_URL = "/curriculum"

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

        root_node = Edge(
            url=urljoin(
                IngestCurriculumUseCaseImpl.BASE_URL,
                IngestCurriculumUseCaseImpl.ROOT_URL,
            ),
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.CURRICULUM,
        )

        await self.__navigator(refresh, root_node)

    async def __navigator(self, refresh: bool, edge: Edge) -> None:
        assert isinstance(edge, Edge)

        cache, resource = await self.__get_resource(refresh, edge)
        parser = self.resource_parser_provider_adapter.get_parser(edge.hierarchy)

        if not cache:
            logger.info("Ingesting %s data for %s", edge.hierarchy.value, resource.url)

            repository = self.repository_provider_adapter.get_repository(edge.hierarchy)
            mapper = self.curriculum_hierarchy_mapper_provider.get_mapper(
                edge.hierarchy
            )

            aux_edge = replace(
                edge, title=await parser.get_title(resource), content=resource.content
            )

            await repository.save(mapper.to_model(aux_edge))

            logger.info("Save %s data for %s", edge.hierarchy.value, resource.url)

        async for child_raw in parser.get_children(resource):
            child = replace(
                child_raw,
                url=urljoin(IngestCurriculumUseCaseImpl.BASE_URL, child_raw.url),
                parent_url=edge.url,
            )

            await self.__navigator(refresh, child)

    async def __get_resource(
        self, refresh: bool, edge: Edge
    ) -> Tuple[bool, ScrapResource[Any]]:

        repository = self.repository_provider_adapter.get_repository(edge.hierarchy)
        cache_node = await repository.find_by_url(edge.url) if not refresh else None
        if cache_node is None:
            downloader = self.downloader_provider.get_downloader(edge.type)
            try:
                return False, await downloader.download(edge.url)
            except Exception:
                if edge.type != ResourceType.PDF:
                    raise
                logger.warning(
                    "PDF download failed for %s; saving empty content", edge.url
                )
                return (
                    False,
                    ScrapResource(url=edge.url, type=ResourceType.PDF, content=b""),
                )

        mapper = self.curriculum_hierarchy_mapper_provider.get_mapper(edge.hierarchy)
        edge = mapper.to_edge(cache_node)
        return True, ScrapResource(url=edge.url, type=edge.type, content=edge.content)
