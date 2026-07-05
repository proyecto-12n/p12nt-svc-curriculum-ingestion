from domain.model.subject import Subject
from infrastructure.adapter.inbound.web.dto.subject_response import SubjectResponse


class TestSubjectResponse:
    def test_given_domain_model_when_from_domain_then_returns_response_fields(self):
        model = Subject(id=1, modality_id=2, url="url", title="title", content="html")

        response = SubjectResponse.from_domain(model)

        assert response.id == 1
        assert response.url == "url"
        assert response.title == "title"
        assert response.modality_id == 2
