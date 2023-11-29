from todoist_api_python.api import TodoistAPI
import os
import json
from dotenv import load_dotenv, find_dotenv
from utils import convert_objects_to_json

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    manager = TodoistAPI(os.getenv("TODOIST_API_KEY"))
    projects = manager.get_tasks()
    json_string = convert_objects_to_json(projects)
    print(json_string)
