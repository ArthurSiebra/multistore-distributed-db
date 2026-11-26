# Issue #12 — Inicialização de Coleções e Índices MongoDB

**Projeto:** MultiStore Distributed DB  
**Data:** 26/11/2026  
**Status:** Implementado e testado em ambiente isolado.

## 1. Objetivo

Implementar a inicialização automática da coleção Avaliacao no MongoDB, incluindo validação de documentos, restrições de integridade e índices para otimização de consultas.

## 2. Ambiente de testes

- Docker: 29.1.3
- Imagem: mongo:8.0
- Container: multistore-mongodb-test
- Banco de dados: multistore
- Volume: multistore_mongodb_issue12_test

## 3. Arquivos implementados

- `init/mongodb/01_schema.js`
- `init/mongodb/02_indexes.js`

## 4. Estrutura da coleção

| Atributo | Tipo BSON | Restrição |
|---|---|---|
| id_avaliacao | int/long | Obrigatório e único |
| id_cliente | int/long | Obrigatório |
| id_produto | int/long | Obrigatório |
| nota | int/long | Obrigatório, entre 1 e 5 |
| comentario | string | Opcional |
| data_avaliacao | date | Obrigatório |

## 5. Índices

| Índice | Atributo | Único |
|---|---|---|
| _id_ | _id | Sim |
| idx_avaliacao_id | id_avaliacao | Sim |
| idx_avaliacao_cliente | id_cliente | Não |
| idx_avaliacao_produto | id_produto | Não |

## 6. Resultados dos testes

| Teste | Resultado |
|---|---|
| Inicialização automática da coleção | Aprovado |
| Criação dos índices | Aprovado |
| Configuração do JSON Schema | Aprovado |
| Inserção válida | Aprovado |
| Consulta de avaliação | Aprovado |
| Bloqueio de nota superior a 5 | Aprovado |
| Bloqueio de identificador duplicado | Aprovado |
| Bloqueio de atributo obrigatório ausente | Aprovado |
| Bloqueio de tipo incorreto | Aprovado |
| Atualização válida | Aprovado |
| Bloqueio de nota inferior a 1 | Aprovado |
| Exclusão e contagem final | Aprovado |

## 7. Evidências de execução

A coleção Avaliacao foi criada automaticamente.

O comando `db.Avaliacao.getIndexes()` retornou quatro índices.

A configuração da coleção confirmou:

- validationLevel: strict
- validationAction: error

As operações inválidas foram rejeitadas com as mensagens:

- Document failed validation
- E11000 duplicate key error

A atualização válida retornou matchedCount igual a 1 e modifiedCount igual a 1.

Após a exclusão do documento de teste, a contagem final retornou zero.

## 8. Decisões técnicas

- Utilização de documentos BSON.
- Validação de documentos por meio de JSON Schema.
- Identificador lógico global independente do ObjectId.
- Identificadores compatíveis com inteiros de 32 e 64 bits.
- Armazenamento de datas utilizando BSON Date.
- Comentário opcional.
- Integridade referencial entre SGBDs delegada ao gateway.

## 9. Limitações

Os testes foram realizados em um container isolado.

A existência dos clientes e produtos referenciados deverá ser validada pelo gateway.

A integração completa com PostgreSQL, MySQL e Docker Compose ainda deverá ser testada.

## 10. Conclusão

A coleção Avaliacao, seus índices e suas regras de validação foram inicializados corretamente. As operações locais de CRUD e os testes de integridade apresentaram os resultados esperados.