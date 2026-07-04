# -*- coding: utf-8 -*-
"""
NextProject © 2026
"""

from typing import Protocol
from domain.model.study_program import StudyProgram


class StudyProgramAgentParser(Protocol):
    async def run(self, content: str) -> StudyProgram:
        """
        Parses educational content and extracts study program details using an LLM.
        """
        ...
