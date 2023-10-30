import requests

# Define the API endpoint and the data to send
quest_url = "https://zadania.aidevs.pl/token/liar"
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
