import requests

author = ""
quote = "Service down"
req = requests.get("https://official-joke-api.appspot.com/random_joke")
if req.status_code == 200:
    request = json.loads(req)  # make an api call
    author = request["punchline"]
    quote = request["setup"]
