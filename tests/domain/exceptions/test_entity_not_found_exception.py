from domain.exceptions import DomainException, EntityNotFoundException


class TestEntityNotFoundException:
    def test_given_entity_id_when_created_then_message_contains_entity_id(self):
        exception = EntityNotFoundException(42)

        assert isinstance(exception, DomainException)
        assert "42" in str(exception)
