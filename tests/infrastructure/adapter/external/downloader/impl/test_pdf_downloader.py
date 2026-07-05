from unittest.mock import AsyncMock, MagicMock, patch

import httpx

from domain.model.resource_type import ResourceType
from infrastructure.adapter.external.downloader.impl.pdf_downloader import PDFDownloader


class TestPDFDownloader:
    async def test_given_successful_response_when_download_then_returns_pdf_resource(
        self,
    ):
        response = MagicMock()
        response.content = b"pdf"
        response.raise_for_status = MagicMock()
        client = AsyncMock(spec=httpx.AsyncClient)
        client.get.return_value = response
        client.__aenter__.return_value = client

        with patch("httpx.AsyncClient", return_value=client):
            resource = await PDFDownloader().download("https://example.test/file.pdf")

        assert resource.url == "https://example.test/file.pdf"
        assert resource.type == ResourceType.PDF
        assert resource.content == b"pdf"
        response.raise_for_status.assert_called_once()
