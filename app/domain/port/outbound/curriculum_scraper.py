# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, List, Dict, Any


class CurriculumScraper(Protocol):
    def fetch_modalities(self) -> List[Dict[str, Any]]:
        """Fetches modalities from the portal. Returns a list of dicts with title, url."""
        pass

    def fetch_subjects(self, modality_url: str) -> List[Dict[str, Any]]:
        """Fetches subjects for a given modality URL."""
        pass

    def fetch_grades(self, subject_url: str) -> List[Dict[str, Any]]:
        """Fetches grade levels for a given subject URL."""
        pass

    def fetch_program_ref(self, grade_url: str) -> Dict[str, Any]:
        """Fetches program download/view link URL for a grade."""
        pass

    def download_program_content(self, program_url: str) -> bytes:
        """Downloads the study program content/file."""
        pass
