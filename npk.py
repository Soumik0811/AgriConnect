import requests
import json

labels = ["soil type", "Temperature", "Humidity", "Nitrogen", "Phosphorus", "Potassium", "PH Level"]

API_URL = "https://flowise-a19s.onrender.com/api/v1/prediction/3f51113d-6be9-4e6a-be7b-406a8b7fc125"

def recommend(payload):
    response = requests.post(API_URL, json=payload)
    output = response.json()
    r = (json.loads(output['text']))
    return dict(zip(labels, r))
