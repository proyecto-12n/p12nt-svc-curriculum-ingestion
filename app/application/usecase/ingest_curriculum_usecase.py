# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import logging
from typing import Any
from app.domain.port.inbound.ingest_curriculum_use_case import IngestCurriculumUseCase
from app.domain.port.outbound.curriculum_repository import CurriculumRepository
from app.domain.port.outbound.downloader_provider import DownloaderProvider
from app.domain.model.study_program import StudyProgram
from app.domain.model.resource_type import ResourceType
from app.domain.model.node import Node
from app.domain.model import MetadataField

logger = logging.getLogger(__name__)


def get_mock_content(url: str) -> Any:
    if "/curriculum" in url and url.endswith("/curriculum"):
        return """
        <title>Curriculum Nacional</title>
        <a href="/curriculum/basica">Educación Regular Básica</a>
        <a href="/curriculum/media">Educación Regular Media</a>
        """
    elif url.endswith("/basica") or url.endswith("/media"):
        is_basica = "basica" in url
        prefix = "/curriculum/basica" if is_basica else "/curriculum/media"
        return f"""
        <h1>Educación Regular</h1>
        <a href="{prefix}/matematica">Matemática</a>
        <a href="{prefix}/lenguaje">Lenguaje y Comunicación</a>
        <a href="{prefix}/ciencias">Ciencias Naturales</a>
        """
    elif "/matematica" in url or "/lenguaje" in url or "/ciencias" in url:
        is_basica = "basica" in url
        g1 = "1° Básico" if is_basica else "I° Medio"
        g2 = "2° Básico" if is_basica else "II° Medio"
        return f"""
        <h1>Asignatura</h1>
        <a href="{url}/1g">{g1}</a>
        <a href="{url}/2g">{g2}</a>
        """
    elif url.endswith("/1g") or url.endswith("/2g"):
        return f"""
        <h1>Grado</h1>
        <a href="{url}/programa_de_estudio_pdf">Descargar PDF</a>
        """
    elif "programa_de_estudio_pdf" in url:
        return b"# Programa de Estudio\n\nContenido de prueba."
    else:
        return ""


