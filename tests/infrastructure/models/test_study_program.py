from infrastructure.models.study_program import StudyProgram
from infrastructure.models.study_program_ref import StudyProgramRef


class TestStudyProgram:
    def test_given_parent_id_when_created_then_parent_id_is_set(self):
        model = StudyProgram(
            id=1,
            parent_id=2,
            url="url",
            title="title",
            checksum="checksum",
            content=b"pdf",
        )

        assert model.parent_id == 2

    def test_given_parent_when_assigned_then_relation_is_available(self):
        study_program_ref = StudyProgramRef(
            id=1, url="ref-url", title="ref", content="html"
        )
        study_program = StudyProgram(
            id=2,
            parent_id=1,
            url="url",
            title="title",
            checksum="checksum",
            content=b"pdf",
        )

        study_program.study_program_ref = study_program_ref

        assert study_program.study_program_ref == study_program_ref
