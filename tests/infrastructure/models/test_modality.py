from infrastructure.models.curriculum import Curriculum
from infrastructure.models.modality import Modality
from infrastructure.models.subject import Subject


class TestModality:
    def test_given_parent_id_when_created_then_parent_id_is_set(self):
        model = Modality(id=1, parent_id=2, url="url", title="title", content="html")

        assert model.parent_id == 2

    def test_given_parent_and_child_when_assigned_then_relations_are_available(self):
        curriculum = Curriculum(
            id=1, url="curriculum-url", title="curriculum", content="html"
        )
        modality = Modality(id=2, parent_id=1, url="url", title="title", content="html")
        subject = Subject(
            id=3, parent_id=2, url="subject-url", title="subject", content="html"
        )

        modality.curriculum = curriculum
        modality.subjects = [subject]

        assert modality.curriculum == curriculum
        assert modality.subjects == [subject]
