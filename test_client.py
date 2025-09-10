import requests
import json

url = "http://127.0.0.1:5000/get_price"

with open("sample_payload.json", "r") as f:
    payload = json.load(f)

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.json())
