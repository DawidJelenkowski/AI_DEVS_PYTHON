"""
API zawsze odpowiada w formacie JSON
Kod błedu 0 (zero) oznacza zaliczone zadanie
Ujemne kody błędów to errory (ich wyjaśnienie jest w polu 'msg')
Od pobrania pytania, na udzielenie odpowiedzi masz 120 sekund
"""
import os
import requests

APIKEY = os.getenv("AI_DEVS_API_KEY")


def get_token(task):
    # Define the API endpoint and the data to send
    quest_url = f"https://zadania.aidevs.pl/token/{task}"
    data = {"apikey": APIKEY}
    print(data)
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


def get_task(token):
    # Define the URL
    token_url = f"https://zadania.aidevs.pl/task/{token}"
    # Send a GET request
    token_response = requests.get(token_url)

    # Check the response status code and content
    if token_response.status_code == 200:
        print("Request was successful")
        print("Response:", token_response.text)

        # Get required content
        response = token_response.json()
        cookie = response['cookie']
        print("Cookie:", cookie)

    else:
        print("Request failed with status code:", token_response.status_code)

    return cookie


def answer_submission(token, answer):
    # Construct the new URL using the received token
    token_url = f"https://zadania.aidevs.pl/answer/{token}"

    # Transform data into json format
    data = {"answer": answer}

    # Send a POST request to the answer URL
    token_response = requests.post(token_url, json=data)

    # Check the response status code and content
    if token_response.status_code == 200:
        print("Answer submission was successful")
        response = token_response.json()
        print("Response:", response)

    else:
        print("Answer submission failed with status code:",
              token_response.status_code)


if __name__ == "__main__":
    token = get_token("helloapi")
    cookie = get_task(token)
    answer_submission(token, cookie)
