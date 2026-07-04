# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime
import logging
from typing import Any

from domain.model.node import Node
from domain.model.study_program import StudyProgram
from domain.port.outbound import StudyProgramRepository
from application.usecase.curriculum_node_resolver import CurriculumNodeResolver
from infrastructure.adapter.outbound.http.parser.impl import StudyProgramNodeParser
from infrastructure.util.id_generator import generate_id

logger = logging.getLogger(__name__)


class StudyProgramResolver:
    def __init__(
        self,
        study_program_repository: StudyProgramRepository,
        node_resolver: CurriculumNodeResolver,
    ):
        self.study_program_repository = study_program_repository
        self.node_resolver = node_resolver

    def resolve_study_program(
        self, prog_node: Node, program_ref: Any, refresh: bool = False
    ) -> None:
        prog_url = self.node_resolver.absolute_url(prog_node.url)
        program = self.study_program_repository.find_study_program_by_url(prog_url)
        if program and not refresh:
            return

        try:
            prog_node_data = self.node_resolver.download_content(
                prog_url, prog_node.type
            )
            prog_parser = StudyProgramNodeParser()
            program_model, _ = prog_parser.parse(
                prog_node_data,
                program_ref.id,
            )
            program = self.study_program_repository.save_study_program(program_model)
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
            self.study_program_repository.save_study_program(program_model)
            logger.info(f"Saved StudyProgram (failed download): {prog_node.url}")
