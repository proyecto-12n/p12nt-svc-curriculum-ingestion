# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from app.infrastructure.adapter.outbound.http.parser.base_html_parser import (
    BaseHTMLParser,
)


class GradeHTMLParser(BaseHTMLParser):
    def _should_include_link(self, href: str) -> bool:
        return "/grado/" in href
