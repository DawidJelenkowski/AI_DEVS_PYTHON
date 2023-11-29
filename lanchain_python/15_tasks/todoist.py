import json
import os
from typing import Any, List, Dict
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Project, Task
from dotenv import load_dotenv, find_dotenv


class TodoistManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TodoistManager, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.initialize_client()
        return cls._instance

    def initialize_client(self) -> None:
        load_dotenv(find_dotenv())
        self.api = TodoistAPI(os.getenv("TODOIST_API_KEY"))

    def get_projects(self) -> List[Project]:
        try:
            return self.api.get_projects()
        except Exception as error:
            print(error)
            return []

    @staticmethod
    def convert_objects_to_json(objects: List[Any]) -> str:
        objects_as_dicts: List[dict] = [vars(obj) for obj in objects]
        return json.dumps(objects_as_dicts, indent=4)

    def add_project(self, name: str) -> Project:
        try:
            return self.api.add_project(name=name)
        except Exception as error:
            print(error)
            return None

    def get_project_id(self, project_name: str) -> str:
        projects = self.get_projects()
        for project in projects:
            if project.name == project_name:
                return project.id

        print("There is no such project")

    def add_new_task(self, content: str, project_id: str) -> Task:
        try:
            task = self.api.add_task(
                content=content,
                project_id=project_id)

            return task
        except Exception as error:
            print(error)

    def get_task_id(self, project_name: str, task: str) -> str:
        project_id = self.get_project_id(project_name)

    def update_task(self, task_id: str, due_string: str = None) -> Task:
        try:
            is_success = self.api.update_task(
                task_id=task_id,
                due_string=due_string)

            print(is_success)

        except Exception as error:
            print(error)

    def complete_task(self, task_id: int) -> Task:
        try:
            is_success = self.api.close_task(task_id=task_id)
            print(is_success)
        except Exception as error:
            print(error)


if __name__ == "__main__":
    manager = TodoistManager()
    projects = manager.get_projects()
    json_string = manager.convert_objects_to_json(projects)
    print(json_string)
project_id = manager.get_project_id("Home")
new_task = manager.add_new_task(
    content="Buy Milk",
    project_id=project_id)

# Use when you want to convert projects to JSON
# projects = manager.get_projects()
# output = manager.object_to_dict(projects)
# json_string = manager.convert_objects_to_json(output)
# print(json_string)
