from types import SimpleNamespace

from infrastructure.adapter.inbound.web.routers.data_quality_kpi_router import (
    get_data_quality_kpis,
    router,
)
from infrastructure.models.curriculum import Curriculum
from infrastructure.models.grade_level import GradeLevel
from infrastructure.models.modality import Modality
from infrastructure.models.study_program import StudyProgram
from infrastructure.models.study_program_markdown import StudyProgramMarkdown
from infrastructure.models.study_program_ref import StudyProgramRef
from infrastructure.models.subject import Subject


class FakeSession:
    def __init__(self, results):
        self.results = iter(results)

    def exec(self, _statement):
        return SimpleNamespace(all=lambda: next(self.results))


class TestDataQualityKPIRouter:
    def test_given_router_when_created_then_exposes_data_quality_endpoint(self):
        paths = {route.path for route in router.routes}

        assert "/kpis/data-quality" in paths

    async def test_given_data_quality_issues_when_get_kpis_then_returns_counts(self):
        session = FakeSession(
            [
                [Curriculum(id=1, url="duplicate", title="Curriculum", content="")],
                [
                    Modality(
                        id=10,
                        parent_id=999,
                        url="duplicate",
                        title="Modality",
                        content="html",
                    )
                ],
                [
                    Subject(
                        id=20,
                        parent_id=10,
                        url="subject",
                        title="Subject",
                        content="",
                    )
                ],
                [
                    GradeLevel(
                        id=30,
                        parent_id=20,
                        url="grade",
                        title="Grade",
                        content="html",
                    )
                ],
                [
                    StudyProgramRef(
                        id=40,
                        parent_id=999,
                        url="ref",
                        title="Ref",
                        content="html",
                    )
                ],
                [
                    StudyProgram(
                        id=50,
                        parent_id=40,
                        url="program",
                        title="Program",
                        content=b"",
                        checksum="checksum",
                    ),
                    StudyProgram(
                        id=51,
                        parent_id=999,
                        url="program-2",
                        title="Program 2",
                        content=b"pdf",
                        checksum="checksum",
                    ),
                ],
                [
                    StudyProgramMarkdown(
                        id=1,
                        study_program_id=50,
                        tool_name="markitdown",
                        content="ñ",
                    )
                ],
            ]
        )

        response = await get_data_quality_kpis(session)

        assert response.study_programs_without_pdf_count == 1
        assert response.study_programs_without_markdown_count == 1
        assert response.duplicate_resource_url_count == 1
        assert response.orphan_hierarchy_items_count == 3
        assert response.empty_content_count == 3
        assert response.markdown_size_bytes[0].study_program_id == 50
        assert response.markdown_size_bytes[0].tool_name == "markitdown"
        assert response.markdown_size_bytes[0].size_bytes == 2
