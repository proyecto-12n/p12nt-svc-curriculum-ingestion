from domain.model.grade_level import GradeLevel
from infrastructure.adapter.inbound.web.dto.grade_level_response import (
    GradeLevelResponse,
)
from infrastructure.models.grade_level import GradeLevel as SqlGradeLevel


class TestGradeLevelResponse:
    def test_given_domain_model_when_from_domain_then_returns_response_fields(self):
        model = GradeLevel(id=1, subject_id=2, url="url", title="title", content="html")

        response = GradeLevelResponse.from_domain(model)

        assert response.id == 1
        assert response.url == "url"
        assert response.title == "title"
        assert response.subject_id == 2

    def test_given_sql_model_when_from_domain_then_maps_parent_id(self):
        model = SqlGradeLevel(
            id=1, parent_id=2, url="url", title="title", content="html"
        )

        response = GradeLevelResponse.from_domain(model)

        assert response.subject_id == 2
