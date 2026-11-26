# Issue #13 - Gateway FastAPI

## 1. Objetivo

Implementar o gateway central do MultiStore Distributed DB,
responsavel pela comunicacao com os bancos de dados,
configuracao por ambiente, padronizacao das respostas,
tratamento de excecoes e documentacao da API.

## 2. Tecnologias utilizadas

- Python 3.12
- FastAPI 0.115.6
- Uvicorn 0.34.0
- PostgreSQL 17
- MySQL 8.4
- MongoDB 8.0
- Docker e Docker Compose
- Pydantic
- Python-dotenv

## 3. Estrutura implementada

gateway/
  main.py
  core/
    config.py
    exceptions.py
  schemas/
    response.py
  routers/
    health.py

## 4. Funcionalidades implementadas

- Configuracao centralizada por variaveis de ambiente.
- Padronizacao das respostas de sucesso e erro.
- Tratamento global de excecoes.
- Endpoint GET /health.
- Verificacao de conectividade com os tres SGBDs.
- Documentacao automatica Swagger, ReDoc e OpenAPI.
- Deteccao de indisponibilidade parcial.
- Recuperacao da conectividade sem reiniciar o gateway.

## 5. Testes realizados

Data: 26/11/2026

| Teste | Resultado | Status |
|---|---|---|
| Build Docker | Imagem construida | Aprovado |
| Inicializacao | 4 containers ativos | Aprovado |
| PostgreSQL | UP | Aprovado |
| MySQL | UP | Aprovado |
| MongoDB | UP | Aprovado |
| GET /health | HTTP 200 | Aprovado |
| Rota inexistente | HTTP 404 | Aprovado |
| Metodo invalido | HTTP 405 | Aprovado |
| Tratador de validacao | HTTP 422 | Aprovado |
| Tratador de erro interno | HTTP 500 | Aprovado |
| Indisponibilidade parcial | HTTP 503 | Aprovado |
| Recuperacao do MySQL | HTTP 200 | Aprovado |
| Swagger | HTTP 200 | Confirmado |
| ReDoc | HTTP 200 | Confirmado |
| OpenAPI | HTTP 200 | Confirmado |

## 6. Evidencias

### 6.1. Infraestrutura operacional

HTTP/1.1 200 OK

{
    "success": true,
    "message": "Gateway operacional",
    "data": {
        "postgresql": "up",
        "mysql": "up",
        "mongodb": "up"
    }
}

### 6.2. Indisponibilidade parcial

O container MySQL foi interrompido propositalmente.

HTTP/1.1 503 Service Unavailable

{
    "success": false,
    "message": "Infraestrutura parcialmente indisponivel",
    "details": {
        "postgresql": "up",
        "mysql": "down",
        "mongodb": "up"
    }
}

### 6.3. Recuperacao

Apos reiniciar somente o MySQL, o gateway retornou
HTTP 200, com os tres bancos disponiveis.

Nao foi necessario reiniciar o gateway.

### 6.4. Tratamento de excecoes

HTTP 404:

{"success":false,"message":"Not Found","details":null}

HTTP 405:

{"success":false,"message":"Method Not Allowed","details":null}

HTTP 422:

{"success":false,"message":"Dados invalidos na requisicao","details":[{"field":"body.id","message":"Field required"}]}

HTTP 500:

{"success":false,"message":"Erro interno do servidor","details":null}

Os tratadores 422 e 500 foram testados diretamente
em memoria, sem adicionar rotas temporarias a API.

## 7. Problema identificado e corrigido

O mysql-connector-python 9.1.0 apresentou
incompatibilidade com os parametros read_timeout
e write_timeout.

Os parametros foram removidos, mantendo
connection_timeout=3.

A conexao foi restabelecida com sucesso.

Como limitacao, os timeouts especificos de leitura
e escrita do MySQL nao estao configurados.

## 8. Conclusao

O gateway foi implementado e validado com sucesso,
estabelecendo comunicacao com PostgreSQL, MySQL
e MongoDB.

A infraestrutura esta preparada para a implementacao
dos adaptadores, catalogo global, roteamento e
operacoes CRUD distribuidas nas proximas etapas.

A verificacao de disponibilidade nao garante
consistencia ou recuperacao de transacoes distribuidas.
EOFmkdir -p docs/evidencias

