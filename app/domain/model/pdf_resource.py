# -*- coding: utf-8 -*-
"""
NextProject © 2026
"""

from dataclasses import dataclass


@dataclass
class PDFResource:
    content: bytes
    source_name: str = "unknown.pdf"
