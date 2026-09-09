# Atividade de Ciência de Dados — API do Spotify

Projeto de estudo que consome a [API Web do Spotify](https://developer.spotify.com/documentation/web-api)
em Python. O script obtém um token pelo fluxo *Client Credentials* e o usa para consultar o
catálogo público — o exemplo pronto busca artistas no endpoint `/v1/search`.

O `main.py` funciona de duas formas: como script (`python main.py`) e como módulo importado célula
a célula no Google Colab. É o mesmo código nos dois casos.

## Requisitos

- Python 3.14 (só para uso local; no Colab a versão do ambiente serve)
- Uma aplicação registrada no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard),
  de onde saem o `CLIENT_ID` e o `CLIENT_SECRET`

## Uso no Google Colab

### 1. Cadastre os Secrets

Não use `.env` no Colab. No painel esquerdo, abra os **Secrets** (ícone de chave 🔑), crie
`CLIENT_ID` e `CLIENT_SECRET` e ative o **Notebook access** em cada um. Assim as credenciais ficam
na sua conta e não acompanham o notebook quando ele for compartilhado.

Faça isso *antes* de importar o módulo. Sem o Notebook access, o import falha com
`NotebookAccessError` — e o erro aparece na linha do `from main import ...`, não onde está a causa.

### 2. Clone o repositório

Cole esta célula no começo do notebook. Ela clona o repositório, entra na pasta e instala as
dependências.

```python
import os

if not os.path.exists("/content/spotify-api-python"):
    !git clone -q https://github.com/AlanAmaral4/spotify-api-python.git

%cd /content/spotify-api-python
%pip install -q -r requirements.txt
```

Dois detalhes que evitam dor de cabeça: use `%pip` em vez de `!pip`, porque o comando mágico
instala no mesmo ambiente em que o notebook roda; e prefira o caminho absoluto no `%cd`, senão
reexecutar a célula tenta entrar na pasta a partir de dentro dela mesma.

Como o `requirements.txt` fixa versões, o pip pode substituir pacotes que já vêm no Colab e pedir
*"You must restart the runtime"*. Se isso acontecer, reinicie (`Ctrl+M .`) e rode a célula de novo.
Para uma sessão mínima, dá para pular o `%pip`: `requests` e `rich` já estão no Colab, e
`python-dotenv` não chega a ser importado lá.

### 3. Importe e consulte

```python
from main import CLIENT_ID, CLIENT_SECRET, create_session, get, get_token

token = get_token(CLIENT_ID, CLIENT_SECRET)
session = create_session(token)

get(session, "search", q="beatles", type="artist")
```

O bloco `if __name__ == "__main__"` faz o import não disparar a busca de exemplo, e a `session`
sobrevive entre células — dá para explorar vários endpoints sem reautenticar:

```python
get(session, "artists/3WrFJ7ztbogyGnTHbHJFl2")           # detalhes de um artista
get(session, "artists/3WrFJ7ztbogyGnTHbHJFl2/albums", limit=50)
get(session, "search", q="year:1967", type="album", limit=20)
```

### 4. Depois de atualizar o código

```python
!git pull
```

Reinicie o runtime (`Ctrl+M .`) para que a nova versão valha: reimportar um módulo já carregado não
basta.

## Uso local

```bash
git clone https://github.com/AlanAmaral4/spotify-api-python.git
cd spotify-api-python

python3.14 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Copie o arquivo de exemplo e preencha com os dados da sua aplicação:

```bash
cp .env.example .env
```

```
CLIENT_ID=seu_client_id
CLIENT_SECRET=seu_client_secret
```

O `.env` está no `.gitignore` e não deve ser versionado. Feito isso:

```bash
.venv/bin/python main.py
```

A saída é o JSON da resposta, formatado com `rich`.

## As funções

| Função | O que faz |
| --- | --- |
| `get_token(client_id, client_secret)` | Autentica a aplicação pelo fluxo *Client Credentials* e devolve o `access_token`. |
| `create_session(token)` | Cria uma `requests.Session` com o header `Authorization` já fixado, reaproveitando a conexão. |
| `get(session, path, **params)` | `GET` em qualquer endpoint da API. O `path` é relativo (`"search"`, `"artists/<id>"`) e os `**params` viram query string. |

O `get` levanta `RuntimeError` com o status **e** o corpo da resposta quando a requisição falha — a
mensagem da própria Spotify costuma ser a pista mais direta em erros 400 e 403.

## Observação

O fluxo *Client Credentials* dá acesso apenas a dados públicos do catálogo. Endpoints que envolvem
dados de usuário (playlists privadas, histórico de reprodução) exigem o fluxo *Authorization Code*.

O token expira em cerca de 1 hora e o script não o renova sozinho: em sessões longas do Colab,
rode de novo o `get_token` / `create_session` para obter um novo.
