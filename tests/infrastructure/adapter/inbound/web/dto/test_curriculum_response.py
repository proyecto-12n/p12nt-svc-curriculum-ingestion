from domain.model.curriculum import Curriculum
from infrastructure.adapter.inbound.web.dto.curriculum_response import (
    CurriculumResponse,
)


class TestCurriculumResponse:
    def test_given_domain_model_when_from_domain_then_returns_response_fields(self):
        model = Curriculum(id=1, url="url", title="title", content="html")

        response = CurriculumResponse.from_domain(model)

        assert response.id == 1
        assert response.url == "url"
        assert response.title == "title"
        assert response.content == "html"
