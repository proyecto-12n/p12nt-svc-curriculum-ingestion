# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from bs4 import BeautifulSoup


class HtmlScrapResourceTitleStrategy:
    @staticmethod
    def extract(soup: BeautifulSoup) -> str:
        h1_tag = soup.find("h1")
        assert h1_tag
        return h1_tag.get_text(strip=True)
