# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol


class IngestCurriculumUseCase(Protocol):
    def execute(self, force_mock: bool = False) -> None:
        """Starts the ingestion process to scrape curriculum.cl/curriculum

        If a node is already present in the database, it skips fetching it.
        If any extraction fails, logs the error and registers the node in a 'PENDING' or 'ERROR' state.
        """
        pass
