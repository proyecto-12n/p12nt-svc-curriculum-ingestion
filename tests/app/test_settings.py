from app.config import Settings


class TestSettings:
    def test_given_project_name_when_created_then_uses_override_and_env_file_config(
        self,
    ):
        settings = Settings(PROJECT_NAME="test-project")

        assert settings.PROJECT_NAME == "test-project"
        assert settings.model_config.get("env_file") == ".env"
        assert settings.model_config.get("case_sensitive") is False
