from domain.model.curriculum_framework import CurriculumFramework
from infrastructure.adapter.inbound.web.dto.curriculum_framework_response import (
    CurriculumFrameworkResponse,
)
from infrastructure.models.curriculum_framework import (
    CurriculumFramework as SqlCurriculumFramework,
)


class TestCurriculumFrameworkResponse:
    def test_given_domain_model_when_from_domain_then_returns_response_fields(self):
        model = CurriculumFramework(
            id=1, curriculum_id=2, url="url", title="title", content="html"
        )

        response = CurriculumFrameworkResponse.from_domain(model)

        assert response.id == 1
        assert response.url == "url"
        assert response.title == "title"
        assert response.curriculum_id == 2

    def test_given_sql_model_when_from_domain_then_maps_parent_id(self):
        model = SqlCurriculumFramework(
            id=1, parent_id=2, url="url", title="title", content="html"
        )

        response = CurriculumFrameworkResponse.from_domain(model)

        assert response.curriculum_id == 2
