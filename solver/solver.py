import os
from typing import Callable, Optional

import requests
from dotenv import load_dotenv

from solver.const import BASE_AUTH_URL, BASE_TASK_URL, BASE_ANSWER_URL
from solver.utils import find_dotenv


class Solver:
    def __init__(self, task) -> None:
        # Load environment variables from a .env file
        load_dotenv(dotenv_path=find_dotenv(
            os.path.dirname(os.path.abspath(__file__))))
        # API key for authentication
        self.api_key: str = os.getenv("AI_DEVS_API_KEY")
        self.task: str = task  # Task identifier
        self.url: str = BASE_AUTH_URL.format(task=task)  # Authentication URL
        # Token for API access, initially None
        self.token: Optional[str] = None
        # Data for the task, initially None
        self.input_data: Optional[dict] = None
        self.answer_from_api = None  # Placeholder for API's answer

    def authorize(self) -> None:
        # Authorize and get a token from the API
        data = {"apikey": self.api_key}
        response = requests.post(self.url, json=data)
        # Extract token from response
        self.token = dict(response.json())["token"]

    def download_input_data(self) -> None:
        # Download input data for the task using the token
        task_url = BASE_TASK_URL.format(token=self.token)
        response = requests.get(task_url)
        self.input_data = dict(response.json())  # Store the input data

    def post_data(self, question: str):
        # Post a question to the API and store the response
        task_url = BASE_TASK_URL.format(token=self.token)
        question_to_send = {"question": question}
        response = requests.post(task_url, data=question_to_send)
        self.answer_from_api = dict(response.json())

    def send_answer(self, solution: Callable, **kwargs):
        # Send the solution to the API and print the result
        if self.input_data:
            # If input data is available, use it for solving
            if kwargs != {}:
                # If additional data is provided, use it
                answer = solution(kwargs["additional_data"])
            else:
                # Use the input data for solving
                answer = solution(self.input_data)
        else:
            # If no input data, use the question and API's answer for solving
            answer = solution(kwargs["question"], self.answer_from_api)

        # Send the answer to the API and check the response
        response = requests.post(
            BASE_ANSWER_URL.format(token=self.token), json=answer)

        # Print the verdict based on the response
        if response.ok:
            print("Done, answer is correct 🚀")
        else:
            print("You failed")

    def solve(self, solving_func, **kwargs):
        # Main method to solve the task
        self.authorize()  # Authorize first
        if kwargs == {}:
            # If no additional arguments, download input data and solve
            self.download_input_data()
            self.send_answer(solving_func)
        elif "additional_data" in kwargs:
            # If additional data is provided, use it along with input data
            additional_data = kwargs.get("additional_data", None)
            self.download_input_data()
            self.send_answer(solving_func, additional_data=additional_data)
        else:
            # If a question is provided, post it and send the answer
            self.post_data(kwargs["question"])
            self.send_answer(solving_func, question=kwargs["question"])


if __name__ == "__main__":
    pass  # Do nothing if the script is run directly
