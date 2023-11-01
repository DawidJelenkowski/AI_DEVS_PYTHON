"""
Zastosuj wiedzę na temat działania modułu do moderacji treści i rozwiąż zadanie o nazwie “moderation” z użyciem naszego API do sprawdzania rozwiązań.
Zadanie polega na odebraniu tablicy zdań (4 sztuki), a następnie zwróceniu tablicy z informacją, które zdania nie przeszły moderacji. 
Jeśli moderacji nie przeszło pierwsze i ostatnie zdanie, to odpowiedź powinna brzmieć [1,0,0,1]. Pamiętaj, aby w polu  'answer' zwrócić tablicę w JSON, a nie czystego stringa.
"""
import os
import requests

APIKEY = os.getenv("AI_DEVS_API_KEY")


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


def get_task(token):
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


def answer_submission(token, answer):
    # Construct the new URL using the received token
    token_url = f"https://zadania.aidevs.pl/answer/{token}"

    data = {"answer": answer}
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


if __name__ == "__main__":
    # run only the first 2 functions
    token = get_token("moderation")
    get_task(token)
    # this one insert in python terminal
    # the 0 is where "majonez" is
    answer_submission(token, [1, 0, 1, 1])
