import os
import requests
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = OpenAI(openai_api_key=OPENAI_API_KEY)


def token_function(zadanie):
    # Define the API endpoint and the data to send
    quest_url = f"https://zadania.aidevs.pl/token/{zadanie}"
    data = {"apikey": "ac9a1ce6-abbf-48d1-a9ae-df7a80cb6488"}

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


def post_function(token):
    # Define the URL
    token_url = f"https://zadania.aidevs.pl/task/{token}"
    # Send a GET request
    token_response = requests.get(token_url)

    # Check the response status code and content
    if token_response.status_code == 200:
        print("Request was successful")
        print("Response:", token_response.text)
    else:
        print("Request failed with status code:", token_response.status_code)

    return token_response


def task_function(token, question):
    # Construct the new URL using the received token
    new_url = f"https://zadania.aidevs.pl/task/{token}"

    # Send a POST request to the new URL
    token_response = requests.post(new_url, data=question)

    if token_response.status_code == 200:
        print("Answer submission was successful")
        response = token_response.json()
        print("Response:", response["answer"])
        response_answer = response["answer"]
    else:
        print("Answer submission failed with status code:",
              token_response.status_code)

    return response_answer


def ask_gpt(response, question):
    template = """
        Take a deep breath and answer the question by carefully explaining your logic step by step. 
        Then add the separator: \n### and answer the question in one word "yes" or "no":
        """
    human_template = "{text}"

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", human_template)
    ])

    chain = chat_prompt | ChatOpenAI()
    output = chain.invoke(
        {"text": f"Is the response: '{response}' related to the question: '{question['question']}'?"})
    answer = output.content

    return answer


def answer_task_function(token, answer):
    # Construct the new URL using the received token
    new_url = f"https://zadania.aidevs.pl/answer/{token}"

    ans = {"answer": answer}
    # Send a POST request to the new URL
    answer_response = requests.post(new_url, json=ans)

    if answer_response.status_code == 200:
        print("Answer submission was successful")
        response = answer_response.json()
        print("Response:", response)
    else:
        print("Answer submission failed with status code:",
              answer_response.status_code)


if __name__ == "__main__":
    token = token_function("liar")
    post_function(token)
    question = {'question': "What is capital of Poland?"}
    response = task_function(token, question)
    answer = ask_gpt(response, question).upper()
    answer_task_function(token, answer)
