# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol


class IngestCurriculumUseCase(Protocol):
    async def execute(self, refresh: bool = False) -> None:
        """Starts the ingestion process to scrape curriculum.cl/curriculum

        If a edge is already present in the database, it skips fetching it unless refresh is True.
        If any extraction fails, logs the error and skips the edge/branch.
        """
        ...
