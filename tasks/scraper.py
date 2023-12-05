import tempfile
from functools import wraps
from pprint import pprint
from time import sleep
from typing import Optional

import requests

from open_ai_connector.const import OpenAiModels
from open_ai_connector.open_ai_connector import OpenAIConnector
from solver.prompt_builder import prepare_prompt
from solver.solver import Solver

ASSISTANT_CONTENT = "This is the source of your knowledge {context}"
USER_CONTENT = "{question}"


def count_calls(func):
    @wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.calls += 1
        print(
            f"Function {func.__name__!r} has been called: {wrapper_count_calls.calls} times"
        )
        return func(*args, **kwargs)

    wrapper_count_calls.calls = 0
    return wrapper_count_calls


@count_calls
def recursively_call_if_status_code_is_not_ok(url: str) -> Optional[str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        pprint(f"Status code: {response.status_code}")
        sleep(1)
        recursively_call_if_status_code_is_not_ok(url)
    else:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt",
            dir=tempfile.gettempdir(),
            mode="w+b",
        ) as temp_file:
            temp_file.write(response.content)
            temp_file.seek(0)
            context_from_data = [line.decode("utf-8")
                                 for line in temp_file.readlines()]
            return context_from_data[0]  # Only one line


def scraper(input_data: dict) -> dict:
    document_url = input_data["input"]
    print(document_url)
    question = input_data["question"]
    print(f"question: {question}")
    context = recursively_call_if_status_code_is_not_ok(document_url)
    print(f"context: {context}")

    oai = OpenAIConnector()
    prompt = prepare_prompt(
        ASSISTANT_CONTENT.format(context=context),
        USER_CONTENT.format(question=question),
    )
    answer = oai.generate_answer(
        model=OpenAiModels.gpt4.value, messages=prompt)
    print(f"answer: {answer}")
    prepared_answer = {"answer": answer}
    print(f"prepared answer: {prepared_answer}")
    return prepared_answer


if __name__ == "__main__":
    sol = Solver("scraper")
    sol.solve(scraper)
