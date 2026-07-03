# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol


class IngestCurriculumUseCase(Protocol):
    def execute(self, refresh: bool = False) -> None:
        """Starts the ingestion process to scrape curriculum.cl/curriculum

        If a node is already present in the database, it skips fetching it unless refresh is True.
        If any extraction fails, logs the error and skips the node/branch.
        """
        pass
