from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp

from domain.model.resource_type import ResourceType
from infrastructure.adapter.external.downloader.impl.html_downloader import (
    HTMLDownloader,
)


class TestHTMLDownloader:
    async def test_given_successful_response_when_download_then_returns_html_resource(
        self,
    ):
        response = MagicMock()
        response.text = AsyncMock(return_value="<html>Hello</html>")
        response.raise_for_status = MagicMock()
        client = AsyncMock(spec=aiohttp.ClientSession)
        client.get.return_value = response
        client.__aenter__.return_value = client

        with patch("aiohttp.ClientSession", return_value=client):
            resource = await HTMLDownloader().download("https://example.test")

        assert resource.url == "https://example.test"
        assert resource.type == ResourceType.HTML
        assert "Hello" in resource.content
        response.raise_for_status.assert_called_once()
