# -*- coding: utf-8 -*-
import pytest
from sqlmodel import SQLModel, create_engine, Session

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from infrastructure.adapter.outbound.db import (
    SqlCurriculumRepositoryAdapter,
    SqlGradeLevelRepositoryAdapter,
    SqlModalityRepositoryAdapter,
    SqlStudyProgramRefRepositoryAdapter,
    SqlStudyProgramRepositoryAdapter,
    SqlSubjectRepositoryAdapter,
    SqlCurriculumHierarchyRepositoryProviderAdapter,
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


def test_provider_resolves_all_repositories(session):
    provider = SqlCurriculumHierarchyRepositoryProviderAdapter(session)

    # Verify matching mappings
    assert isinstance(
        provider.get_repository(CurriculumHierarchyType.CURRICULUM),
        SqlCurriculumRepositoryAdapter,
    )
    assert isinstance(
        provider.get_repository(CurriculumHierarchyType.MODALITY),
        SqlModalityRepositoryAdapter,
    )
    assert isinstance(
        provider.get_repository(CurriculumHierarchyType.SUBJECT),
        SqlSubjectRepositoryAdapter,
    )
    assert isinstance(
        provider.get_repository(CurriculumHierarchyType.GRADE_LEVEL),
        SqlGradeLevelRepositoryAdapter,
    )
    assert isinstance(
        provider.get_repository(CurriculumHierarchyType.STUDY_PROGRAM_REF),
        SqlStudyProgramRefRepositoryAdapter,
    )
    assert isinstance(
        provider.get_repository(CurriculumHierarchyType.STUDY_PROGRAM),
        SqlStudyProgramRepositoryAdapter,
    )


def test_provider_raises_error_for_invalid_type(session):
    provider = SqlCurriculumHierarchyRepositoryProviderAdapter(session)

    with pytest.raises(ValueError) as excinfo:
        provider.get_repository("invalid_type")
    assert "No repository configured for edge type" in str(excinfo.value)
