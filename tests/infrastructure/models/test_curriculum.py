from infrastructure.models.curriculum import Curriculum
from infrastructure.models.curriculum_framework import CurriculumFramework


class TestCurriculum:
    def test_given_valid_values_when_created_then_values_are_stored(self):
        model = Curriculum(id=1, url="url", title="title", content="html")

        assert model.id == 1
        assert model.url == "url"
        assert model.title == "title"
        assert model.content == "html"

    def test_given_curriculum_framework_when_assigned_then_relation_is_available(self):
        curriculum = Curriculum(id=1, url="url", title="title", content="html")
        curriculum_framework = CurriculumFramework(
            id=2,
            parent_id=1,
            url="curriculum_framework-url",
            title="Curriculum Framework",
            content="html",
        )

        curriculum.curriculum_frameworks = [curriculum_framework]
        curriculum_framework.curriculum = curriculum

        assert curriculum.curriculum_frameworks == [curriculum_framework]
        assert curriculum_framework.curriculum == curriculum
