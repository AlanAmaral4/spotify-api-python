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

Copie o arquivo de exemplo e preencha com os dados da sua aplicação:

```bash
cp .env.example .env
```

```
CLIENT_ID=seu_client_id
CLIENT_SECRET=seu_client_secret
```

O `.env` está no `.gitignore` e não deve ser versionado.

## Execução

```bash
.venv/bin/python main.py
```

A saída é o código HTTP da requisição seguido do JSON da resposta, formatado com `rich`.

## Observação

O fluxo *Client Credentials* dá acesso apenas a dados públicos do catálogo. Endpoints que
envolvem dados de usuário (playlists privadas, histórico) exigem o fluxo *Authorization Code*.
