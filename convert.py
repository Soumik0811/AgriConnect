import requests
import re
import json

API_URL = "https://flowise-a19s.onrender.com/api/v1/prediction/eb917199-c2a9-4f99-922f-ed6b2cc74ef1"
def query(payload):
    response = requests.post(API_URL, json=payload)
    output = response.json()
    cleaned_json = re.sub(r'`', '', output['text'])
    return (json.loads(cleaned_json))




