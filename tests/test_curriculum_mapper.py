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
    node = mapper.to_domain_node(sql_curr)

    assert node.url == "https://www.curriculumnacional.cl/curriculum"
    assert node.type == ResourceType.HTML
    assert node.level == CurriculumHierarchyType.CURRICULUM
    assert node.title == "Test Title"
    assert node.content == "Test Content HTML"
