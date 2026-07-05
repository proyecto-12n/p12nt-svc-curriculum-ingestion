from domain.model.modality import Modality
from infrastructure.adapter.inbound.web.dto.modality_response import ModalityResponse


class TestModalityResponse:
    def test_given_domain_model_when_from_domain_then_returns_response_fields(self):
        model = Modality(
            id=1, curriculum_id=2, url="url", title="title", content="html"
        )

        response = ModalityResponse.from_domain(model)

        assert response.id == 1
        assert response.url == "url"
        assert response.title == "title"
        assert response.curriculum_id == 2
