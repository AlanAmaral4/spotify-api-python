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

Como o `requirements.txt` fixa versões, o pip pode substituir pacotes que já vêm no Colab e
pedir *"You must restart the runtime"*. Se isso acontecer, reinicie (`Ctrl+M .`) e rode a célula
de novo. Para uma sessão mínima, dá para pular o `%pip`: `requests` e `rich` já estão no Colab,
e `python-dotenv` não chega a ser importado lá.

Antes de importar, confirme que os Secrets estão cadastrados e com *Notebook access* ativo (veja
**Credenciais → Google Colab**). Sem isso o import falha com `NotebookAccessError`, e o erro
aparece na linha do `from main import ...`, não onde está a causa.

Feito o setup, importe as funções:

```python
from main import CLIENT_ID, CLIENT_SECRET, create_session, get, get_token

token = get_token(CLIENT_ID, CLIENT_SECRET)
session = create_session(token)

get(session, "search", q="beatles", type="artist")
```

O bloco `if __name__ == "__main__"` faz o import não disparar a busca de exemplo, e a `session`
sobrevive entre células — dá para explorar vários endpoints sem reautenticar.

Depois de um `!git pull`, reinicie o runtime (`Ctrl+M .`) para que o novo código valha: reimportar
um módulo já carregado não basta.

## Observação

O fluxo *Client Credentials* dá acesso apenas a dados públicos do catálogo. Endpoints que
envolvem dados de usuário (playlists privadas, histórico) exigem o fluxo *Authorization Code*.
