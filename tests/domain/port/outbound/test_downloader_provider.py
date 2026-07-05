from domain.port.outbound.downloader_provider import DownloaderProvider


class ConcreteDownloaderProvider:
    def get_downloader(self, resource_type):
        return resource_type


class TestDownloaderProvider:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: DownloaderProvider = ConcreteDownloaderProvider()

        assert port.get_downloader("html") == "html"
