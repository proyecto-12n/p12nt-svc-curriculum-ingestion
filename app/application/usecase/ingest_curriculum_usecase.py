# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import logging

from application.usecase.curriculum_node_resolver import CurriculumNodeResolver
from application.usecase.study_program_resolver import StudyProgramResolver
from domain.model.resource_type import ResourceType
from domain.port.inbound import IngestCurriculumUseCase
from domain.port.outbound import (
    SubjectRepository,
    GradeLevelRepository,
    StudyProgramRefRepository,
    StudyProgramRepository,
    DownloaderProvider,
)
from infrastructure.adapter.outbound.http.parser.impl import (
    CurriculumNodeParser,
    GradeLevelNodeParser,
    ModalityNodeParser,
    StudyProgramRefNodeParser,
    SubjectNodeParser,
)
from domain.model import Curriculum, Modality
from domain.port.outbound.knowledge_repository import KnowledgeRepository

logger = logging.getLogger(__name__)

_ROOT_URL = "https://www.curriculumnacional.cl/curriculum"


class IngestCurriculumUseCaseImpl(IngestCurriculumUseCase):
    def __init__(
            self,
            curriculum_repository: KnowledgeRepository[Curriculum],
            modality_repository: KnowledgeRepository[Modality],
            subject_repository: SubjectRepository,
            grade_level_repository: GradeLevelRepository,
            study_program_ref_repository: StudyProgramRefRepository,
            study_program_repository: StudyProgramRepository,
            downloader_provider: DownloaderProvider,
            node_resolver: CurriculumNodeResolver = None,
            study_program_resolver: StudyProgramResolver = None,
    ):
        self.curriculum_repository = curriculum_repository
        self.modality_repository = modality_repository
        self.subject_repository = subject_repository
        self.grade_level_repository = grade_level_repository
        self.study_program_ref_repository = study_program_ref_repository
        self.study_program_repository = study_program_repository
        self.downloader_provider = downloader_provider

        # Setup resolvers (maintaining backward compatibility)
        self.node_resolver = node_resolver or CurriculumNodeResolver(
            downloader_provider=downloader_provider
        )
        self.study_program_resolver = study_program_resolver or StudyProgramResolver(
            study_program_repository=study_program_repository,
            node_resolver=self.node_resolver,
        )

    def execute(self, refresh: bool = False) -> None:
        logger.info("Starting ingestion of curriculum data...")

        curriculum, modality_nodes = self.node_resolver.resolve_node(
            url=_ROOT_URL,
            resource_type=ResourceType.HTML,
            find_fn=lambda: self.curriculum_repository.find_by_url(
                _ROOT_URL
            ),
            save_fn=self.curriculum_repository.save,
            parser=CurriculumNodeParser(),
            parent_id=0,
            refresh=refresh,
        )

        for mod_node in modality_nodes:
            try:
                modality, subject_nodes = self.node_resolver.resolve_node(
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
                    subject, grade_nodes = self.node_resolver.resolve_node(
                        url=sub_node.url,
                        resource_type=ResourceType.HTML,
                        find_fn=lambda: (
                            self.subject_repository.find_subject_by_title_and_modality(
                                sub_node.title, modality.id
                            )
                        ),
                        save_fn=self.subject_repository.save_subject,
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
                        grade, ref_nodes = self.node_resolver.resolve_node(
                            url=grade_node.url,
                            resource_type=ResourceType.HTML,
                            find_fn=lambda: (
                                self.grade_level_repository.find_grade_level_by_title_and_subject(
                                    grade_node.title, subject.id
                                )
                            ),
                            save_fn=self.grade_level_repository.save_grade_level,
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
                            program_ref, prog_nodes = self.node_resolver.resolve_node(
                                url=ref_node.url,
                                resource_type=ref_node.type,
                                find_fn=lambda: (
                                    self.study_program_ref_repository.find_study_program_ref_by_url(
                                        self.node_resolver.absolute_url(ref_node.url)
                                    )
                                ),
                                save_fn=self.study_program_ref_repository.save_study_program_ref,
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
                            self.study_program_resolver.resolve_study_program(
                                prog_node, program_ref, refresh=refresh
                            )

        logger.info("Ingestion completed successfully.")
