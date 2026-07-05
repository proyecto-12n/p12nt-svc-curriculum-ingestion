from domain.model.study_program_ref import StudyProgramRef
from infrastructure.adapter.inbound.web.dto.study_program_ref_response import (
    StudyProgramRefResponse,
)
from infrastructure.models.study_program_ref import (
    StudyProgramRef as SqlStudyProgramRef,
)


class TestStudyProgramRefResponse:
    def test_given_domain_model_when_from_domain_then_returns_response_fields(self):
        model = StudyProgramRef(
            id=1, grade_level_id=2, url="url", title="title", content="html"
        )

        response = StudyProgramRefResponse.from_domain(model)

        assert response.id == 1
        assert response.url == "url"
        assert response.title == "title"
        assert response.grade_level_id == 2

    def test_given_sql_model_when_from_domain_then_maps_parent_id(self):
        model = SqlStudyProgramRef(
            id=1, parent_id=2, url="url", title="title", content="html"
        )

        response = StudyProgramRefResponse.from_domain(model)

        assert response.grade_level_id == 2
