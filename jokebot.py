import requests

def get_joke():
    response = requests.get("https://api.jokes.one/jod")
    return response.json()
