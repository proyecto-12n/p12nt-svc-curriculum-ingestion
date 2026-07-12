# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol


class IngestCurriculumUseCase(Protocol):
    async def execute(
        self,
        refresh: bool = False,
        ignore_pdf_resources: bool = False,
        reprocess_titles: bool = False,
    ) -> None:
        """Starts the ingestion process to scrape curriculum.cl/curriculum

        If a edge is already present in the database, it skips fetching it unless refresh is True.
        If ignore_pdf_resources is True, it skips PDF resources.
        If reprocess_titles is True, it reparses and saves titles using cached content.
        If any extraction fails, logs the error and skips the edge/branch.
        """
        ...
