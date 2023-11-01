"""
Skorzystaj z API zadania.aidevs.pl, aby pobrać dane zadania inprompt. 
Znajdziesz w niej dwie właściwości — input, czyli tablicę / listę zdań na temat różnych osób 
(każde z nich zawiera imię jakiejś osoby) oraz question będące pytaniem na temat jednej z tych osób. 
Lista jest zbyt duża, aby móc ją wykorzystać w jednym zapytaniu, więc dowolną techniką odfiltruj te zdania, 
które zawierają wzmiankę na temat osoby wspomnianej w pytaniu. 
Ostatnim krokiem jest wykorzystanie odfiltrowanych danych jako kontekst na podstawie którego model ma udzielić odpowiedzi na pytanie. 
Zatem: pobierz listę zdań oraz pytanie, skorzystaj z LLM, aby odnaleźć w pytaniu imię, 
programistycznie lub z pomocą no-code odfiltruj zdania zawierające to imię. 
Ostatecznie spraw by model odpowiedział na pytanie, a jego odpowiedź prześlij do naszego API w obiekcie JSON zawierającym jedną właściwość “answer”.
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
    template = f"""
        {response['msg']}
        """
    human_template = "{text}"

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", human_template)
    ])

    chain = chat_prompt | ChatOpenAI()
    output = chain.invoke(
        {"text": f"'{response['input']}'"})
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
    token = get_token("inprompt")
    answer = get_task(token)
    answer_submission(token, answer)
