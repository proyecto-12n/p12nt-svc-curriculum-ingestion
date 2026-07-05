from unittest.mock import MagicMock, patch

from infrastructure import database


class TestDatabase:
    def test_given_session_when_get_db_then_closes_after_use(self):
        session = MagicMock()

        with patch.object(database, "SessionLocal", return_value=session):
            db = database.get_db()
            assert next(db) is session
            try:
                next(db)
            except StopIteration:
                pass

        session.close.assert_called_once_with()

    def test_given_non_postgresql_engine_when_init_db_then_creates_tables(self):
        engine = MagicMock()
        engine.url = "sqlite:///:memory:"

        with (
            patch.object(database, "engine", engine),
            patch("sqlmodel.SQLModel.metadata.create_all") as create_all,
        ):
            database.init_db()

        create_all.assert_called_once_with(engine)
