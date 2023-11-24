from typing import Callable, Dict
from langchain.chains.openai_functions import (
    convert_to_openai_function,
    get_openai_output_parser,
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

llm = ChatOpenAI(model="gpt-4", temperature=0)

multiply_schema = {
    "name": "multiply",
    "description": "Multiply two numbers",
    "parameters": {
        "type": "object",
        "properties": {
            "first": {
                "type": "number",
                "description": "First value to multiply"
            },
            "second": {
                "type": "number",
                "description": "Second value to multiply"
            }
        },
        "required": [
            "first", "second"
        ]
    }
}
add_schema = {
    "name": "add",
    "description": "Add two numbers",
    "parameters": {
        "type": "object",
        "properties": {
            "first": {
                "type": "number",
                "description": "First value to add"
            },
            "second": {
                "type": "number",
                "description": "Second value to add"
            }
        },
        "required": [
            "first", "second"
        ]
    }
}
subtract_schema = {
    "name": "subtract",
    "description": "Subtract two numbers",
    "parameters": {
        "type": "object",
        "properties": {
            "first": {
                "type": "number",
                "description": "First value to subtract"
            },
            "second": {
                "type": "number",
                "description": "Second value to subtract"
            }
        },
        "required": [
            "first", "second"
        ]
    }
}


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a world class algorithm for recording entities."),
        (
            "human",
            "Make calls to the relevant function to record the entities in the following input: {input}",
        ),
        ("human", "Tip: Make sure to answer in the correct format"),
    ]
)


class Tools:
    def __init__(self) -> None:
        self.methods: Dict[str, Callable[[float, float], float]] = {
            'add': self.add,
            'subtract': self.subtract,
            'multiply': self.multiply
        }

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def execute(self, method_name: str, a: float, b: float) -> float:
        if method_name in self.methods:
            return self.methods[method_name](a, b)
        else:
            raise ValueError(f"Method {method_name} not found")


openai_functions = [convert_to_openai_function(f) for f in (
    add_schema, multiply_schema, subtract_schema)]
llm_kwargs = {"functions": openai_functions}
if len(openai_functions) == 1:
    llm_kwargs["function_call"] = {"name": openai_functions[0]["name"]}
output_parser = get_openai_output_parser(
    (add_schema, multiply_schema, subtract_schema))
runnable = prompt | llm.bind(**llm_kwargs) | output_parser

action = runnable.invoke({"input": "2929590 * 129359"})

tools = Tools()

# Extract the method name and arguments from the action
method_name = action.get('name')
args = action.get('arguments')

# Check if the method name exists in the Tools methods and if the arguments are valid
if method_name in tools.methods and args is not None:
    # Extract the individual arguments
    first_arg = args.get('first')
    second_arg = args.get('second')

    # Execute the method from Tools class with the given arguments
    try:
        result = tools.execute(method_name, first_arg, second_arg)
        print(f"The result is {result}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Invalid method name or arguments")
