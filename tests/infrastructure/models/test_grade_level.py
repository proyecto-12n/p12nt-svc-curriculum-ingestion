from infrastructure.models.grade_level import GradeLevel
from infrastructure.models.study_program_ref import StudyProgramRef
from infrastructure.models.subject import Subject


class TestGradeLevel:
    def test_given_parent_id_when_created_then_parent_id_is_set(self):
        model = GradeLevel(id=1, parent_id=2, url="url", title="title", content="html")

        assert model.parent_id == 2

    def test_given_parent_and_child_when_assigned_then_relations_are_available(self):
        subject = Subject(
            id=1, parent_id=9, url="subject-url", title="subject", content="html"
        )
        grade_level = GradeLevel(
            id=2, parent_id=1, url="url", title="title", content="html"
        )
        study_program_ref = StudyProgramRef(
            id=3, url="ref-url", title="ref", content="html"
        )

        grade_level.subject = subject
        grade_level.study_program_refs = [study_program_ref]
        study_program_ref.grade_levels = [grade_level]

        assert grade_level.subject == subject
        assert grade_level.study_program_refs == [study_program_ref]
        assert study_program_ref.grade_levels == [grade_level]
