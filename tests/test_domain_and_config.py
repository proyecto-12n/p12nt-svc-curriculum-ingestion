# -*- coding: utf-8 -*-
import pytest
import logging
from datetime import datetime
from unittest.mock import MagicMock, patch

from app.domain.exceptions import EntityNotFoundException, DomainException
from app.domain.model.study_program import StudyProgram
from app.config import Settings, settings
from app.utils import log_execution_time
from app.infrastructure.database import get_db
from app.domain.port.outbound.curriculum_repository import CurriculumRepository


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
        extracted_at=datetime.now()
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
    assert s.Config.env_file == ".env"
    assert s.Config.case_sensitive is True


def test_get_db():
    with patch("app.infrastructure.database.SessionLocal") as mock_session_maker:
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
    class DummyRepository(CurriculumRepository):
        pass
    
    repo = DummyRepository()
    repo.find_curriculum_by_url("url")
    repo.save_curriculum(None)
    repo.find_modality_by_url("url")
    repo.save_modality(None)
    repo.find_subject_by_title_and_modality("title", 1)
    repo.save_subject(None)
    repo.find_grade_level_by_title_and_subject("title", 1)
    repo.save_grade_level(None)
    repo.find_study_program_ref_by_url("url")
    repo.save_study_program_ref(None)
    repo.find_study_program_by_url("url")
    repo.save_study_program(None)
