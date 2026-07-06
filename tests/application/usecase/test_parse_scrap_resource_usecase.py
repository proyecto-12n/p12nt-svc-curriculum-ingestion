from types import SimpleNamespace

from application.usecase.parse_scrap_resource_usecase import (
    ParseScrapResourceUseCaseImpl,
)
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType


class TestParseScrapResourceUseCaseImpl:
    async def test_given_item_when_execute_then_returns_title_and_children(self):
        child = Edge(url="child", type=ResourceType.HTML)
        use_case = ParseScrapResourceUseCaseImpl(
            SimpleNamespace(find_by_id=_async_return(_item())),
            _provider(_parser(title="Parsed", children=[child])),
            CurriculumHierarchyType.CURRICULUM,
        )

        result = await use_case.execute(1)

        assert result.title == "Parsed"
        assert result.children == [child]

    async def test_given_missing_item_when_execute_then_returns_none(self):
        use_case = ParseScrapResourceUseCaseImpl(
            SimpleNamespace(find_by_id=_async_return(None)),
            _provider(_parser()),
            CurriculumHierarchyType.CURRICULUM,
        )

        assert await use_case.execute(1) is None


def _item():
    return SimpleNamespace(url="url", content="html")


def _provider(parser):
    return SimpleNamespace(get_parser=lambda _hierarchy_type: parser)


def _parser(title=None, children=None):
    async def get_title(_resource):
        return title

    async def get_children(_resource):
        for child in children or []:
            yield child

    return SimpleNamespace(
        get_title=get_title,
        get_children=get_children,
    )


def _async_return(value):
    async def inner(*_args):
        return value

    return inner