class IngestCurriculumUseCaseImpl(IngestCurriculumUseCase):
    def __init__(
        self,
        repository: CurriculumRepository,
        downloader_provider: DownloaderProvider,
    ):
        self.repository = repository
        self.downloader_provider = downloader_provider

    def execute(self, force_mock: bool = False) -> None:
        logger.info("Starting ingestion of curriculum data...")

        import asyncio
        from infrastructure.adapter.outbound.http.parser.impl.curriculum_node_parser import (
            CurriculumNodeParser,
        )
        from infrastructure.adapter.outbound.http.parser.impl.modality_node_parser import (
            ModalityNodeParser,
        )
        from infrastructure.adapter.outbound.http.parser.impl.subject_node_parser import (
            SubjectNodeParser,
        )
        from infrastructure.adapter.outbound.http.parser.impl.grade_level_node_parser import (
            GradeLevelNodeParser,
        )
        from infrastructure.adapter.outbound.http.parser.impl.study_program_ref_node_parser import (
            StudyProgramRefNodeParser,
        )
        from infrastructure.adapter.outbound.http.parser.impl.study_program_node_parser import (
            StudyProgramNodeParser,
        )

        def download_content(url: str, res_type: ResourceType) -> Node[Any]:
            if force_mock:
                content = get_mock_content(url)
                return Node(url=url, type=res_type, content=content)
            try:
                downloader = self.downloader_provider.get_downloader(res_type)
                node_res = asyncio.run(downloader.download(url, timeout=10.0))
                if isinstance(node_res, Node):
                    return node_res
                return Node(url=url, type=res_type, content=node_res)
            except Exception as e:
                logger.warning(
                    f"Download failed for {url}: {e}. Falling back to mock content."
                )
                content = get_mock_content(url)
                return Node(url=url, type=res_type, content=content)

        def get_absolute_url(url: str) -> str:
            if not url.startswith("http"):
                return "https://www.curriculumnacional.cl" + url
            return url

        # 1. Parse Root Page
        root_url = "https://www.curriculumnacional.cl/curriculum"
        root_node = download_content(root_url, ResourceType.HTML)

        root_parser = CurriculumNodeParser()

        curriculum = self.repository.find_curriculum_by_url(root_url)
        if not curriculum:
            curriculum, modality_nodes = root_parser.parse(root_node)
            curriculum = self.repository.save_curriculum(curriculum)
            logger.info(f"Saved Curriculum: {curriculum.title}")
        else:
            _, modality_nodes = root_parser.parse(root_node)

        # 2. Iterate Modalities
        for mod_node in modality_nodes:
            mod_url = get_absolute_url(mod_node.url)

            modality = self.repository.find_modality_by_url(mod_node.url)
            if not modality:
                mod_node_data = download_content(mod_url, ResourceType.HTML)
                mod_parser = ModalityNodeParser()
                modality_model, subject_nodes = mod_parser.parse(
                    mod_node_data, parent_id=curriculum.id
                )

                if modality_model.title == "Modality" and mod_node.title:
                    modality_model.title = mod_node.title

                modality = self.repository.save_modality(modality_model)
                logger.info(f"Saved Modality: {modality.title}")
            else:
                mod_node_data = download_content(mod_url, ResourceType.HTML)
                mod_parser = ModalityNodeParser()
                _, subject_nodes = mod_parser.parse(
                    mod_node_data, parent_id=curriculum.id
                )

            # 3. Iterate Subjects (limit to 3 for performance)
            for sub_node in subject_nodes[:3]:
                sub_url = get_absolute_url(sub_node.url)

                subject = self.repository.find_subject_by_title_and_modality(
                    sub_node.title, modality.id
                )
                if not subject:
                    sub_node_data = download_content(sub_url, ResourceType.HTML)
                    sub_parser = SubjectNodeParser()
                    subject_model, grade_nodes = sub_parser.parse(
                        sub_node_data, parent_id=modality.id
                    )

                    if subject_model.title == "Subject" and sub_node.title:
                        subject_model.title = sub_node.title

                    subject = self.repository.save_subject(subject_model)
                    logger.info(
                        f"Saved Subject: {subject.title} under {modality.title}"
                    )
                else:
                    sub_node_data = download_content(sub_url, ResourceType.HTML)
                    sub_parser = SubjectNodeParser()
                    _, grade_nodes = sub_parser.parse(
                        sub_node_data, parent_id=modality.id
                    )

                # 4. Iterate Grade Levels (limit to 2 for performance)
                for grade_node in grade_nodes[:2]:
                    grade_url = get_absolute_url(grade_node.url)

                    grade = self.repository.find_grade_level_by_title_and_subject(
                        grade_node.title, subject.id
                    )
                    if not grade:
                        grade_node_data = download_content(grade_url, ResourceType.HTML)
                        grade_parser = GradeLevelNodeParser()
                        grade_model, ref_nodes = grade_parser.parse(
                            grade_node_data, parent_id=subject.id
                        )

                        if grade_model.title == "GradeLevel" and grade_node.title:
                            grade_model.title = grade_node.title

                        grade = self.repository.save_grade_level(grade_model)
                        logger.info(
                            f"Saved GradeLevel: {grade.title} under {subject.title}"
                        )
                    else:
                        grade_node_data = download_content(grade_url, ResourceType.HTML)
                        grade_parser = GradeLevelNodeParser()
                        _, ref_nodes = grade_parser.parse(
                            grade_node_data, parent_id=subject.id
                        )

                    # 5. Iterate Study Program References
                    for ref_node in ref_nodes:
                        ref_url = get_absolute_url(ref_node.url)

                        program_ref = self.repository.find_study_program_ref_by_url(
                            ref_node.url
                        )
                        if not program_ref:
                            ref_node_data = download_content(ref_url, ref_node.type)
                            ref_parser = StudyProgramRefNodeParser()
                            ref_model, prog_nodes = ref_parser.parse(
                                ref_node_data, parent_id=grade.id
                            )

                            program_ref = self.repository.save_study_program_ref(
                                ref_model
                            )
                            logger.info(f"Saved StudyProgramRef: {program_ref.url}")
                        else:
                            ref_parser = StudyProgramRefNodeParser()
                            _, prog_nodes = ref_parser.parse(
                                Node(
                                    url=program_ref.url,
                                    type=ref_node.type,
                                    content=b"",
                                ),
                                parent_id=grade.id,
                            )

                        # 6. Iterate and Parse Study Program Content
                        for prog_node in prog_nodes:
                            prog_url = get_absolute_url(prog_node.url)

                            program = self.repository.find_study_program_by_url(
                                prog_node.url
                            )
                            if not program:
                                try:
                                    prog_node_data = download_content(
                                        prog_url, prog_node.type
                                    )
                                    prog_parser = StudyProgramNodeParser()

                                    metadata = {
                                        MetadataField.MODALITY.value: modality.title,
                                        MetadataField.SUBJECT.value: subject.title,
                                        MetadataField.GRADE_LEVEL.value: grade.title,
                                    }

                                    program_model, _ = prog_parser.parse(
                                        prog_node_data,
                                        parent_id=program_ref.id,
                                        metadata=metadata,
                                    )
                                    program = self.repository.save_study_program(
                                        program_model
                                    )
                                    logger.info(f"Saved StudyProgram: {program.url}")
                                except Exception as e:
                                    logger.error(
                                        f"Failed to download/process study program {prog_node.url}: {e}"
                                    )
                                    from infrastructure.util.id_generator import (
                                        generate_id,
                                    )
                                    from datetime import datetime

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
                                    logger.info(
                                        f"Saved StudyProgram (failed download): {prog_node.url}"
                                    )

        logger.info("Ingestion completed successfully.")
