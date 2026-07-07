from infrastructure.models.grade_level import GradeLevel
from infrastructure.models.study_program import StudyProgram
from infrastructure.models.study_program_ref import StudyProgramRef


class TestStudyProgramRef:
    def test_given_values_when_created_then_values_are_set(self):
        model = StudyProgramRef(id=1, url="url", title="title", content="html")

        assert model.id == 1
        assert model.url == "url"

    def test_given_parent_and_child_when_assigned_then_relations_are_available(self):
        grade_level = GradeLevel(
            id=1, parent_id=9, url="grade-url", title="grade", content="html"
        )
        study_program_ref = StudyProgramRef(
            id=2, url="url", title="title", content="html"
        )
        study_program = StudyProgram(
            id=3,
            parent_id=2,
            url="program-url",
            title="program",
            content=b"pdf",
            checksum="checksum",
        )

        study_program_ref.grade_levels = [grade_level]
        study_program_ref.study_programs = [study_program]

        assert study_program_ref.grade_levels == [grade_level]
        assert study_program_ref.study_programs == [study_program]
