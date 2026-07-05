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

    def test_given_postgresql_engine_when_init_db_then_ensures_schema(self):
        engine = MagicMock()
        engine.url = "postgresql://test"
        connection = MagicMock()
        engine.connect.return_value.__enter__.return_value = connection

        with (
            patch.object(database, "engine", engine),
            patch("sqlmodel.SQLModel.metadata.create_all"),
        ):
            database.init_db()

        executed_sql = [str(call.args[0]) for call in connection.execute.call_args_list]
        assert any("CREATE SCHEMA" in statement for statement in executed_sql)
        connection.commit.assert_called_once_with()
