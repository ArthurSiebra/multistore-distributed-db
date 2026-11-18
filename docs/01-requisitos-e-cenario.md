
# MultiStore Distributed DB
## Especificação de Cenário e Requisitos

**Projeto:** E-commerce Multirregional Brasileiro  
**Disciplina:** Banco de Dados II  
**Issue:** #02 — Definir cenário e requisitos  
**Status:** Proposta inicial

---

## 1. Visão Geral

O MultiStore é um sistema acadêmico de comércio eletrônico multirregional que demonstra conceitos de bancos de dados distribuídos.

A plataforma permite gerenciar clientes, produtos, pedidos, itens de pedidos e avaliações, distribuindo informações entre PostgreSQL, MySQL e MongoDB.

Um gateway desenvolvido com FastAPI oferece uma interface única para operações de escrita, leitura e consultas distribuídas.

## 2. Objetivos

### Objetivo geral

Projetar e implementar um sistema de banco de dados distribuído para um e-commerce brasileiro, demonstrando fragmentação, distribuição, reconstrução e integração de dados heterogêneos.

### Objetivos específicos

- Modelar cinco entidades de negócio.
- Implementar fragmentação horizontal e vertical.
- Integrar PostgreSQL, MySQL e MongoDB.
- Disponibilizar operações CRUD pelo gateway.
- Executar consultas distribuídas.
- Demonstrar reconstrução dos dados fragmentados.
- Validar consistência e recuperação de falhas.
- Avaliar o comportamento das consultas distribuídas.

## 3. Cenário Multirregional

O sistema representa operações nas cinco regiões brasileiras:

- Norte
- Nordeste
- Centro-Oeste
- Sudeste
- Sul

Cada cliente pertence a uma região, determinada pelo estado de seu endereço cadastrado.

Os pedidos são associados à região do cliente no momento da criação.

A infraestrutura utilizará três SGBDs, sem exigir um servidor físico para cada região.

A distribuição dos fragmentos será definida no documento de modelagem.

## 4. Entidades de Negócio

### 4.1 Cliente

Representa uma pessoa cadastrada na plataforma.

Atributos preliminares:

- id
- nome
- email
- telefone
- estado
- regiao
- data_cadastro

### 4.2 Produto

Representa um item comercializado.

Atributos preliminares:

- id
- nome
- descricao
- categoria
- preco
- estoque
- categoria

### 4.3 Pedido

Representa uma compra realizada por um cliente.

Atributos preliminares:

- id
- cliente_id
- data_pedido
- status
- valor_total
- regiao

### 4.4 ItemPedido

Representa um produto incluído em um pedido.

Atributos preliminares:

- id
- pedido_id
- produto_id
- quantidade
- preco_unitario

### 4.5 Avaliacao

Representa uma avaliação realizada por um cliente sobre um produto.

Atributos preliminares:

- id
- cliente_id
- produto_id
- nota
- comentario
- data_avaliacao

Os atributos e relacionamentos definitivos serão estabelecidos na Issue #03.

## 5. Requisitos Funcionais

| ID | Requisito |
|---|---|
| RF01 | Cadastrar e consultar clientes |
| RF02 | Atualizar e excluir clientes conforme as restrições de integridade |
| RF03 | Cadastrar, consultar, atualizar e excluir produtos |
| RF04 | Criar e consultar pedidos |
| RF05 | Atualizar o estado de um pedido |
| RF06 | Gerenciar itens associados aos pedidos |
| RF07 | Cadastrar, consultar, atualizar e excluir avaliações |
| RF08 | Consultar informações por região |
| RF09 | Reconstruir informações armazenadas em fragmentos |
| RF10 | Executar consultas agregadas entre nós |
| RF11 | Consultar dados relacionais associados a documentos MongoDB |
| RF12 | Disponibilizar estatísticas de distribuição dos registros |
| RF13 | Registrar os nós acessados durante consultas |
| RF14 | Tratar falhas em operações distribuídas |

## 6. Operações CRUD

