# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from os import path
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup

from domain.model.scrap_resource import ScrapResource


class ScrapResourceTitleHelper:
    @staticmethod
    def extract_from_soup(soup: BeautifulSoup) -> str:
        h1_tag = soup.find("h1")
        assert h1_tag
        return h1_tag.get_text(strip=True)

    @staticmethod
    def extract_from_pdf(resource: ScrapResource[bytes]) -> str:
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
