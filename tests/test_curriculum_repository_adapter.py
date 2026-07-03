# -*- coding: utf-8 -*-
import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.infrastructure.adapter.outbound.db import (
    SqlCurriculumRepositoryAdapter,
    SqlModalityRepositoryAdapter,
    SqlSubjectRepositoryAdapter,
    SqlGradeLevelRepositoryAdapter,
    SqlStudyProgramRefRepositoryAdapter,
    SqlStudyProgramRepositoryAdapter,
)
from app.domain.model import (
    Curriculum,
    Modality,
    Subject,
    GradeLevel,
    StudyProgram,
    StudyProgramRef,
)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    # Remove schema from table metadata so it works with SQLite
    for table in SQLModel.metadata.tables.values():
        table.schema = None
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_save_and_find_curriculum(session):
    adapter = SqlCurriculumRepositoryAdapter(session)
    curr = Curriculum(
        id=1, title="Parvularia", url="http://test.url/curr", content="HTML content"
    )
    saved = adapter.save_curriculum(curr)
    assert saved.id == 1

    found = adapter.find_curriculum_by_url("http://test.url/curr")
    assert found is not None
    assert found.title == "Parvularia"
    assert found.content == "HTML content"


def test_save_and_find_modality(session):
    curr_adapter = SqlCurriculumRepositoryAdapter(session)
    mod_adapter = SqlModalityRepositoryAdapter(session)

    curr = Curriculum(
        id=1, title="Parvularia", url="http://test.url/curr", content="HTML"
    )
    curr_adapter.save_curriculum(curr)

    mod = Modality(
        id=10,
        curriculum_id=1,
        url="http://test.url/mod",
        title="Nivel Medio",
        content="HTML Mod",
    )
    mod_adapter.save_modality(mod)

    found = mod_adapter.find_modality_by_url("http://test.url/mod")
    assert found is not None
    assert found.title == "Nivel Medio"
    assert found.content == "HTML Mod"


def test_save_and_find_subject(session):
    curr_adapter = SqlCurriculumRepositoryAdapter(session)
    mod_adapter = SqlModalityRepositoryAdapter(session)
    sub_adapter = SqlSubjectRepositoryAdapter(session)

    curr = Curriculum(
        id=1, title="Parvularia", url="http://test.url/curr", content="HTML"
    )
    curr_adapter.save_curriculum(curr)

    mod = Modality(
        id=10,
        curriculum_id=1,
        url="http://test.url/mod",
        title="Nivel Medio",
        content="HTML Mod",
    )
    mod_adapter.save_modality(mod)

    sub = Subject(
        id=100,
        modality_id=10,
        url="http://test.url/sub",
        title="Matemáticas",
        content="HTML Sub",
    )
    sub_adapter.save_subject(sub)

    found = sub_adapter.find_subject_by_title_and_modality("Matemáticas", 10)
    assert found is not None
    assert found.url == "http://test.url/sub"
    assert found.content == "HTML Sub"


def test_save_and_find_grade_level(session):
    curr_adapter = SqlCurriculumRepositoryAdapter(session)
    mod_adapter = SqlModalityRepositoryAdapter(session)
    sub_adapter = SqlSubjectRepositoryAdapter(session)
    grade_adapter = SqlGradeLevelRepositoryAdapter(session)

    curr = Curriculum(
        id=1, title="Parvularia", url="http://test.url/curr", content="HTML"
    )
    curr_adapter.save_curriculum(curr)

    mod = Modality(
        id=10,
        curriculum_id=1,
        url="http://test.url/mod",
        title="Nivel Medio",
        content="HTML Mod",
    )
    mod_adapter.save_modality(mod)

    sub = Subject(
        id=100,
        modality_id=10,
        url="http://test.url/sub",
        title="Matemáticas",
        content="HTML Sub",
    )
    sub_adapter.save_subject(sub)

    grade = GradeLevel(
        id=1000,
        subject_id=100,
        url="http://test.url/grade",
        title="1 Básico",
        content="HTML Grade",
    )
    grade_adapter.save_grade_level(grade)

    found = grade_adapter.find_grade_level_by_title_and_subject("1 Básico", 100)
    assert found is not None
    assert found.url == "http://test.url/grade"
    assert found.content == "HTML Grade"


