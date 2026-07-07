from infrastructure.models.curriculum import Curriculum
from infrastructure.models.modality import Modality


class TestCurriculum:
    def test_given_valid_values_when_created_then_values_are_stored(self):
        model = Curriculum(id=1, url="url", title="title", content="html")

        assert model.id == 1
        assert model.url == "url"
        assert model.title == "title"
        assert model.content == "html"

    def test_given_modality_when_assigned_then_relation_is_available(self):
        curriculum = Curriculum(id=1, url="url", title="title", content="html")
        modality = Modality(
            id=2, parent_id=1, url="modality-url", title="modality", content="html"
        )

        curriculum.modalities = [modality]
        modality.curriculum = curriculum

        assert curriculum.modalities == [modality]
        assert modality.curriculum == curriculum
