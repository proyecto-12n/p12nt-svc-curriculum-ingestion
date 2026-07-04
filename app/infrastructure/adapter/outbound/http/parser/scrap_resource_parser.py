# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Any, TypeVar, Protocol, AsyncGenerator

from domain.model.node import Node
from domain.model.scrap_resource import ScrapResource

T = TypeVar("T")


class ScrapResourceParser(Protocol[T]):
    async def get_node(self, resource: ScrapResource[T]) -> Node[T]: ...

    async def get_children(
        self, resource: ScrapResource[T]
    ) -> AsyncGenerator[Node[Any], Any]: ...
