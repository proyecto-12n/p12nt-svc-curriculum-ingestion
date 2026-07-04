# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from unittest.mock import MagicMock, patch

from app.config import Settings
from app.utils import log_execution_time
from domain.exceptions import EntityNotFoundException, DomainException
from domain.model import Curriculum, Modality
from domain.model.study_program import StudyProgram
from domain.port.outbound.knowledge_repository import KnowledgeRepository
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


def test_curriculum_repository_protocol():
    from domain.port.outbound import (
        SubjectRepository,
        GradeLevelRepository,
        StudyProgramRefRepository,
        StudyProgramRepository,
    )

    class DummyCurriculumRepo(KnowledgeRepository[Curriculum]):
        pass

    repo1 = DummyCurriculumRepo()
    repo1.find_by_url("url")
    repo1.save(None)

    class DummyModalityRepo(KnowledgeRepository[Modality]):
        pass

    repo2 = DummyModalityRepo()
    repo2.find_by_url("url")
    repo2.save(None)

    class DummySubjectRepo(SubjectRepository):
        pass

    repo3 = DummySubjectRepo()
    repo3.find_subject_by_title_and_modality("title", 1)
    repo3.save_subject(None)

    class DummyGradeLevelRepo(GradeLevelRepository):
        pass

    repo4 = DummyGradeLevelRepo()
    repo4.find_grade_level_by_title_and_subject("title", 1)
    repo4.save_grade_level(None)

    class DummyStudyProgramRefRepo(StudyProgramRefRepository):
        pass

    repo5 = DummyStudyProgramRefRepo()
    repo5.find_study_program_ref_by_url("url")
    repo5.save_study_program_ref(None)

    class DummyStudyProgramRepo(StudyProgramRepository):
        pass

    repo6 = DummyStudyProgramRepo()
    repo6.find_study_program_by_url("url")
    repo6.save_study_program(None)
