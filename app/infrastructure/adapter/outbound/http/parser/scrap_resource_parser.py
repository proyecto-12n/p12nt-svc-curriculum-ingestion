# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Tuple, Any, TypeVar, Protocol, List

from domain.model.node import Node
from domain.model.scrap_resource import ScrapResource

T = TypeVar("T")


class ScrapResourceParser(Protocol[T]):
    async def parse(
        self,
        node: ScrapResource[T],
        parent_id: int,
    ) -> Tuple[Any, List[Node]]:
        """
        Parses the downloaded content of a node.
        Returns a tuple of (level_model, list_of_nodes_to_resolve).
        """
        ...
