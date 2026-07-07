import pytest

from domain.model.resource_type import ResourceType
from infrastructure.adapter.external.downloader.downloader_provider import (
    DownloaderProvider,
)
from infrastructure.adapter.external.downloader.impl import (
    HTMLDownloader,
    PDFDownloader,
)


class TestDownloaderProvider:
    def setup_method(self):
        self.provider = DownloaderProvider()

    def test_given_html_type_when_get_downloader_then_returns_html_downloader(self):
        downloader = self.provider.get_downloader(ResourceType.HTML)

        assert isinstance(downloader, HTMLDownloader)

    def test_given_pdf_type_when_get_downloader_then_returns_pdf_downloader(self):
        downloader = self.provider.get_downloader(ResourceType.PDF)

        assert isinstance(downloader, PDFDownloader)

    def test_given_unknown_type_when_get_downloader_then_raises_value_error(self):
        with pytest.raises(ValueError, match="No downloader configured"):
            self.provider.get_downloader(None)
