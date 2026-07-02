# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Tuple, List, Any, Optional, TypeVar, Protocol
from app.domain.model.node import Node

T = TypeVar("T")


class NodeParser(Protocol[T]):
    def parse(
        self,
        node: Node[T],
        parent_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> Tuple[Any, List[Node]]:
        """
        Parses the downloaded content of a node.
        Returns a tuple of (level_model, list_of_nodes_to_resolve).
        """
        ...
