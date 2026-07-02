# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Any
from app.domain.model.curriculum_node_type import CurriculumNodeType


class NodeParserProvider(Protocol):
    def get_parser(self, discriminator: CurriculumNodeType) -> Any:
        """
        Retrieves a NodeParser implementation matching the CurriculumNodeType discriminator.
        """
        ...
