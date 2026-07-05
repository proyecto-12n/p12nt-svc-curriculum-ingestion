from infrastructure.models.modality import Modality


class TestModality:
    def test_given_explicit_parent_alias_when_created_then_parent_id_is_set(self):
        model = Modality(
            id=1, curriculum_id=2, url="url", title="title", content="html"
        )

        assert model.parent_id == 2
        assert model.curriculum_id == 2

    def test_given_parent_alias_when_updated_then_parent_id_changes(self):
        model = Modality(id=1, parent_id=2, url="url", title="title", content="html")

        model.curriculum_id = 3

        assert model.parent_id == 3