def test_save_and_find_study_program_ref(session):
    curr_adapter = SqlCurriculumRepositoryAdapter(session)
    mod_adapter = SqlModalityRepositoryAdapter(session)
    sub_adapter = SqlSubjectRepositoryAdapter(session)
    grade_adapter = SqlGradeLevelRepositoryAdapter(session)
    ref_adapter = SqlStudyProgramRefRepositoryAdapter(session)

    curr = Curriculum(
        id=1, title="Parvularia", url="http://test.url/curr", content="HTML"
    )
    curr_adapter.save_curriculum(curr)

    mod = Modality(
        id=10,
        curriculum_id=1,
        url="http://test.url/mod",
        title="Nivel Medio",
        content="HTML Mod",
    )
    mod_adapter.save_modality(mod)

    sub = Subject(
        id=100,
        modality_id=10,
        url="http://test.url/sub",
        title="Matemáticas",
        content="HTML Sub",
    )
    sub_adapter.save_subject(sub)

    grade = GradeLevel(
        id=1000,
        subject_id=100,
        url="http://test.url/grade",
        title="1 Básico",
        content="HTML Grade",
    )
    grade_adapter.save_grade_level(grade)

    ref = StudyProgramRef(
        id=2000,
        grade_level_id=1000,
        url="http://test.url/ref",
        title="Ref Programa",
        content="HTML Ref",
    )
    ref_adapter.save_study_program_ref(ref)

    found = ref_adapter.find_study_program_ref_by_url("http://test.url/ref")
    assert found is not None
    assert found.title == "Ref Programa"
    assert found.content == "HTML Ref"


def test_save_and_find_study_program(session):
    curr_adapter = SqlCurriculumRepositoryAdapter(session)
    mod_adapter = SqlModalityRepositoryAdapter(session)
    sub_adapter = SqlSubjectRepositoryAdapter(session)
    grade_adapter = SqlGradeLevelRepositoryAdapter(session)
    ref_adapter = SqlStudyProgramRefRepositoryAdapter(session)
    prog_adapter = SqlStudyProgramRepositoryAdapter(session)

    curr = Curriculum(
        id=1, title="Parvularia", url="http://test.url/curr", content="HTML"
    )
    curr_adapter.save_curriculum(curr)

    mod = Modality(
        id=10,
        curriculum_id=1,
        url="http://test.url/mod",
        title="Nivel Medio",
        content="HTML Mod",
    )
    mod_adapter.save_modality(mod)

    sub = Subject(
        id=100,
        modality_id=10,
        url="http://test.url/sub",
        title="Matemáticas",
        content="HTML Sub",
    )
    sub_adapter.save_subject(sub)

    grade = GradeLevel(
        id=1000,
        subject_id=100,
        url="http://test.url/grade",
        title="1 Básico",
        content="HTML Grade",
    )
    grade_adapter.save_grade_level(grade)

    ref = StudyProgramRef(
        id=2000,
        grade_level_id=1000,
        url="http://test.url/ref",
        title="Ref Programa",
        content="HTML Ref",
    )
    ref_adapter.save_study_program_ref(ref)

    prog = StudyProgram(
        id=3000,
        study_program_ref_id=2000,
        url="http://test.url/prog.pdf",
        title="Art-1.pdf",
        content=b"binary pdf data",
        checksum="abcd",
    )
    prog_adapter.save_study_program(prog)

    found = prog_adapter.find_study_program_by_url("http://test.url/prog.pdf")
    assert found is not None
    assert found.title == "Art-1.pdf"
    assert found.content == b"binary pdf data"
    assert found.checksum == "abcd"
