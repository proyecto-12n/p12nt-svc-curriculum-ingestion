# -*- coding: utf-8 -*-
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.config import settings


@patch("main.init_db")
def test_health_check(mock_init_db):
    from app.main import app

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": settings.PROJECT_NAME}
