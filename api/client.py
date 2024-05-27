import requests

endpoint = "http://127.0.0.1:8000/users/"

get_response = requests.get(endpoint, json={"id": 1})

print(get_response.json())
