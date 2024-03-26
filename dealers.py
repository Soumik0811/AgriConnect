import requests
from convert import query


API_URL = "https://flowise-a19s.onrender.com/api/v1/prediction/5d836cfb-3983-45bd-b224-5c15d3b32e4b"

def fun(payload):
    response = requests.post(API_URL, json=payload)
    output = response.json()
    result = str(output['text'].strip())
    print(result)
    fout = (query({"question":result}))
    return fout