cat > docs/evidencias/issue-13-fastapi-gateway.md <<'EOF'
# Issue #13 - Gateway FastAPI

## 1. Objetivo

Implementar o gateway central do MultiStore Distributed DB,
responsavel pela comunicacao com os bancos de dados,
configuracao por ambiente, padronizacao das respostas,
tratamento de excecoes e documentacao da API.

## 2. Tecnologias utilizadas

- Python 3.12
- FastAPI 0.115.6
- Uvicorn 0.34.0
- PostgreSQL 17
- MySQL 8.4
- MongoDB 8.0
- Docker e Docker Compose
- Pydantic
- Python-dotenv

## 3. Estrutura implementada

gateway/
  main.py
  core/
    config.py
    exceptions.py
  schemas/
    response.py
  routers/
    health.py

## 4. Funcionalidades implementadas

- Configuracao centralizada por variaveis de ambiente.
- Padronizacao das respostas de sucesso e erro.
- Tratamento global de excecoes.
- Endpoint GET /health.
- Verificacao de conectividade com os tres SGBDs.
- Documentacao automatica Swagger, ReDoc e OpenAPI.
- Deteccao de indisponibilidade parcial.
- Recuperacao da conectividade sem reiniciar o gateway.

## 5. Testes realizados

Data: 26/11/2026

| Teste | Resultado | Status |
|---|---|---|
| Build Docker | Imagem construida | Aprovado |
| Inicializacao | 4 containers ativos | Aprovado |
| PostgreSQL | UP | Aprovado |
| MySQL | UP | Aprovado |
| MongoDB | UP | Aprovado |
| GET /health | HTTP 200 | Aprovado |
| Rota inexistente | HTTP 404 | Aprovado |
| Metodo invalido | HTTP 405 | Aprovado |
| Tratador de validacao | HTTP 422 | Aprovado |
| Tratador de erro interno | HTTP 500 | Aprovado |
| Indisponibilidade parcial | HTTP 503 | Aprovado |
| Recuperacao do MySQL | HTTP 200 | Aprovado |
| Swagger | HTTP 200 | Confirmado |
| ReDoc | HTTP 200 | Confirmado |
| OpenAPI | HTTP 200 | Confirmado |

## 6. Evidencias

### 6.1. Infraestrutura operacional

HTTP/1.1 200 OK

{
    "success": true,
    "message": "Gateway operacional",
    "data": {
        "postgresql": "up",
        "mysql": "up",
        "mongodb": "up"
    }
}

### 6.2. Indisponibilidade parcial

O container MySQL foi interrompido propositalmente.

HTTP/1.1 503 Service Unavailable

{
    "success": false,
    "message": "Infraestrutura parcialmente indisponivel",
    "details": {
        "postgresql": "up",
        "mysql": "down",
        "mongodb": "up"
    }
}

### 6.3. Recuperacao

Apos reiniciar somente o MySQL, o gateway retornou
HTTP 200, com os tres bancos disponiveis.

Nao foi necessario reiniciar o gateway.

### 6.4. Tratamento de excecoes

HTTP 404:

{"success":false,"message":"Not Found","details":null}

HTTP 405:

{"success":false,"message":"Method Not Allowed","details":null}

HTTP 422:

{"success":false,"message":"Dados invalidos na requisicao","details":[{"field":"body.id","message":"Field required"}]}

HTTP 500:

{"success":false,"message":"Erro interno do servidor","details":null}

Os tratadores 422 e 500 foram testados diretamente
em memoria, sem adicionar rotas temporarias a API.

## 7. Problema identificado e corrigido

O mysql-connector-python 9.1.0 apresentou
incompatibilidade com os parametros read_timeout
e write_timeout.

Os parametros foram removidos, mantendo
connection_timeout=3.

A conexao foi restabelecida com sucesso.

Como limitacao, os timeouts especificos de leitura
e escrita do MySQL nao estao configurados.

## 8. Conclusao

O gateway foi implementado e validado com sucesso,
estabelecendo comunicacao com PostgreSQL, MySQL
e MongoDB.

A infraestrutura esta preparada para a implementacao
dos adaptadores, catalogo global, roteamento e
operacoes CRUD distribuidas nas proximas etapas.

A verificacao de disponibilidade nao garante
consistencia ou recuperacao de transacoes distribuidas.
