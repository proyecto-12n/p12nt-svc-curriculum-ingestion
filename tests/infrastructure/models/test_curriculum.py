from infrastructure.models.curriculum import Curriculum


class TestCurriculum:
    def test_given_valid_values_when_created_then_values_are_stored(self):
        model = Curriculum(id=1, url="url", title="title", content="html")

        assert model.id == 1
        assert model.url == "url"
        assert model.title == "title"
        assert model.content == "html"
