# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from datetime import datetime
import logging
from typing import Any, Callable, List, Tuple

from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.domain.model.study_program import StudyProgram
from app.domain.port.inbound.ingest_curriculum_use_case import IngestCurriculumUseCase
from app.domain.port.outbound.curriculum_repository import CurriculumRepository
from app.domain.port.outbound.downloader_provider import DownloaderProvider
from app.infrastructure.util.id_generator import generate_id

from infrastructure.adapter.outbound.http.parser.impl.curriculum_node_parser import (
    CurriculumNodeParser,
)
from infrastructure.adapter.outbound.http.parser.impl.grade_level_node_parser import (
    GradeLevelNodeParser,
)
from infrastructure.adapter.outbound.http.parser.impl.modality_node_parser import (
    ModalityNodeParser,
)
from infrastructure.adapter.outbound.http.parser.impl.study_program_node_parser import (
    StudyProgramNodeParser,
)
from infrastructure.adapter.outbound.http.parser.impl.study_program_ref_node_parser import (
    StudyProgramRefNodeParser,
)
from infrastructure.adapter.outbound.http.parser.impl.subject_node_parser import (
    SubjectNodeParser,
)

logger = logging.getLogger(__name__)

_DEFAULT_TITLES = {"Modality", "Subject", "GradeLevel"}
_ROOT_URL = "https://www.curriculumnacional.cl/curriculum"


class IngestCurriculumUseCaseImpl(IngestCurriculumUseCase):
    def __init__(
        self,
        repository: CurriculumRepository,
        downloader_provider: DownloaderProvider,
    ):
        self.repository = repository
        self.downloader_provider = downloader_provider

    @staticmethod
    def _absolute_url(url: str) -> str:
        if not url.startswith("http"):
            return "https://www.curriculumnacional.cl" + url
        return url

    def _download_content(self, url: str, res_type: ResourceType) -> Node[Any]:
        downloader = self.downloader_provider.get_downloader(res_type)
        node_res = asyncio.run(downloader.download(url, timeout=10.0))
        if isinstance(node_res, Node):
            return node_res
        return Node(url=url, type=res_type, content=node_res)

    def _resolve_node(
        self,
        url: str,
        resource_type: ResourceType,
        find_fn: Callable[[], Any],
        save_fn: Callable[[Any], Any],
        parser: Any,
        parent_id: int,
        title_hint: str = None,
    ) -> Tuple[Any, List[Node]]:
        abs_url = self._absolute_url(url)
        entity = find_fn()

        if entity:
            stored_node = Node(
                url=entity.url, type=resource_type, content=entity.content
            )
            _, children = parser.parse(stored_node, parent_id)
            logger.debug(
                f"Found existing {type(entity).__name__}: {getattr(entity, 'title', entity.url)}"
            )
            return entity, children

        node_data = self._download_content(abs_url, resource_type)
        model, children = parser.parse(node_data, parent_id)

        if title_hint and hasattr(model, "title") and model.title in _DEFAULT_TITLES:
            model.title = title_hint

        entity = save_fn(model)
        logger.info(
            f"Saved {type(entity).__name__}: {getattr(entity, 'title', entity.url)}"
        )
        return entity, children

    def _resolve_study_program(self, prog_node: Node, program_ref: Any):
        prog_url = self._absolute_url(prog_node.url)
        program = self.repository.find_study_program_by_url(prog_node.url)
        if program:
            return

        try:
            prog_node_data = self._download_content(prog_url, prog_node.type)
            prog_parser = StudyProgramNodeParser()
            program_model, _ = prog_parser.parse(
                prog_node_data,
                program_ref.id,
            )
            program = self.repository.save_study_program(program_model)
            logger.info(f"Saved StudyProgram: {program.url}")
        except Exception as e:
            logger.error(
                f"Failed to download/process study program {prog_node.url}: {e}"
            )
            program_model = StudyProgram(
                id=generate_id(prog_node.url),
                study_program_ref_id=program_ref.id,
                title=prog_node.title or "",
                url=prog_node.url,
                content=b"",
                checksum="",
                extracted_at=datetime.now(),
            )
            self.repository.save_study_program(program_model)
            logger.info(f"Saved StudyProgram (failed download): {prog_node.url}")

    def execute(self) -> None:
        logger.info("Starting ingestion of curriculum data...")

        curriculum, modality_nodes = self._resolve_node(
            url=_ROOT_URL,
            resource_type=ResourceType.HTML,
            find_fn=lambda: self.repository.find_curriculum_by_url(_ROOT_URL),
            save_fn=self.repository.save_curriculum,
            parser=CurriculumNodeParser(),
            parent_id=0,
        )

        for mod_node in modality_nodes:
            try:
                modality, subject_nodes = self._resolve_node(
                    url=mod_node.url,
                    resource_type=ResourceType.HTML,
                    find_fn=lambda: self.repository.find_modality_by_url(mod_node.url),
                    save_fn=self.repository.save_modality,
                    parser=ModalityNodeParser(),
                    parent_id=curriculum.id,
                    title_hint=mod_node.title,
                )
            except Exception as e:
                logger.error(f"Failed to resolve modality node {mod_node.url}: {e}")
                continue

            for sub_node in subject_nodes[:3]:
                try:
                    subject, grade_nodes = self._resolve_node(
                        url=sub_node.url,
                        resource_type=ResourceType.HTML,
                        find_fn=lambda: (
                            self.repository.find_subject_by_title_and_modality(
                                sub_node.title, modality.id
                            )
                        ),
                        save_fn=self.repository.save_subject,
                        parser=SubjectNodeParser(),
                        parent_id=modality.id,
                        title_hint=sub_node.title,
                    )
                except Exception as e:
                    logger.error(f"Failed to resolve subject node {sub_node.url}: {e}")
                    continue

                for grade_node in grade_nodes[:2]:
                    try:
                        grade, ref_nodes = self._resolve_node(
                            url=grade_node.url,
                            resource_type=ResourceType.HTML,
                            find_fn=lambda: (
                                self.repository.find_grade_level_by_title_and_subject(
                                    grade_node.title, subject.id
                                )
                            ),
                            save_fn=self.repository.save_grade_level,
                            parser=GradeLevelNodeParser(),
                            parent_id=subject.id,
                            title_hint=grade_node.title,
                        )
                    except Exception as e:
                        logger.error(
                            f"Failed to resolve grade level node {grade_node.url}: {e}"
                        )
                        continue

                    for ref_node in ref_nodes:
                        try:
                            program_ref, prog_nodes = self._resolve_node(
                                url=ref_node.url,
                                resource_type=ref_node.type,
                                find_fn=lambda: (
                                    self.repository.find_study_program_ref_by_url(
                                        ref_node.url
                                    )
                                ),
                                save_fn=self.repository.save_study_program_ref,
                                parser=StudyProgramRefNodeParser(),
                                parent_id=grade.id,
                            )
                        except Exception as e:
                            logger.error(
                                f"Failed to resolve study program ref node {ref_node.url}: {e}"
                            )
                            continue

                        for prog_node in prog_nodes:
                            self._resolve_study_program(prog_node, program_ref)

        logger.info("Ingestion completed successfully.")
