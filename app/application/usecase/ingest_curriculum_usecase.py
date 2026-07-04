# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import logging
from typing import Any, AsyncGenerator, Tuple

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
            level=CurriculumHierarchyType.CURRICULUM,
        )

        async for node in self._navigator(root_node):
            logger.info(f"Ingesting curriculum data for {node.url}")

    async def _navigator(
        self, node: Node, refresh: bool = False
    ) -> AsyncGenerator[Node, Any]:

        # repository = self.repository_provider_adapter.get_repository(node.level)
        aux_node = await self.__get_resource(node, refresh)

        logger.info(f"Ingesting curriculum data for {aux_node}")

        yield node

    async def __get_resource(
        self, node: Node, refresh: bool = False
    ) -> Tuple[bool, ScrapResource[Any]]:
        repository = self.repository_provider_adapter.get_repository(node.level)
        cache_node = await repository.find_by_url(node.url) if not refresh else None
        if cache_node is None:
            downloader = self.downloader_provider.get_downloader(node.type)
            return await False, downloader.download(node.url)

        return True, cache_node

        """
        curriculum, modality_nodes = await self.node_resolver.resolve_node(
            url=_ROOT_URL,
            resource_type=ResourceType.HTML,
            find_fn=lambda: self.curriculum_repository.find_by_url(_ROOT_URL),
            save_fn=self.curriculum_repository.save,
            parser=CurriculumNodeParser(),
            parent_id=0,
            refresh=refresh,
        )

        for mod_node in modality_nodes:
            try:
                modality, subject_nodes = await self.node_resolver.resolve_node(
                    url=mod_node.url,
                    resource_type=ResourceType.HTML,
                    find_fn=lambda: self.modality_repository.find_by_url(
                        self.node_resolver.absolute_url(mod_node.url)
                    ),
                    save_fn=self.modality_repository.save,
                    parser=ModalityNodeParser(),
                    parent_id=curriculum.id,
                    title_hint=mod_node.title,
                    refresh=refresh,
                )
            except Exception as e:
                logger.error(f"Failed to resolve modality node {mod_node.url}: {e}")
                continue

            for sub_node in subject_nodes[:3]:
                try:
                    subject, grade_nodes = await self.node_resolver.resolve_node(
                        url=sub_node.url,
                        resource_type=ResourceType.HTML,
                        find_fn=lambda: (
                            self.subject_repository.find_subject_by_title_and_modality(
                                sub_node.title, modality.id
                            )
                        ),
                        save_fn=self.subject_repository.save,
                        parser=SubjectNodeParser(),
                        parent_id=modality.id,
                        title_hint=sub_node.title,
                        refresh=refresh,
                    )
                except Exception as e:
                    logger.error(f"Failed to resolve subject node {sub_node.url}: {e}")
                    continue

                for grade_node in grade_nodes[:2]:
                    try:
                        grade, ref_nodes = await self.node_resolver.resolve_node(
                            url=grade_node.url,
                            resource_type=ResourceType.HTML,
                            find_fn=lambda: (
                                self.grade_level_repository.find_grade_level_by_title_and_subject(
                                    grade_node.title, subject.id
                                )
                            ),
                            save_fn=self.grade_level_repository.save,
                            parser=GradeLevelNodeParser(),
                            parent_id=subject.id,
                            title_hint=grade_node.title,
                            refresh=refresh,
                        )
                    except Exception as e:
                        logger.error(
                            f"Failed to resolve grade level node {grade_node.url}: {e}"
                        )
                        continue

                    for ref_node in ref_nodes:
                        try:
                            (
                                program_ref,
                                prog_nodes,
                            ) = await self.node_resolver.resolve_node(
                                url=ref_node.url,
                                resource_type=ref_node.type,
                                find_fn=lambda: (
                                    self.study_program_ref_repository.find_by_url(
                                        self.node_resolver.absolute_url(ref_node.url)
                                    )
                                ),
                                save_fn=self.study_program_ref_repository.save,
                                parser=StudyProgramRefNodeParser(),
                                parent_id=grade.id,
                                refresh=refresh,
                            )
                        except Exception as e:
                            logger.error(
                                f"Failed to resolve study program ref node {ref_node.url}: {e}"
                            )
                            continue

                        for prog_node in prog_nodes:
                            await self.study_program_resolver.resolve_study_program(
                                prog_node, program_ref, refresh=refresh
                            )

        logger.info("Ingestion completed successfully.")
        """
