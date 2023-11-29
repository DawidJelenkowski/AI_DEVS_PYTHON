import json
from typing import Any, List


def convert_objects_to_json(objects: list) -> str:
    objects_as_dicts: list = [vars(obj) for obj in objects]
    return json.dumps(objects_as_dicts, indent=4)
