import json
from importlib import resources
from pathlib import Path
from typing import Any, cast

import yaml
from jsonschema import Draft202012Validator

from infra_conformance.models import Scenario


def _load_schema() -> dict[str, Any]:
    schema_file = resources.files("infra_conformance.contracts").joinpath("scenario.schema.json")
    return cast(dict[str, Any], json.loads(schema_file.read_text(encoding="utf-8")))


def load_scenario(path: Path) -> Scenario:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(_load_schema())
    errors = sorted(validator.iter_errors(raw), key=lambda error: list(error.path))
    if errors:
        details = "; ".join(error.message for error in errors)
        raise ValueError(f"Scenario contract validation failed: {details}")
    return Scenario.model_validate(raw)
