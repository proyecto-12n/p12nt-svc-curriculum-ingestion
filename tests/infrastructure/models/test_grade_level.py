from infrastructure.models.grade_level import GradeLevel


class TestGradeLevel:
    def test_given_explicit_parent_alias_when_created_then_parent_id_is_set(self):
        model = GradeLevel(id=1, subject_id=2, url="url", title="title", content="html")

        assert model.parent_id == 2
        assert model.subject_id == 2

    def test_given_parent_alias_when_updated_then_parent_id_changes(self):
        model = GradeLevel(id=1, parent_id=2, url="url", title="title", content="html")

        model.subject_id = 3

        assert model.parent_id == 3
