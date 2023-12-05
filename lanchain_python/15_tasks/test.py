from langchain.chat_models import ChatOpenAI
from datetime import datetime
import os
import json
import requests
from todoist_api_python.api import TodoistAPI
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

api_todoist = TodoistAPI(os.getenv("TODOIST_API_KEY"))
client = OpenAI()
# Set your Todoist API token and OpenAI API key


def api_call(endpoint='/tasks', method='GET', body=None):
    """Generic function to make API calls to Todoist."""
    headers = {
        'Authorization': f'Bearer {api_todoist}',
        'Content-Type': 'application/json'
    }
    response = requests.request(
        method, f'https://api.todoist.com/rest/v2{endpoint}', headers=headers, json=body)
    return response.json() if response.status_code != 204 else {}


def list_uncompleted():
    """List uncompleted tasks from Todoist."""
    tasks = api_call('/tasks', 'GET')
    return tasks


def add_task(content, due_string=None):
    """Add a task to Todoist."""
    task = {'content': content, 'due_string': due_string}
    response = api_call('/tasks', 'POST', task)
    return response


def update_task(task_id, content=None, due_string=None):
    """Update a task in Todoist."""
    task = {'content': content, 'due_string': due_string}
    response = api_call(f'/tasks/{task_id}', 'POST', task)
    return response


def close_task(task_id):
    """Close a task in Todoist."""
    response = api_call(f'/tasks/{task_id}/close', 'POST')
    return response


def process_input(input_text):
    """Process the user input and interact with Todoist API."""
    response = client.chat.completions.create(model="gpt-4", temperature=1,
                                              messages=[
                                                  {"role": "system",
                                                   "content": f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"},
                                                  {"role": "user",
                                                      "content": input_text},
                                              ])
    # Logic to parse the response and call Todoist API functions
    # Needs to be implemented based on the specific use case and response structure

    return response


# Example usage
response = process_input(
    "I need to write a newsletter about GPT-4 on Monday, can you add it?")
print(response)
