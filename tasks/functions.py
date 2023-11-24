"""
Wykonaj zadanie o nazwie functions zgodnie ze standardem zgłaszania odpowiedzi opisanym na zadania.aidevs.pl. 
Zadanie polega na zdefiniowaniu funkcji o nazwie addUser, 
która przyjmuje jako parametr obiekt z właściwościami: imię (name, string), nazwisko (surname, string) 
oraz rok urodzenia osoby (year, integer). 
Jako odpowiedź musisz wysłać jedynie ciało funkcji w postaci JSON-a. 
Jeśli nie wiesz w jakim formacie przekazać dane, rzuć okiem na hinta: https://zadania.aidevs.pl/hint/functions 
"""
from open_ai_connector.const import OpenAiModels
from open_ai_connector.open_ai_connector import OpenAIConnector
from solver.prompt_builder import prepare_prompt
from solver.solver import Solver


ASSISTANT_CONTENT = ""
USER_CONTENT = "I would like to add user Jerzy Urban that was born in 1933"


FUNCTIONS = {
    "name": "addUser",
    "description": "Add user to stdout",
    "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the user",
                },
                "surname": {
                    "type": "string",
                    "description": "Surname of the user",
                },
                "year": {
                    "type": "integer",
                    "description": "Year of born",
                },
            },
        "required": ["name", "surname", "year"],
    },
    "name": "facts",
    "description": "Return 7 interesting facts about the city given by the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "array",
                "description": "facts",
                "items": {"type": "string"}
            },
            "required": "facts"
        },
    }
}


def addUser(name: str, surname: str, year: int) -> None:
    print(f"I'm adding user {name}, {surname}, that was born in {year}")


def functions(input_data: dict):
    oai = OpenAIConnector()
    prompt = prepare_prompt(
        ASSISTANT_CONTENT,
        USER_CONTENT,
    )
    name_of_the_function, arguments = oai.function_calls(
        model=OpenAiModels.gpt4.value, messages=prompt, functions=FUNCTIONS
    )
    func_to_call = eval(name_of_the_function)
    func_to_call(**arguments)
    prepared_answer = {"answer": FUNCTIONS[0]}
    return prepared_answer


if __name__ == "__main__":
    sol = Solver("functions")
    sol.solve(functions)
