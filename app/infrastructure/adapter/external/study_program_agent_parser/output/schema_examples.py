from typing import Any

from pydantic import ConfigDict


def schema_examples(*examples: dict[str, Any]) -> ConfigDict:
    return ConfigDict(extra="allow", json_schema_extra={"examples": list(examples)})
