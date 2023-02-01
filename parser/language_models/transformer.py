"""
This is an attempt at parser the receipt using a question-answering model from the
transformers library by huggingface. 
This specific model works well if we can specify which food item in the receipt and ask
for its price.

However, we don't currently use this script because it does not work as well as ChatGPT.
See gpt.py
"""


import json
import requests


API_TOKEN = None  # TODO: get API token from HuggingFace
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/svalabs/rembert-german-question-answering"
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))
data = query(
    {
        "inputs": {
            "question": "What's my name?",
            "context": "My name is Clara and I live in Berkeley.",
        }
    }
)
print(data)
