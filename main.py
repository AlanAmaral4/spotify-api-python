import os

import requests
from dotenv import load_dotenv
from rich import print_json

load_dotenv()

API = "https://api.spotify.com/v1"
TOKEN_URL = "https://accounts.spotify.com/api/token"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise SystemExit("Defina CLIENT_ID e CLIENT_SECRET no .env")


def get_token(client_id, client_secret):
    """Fluxo Client Credentials: autentica a aplicação e devolve o access_token."""
    req = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    req.raise_for_status()
    return req.json()["access_token"]


def create_session(token):
    """Sessão com o header de autorização já fixado, reaproveitando a conexão TCP."""
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"
    return session


def get(session, path, **params):
    """Faz um GET em qualquer endpoint da API. Ex.: get(s, "search", q="beatles", type="artist")"""
    req = session.get(f"{API}/{path.lstrip('/')}", params=params)
    if not req.ok:
        raise RuntimeError(f"HTTP {req.status_code} em {path}: {req.text.strip()}")
    return req.json()


if __name__ == "__main__":
    token = get_token(CLIENT_ID, CLIENT_SECRET)
    session = create_session(token)

    search = get(session, "search", q="beatles", type="artist")
    print_json(data=search)
