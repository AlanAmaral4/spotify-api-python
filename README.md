# Atividade de Ciência de Dados — API do Spotify

Projeto de estudo que consome a [API Web do Spotify](https://developer.spotify.com/documentation/web-api)
em Python. O script obtém um token pelo fluxo *Client Credentials* e o usa para buscar artistas
no endpoint `/v1/search`.

## Requisitos

- Python 3.14
- Uma aplicação registrada no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Instalação

```bash
python3.14 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Credenciais

O script lê `CLIENT_ID` e `CLIENT_SECRET` de duas origens e detecta sozinho qual usar.

### Local

Copie o arquivo de exemplo e preencha com os dados da sua aplicação:

```bash
cp .env.example .env
```

```
CLIENT_ID=seu_client_id
CLIENT_SECRET=seu_client_secret
```

O `.env` está no `.gitignore` e não deve ser versionado.

### Google Colab

Não use `.env`. No painel esquerdo, abra os **Secrets** (ícone de chave), crie `CLIENT_ID` e
`CLIENT_SECRET` e ative o *Notebook access* em cada um. Assim as credenciais ficam na sua
conta e não acompanham o notebook quando ele for compartilhado.

## Execução

### Local

```bash
.venv/bin/python main.py
```

A saída é o JSON da resposta, formatado com `rich`.

### Google Colab

Traga o repositório para a sessão:

```python
!git clone https://github.com/AlanAmaral4/spotify-api-python.git
%cd spotify-api-python
```

E importe as funções:

```python
from main import CLIENT_ID, CLIENT_SECRET, create_session, get, get_token

token = get_token(CLIENT_ID, CLIENT_SECRET)
session = create_session(token)

get(session, "search", q="beatles", type="artist")
```

O bloco `if __name__ == "__main__"` faz o import não disparar a busca de exemplo, e a `session`
sobrevive entre células — dá para explorar vários endpoints sem reautenticar. `requests` e
`rich` já vêm instalados no Colab; `python-dotenv` não é usado lá.

Depois de um `!git pull`, reinicie o runtime (`Ctrl+M .`) para que o novo código valha: reimportar
um módulo já carregado não basta.

## Observação

O fluxo *Client Credentials* dá acesso apenas a dados públicos do catálogo. Endpoints que
envolvem dados de usuário (playlists privadas, histórico) exigem o fluxo *Authorization Code*.
