# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from os import path
from typing import AsyncGenerator, Any, Optional
from urllib.parse import unquote, urlparse

from domain.model import ResourceType, CurriculumHierarchyType
from domain.model.edge import Edge
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser import (
    ScrapResourceParser,
)


class StudyProgramScrapResourceParser(ScrapResourceParser[bytes]):
    async def get_children(
        self, resource: ScrapResource[bytes]
    ) -> AsyncGenerator[Edge[bytes], Any]:
        if False:
            yield

    async def get_edge(self, resource: ScrapResource[bytes]) -> Edge[bytes]:

        title = await self.__extract_title(resource)

        return Edge(
            url=resource.url,
            type=ResourceType.PDF,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
            title=title,
            content=resource.content,
        )

    async def get_title(self, resource: ScrapResource[bytes]) -> Optional[str]:
        return await self.__extract_title(resource)

    @staticmethod
    async def __extract_title(resource: ScrapResource[bytes]) -> Optional[str]:
        try:
            from io import BytesIO
            import pymupdf

            with pymupdf.Document(
                stream=BytesIO(resource.content), filetype="pdf"
            ) as doc:
                title = (doc.metadata or {}).get("title", "")
                if title and title.strip():
                    return title.strip()
        except Exception:
            pass

        filename = unquote(path.basename(urlparse(resource.url).path))
        return path.splitext(filename)[0] if filename else ""
