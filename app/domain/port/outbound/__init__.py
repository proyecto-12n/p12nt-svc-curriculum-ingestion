# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from domain.port.outbound.content_downloader import ContentDownloader
from domain.port.outbound.downloader_provider import DownloaderProvider
from domain.port.outbound.curriculum_hierarchy_repository import (
    CurriculumHierarchyRepository,
)
from domain.port.outbound.curriculum_hierarchy_repository_provider import (
    CurriculumHierarchyRepositoryProvider,
)
from domain.port.outbound.curriculum_hierarchy_mapper import (
    CurriculumHierarchyMapper,
)
from domain.port.outbound.curriculum_hierarchy_mapper_provider import (
    CurriculumHierarchyMapperProvider,
)
from domain.port.outbound.scrap_resource_parser_provider import (
    ScrapResourceParserProvider,
)
from domain.port.outbound.scrap_resource_parser import ScrapResourceParser
from domain.port.outbound.pdf_converter import PDFConverter
from domain.port.outbound.pdf_converter_provider import PDFConverterProvider

__all__ = [
    "ContentDownloader",
    "DownloaderProvider",
    "ScrapResourceParserProvider",
    "ScrapResourceParser",
    "PDFConverter",
    "PDFConverterProvider",
    "CurriculumHierarchyRepository",
    "CurriculumHierarchyRepositoryProvider",
    "CurriculumHierarchyMapper",
    "CurriculumHierarchyMapperProvider",
]
