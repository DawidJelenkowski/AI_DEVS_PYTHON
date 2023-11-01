"""
Napisz wpis na bloga (w języku polskim) na temat przyrządzania pizzy Margherity. Zadanie w API nazywa się ”blogger”.
Jako wejście otrzymasz spis 4 rozdziałów, które muszą pojawić się we wpisie.
Jako odpowiedź musisz zwrócić tablicę (w formacie JSON) złożoną z 4 pól reprezentujących te cztery rozdziały, np.: {"answer":["tekst 1","tekst 2","tekst 3","tekst 4"]}
"""
import os
import requests
import ast
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

APIKEY = os.getenv("AI_DEVS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = OpenAI(openai_api_key=OPENAI_API_KEY)


def get_token(task):
    # Define the API endpoint and the data to send
    quest_url = f"https://zadania.aidevs.pl/token/{task}"
    data = {"apikey": APIKEY}

    # Send the POST request
    quest_response = requests.post(quest_url, json=data)

    # Check the response status code and content
    if quest_response.status_code == 200:
        token_data = quest_response.json()
        token = token_data["token"]
        print("Token received:", token)
    else:
        print("Request failed with status code:", quest_response.status_code)

    return token


def ask_gpt(response):
    template = """
        Take a deep breath and write content (in Polish) about making Margherita pizza, for the each provided outline, you can only use one sentence for each outline.
        Each record in array should contain content, as shown in the example. Return only created array.
        example```
        ["content 1","content 2","content 3","content 4"]
        """
    human_template = "{text}"

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", human_template)
    ])

    chain = chat_prompt | ChatOpenAI()
    output = chain.invoke(
        {"text": f"'{response['blog']}'"})
    answer = output.content

    return answer


def get_task(token):
    # Define the URL
    token_url = f"https://zadania.aidevs.pl/task/{token}"
    # Send a GET request
    token_response = requests.get(token_url)

    # Check the response status code and content
    if token_response.status_code == 200:
        print("Request was successful")
        print("Response:", token_response.text)

        response = token_response.json()

        answer = ask_gpt(response)
        return answer

    else:
        print("Request failed with status code:", token_response.status_code)


def answer_submission(token, answer):
    # Construct the new URL using the received token
    token_url = f"https://zadania.aidevs.pl/answer/{token}"

    cleaned_answer = ast.literal_eval(answer)

    data = {"answer": cleaned_answer}
    # Send a POST request to the new URL
    token_response = requests.post(token_url, json=data)

    # Check the response status code and content
    if token_response.status_code == 200:
        print("Answer submission was successful")
        response = token_response.json()
        print("Response:", response)

    else:
        print("Answer submission failed with status code:",
              token_response.status_code)
        print(token_response.json())

    return data


if __name__ == "__main__":
    # run only the first 2 functions
    token = get_token("blogger")
    answer = get_task(token)
    answer_submission(token, answer)
