from infrastructure.models.curriculum import Curriculum
from infrastructure.models.curriculum_framework import CurriculumFramework
from infrastructure.models.subject import Subject


class TestCurriculumFramework:
    def test_given_parent_id_when_created_then_parent_id_is_set(self):
        model = CurriculumFramework(
            id=1, parent_id=2, url="url", title="title", content="html"
        )

        assert model.parent_id == 2

    def test_given_parent_and_child_when_assigned_then_relations_are_available(self):
        curriculum = Curriculum(
            id=1, url="curriculum-url", title="curriculum", content="html"
        )
        curriculum_framework = CurriculumFramework(
            id=2, parent_id=1, url="url", title="title", content="html"
        )
        subject = Subject(
            id=3, parent_id=2, url="subject-url", title="subject", content="html"
        )

        curriculum_framework.curriculum = curriculum
        curriculum_framework.subjects = [subject]

        assert curriculum_framework.curriculum == curriculum
        assert curriculum_framework.subjects == [subject]
