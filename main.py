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

    search = get(
        session,
        "search",
        q="album:Thriller artist:Michael Jackson",
        type="album",
        limit=5,
    )

    albums = search["albums"]["items"]

    album_escolhido = None

    for album in albums:
        if album["name"] == "Thriller" and album["total_tracks"] == 9:
            album_escolhido = album
            break

    if album_escolhido is None:
        raise SystemExit("Álbum esperado não foi encontrado.")

    print("Álbum escolhido:", album_escolhido["name"])
    print("ID:", album_escolhido["id"])
    print("Data:", album_escolhido["release_date"])
    print("Faixas:", album_escolhido["total_tracks"])
    print("-" * 40)

    album_id = album_escolhido["id"]

    tracks = get(
        session,
        f"albums/{album_id}/tracks",
        limit=50,
    )

    dados = []

    ano = int(album_escolhido["release_date"][:4])
    decada = (ano // 10) * 10

    for track in tracks["items"]:
        duracao_min = track["duration_ms"] / 60000

        musica = {
            "artista": "Michael Jackson",
            "album": album_escolhido["name"],
            "faixa": track["name"],
            "data_lancamento": album_escolhido["release_date"],
            "ano": ano,
            "decada": decada,
            "duracao_ms": track["duration_ms"],
            "duracao_min": round(duracao_min, 2),
        }

        dados.append(musica)

    for musica in dados:
        print(musica)