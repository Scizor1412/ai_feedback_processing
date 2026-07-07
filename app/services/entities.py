"""Load known schools and services from SCHOOLS_DEPARTMENTS.json at import time."""
import json
from pathlib import Path

_path = Path(__file__).parent.parent.parent / "DUMMY_DATA" / "SCHOOLS_DEPARTMENTS.json"
_data = json.loads(_path.read_text())

# {id: name}
SCHOOLS: dict[str, str] = {s["id"]: s["name"] for s in _data["schools"]}
SERVICES: dict[str, str] = {s["id"]: s["name"] for s in _data["services"]}

# {id: (name, entity_type_str)}
ALL_ENTITIES: dict[str, tuple[str, str]] = {
    **{id_: (name, "school") for id_, name in SCHOOLS.items()},
    **{id_: (name, "service") for id_, name in SERVICES.items()},
}
