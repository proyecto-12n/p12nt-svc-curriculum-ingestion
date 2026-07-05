# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from domain.model.resource_type import ResourceType
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from infrastructure.models.curriculum import Curriculum as SqlCurriculum
from infrastructure.mapper.impl.curriculum_mapper import CurriculumMapper


def test_to_domain_node_mapping():
    now = datetime.now(timezone.utc)
    sql_curr = SqlCurriculum(
        id=123,
        url="https://www.curriculumnacional.cl/curriculum",
        title="Test Title",
        content="Test Content HTML",
        extracted_at=now,
    )

    mapper = CurriculumMapper()
    edge = mapper.to_edge(sql_curr)

    assert edge.url == "https://www.curriculumnacional.cl/curriculum"
    assert edge.type == ResourceType.HTML
    assert edge.hierarchy == CurriculumHierarchyType.CURRICULUM
    assert edge.title == "Test Title"
    assert edge.content == "Test Content HTML"
