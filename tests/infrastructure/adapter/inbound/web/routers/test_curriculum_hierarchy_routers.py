from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from domain.model import (
    Curriculum,
    GradeLevel,
    GradeLevelDetailReport,
    Modality,
    StudyProgram,
    StudyProgramRef,
    Subject,
)
from infrastructure.adapter.inbound.web.routers import (
    curriculum_router,
    grade_level_router,
    modality_router,
    study_program_ref_router,
    study_program_router,
    subject_router,
)


LIST_CASES = [
    (
        curriculum_router.list_curriculums,
        None,
        Curriculum(id=1, url="url", title="Curriculum", content="html"),
    ),
    (
        modality_router.list_modalities,
        1,
        Modality(
            id=2,
            curriculum_id=1,
            url="url",
            title="Modality",
            content="html",
        ),
    ),
    (
        subject_router.list_subjects,
        2,
        Subject(id=3, modality_id=2, url="url", title="Subject", content="html"),
    ),
    (
        grade_level_router.list_grade_levels,
        3,
        GradeLevel(id=4, subject_id=3, url="url", title="Grade level", content="html"),
    ),
    (
        study_program_ref_router.list_study_program_refs,
        4,
        StudyProgramRef(
            id=5,
            grade_level_id=4,
            url="url",
            title="Study program ref",
            content="html",
        ),
    ),
    (
        study_program_router.list_study_programs,
        5,
        StudyProgram(
            id=6,
            study_program_ref_id=5,
            url="url",
            title="Study program",
            content=b"pdf",
            checksum="checksum",
        ),
    ),
]

GET_CASES = [
    (
        curriculum_router.get_curriculum,
        Curriculum(id=1, url="url", title="Curriculum", content="html"),
        "Curriculum not found",
    ),
    (
        modality_router.get_modality,
        Modality(
            id=2,
            curriculum_id=1,
            url="url",
            title="Modality",
            content="html",
        ),
        "Modality not found",
    ),
    (
        subject_router.get_subject,
        Subject(id=3, modality_id=2, url="url", title="Subject", content="html"),
        "Subject not found",
    ),
    (
        grade_level_router.get_grade_level,
        GradeLevel(id=4, subject_id=3, url="url", title="Grade level", content="html"),
        "Grade level not found",
    ),
    (
        study_program_ref_router.get_study_program_ref,
        StudyProgramRef(
            id=5,
            grade_level_id=4,
            url="url",
            title="Study program ref",
            content="html",
        ),
        "Study program ref not found",
    ),
    (
        study_program_router.get_study_program,
        StudyProgram(
            id=6,
            study_program_ref_id=5,
            url="url",
            title="Study program",
            content=b"pdf",
            checksum="checksum",
        ),
        "Study program not found",
    ),
]

FACTORY_CASES = [
    curriculum_router.get_list_curriculums_use_case,
    curriculum_router.get_get_curriculum_use_case,
    modality_router.get_list_modalities_use_case,
    modality_router.get_get_modality_use_case,
    subject_router.get_list_subjects_use_case,
    subject_router.get_get_subject_use_case,
    grade_level_router.get_list_grade_levels_use_case,
    grade_level_router.get_get_grade_level_use_case,
    grade_level_router.get_list_grade_level_detail_report_use_case,
    study_program_ref_router.get_list_study_program_refs_use_case,
    study_program_ref_router.get_get_study_program_ref_use_case,
    study_program_router.get_list_study_programs_use_case,
    study_program_router.get_get_study_program_use_case,
]

PARENT_FILTER_ROUTERS = [
    modality_router.router,
    subject_router.router,
    grade_level_router.router,
    study_program_ref_router.router,
    study_program_router.router,
]

LIST_ROUTERS = [curriculum_router.router, *PARENT_FILTER_ROUTERS]


def get_list_route(router):
    return next(route for route in router.routes if "{id}" not in route.path)


def get_detail_route(router):
    return next(route for route in router.routes if "{id}" in route.path)


class TestCurriculumHierarchyRouters:
    @pytest.mark.parametrize("handler,parent_id,model", LIST_CASES)
    async def test_given_use_case_when_list_then_returns_response(
        self, handler, parent_id, model
    ):
        use_case = SimpleNamespace(execute=AsyncMock(return_value=[model]))

        if parent_id is None:
            result = await handler(use_case=use_case)
            use_case.execute.assert_awaited_once_with()
        else:
            result = await handler(parent_id=parent_id, use_case=use_case)
            use_case.execute.assert_awaited_once_with(parent_id)

        assert result[0].id == model.id

    @pytest.mark.parametrize("handler,model,_detail", GET_CASES)
    async def test_given_existing_id_when_get_then_returns_response(
        self, handler, model, _detail
    ):
        use_case = SimpleNamespace(execute=AsyncMock(return_value=model))

        result = await handler(1, use_case=use_case)

        assert result.id == model.id
        use_case.execute.assert_awaited_once_with(1)

    @pytest.mark.parametrize("handler,_model,detail", GET_CASES)
    async def test_given_missing_id_when_get_then_raises_not_found(
        self, handler, _model, detail
    ):
        use_case = SimpleNamespace(execute=AsyncMock(return_value=None))

        with pytest.raises(HTTPException) as exc_info:
            await handler(1, use_case=use_case)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == detail

    @pytest.mark.parametrize("factory", FACTORY_CASES)
    def test_given_session_when_get_use_case_then_returns_use_case(self, factory):
        use_case = factory(MagicMock())

        assert hasattr(use_case, "execute")

    @pytest.mark.parametrize("router", PARENT_FILTER_ROUTERS)
    def test_given_child_list_route_when_inspected_then_requires_parent_id(
        self, router
    ):
        route = get_list_route(router)
        query_params = {param.name: param for param in route.dependant.query_params}

        assert query_params["parent_id"].field_info.is_required()

    def test_given_curriculum_list_route_when_inspected_then_has_no_parent_filter(
        self,
    ):
        route = get_list_route(curriculum_router.router)

        assert route.dependant.query_params == []

    async def test_given_report_rows_when_list_grade_level_detail_report_then_returns_response(
        self,
    ):
        use_case = SimpleNamespace(
            execute=AsyncMock(
                return_value=[
                    GradeLevelDetailReport(
                        id=1,
                        title="Grade",
                        url="grade-url",
                        study_program_ref_id=2,
                        study_program_id=3,
                        study_program_markitdown_id=4,
                        study_program_pymupdf4llm_id=None,
                    )
                ]
            )
        )

        result = await grade_level_router.list_grade_level_detail_report(use_case)

        assert result[0].id == 1
        assert result[0].study_program_ref_id == 2
        assert result[0].study_program_id == 3
        assert result[0].study_program_markitdown_id == 4
        assert result[0].study_program_pymupdf4llm_id is None
        use_case.execute.assert_awaited_once_with()

    @pytest.mark.parametrize("router", LIST_ROUTERS)
    def test_given_list_route_when_inspected_then_excludes_content(self, router):
        route = get_list_route(router)

        assert route.response_model_exclude == {"__all__": {"content"}}

    @pytest.mark.parametrize("router", LIST_ROUTERS)
    def test_given_detail_route_when_inspected_then_includes_content(self, router):
        route = get_detail_route(router)

        assert route.response_model_exclude is None
