from typing import Any, AsyncGenerator, Protocol, TypeVar

from domain.model.edge import Edge
from domain.model.scrap_resource import ScrapResource

T = TypeVar("T")


class ScrapResourceParser(Protocol[T]):
    async def get_children(
        self, resource: ScrapResource[T]
    ) -> AsyncGenerator[Edge[Any], None]: ...

    async def get_title(self, resource: ScrapResource[T]) -> str: ...