| Entidade | Create | Read | Update | Delete |
|---|---|---|---|---|
| Cliente | Sim | Sim | Sim | Sim |
| Produto | Sim | Sim | Sim | Sim |
| Pedido | Sim | Sim | Sim | Condicional |
| ItemPedido | Sim | Sim | Sim | Condicional |
| Avaliacao | Sim | Sim | Sim | Sim |

As exclusões condicionais deverão respeitar as regras de integridade e o histórico das operações.

## 7. Consultas Distribuídas

O sistema deverá demonstrar:

1. Consulta global de clientes independentemente da região.
2. Consulta de pedidos por região.
3. Reconstrução de registros divididos verticalmente.
4. Agregação do valor de pedidos entre diferentes nós.
5. Consulta que relacione entidades SQL e avaliações armazenadas no MongoDB.
6. Consulta otimizada que acesse somente os fragmentos necessários.

## 8. Casos de Uso

### UC01 — Cadastrar cliente

Um operador cadastra um cliente informando seus dados e estado.

O gateway identifica a região e encaminha os dados conforme o catálogo global.

### UC02 — Consultar produtos

Um consumidor consulta os produtos disponíveis.

O gateway retorna uma visão lógica dos produtos, independentemente da localização física dos registros.

### UC03 — Realizar pedido

Um cliente seleciona produtos e realiza uma compra.

O sistema registra o pedido e seus itens, respeitando as regras de consistência.

### UC04 — Avaliar produto

Um cliente registra uma nota e um comentário sobre um produto.

A avaliação pode ser armazenada em um banco documental e recuperada por meio do gateway.

### UC05 — Consultar vendas regionais

Um operador solicita o total de vendas por região.

O gateway executa as consultas necessárias e consolida os resultados.

### UC06 — Consultar dados reconstruídos

Um operador consulta uma entidade cujos atributos estejam distribuídos entre diferentes fragmentos.

O gateway combina os fragmentos para apresentar o registro lógico completo.

## 9. Premissas e Regras de Negócio

- Os identificadores serão globalmente únicos.
- Cada estado brasileiro pertence a uma única região.
- O email de cada cliente deverá ser único globalmente.
- Produtos terão preço não negativo.
- Quantidades dos itens deverão ser maiores que zero.
- Avaliações terão notas inteiras de 1 a 5.
- O valor total do pedido será calculado a partir dos itens.
- O preço unitário do item será preservado no momento da compra.
- O estoque não poderá ficar negativo após uma operação confirmada.
- Pedidos finalizados não poderão ser excluídos fisicamente pela API.
- Operações distribuídas deverão prever tratamento de falhas e compensações.
- Não serão processados pagamentos reais.

## 10. Requisitos Não Funcionais

| ID | Requisito |
|---|---|
| RNF01 | Executar a infraestrutura com Docker Compose |
| RNF02 | Utilizar PostgreSQL, MySQL e MongoDB |
| RNF03 | Implementar gateway REST com FastAPI |
| RNF04 | Configurar serviços por variáveis de ambiente |
| RNF05 | Registrar erros e operações relevantes |
| RNF06 | Permitir execução reproduzível em ambiente limpo |
| RNF07 | Implementar testes automatizados |
| RNF08 | Gerar pelo menos 10.000 registros sintéticos |
| RNF09 | Documentar os experimentos de desempenho |
| RNF10 | Não armazenar credenciais reais no repositório |

## 11. Limitações do Escopo

O projeto não implementará uma plataforma comercial completa.

Não fazem parte do escopo obrigatório:

- Interface web de compras.
- Integração com serviços reais de pagamento.
- Processamento de cartões.
- Integração com transportadoras.
- Autenticação comercial completa.
- Implantação em infraestrutura de nuvem.

O foco será o funcionamento e a avaliação do banco de dados distribuído.

## 12. Decisões Pendentes

As seguintes definições serão realizadas nas próximas Issues:

- Modelo lógico e relacionamentos definitivos.
- Predicados de fragmentação horizontal.
- Atributos da fragmentação vertical.
- Alocação física dos fragmentos.
- Contratos dos adapters.
- Estratégia de consistência distribuída.
- Consultas e experimentos de desempenho.

---

**Documento vinculado à Issue #02.**
