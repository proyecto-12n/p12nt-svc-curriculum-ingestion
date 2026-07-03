# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
import logging
from typing import Any, Callable, List, Tuple

from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.domain.port.outbound import DownloaderProvider

logger = logging.getLogger(__name__)

_DEFAULT_TITLES = {"Modality", "Subject", "GradeLevel"}


class CurriculumNodeResolver:
    def __init__(self, downloader_provider: DownloaderProvider):
        self.downloader_provider = downloader_provider

    @staticmethod
    def absolute_url(url: str) -> str:
        if not url.startswith("http"):
            return "https://www.curriculumnacional.cl" + url
        return url

    def download_content(self, url: str, res_type: ResourceType) -> Node[Any]:
        downloader = self.downloader_provider.get_downloader(res_type)
        node_res = asyncio.run(downloader.download(url, timeout=10.0))
        if isinstance(node_res, Node):
            return node_res
        return Node(url=url, type=res_type, content=node_res)

    def resolve_node(
        self,
        url: str,
        resource_type: ResourceType,
        find_fn: Callable[[], Any],
        save_fn: Callable[[Any], Any],
        parser: Any,
        parent_id: int,
        title_hint: str = None,
        refresh: bool = False,
    ) -> Tuple[Any, List[Node]]:
        abs_url = self.absolute_url(url)
        entity = find_fn()

        if entity and not refresh:
            stored_node = Node(
                url=entity.url, type=resource_type, content=entity.content
            )
            _, children = parser.parse(stored_node, parent_id)
            logger.debug(
                f"Found existing {type(entity).__name__}: {getattr(entity, 'title', entity.url)}"
            )
            return entity, children

        node_data = self.download_content(abs_url, resource_type)
        model, children = parser.parse(node_data, parent_id)

        if title_hint and hasattr(model, "title") and model.title in _DEFAULT_TITLES:
            model.title = title_hint

        entity = save_fn(model)
        logger.info(
            f"Saved {type(entity).__name__}: {getattr(entity, 'title', entity.url)}"
        )
        return entity, children
