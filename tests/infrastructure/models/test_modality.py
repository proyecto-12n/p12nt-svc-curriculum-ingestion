from infrastructure.models.modality import Modality


class TestModality:
    def test_given_parent_id_when_created_then_parent_id_is_set(self):
        model = Modality(id=1, parent_id=2, url="url", title="title", content="html")

        assert model.parent_id == 2
