from domain.port.outbound.curriculum_hierarchy_repository import (
    CurriculumHierarchyRepository,
)


class ConcreteCurriculumHierarchyRepository:
    async def find_by_id(self, id):
        return id

    async def find_by_url(self, url):
        return url

    async def list(self, parent_id=None):
        return [parent_id]

    async def save(self, knowledge):
        return knowledge


class TestCurriculumHierarchyRepository:
    async def test_given_concrete_repository_when_methods_called_then_contract_is_satisfied(
        self,
    ):
        repository: CurriculumHierarchyRepository[int] = (
            ConcreteCurriculumHierarchyRepository()
        )

        assert await repository.find_by_id(1) == 1
        assert await repository.find_by_url("url") == "url"
        assert await repository.list(2) == [2]
        assert await repository.save(3) == 3
