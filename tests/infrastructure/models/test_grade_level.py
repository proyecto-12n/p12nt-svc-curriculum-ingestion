from infrastructure.models.grade_level import GradeLevel


class TestGradeLevel:
    def test_given_parent_id_when_created_then_parent_id_is_set(self):
        model = GradeLevel(id=1, parent_id=2, url="url", title="title", content="html")

        assert model.parent_id == 2
