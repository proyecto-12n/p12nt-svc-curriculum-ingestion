from domain.port.outbound.content_downloader import ContentDownloader


class ConcreteContentDownloader:
    async def download(self, url):
        return url


class TestContentDownloader:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: ContentDownloader = ConcreteContentDownloader()

        assert await port.download("url") == "url"
