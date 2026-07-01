# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from html.parser import HTMLParser
from typing import List, Dict


class BaseHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: List[Dict[str, str]] = []
        self._current_tag = None
        self._current_attrs = {}
        self._temp_text = []

    def handle_starttag(self, tag, attrs):
        self._current_tag = tag
        self._current_attrs = dict(attrs)
        self._temp_text = []

    def handle_data(self, data):
        if self._current_tag in ["a", "span", "div", "h1", "h2", "h3", "h4"]:
            self._temp_text.append(data.strip())

    def handle_endtag(self, tag):
        if tag == "a" and "href" in self._current_attrs:
            href = self._current_attrs["href"]
            if self._should_include_link(href):
                text = " ".join(self._temp_text).strip()
                self.links.append({"text": text, "href": href})
        self._current_tag = None
        self._current_attrs = {}
        self._temp_text = []

    def _should_include_link(self, href: str) -> bool:
        return True
