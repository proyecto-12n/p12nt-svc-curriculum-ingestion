# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from hashlib import sha256
from datetime import datetime
from os import path
from typing import Tuple, List
from urllib.parse import urlparse

from domain.model import StudyProgram
from domain.model.node import Node
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser import (
    ScrapResourceParser,
)
from infrastructure.util.id_generator import generate_id


class StudyProgramScrapResourceParser(ScrapResourceParser[bytes]):
    async def parse(
        self,
        resource: ScrapResource[bytes],
        parent_id: int,
    ) -> Tuple[StudyProgram, List[Node]]:
        checksum = sha256(resource.content)
        title = self._calculate_title(resource)

        return StudyProgram(
            id=generate_id(resource.url),
            study_program_ref_id=parent_id,
            url=resource.url,
            title=title,
            content=resource.content,
            checksum=checksum.hexdigest(),
            extracted_at=datetime.now(),
        ), []

    def _calculate_title(self, node: Node[bytes]) -> str:
        parsed_url = urlparse(node.url)
        filename = path.basename(parsed_url.path)

        title = None
        try:
            from io import BytesIO
            import pymupdf

            with pymupdf.Document(stream=BytesIO(node.content), filetype="pdf") as doc:
                metadata = doc.metadata
                if metadata:
                    title = metadata.get("title")
        except Exception:
            pass

        if not isinstance(title, str) or not title.strip():
            title, _ = path.splitext(filename) if filename else ("", "")
        else:
            title = title.strip()

        return title
