
import sys
sys.path.append("/home/xbloc/respos/2nd-devs-python/solver")
sys.path.append("/home/xbloc/respos/2nd-devs-python/open_ai_connector")
from pydantic import BaseModel
from fastapi import FastAPI

from solver.prompt_builder import prepare_prompt
from solver.solver import Solver
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

ASSISTANT_CONTENT = '''
User can pass the information or ask the question. Based on data:
###  
{knowledge}
###
Or based on your knowledge
answer the question ultra-briefly.'''
USER_CONTENT = "{question}"


class Question(BaseModel):
    question: str


app = FastAPI()


def save_as_memory(info: str):
    with open('knowledge.txt', 'w') as file:
        file.write(info)


def read_from_memory() -> str:
    with open('knowledge.txt', 'r') as file:
        knowledge = file.read()
        return knowledge


@app.post("/ask-question/")
def handle_question(question_data: Question):
    # Process the question here
    question = question_data.question
    knowledge = ''
    if '?' not in question:
        save_as_memory(question)
    else:
        knowledge += read_from_memory()
    oai = OpenAIConnector()
    prompt = prepare_prompt(
        ASSISTANT_CONTENT.format(knowledge=knowledge),
        USER_CONTENT.format(question=question),
    )
    answer = oai.generate_answer(
        model='gpt-4', messages=prompt)
    prepared_answer = {"reply": answer}
    return prepared_answer


def solverr():
    url = "http://127.0.0.1:8000/ask-question/"
    sol = Solver("ownapi")
    sol.authorize()
    prepared_answer = {"answer": url}
    sol.solve(answer=prepared_answer)


if __name__ == '__main__':
    solverr()
