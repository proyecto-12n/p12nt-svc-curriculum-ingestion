from unittest.mock import MagicMock, patch


from app import main


class TestMain:
    def test_given_health_check_when_called_then_returns_service_status(self):
        response = main.health_check()

        assert response == {
            "status": "healthy",
            "service": main.settings.PROJECT_NAME,
        }

    async def test_given_lifespan_when_entered_then_initializes_database(self):
        with patch.object(main, "init_db") as init_db:
            async with main.lifespan(MagicMock()):
                init_db.assert_called_once_with()

    def test_given_app_when_created_then_registers_health_route(self):
        paths = {route.path for route in main.app.routes if hasattr(route, "path")}

        assert "/health" in paths
