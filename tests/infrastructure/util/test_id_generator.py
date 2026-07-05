from infrastructure.util.id_generator import generate_id


class TestGenerateId:
    def test_given_same_values_when_generate_id_then_returns_same_integer(self):
        first = generate_id("Bases", "Parvularia")
        second = generate_id("Bases", "Parvularia")

        assert first == second
        assert isinstance(first, int)
        assert first > 0
