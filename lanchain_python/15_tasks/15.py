import os
import sys
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv, find_dotenv
from utils import convert_objects_to_json, current_date
from schema import get_tasks_schema, add_tasks_schema, finish_tasks_schema, update_tasks_schema
from langchain.chains.openai_functions import (
    convert_to_openai_function,
    get_openai_output_parser,
)

manager = TodoistAPI(os.getenv("TODOIST_API_KEY"))

sys.path.append(r'/home/xbloc/respos/2nd-devs-python/lanchain_python/15_tasks')

load_dotenv(find_dotenv())


projects = manager.get_projects()
json_string = convert_objects_to_json(projects)
print(json_string)
