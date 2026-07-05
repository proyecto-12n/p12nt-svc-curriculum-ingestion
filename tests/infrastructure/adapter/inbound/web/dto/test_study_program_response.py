import base64

from domain.model.study_program import StudyProgram
from infrastructure.adapter.inbound.web.dto.study_program_response import (
    StudyProgramResponse,
)
from infrastructure.models.study_program import StudyProgram as SqlStudyProgram


class TestStudyProgramResponse:
    def test_given_domain_model_when_from_domain_then_encodes_content_as_base64(self):
        model = StudyProgram(
            id=1,
            study_program_ref_id=2,
            url="url",
            title="title",
            content=b"pdf",
            checksum="checksum",
        )

        response = StudyProgramResponse.from_domain(model)

        assert response.study_program_ref_id == 2
        assert base64.b64decode(response.content) == b"pdf"
        assert response.checksum == "checksum"

    def test_given_sql_model_when_from_domain_then_maps_parent_id(self):
        model = SqlStudyProgram(
            id=1,
            parent_id=2,
            url="url",
            title="title",
            content=b"pdf",
            checksum="checksum",
        )

        response = StudyProgramResponse.from_domain(model)

        assert response.study_program_ref_id == 2
