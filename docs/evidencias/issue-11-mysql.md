# Issue #11 — Inicialização do Esquema e Índices MySQL

**Projeto:** MultiStore Distributed DB  
**Data:** 26/11/2026  
**Status:** Implementado e testado em ambiente isolado.

## 1. Objetivo

Implementar os scripts de inicialização automática das tabelas, constraints e índices dos fragmentos alocados ao MySQL, conforme o catálogo global do projeto.

## 2. Ambiente de testes

- Docker: 29.1.3
- Docker Compose: 2.40.3
- MySQL: 8.4.13
- Container: multistore-mysql-test
- Banco de dados: multistore
- Volume: multistore_mysql_issue11_test

## 3. Arquivos implementados

- `init/mysql/01_schema.sql`
- `init/mysql/02_indexes.sql`

## 4. Fragmentos implementados

| Fragmento | Tipo de fragmentação |
|---|---|
| CLI_SE | Horizontal primária |
| CLI_S | Horizontal primária |
| PED_SE | Horizontal primária |
| PED_S | Horizontal primária |
| ITEM_SE | Horizontal derivada |
| ITEM_S | Horizontal derivada |
| PROD_OPERACIONAL | Vertical |

## 5. Resultados dos testes

| Teste | Resultado |
|---|---|
| Inicialização automática em volume novo | Aprovado |
| Criação das sete tabelas | Aprovado |
| Inserção de clientes válidos | Aprovado |
| Inserção de produtos válidos | Aprovado |
| Inserção de pedidos válidos | Aprovado |
| Inserção de item válido no Sul | Aprovado |
| Bloqueio de região incorreta | Aprovado |
| Bloqueio de estoque negativo | Aprovado |
| Bloqueio de quantidade zero | Aprovado |
| Bloqueio de valor total negativo | Aprovado |
| Bloqueio de preço unitário negativo | Aprovado |
| Bloqueio de pedido inexistente | Aprovado |
| Bloqueio de produto inexistente | Aprovado |
| Proteção contra exclusão de pedido referenciado | Aprovado |
| Consulta JOIN entre quatro tabelas | Aprovado |
| Verificação dos índices | Aprovado |
| Execução do ROLLBACK | Aprovado |

## 6. Evidências de execução

A inicialização automática executou os scripts `01_schema.sql` e `02_indexes.sql` sem erros.

O comando `SHOW TABLES` retornou sete tabelas.

As operações inválidas foram rejeitadas com os seguintes códigos:

- ERROR 3819: violação de CHECK.
- ERROR 1452: violação de chave estrangeira.
- ERROR 1451: tentativa de exclusão de registro referenciado.

A consulta JOIN retornou corretamente um pedido de valor total R$ 800,00, contendo duas unidades de um produto com preço unitário de R$ 400,00.

## 7. Decisões técnicas

- Utilização do mecanismo InnoDB.
- Identificadores BIGINT sem geração automática local.
- Valores monetários representados por DECIMAL(12,2).
- Restrições CHECK para garantir regras de negócio e fragmentação.
- Chaves estrangeiras locais para Item_Pedido.
- Validação distribuída de clientes e unicidade global prevista no gateway.
- Aproveitamento dos índices criados automaticamente pelo InnoDB.

## 8. Limitações e pendências

A validação foi realizada em um container MySQL isolado.

A integração com o Docker Compose oficial ainda deverá ser verificada.

Existe uma divergência entre PostgreSQL e MySQL quanto à utilização de chaves estrangeiras entre Cliente e Pedido, que deverá ser alinhada com a equipe.

A padronização do tratamento de datas e fusos horários também deverá ser definida.

Os testes realizados não abrangem todas as combinações possíveis de constraints nem as operações distribuídas entre SGBDs.

## 9. Conclusão

Os sete fragmentos MySQL foram inicializados automaticamente e os testes realizados apresentaram os resultados esperados. A implementação está preparada para revisão e posterior integração à infraestrutura do projeto.