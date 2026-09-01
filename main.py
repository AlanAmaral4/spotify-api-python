import os
import requests
from dotenv import load_dotenv

from rich import print_json

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

req = requests.post(
    "https://accounts.spotify.com/api/token",
    data={"grant_type": "client_credentials"},
    auth=(CLIENT_ID, CLIENT_SECRET),
)

token = req.json()["access_token"]

header = {"Authorization": f"Bearer {token}"}
req2 = requests.get(
    "https://api.spotify.com/v1/search?q=beatles&type=artist",
    headers=header,
)

print(req2.status_code)
print_json(data=req2.json())
