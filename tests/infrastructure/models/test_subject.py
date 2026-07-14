from infrastructure.models.grade_level import GradeLevel
from infrastructure.models.modality import Modality
from infrastructure.models.subject import Subject


class TestSubject:
    def test_given_parent_id_when_created_then_parent_id_is_set(self):
        model = Subject(id=1, parent_id=2, url="url", title="title", content="html")

        assert model.parent_id == 2

    def test_given_parent_and_child_when_assigned_then_relations_are_available(self):
        modality = Modality(
            id=1,
            parent_id=9,
            url="modality-url",
            title="Curriculum Framework",
            content="html",
        )
        subject = Subject(id=2, parent_id=1, url="url", title="title", content="html")
        grade_level = GradeLevel(
            id=3, parent_id=2, url="grade-url", title="grade", content="html"
        )

        subject.modality = modality
        subject.grade_levels = [grade_level]

        assert subject.modality == modality
        assert subject.grade_levels == [grade_level]
