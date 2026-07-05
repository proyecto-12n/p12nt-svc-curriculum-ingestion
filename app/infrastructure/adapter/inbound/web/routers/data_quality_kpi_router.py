from collections import Counter

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from infrastructure.adapter.inbound.web.dto.data_quality_kpi_response import (
    DataQualityKPIResponse,
)
from infrastructure.adapter.inbound.web.dto.markdown_size_response import (
    MarkdownSizeResponse,
)
from infrastructure.database import get_db
from infrastructure.models.curriculum import Curriculum
from infrastructure.models.grade_level import GradeLevel
from infrastructure.models.modality import Modality
from infrastructure.models.study_program import StudyProgram
from infrastructure.models.study_program_markdown import StudyProgramMarkdown
from infrastructure.models.study_program_ref import StudyProgramRef
from infrastructure.models.subject import Subject

router = APIRouter(prefix="/kpis", tags=["KPIs"])


def is_empty(value: str | bytes | None) -> bool:
    return value is None or value == "" or value == b""


def count_orphans(children, parent_ids: set[int]) -> int:
    return sum(1 for child in children if child.parent_id not in parent_ids)


@router.get("/data-quality", response_model=DataQualityKPIResponse)
async def get_data_quality_kpis(
    session: Session = Depends(get_db),
) -> DataQualityKPIResponse:
    curriculums = session.exec(select(Curriculum)).all()
    modalities = session.exec(select(Modality)).all()
    subjects = session.exec(select(Subject)).all()
    grade_levels = session.exec(select(GradeLevel)).all()
    study_program_refs = session.exec(select(StudyProgramRef)).all()
    study_programs = session.exec(select(StudyProgram)).all()
    markdowns = session.exec(select(StudyProgramMarkdown)).all()

    resources = [
        *curriculums,
        *modalities,
        *subjects,
        *grade_levels,
        *study_program_refs,
        *study_programs,
    ]
    markdown_program_ids = {markdown.study_program_id for markdown in markdowns}
    url_counts = Counter(resource.url for resource in resources if resource.url)

    return DataQualityKPIResponse(
        study_programs_without_pdf_count=sum(
            1 for program in study_programs if is_empty(program.content)
        ),
        study_programs_without_markdown_count=sum(
            1 for program in study_programs if program.id not in markdown_program_ids
        ),
        duplicate_resource_url_count=sum(
            1 for count in url_counts.values() if count > 1
        ),
        orphan_hierarchy_items_count=(
            count_orphans(modalities, {item.id for item in curriculums})
            + count_orphans(subjects, {item.id for item in modalities})
            + count_orphans(grade_levels, {item.id for item in subjects})
            + count_orphans(study_program_refs, {item.id for item in grade_levels})
            + count_orphans(study_programs, {item.id for item in study_program_refs})
        ),
        empty_content_count=sum(
            1 for item in [*resources, *markdowns] if is_empty(item.content)
        ),
        markdown_size_bytes=[
            MarkdownSizeResponse(
                study_program_id=markdown.study_program_id,
                tool_name=markdown.tool_name,
                size_bytes=len(markdown.content.encode("utf-8")),
            )
            for markdown in markdowns
        ],
    )
