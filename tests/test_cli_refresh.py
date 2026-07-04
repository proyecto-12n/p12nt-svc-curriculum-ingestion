# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import Session, SQLModel, create_engine

from domain.model.curriculum import Curriculum
from domain.model.grade_level import GradeLevel
from domain.model.modality import Modality
from domain.model.study_program import StudyProgram
from domain.model.study_program_ref import StudyProgramRef
from domain.model.subject import Subject
from infrastructure.adapter.outbound.db import (
    SqlCurriculumRepositoryAdapter,
    SqlModalityRepositoryAdapter,
    SqlSubjectRepositoryAdapter,
    SqlGradeLevelRepositoryAdapter,
    SqlStudyProgramRefRepositoryAdapter,
    SqlStudyProgramRepositoryAdapter,
)
from infrastructure.cli.ingest_curriculum import run_cli


@pytest.fixture(name="db_session")
def db_session_fixture():
    engine = create_engine("sqlite:///:memory:")
    # Remove schema from table metadata so it works with SQLite
    for table in SQLModel.metadata.tables.values():
        table.schema = None
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.mark.skip
@pytest.mark.asyncio
async def test_repository_upsert_behavior(db_session):
    # Arrange
    curr_repo = SqlCurriculumRepositoryAdapter(db_session)
    modality_repo = SqlModalityRepositoryAdapter(db_session)
    subject_repo = SqlSubjectRepositoryAdapter(db_session)
    grade_repo = SqlGradeLevelRepositoryAdapter(db_session)
    ref_repo = SqlStudyProgramRefRepositoryAdapter(db_session)
    prog_repo = SqlStudyProgramRepositoryAdapter(db_session)

    # 1. Test Curriculum Upsert
    curriculum = Curriculum(
        id=1, url="http://test.url/cur", title="Initial Curriculum", content="Init"
    )
    await curr_repo.save(curriculum)

    curriculum.title = "Updated Curriculum"
    curriculum.content = "Updated"
    await curr_repo.save(curriculum)

    saved_cur = await curr_repo.find_by_url("http://test.url/cur")
    assert saved_cur.title == "Updated Curriculum"
    assert saved_cur.content == "Updated"

    # 2. Test Modality Upsert
    modality = Modality(
        id=1,
        curriculum_id=1,
        url="http://test.url/mod",
        title="Initial Modality",
        content="Init",
    )
    await modality_repo.save(modality)

    modality.title = "Updated Modality"
    await modality_repo.save(modality)

    saved_mod = await modality_repo.find_by_url("http://test.url/mod")
    assert saved_mod.title == "Updated Modality"

    # 3. Test Subject Upsert
    subject = Subject(
        id=1,
        modality_id=1,
        url="http://test.url/sub",
        title="Initial Subject",
        content="Init",
    )
    await subject_repo.save(subject)

    subject.url = "http://test.url/sub-updated"
    await subject_repo.save(subject)

    saved_sub = await subject_repo.find_subject_by_title_and_modality(
        "Initial Subject", 1
    )
    assert saved_sub.url == "http://test.url/sub-updated"

    # 4. Test GradeLevel Upsert
    grade = GradeLevel(
        id=1,
        subject_id=1,
        url="http://test.url/grade",
        title="Initial Grade",
        content="Init",
    )
    await grade_repo.save(grade)

    grade.url = "http://test.url/grade-updated"
    await grade_repo.save(grade)

    saved_grade = await grade_repo.find_grade_level_by_title_and_subject(
        "Initial Grade", 1
    )
    assert saved_grade.url == "http://test.url/grade-updated"

    # 5. Test StudyProgramRef Upsert
    ref = StudyProgramRef(
        id=1,
        grade_level_id=1,
        url="http://test.url/ref",
        title="Initial Ref",
        content="Init",
    )
    await ref_repo.save(ref)

    ref.title = "Updated Ref"
    await ref_repo.save(ref)

    saved_ref = await ref_repo.find_by_url("http://test.url/ref")
    assert saved_ref.title == "Updated Ref"

    # 6. Test StudyProgram Upsert
    program = StudyProgram(
        id=1,
        study_program_ref_id=1,
        url="http://test.url/prog",
        title="Initial Program",
        checksum="123",
        content=b"Init",
    )
    await prog_repo.save(program)

    program.title = "Updated Program"
    await prog_repo.save(program)

    saved_prog = await prog_repo.find_by_url("http://test.url/prog")
    assert saved_prog.title == "Updated Program"


def test_cli_refresh_flag_propagation():
    with (
        patch("infrastructure.cli.ingest_curriculum.Session") as mock_session_class,
        patch("infrastructure.database.init_db") as mock_init_db,
        patch(
            "infrastructure.cli.ingest_curriculum.IngestCurriculumUseCaseImpl"
        ) as mock_usecase_class,
        patch("argparse.ArgumentParser.parse_args") as mock_parse_args,
    ):
        # Configure mock arguments to have refresh = True
        mock_args = MagicMock()
        mock_args.refresh = True
        mock_parse_args.return_value = mock_args

        mock_engine = MagicMock()
        mock_engine.url = "sqlite:///:memory:"
        mock_engine.dialect.name = "sqlite"

        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        mock_usecase = MagicMock()

        async def mock_execute(*args, **kwargs):
            pass

        mock_usecase.execute = MagicMock(side_effect=mock_execute)
        mock_usecase_class.return_value = mock_usecase

        with patch("infrastructure.database.engine", new=mock_engine):
            run_cli()

            mock_init_db.assert_called_once()
            mock_usecase_class.assert_called_once()
            mock_usecase.execute.assert_called_once_with(refresh=True)
