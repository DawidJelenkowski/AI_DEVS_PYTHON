from __future__ import annotations
import os
import asyncio
import json
from dotenv import load_dotenv, find_dotenv
from typing import List, Any

from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import (
    Collaborator,
    Comment,
    CompletedItems,
    Label,
    Project,
    QuickAddResult,
    Section,
    Task,
)
from todoist_api_python.utils import run_async


class TodoistAPIAsync:
    def __init__(self, token: str) -> None:
        load_dotenv(find_dotenv())
        self._api = TodoistAPI(os.getenv("TODOIST_API_KEY"))

    @staticmethod
    def convert_objects_to_json(objects: List[Any]) -> str:
        objects_as_dicts: List[dict] = [vars(obj) for obj in objects]
        return json.dumps(objects_as_dicts, indent=4)

    async def get_projects(self) -> List[Project]:
        return await run_async(lambda: self._api.get_projects())


if __name__ == "__main__":
    async def main():
        manager = TodoistAPIAsync(os.getenv("TODOIST_API_KEY"))
        projects = await manager.get_projects()
        json_string = manager.convert_objects_to_json(projects)
        print(json_string)

    asyncio.run(main())
