# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import hashlib
import logging
from datetime import datetime
from app.domain.port.inbound.ingest_curriculum_use_case import IngestCurriculumUseCase
from app.domain.port.outbound.curriculum_repository import CurriculumRepository
from app.domain.port.outbound.curriculum_scraper import CurriculumScraper
from app.domain.port.outbound.downloader_provider import DownloaderProvider
from app.domain.model.modality import Modality
from app.domain.model.subject import Subject
from app.domain.model.grade_level import GradeLevel
from app.domain.model.study_program_ref import StudyProgramRef
from app.domain.model.study_program import StudyProgram
from app.domain.model.resource_type import ResourceType

logger = logging.getLogger(__name__)


class IngestCurriculumUseCaseImpl(IngestCurriculumUseCase):
    def __init__(
        self,
        repository: CurriculumRepository,
        scraper: CurriculumScraper,
        downloader_provider: DownloaderProvider,
    ):
        self.repository = repository
        self.scraper = scraper
        self.downloader_provider = downloader_provider

    def execute(self, force_mock: bool = False) -> None:
        logger.info("Starting ingestion of curriculum data...")

        # 1. Fetch Modalities
        try:
            modalities_data = self.scraper.fetch_modalities()
        except Exception as e:
            logger.error(f"Failed to fetch modalities: {e}")
            return

        for m_data in modalities_data:
            # 2. Priority: check DB before HTTP request
            modality = self.repository.find_modality_by_url(m_data["url"])
            if not modality:
                modality = Modality(title=m_data["title"], url=m_data["url"])
                modality = self.repository.save_modality(modality)
                logger.info(f"Saved Modality: {modality.title}")

            # 3. Fetch Subjects
            try:
                subjects_data = self.scraper.fetch_subjects(modality.url)
            except Exception as e:
                logger.error(
                    f"Failed to fetch subjects for modality {modality.title}: {e}"
                )
                continue

            for s_data in subjects_data:
                subject = self.repository.find_subject_by_title_and_modality(
                    s_data["title"], modality.id
                )
                if not subject:
                    subject = Subject(title=s_data["title"], modality_id=modality.id)
                    subject = self.repository.save_subject(subject)
                    logger.info(
                        f"Saved Subject: {subject.title} under {modality.title}"
                    )

                # 4. Fetch Grades
                try:
                    grades_data = self.scraper.fetch_grades(
                        s_data.get("url", modality.url)
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to fetch grades for subject {subject.title}: {e}"
                    )
                    continue

                for g_data in grades_data:
                    grade = self.repository.find_grade_level_by_title_and_subject(
                        g_data["title"], subject.id
                    )
                    if not grade:
                        grade = GradeLevel(title=g_data["title"], subject_id=subject.id)
                        grade = self.repository.save_grade_level(grade)
                        logger.info(
                            f"Saved GradeLevel: {grade.title} under {subject.title}"
                        )

                    # 5. Fetch StudyProgramRef
                    try:
                        ref_data = self.scraper.fetch_program_ref(
                            g_data.get("url", modality.url)
                        )
                        ref_url = ref_data["url"]
                    except Exception as e:
                        logger.error(
                            f"Failed to fetch program ref for grade {grade.title}: {e}"
                        )
                        continue

                    program_ref = self.repository.find_study_program_ref_by_url(ref_url)
                    if not program_ref:
                        program_ref = StudyProgramRef(
                            grade_level_id=grade.id, url=ref_url
                        )
                        program_ref = self.repository.save_study_program_ref(
                            program_ref
                        )
                        logger.info(f"Saved StudyProgramRef: {ref_url}")

                    # 6. Fetch StudyProgram content
                    program = self.repository.find_study_program_by_url(ref_url)
                    if not program:
                        # Attempt to download and format content
                        status = "PENDING"
                        error_log = None
                        content = b""
                        md5 = ""

                        try:
                            res_type = (
                                ResourceType.PDF
                                if ".pdf" in ref_url.lower()
                                else ResourceType.HTML
                            )
                            downloader = self.downloader_provider.get_downloader(
                                res_type
                            )
                            import asyncio

                            downloaded = asyncio.run(downloader.download(ref_url))
                            if isinstance(downloaded, str):
                                raw_content = downloaded.encode("utf-8")
                            else:
                                raw_content = downloaded

                            # Formating as Canonical Markdown structure (traceability metadata header)
                            metadata_header = (
                                f"---\n"
                                f"source_url: {ref_url}\n"
                                f"extracted_at: {datetime.utcnow().isoformat()}\n"
                                f"version: 1.0\n"
                                f"modality: {modality.title}\n"
                                f"subject: {subject.title}\n"
                                f"grade_level: {grade.title}\n"
                                f"---\n\n"
                            ).encode("utf-8")

                            # Prepend metadata to the canonical markdown content
                            content = metadata_header + raw_content
                            md5 = hashlib.md5(content).hexdigest()
                        except Exception as e:
                            logger.error(
                                f"Failed to download/process study program {ref_url}: {e}"
                            )
                            status = "PENDING"  # Store in PENDING for the IA Parser even on failure (RF-001)
                            error_log = str(e)

                        program = StudyProgram(
                            url=ref_url,
                            study_program_ref_id=program_ref.id,
                            md5sum=md5,
                            content=content,
                            status=status,
                            error_log=error_log,
                        )
                        self.repository.save_study_program(program)
                        logger.info(
                            f"Saved StudyProgram: {ref_url} with status {status}"
                        )
