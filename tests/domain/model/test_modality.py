from datetime import datetime

from domain.model.modality import Modality


class TestModality:
    def test_given_valid_values_when_created_then_stores_values_and_extraction_time(
        self,
    ):
        model = Modality(
            id=1, curriculum_id=2, url="url", title="title", content="html"
        )

        assert model.id == 1
        assert model.url == "url"
        assert model.title == "title"
        assert model.content == "html"
        assert isinstance(model.extracted_at, datetime)
