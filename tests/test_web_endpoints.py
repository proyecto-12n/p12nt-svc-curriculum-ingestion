# -*- coding: utf-8 -*-
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.domain.model import (
    Curriculum,
    Modality,
    Subject,
    GradeLevel,
    StudyProgramRef,
    StudyProgram,
)
from app.infrastructure.database import get_db


@pytest.fixture(name="db_session")
def db_session_fixture():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    # Remove schema from table metadata so it works with SQLite
    for table in SQLModel.metadata.tables.values():
        table.schema = None
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@patch("app.main.init_db")
def test_curriculum_endpoints(mock_init_db, db_session):
    from app.main import app
    from app.infrastructure.adapter.outbound.db import SqlCurriculumRepositoryAdapter

    # Seed database
    repo = SqlCurriculumRepositoryAdapter(db_session)
    curr = Curriculum(
        id=1, url="http://test.url/cur", title="Initial Curriculum", content="Init"
    )
    saved_curr = repo.save_curriculum(curr)

    # Dependency override
    app.dependency_overrides[get_db] = lambda: db_session

    client = TestClient(app)

    # Test list
    response = client.get("/api/v1/curriculums")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["url"] == "http://test.url/cur"

    # Test get by ID
    response = client.get(f"/api/v1/curriculums/{saved_curr.id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Initial Curriculum"

    # Test 404
    response = client.get("/api/v1/curriculums/999")
    assert response.status_code == 404

    # Clean up overrides
    app.dependency_overrides.clear()


@patch("app.main.init_db")
def test_modality_endpoints(mock_init_db, db_session):
    from app.main import app
    from app.infrastructure.adapter.outbound.db import (
        SqlCurriculumRepositoryAdapter,
        SqlModalityRepositoryAdapter,
    )

    curr_repo = SqlCurriculumRepositoryAdapter(db_session)
    mod_repo = SqlModalityRepositoryAdapter(db_session)

    curr = Curriculum(id=1, url="http://test.url/cur", title="Cur", content="Init")
    saved_curr = curr_repo.save_curriculum(curr)

    mod = Modality(
        id=10,
        curriculum_id=saved_curr.id,
        url="http://test.url/mod",
        title="Mod",
        content="Init",
    )
    saved_mod = mod_repo.save_modality(mod)

    app.dependency_overrides[get_db] = lambda: db_session
    client = TestClient(app)

    # List all modalities
    response = client.get("/api/v1/modalities")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Filter by curriculum ID
    response = client.get(f"/api/v1/modalities?curriculum_id={saved_curr.id}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/api/v1/modalities?curriculum_id=99")
    assert response.status_code == 200
    assert len(response.json()) == 0

    # Get by ID
    response = client.get(f"/api/v1/modalities/{saved_mod.id}")
    assert response.status_code == 200
    assert response.json()["url"] == "http://test.url/mod"

    # Get by ID 404
    response = client.get("/api/v1/modalities/999")
    assert response.status_code == 404

    app.dependency_overrides.clear()


@patch("app.main.init_db")
def test_subject_endpoints(mock_init_db, db_session):
    from app.main import app
    from app.infrastructure.adapter.outbound.db import (
        SqlCurriculumRepositoryAdapter,
        SqlModalityRepositoryAdapter,
        SqlSubjectRepositoryAdapter,
    )

    curr_repo = SqlCurriculumRepositoryAdapter(db_session)
    mod_repo = SqlModalityRepositoryAdapter(db_session)
    sub_repo = SqlSubjectRepositoryAdapter(db_session)

    curr = Curriculum(id=1, url="http://test.url/cur", title="Cur", content="Init")
    saved_curr = curr_repo.save_curriculum(curr)

    mod = Modality(
        id=10,
        curriculum_id=saved_curr.id,
        url="http://test.url/mod",
        title="Mod",
        content="Init",
    )
    saved_mod = mod_repo.save_modality(mod)

    sub = Subject(
        id=100,
        modality_id=saved_mod.id,
        url="http://test.url/sub",
        title="Math",
        content="Init",
    )
    saved_sub = sub_repo.save_subject(sub)

    app.dependency_overrides[get_db] = lambda: db_session
    client = TestClient(app)

    # List all subjects
    response = client.get("/api/v1/subjects")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Filter by modality ID
    response = client.get(f"/api/v1/subjects?modality_id={saved_mod.id}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Get by ID
    response = client.get(f"/api/v1/subjects/{saved_sub.id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Math"

    app.dependency_overrides.clear()


@patch("app.main.init_db")
def test_grade_level_endpoints(mock_init_db, db_session):
    from app.main import app
    from app.infrastructure.adapter.outbound.db import (
        SqlCurriculumRepositoryAdapter,
        SqlModalityRepositoryAdapter,
        SqlSubjectRepositoryAdapter,
        SqlGradeLevelRepositoryAdapter,
    )

    curr_repo = SqlCurriculumRepositoryAdapter(db_session)
    mod_repo = SqlModalityRepositoryAdapter(db_session)
    sub_repo = SqlSubjectRepositoryAdapter(db_session)
    grade_repo = SqlGradeLevelRepositoryAdapter(db_session)

    curr = Curriculum(id=1, url="http://test.url/cur", title="Cur", content="Init")
    saved_curr = curr_repo.save_curriculum(curr)

    mod = Modality(
        id=10,
        curriculum_id=saved_curr.id,
        url="http://test.url/mod",
        title="Mod",
        content="Init",
    )
    saved_mod = mod_repo.save_modality(mod)

    sub = Subject(
        id=100,
        modality_id=saved_mod.id,
        url="http://test.url/sub",
        title="Math",
        content="Init",
    )
    saved_sub = sub_repo.save_subject(sub)

    grade = GradeLevel(
        id=1000,
        subject_id=saved_sub.id,
        url="http://test.url/grade",
        title="1st Grade",
        content="Init",
    )
    saved_grade = grade_repo.save_grade_level(grade)

    app.dependency_overrides[get_db] = lambda: db_session
    client = TestClient(app)

    # List all grade levels
    response = client.get("/api/v1/grade-levels")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Filter by subject ID
    response = client.get(f"/api/v1/grade-levels?subject_id={saved_sub.id}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Get by ID
    response = client.get(f"/api/v1/grade-levels/{saved_grade.id}")
    assert response.status_code == 200
    assert response.json()["title"] == "1st Grade"

    app.dependency_overrides.clear()


@patch("app.main.init_db")
def test_study_program_ref_endpoints(mock_init_db, db_session):
    from app.main import app
    from app.infrastructure.adapter.outbound.db import (
        SqlCurriculumRepositoryAdapter,
        SqlModalityRepositoryAdapter,
        SqlSubjectRepositoryAdapter,
        SqlGradeLevelRepositoryAdapter,
        SqlStudyProgramRefRepositoryAdapter,
    )

    curr_repo = SqlCurriculumRepositoryAdapter(db_session)
    mod_repo = SqlModalityRepositoryAdapter(db_session)
    sub_repo = SqlSubjectRepositoryAdapter(db_session)
    grade_repo = SqlGradeLevelRepositoryAdapter(db_session)
    ref_repo = SqlStudyProgramRefRepositoryAdapter(db_session)

    curr = Curriculum(id=1, url="http://test.url/cur", title="Cur", content="Init")
    saved_curr = curr_repo.save_curriculum(curr)

    mod = Modality(
        id=10,
        curriculum_id=saved_curr.id,
        url="http://test.url/mod",
        title="Mod",
        content="Init",
    )
    saved_mod = mod_repo.save_modality(mod)

    sub = Subject(
        id=100,
        modality_id=saved_mod.id,
        url="http://test.url/sub",
        title="Math",
        content="Init",
    )
    saved_sub = sub_repo.save_subject(sub)

    grade = GradeLevel(
        id=1000,
        subject_id=saved_sub.id,
        url="http://test.url/grade",
        title="1st Grade",
        content="Init",
    )
    saved_grade = grade_repo.save_grade_level(grade)

    ref = StudyProgramRef(
        id=2000,
        grade_level_id=saved_grade.id,
        url="http://test.url/ref",
        title="Ref",
        content="Init",
    )
    saved_ref = ref_repo.save_study_program_ref(ref)

    app.dependency_overrides[get_db] = lambda: db_session
    client = TestClient(app)

    # List all study program refs
    response = client.get("/api/v1/study-program-refs")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Filter by grade level ID
    response = client.get(f"/api/v1/study-program-refs?grade_level_id={saved_grade.id}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Get by ID
    response = client.get(f"/api/v1/study-program-refs/{saved_ref.id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Ref"

    app.dependency_overrides.clear()


@patch("app.main.init_db")
def test_study_program_endpoints(mock_init_db, db_session):
    from app.main import app
    from app.infrastructure.adapter.outbound.db import (
        SqlCurriculumRepositoryAdapter,
        SqlModalityRepositoryAdapter,
        SqlSubjectRepositoryAdapter,
        SqlGradeLevelRepositoryAdapter,
        SqlStudyProgramRefRepositoryAdapter,
        SqlStudyProgramRepositoryAdapter,
    )

    curr_repo = SqlCurriculumRepositoryAdapter(db_session)
    mod_repo = SqlModalityRepositoryAdapter(db_session)
    sub_repo = SqlSubjectRepositoryAdapter(db_session)
    grade_repo = SqlGradeLevelRepositoryAdapter(db_session)
    ref_repo = SqlStudyProgramRefRepositoryAdapter(db_session)
    prog_repo = SqlStudyProgramRepositoryAdapter(db_session)

    curr = Curriculum(id=1, url="http://test.url/cur", title="Cur", content="Init")
    saved_curr = curr_repo.save_curriculum(curr)

    mod = Modality(
        id=10,
        curriculum_id=saved_curr.id,
        url="http://test.url/mod",
        title="Mod",
        content="Init",
    )
    saved_mod = mod_repo.save_modality(mod)

    sub = Subject(
        id=100,
        modality_id=saved_mod.id,
        url="http://test.url/sub",
        title="Math",
        content="Init",
    )
    saved_sub = sub_repo.save_subject(sub)

    grade = GradeLevel(
        id=1000,
        subject_id=saved_sub.id,
        url="http://test.url/grade",
        title="1st Grade",
        content="Init",
    )
    saved_grade = grade_repo.save_grade_level(grade)

    ref = StudyProgramRef(
        id=2000,
        grade_level_id=saved_grade.id,
        url="http://test.url/ref",
        title="Ref",
        content="Init",
    )
    saved_ref = ref_repo.save_study_program_ref(ref)

    prog = StudyProgram(
        id=3000,
        study_program_ref_id=saved_ref.id,
        url="http://test.url/prog",
        title="Math Program",
        content=b"test PDF data",
        checksum="12345",
    )
    saved_prog = prog_repo.save_study_program(prog)

    app.dependency_overrides[get_db] = lambda: db_session
    client = TestClient(app)

    # List all study programs
    response = client.get("/api/v1/study-programs")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Filter by study program ref ID
    response = client.get(f"/api/v1/study-programs?study_program_ref_id={saved_ref.id}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Get by ID
    response = client.get(f"/api/v1/study-programs/{saved_prog.id}")
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["title"] == "Math Program"
    # Verify base64 content
    import base64

    assert base64.b64decode(res_data["content"]) == b"test PDF data"

    app.dependency_overrides.clear()
