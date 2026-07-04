# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from app.config import Settings
from app.utils import log_execution_time
from domain.exceptions import EntityNotFoundException, DomainException
from domain.model import Curriculum, Modality, Subject, GradeLevel, StudyProgramRef
from domain.model.study_program import StudyProgram
from domain.port.outbound.curriculum_hierarchy_repository import (
    CurriculumHierarchyRepository,
)
from infrastructure.database import get_db


def test_entity_not_found_exception():
    exc = EntityNotFoundException(42)
    assert "42" in str(exc)
    assert isinstance(exc, DomainException)


def test_study_program_md5sum():
    prog = StudyProgram(
        id=1,
        study_program_ref_id=2,
        url="http://test",
        title="test",
        content=b"test",
        checksum="my-checksum",
        extracted_at=datetime.now(),
    )
    assert prog.md5sum == "my-checksum"


def test_log_execution_time(caplog):
    @log_execution_time
    def dummy_func(x):
        return x + 1

    with caplog.at_level(logging.INFO):
        res = dummy_func(5)
    assert res == 6
    assert any("dummy_func took" in record.message for record in caplog.records)


def test_settings():
    s = Settings(PROJECT_NAME="test-project")
    assert s.PROJECT_NAME == "test-project"
    assert s.model_config.get("env_file") == ".env"
    assert s.model_config.get("case_sensitive") is False


def test_get_db():
    with patch("infrastructure.database.SessionLocal") as mock_session_maker:
        mock_session = MagicMock()
        mock_session_maker.return_value = mock_session

        db_generator = get_db()
        db = next(db_generator)
        assert db == mock_session

        try:
            next(db_generator)
        except StopIteration:
            pass
        mock_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_curriculum_repository_protocol():
    class DummyCurriculumRepo(CurriculumHierarchyRepository[Curriculum]):
        pass

    repo1 = DummyCurriculumRepo()
    await repo1.find_by_url("url")
    await repo1.save(None)

    class DummyModalityRepo(CurriculumHierarchyRepository[Modality]):
        pass

    repo2 = DummyModalityRepo()
    await repo2.find_by_url("url")
    await repo2.save(None)

    class DummySubjectRepo(CurriculumHierarchyRepository[Subject]):
        pass

    repo3 = DummySubjectRepo()
    await repo3.find_by_url("url")
    await repo3.save(None)

    class DummyGradeLevelRepo(CurriculumHierarchyRepository[GradeLevel]):
        pass

    repo4 = DummyGradeLevelRepo()
    await repo4.find_by_url("url")
    await repo4.save(None)

    class DummyStudyProgramRefRepo(CurriculumHierarchyRepository[StudyProgramRef]):
        pass

    repo5 = DummyStudyProgramRefRepo()
    await repo5.find_by_url("url")
    await repo5.save(None)

    class DummyStudyProgramRepo(CurriculumHierarchyRepository[StudyProgram]):
        pass

    repo6 = DummyStudyProgramRepo()
    await repo6.find_by_url("url")
    await repo6.save(None)
