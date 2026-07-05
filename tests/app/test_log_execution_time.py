import logging

from app.utils import log_execution_time


class TestLogExecutionTime:
    def test_given_decorated_function_when_called_then_returns_value_and_logs_duration(
        self, caplog
    ):
        @log_execution_time
        def add_one(value):
            return value + 1

        with caplog.at_level(logging.INFO):
            result = add_one(1)

        assert result == 2
        assert any("add_one took" in record.message for record in caplog.records)
