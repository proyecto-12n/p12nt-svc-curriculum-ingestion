from infrastructure.models.study_program_ref import StudyProgramRef


class TestStudyProgramRef:
    def test_given_explicit_parent_alias_when_created_then_parent_id_is_set(self):
        model = StudyProgramRef(
            id=1, grade_level_id=2, url="url", title="title", content="html"
        )

        assert model.parent_id == 2
        assert model.grade_level_id == 2

    def test_given_parent_alias_when_updated_then_parent_id_changes(self):
        model = StudyProgramRef(
            id=1, parent_id=2, url="url", title="title", content="html"
        )

        model.grade_level_id = 3

        assert model.parent_id == 3
