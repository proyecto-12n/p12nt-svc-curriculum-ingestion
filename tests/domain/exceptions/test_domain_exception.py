from domain.exceptions import DomainException


class TestDomainException:
    def test_given_message_when_created_then_behaves_like_exception(self):
        exception = DomainException("domain error")

        assert isinstance(exception, Exception)
        assert str(exception) == "domain error"
