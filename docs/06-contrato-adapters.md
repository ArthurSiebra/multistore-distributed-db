
# Contrato dos Adapters — MultiStore

**Projeto:** MultiStore Distributed DB  
**Issue:** #06 — Catálogo Global e Adapters  
**Status:** Especificação técnica proposta

## 1. Objetivo

Definir um padrão de comunicação entre o gateway FastAPI e os três bancos de dados utilizados no MultiStore:

- PostgreSQL
- MySQL
- MongoDB

O gateway utilizará o catálogo global (`config/catalogo.json`) para identificar onde os dados estão armazenados.

Os adapters serão responsáveis por executar as operações nos respectivos bancos, mantendo uma interface comum.

## 2. Interface dos adapters

Todos os adapters deverão oferecer cinco operações:

| Operação | Descrição |
|---|---|
| find | Busca registros conforme os filtros informados |
| insert | Insere um novo registro |
| update | Atualiza registros existentes |
| delete | Remove registros |
| count | Conta registros conforme os filtros |

Interface proposta em Python:

```python
class DatabaseAdapter:

    def find(self, fragmento, filtros=None):
        pass

    def insert(self, fragmento, dados):
        pass

    def update(self, fragmento, filtros, dados):
        pass

    def delete(self, fragmento, filtros):
        pass

    def count(self, fragmento, filtros=None):
        pass
```

Essa interface é apenas uma especificação. A implementação será realizada nas etapas de desenvolvimento.

## 3. Padrão dos filtros

Os filtros deverão ser representados por dicionários Python ou objetos JSON.

Exemplo:

```json
{
  "regiao": "Nordeste",
  "status": "Confirmado"
}
```

Inicialmente, os filtros terão suporte às seguintes operações:

| Operador | Significado |
|---|---|
| eq | Igual |
| ne | Diferente |
| gt | Maior que |
| gte | Maior ou igual |
| lt | Menor que |
| lte | Menor ou igual |
| in | Pertence a uma lista |

Exemplo com operadores:

```json
{
  "preco": {
    "gte": 50,
    "lte": 200
  }
}
```

Filtros simples, como `"regiao": "Nordeste"`, serão interpretados como igualdade.

Quando houver mais de um campo, as condições serão combinadas por AND.

Os adapters deverão converter esses filtros para consultas SQL parametrizadas ou consultas MongoDB, sem concatenar diretamente valores fornecidos pelo usuário.

## 4. Padrão das respostas

As respostas deverão utilizar uma estrutura padronizada, independentemente do banco de dados.

### 4.1 Consulta

Exemplo de resposta da operação find:

```json
{
  "sucesso": true,
  "dados": [
    {
      "id_cliente": 1,
      "nome": "Maria",
      "regiao": "Nordeste"
    }
  ],
  "total": 1,
  "erro": null
}
```

### 4.2 Inserção

```json
{
  "sucesso": true,
  "dados": {
    "id_cliente": 1
  },
  "total": 1,
  "erro": null
}
```

### 4.3 Atualização e exclusão

As operações update e delete deverão informar a quantidade de registros afetados no campo `total`.

### 4.4 Contagem

A operação count retornará o número de registros encontrados no campo `total`, com `dados` igual a null.

## 5. Tratamento de erros

Os adapters deverão retornar erros padronizados.

Exemplo:

```json
{
  "sucesso": false,
  "dados": null,
  "total": 0,
  "erro": {
    "codigo": "CONNECTION_ERROR",
    "mensagem": "Não foi possível conectar ao banco de dados."
  }
}
```

Códigos previstos:

| Código | Significado |
|---|---|
| CONNECTION_ERROR | Falha de conexão |
| FRAGMENT_NOT_FOUND | Fragmento não localizado |
| VALIDATION_ERROR | Dados ou filtros inválidos |
| DUPLICATE_KEY | Identificador duplicado |
| RECORD_NOT_FOUND | Registro não encontrado |
| DATABASE_ERROR | Erro durante a operação |
| PARTIAL_FAILURE | Falha em operação distribuída |

O gateway será responsável por interpretar esses erros e retornar uma resposta adequada à aplicação.

## 6. Funcionamento do gateway

O gateway FastAPI será responsável por:

1. Receber a requisição da aplicação.
2. Consultar o catálogo global.
3. Identificar os fragmentos necessários.
4. Selecionar o adapter correspondente.
5. Executar a operação.
6. Consolidar os resultados, quando necessário.
7. Retornar uma resposta padronizada.

Exemplo:

Uma consulta de pedidos da região Nordeste deverá ser direcionada ao fragmento `PED_NE`, armazenado no PostgreSQL.

Uma consulta completa de Produto deverá acessar:

- `PROD_COMERCIAL`, no PostgreSQL.
- `PROD_OPERACIONAL`, no MySQL.

O gateway combinará os resultados utilizando `id_produto`.

## 7. Integridade e operações distribuídas

Os identificadores deverão ser globalmente únicos.

O gateway deverá validar os relacionamentos entre entidades armazenadas em bancos diferentes.

Operações envolvendo múltiplos SGBDs deverão prever falhas parciais e mecanismos de recuperação ou compensação.

A implementação dessas estratégias será detalhada nas etapas seguintes.

## 8. Critérios de aceitação

- [x] Catálogo global definido.
- [x] Localização dos fragmentos documentada.
- [x] Interface comum dos adapters especificada.
- [x] Operações find, insert, update, delete e count definidas.
- [x] Padrão de filtros definido.
- [x] Padrão de respostas definido.
- [x] Tratamento de erros especificado.
- [ ] Validar as decisões com a equipe.
- [ ] Implementar os adapters nas próximas etapas.

---

Documento vinculado à Issue #06 — MultiStore Distributed DB.
