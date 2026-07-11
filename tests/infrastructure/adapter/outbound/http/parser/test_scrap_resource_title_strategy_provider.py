import pytest

from domain.model.resource_type import ResourceType
from infrastructure.adapter.outbound.http.parser.html_scrap_resource_title_strategy import (
    HtmlScrapResourceTitleStrategy,
)
from infrastructure.adapter.outbound.http.parser.pdf_scrap_resource_title_strategy import (
    PdfScrapResourceTitleStrategy,
)
from infrastructure.adapter.outbound.http.parser.scrap_resource_title_strategy_provider import (
    ScrapResourceTitleStrategyProvider,
)


class TestScrapResourceTitleStrategyProvider:
    def test_given_html_resource_type_when_get_strategy_then_returns_html_strategy(
        self,
    ):
        assert (
            ScrapResourceTitleStrategyProvider.get_strategy(ResourceType.HTML)
            is HtmlScrapResourceTitleStrategy
        )

    def test_given_pdf_resource_type_when_get_strategy_then_returns_pdf_strategy(self):
        assert (
            ScrapResourceTitleStrategyProvider.get_strategy(ResourceType.PDF)
            is PdfScrapResourceTitleStrategy
        )

    def test_given_unknown_resource_type_when_get_strategy_then_raises_value_error(
        self,
    ):
        with pytest.raises(ValueError):
            ScrapResourceTitleStrategyProvider.get_strategy("invalid")
