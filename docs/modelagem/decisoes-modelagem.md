# Modelagem do Esquema Global - Multistore

## 1. Entidades

O modelo global do sistema Multistore possui cinco entidades principais:

- **Cliente:** armazena nome, e-mail, telefone, cidade, estado e regiao.
- **Produto:** armazena nome, descricao, categoria, preco e estoque.
- **Pedido:** registra a data, o valor total, o status e a regiao da compra.
- **Item_Pedido:** registra os produtos de cada pedido, incluindo quantidade e preco unitario.
- **Avaliacao:** armazena a nota, o comentario e a data da avaliacao de um produto.

Cada entidade possui uma chave primaria para identificar seus registros.

## 2. Relacionamentos e cardinalidades

- **Cliente - Pedido (1:N):** um cliente pode realizar varios pedidos, mas cada pedido pertence a apenas um cliente.
- **Pedido - Item_Pedido (1:N):** um pedido deve conter pelo menos um item, e cada item pertence a um unico pedido.
- **Produto - Item_Pedido (1:N):** um produto pode aparecer em varios itens de pedidos, mas cada item se refere a apenas um produto.
- **Cliente - Avaliacao (1:N):** um cliente pode realizar varias avaliacoes, mas cada avaliacao pertence a um unico cliente.
- **Produto - Avaliacao (1:N):** um produto pode receber varias avaliacoes, mas cada avaliacao corresponde a apenas um produto.

## 3. Decisoes de modelagem

A entidade Item_Pedido foi criada para representar os produtos associados a cada pedido, permitindo armazenar a quantidade e o preco unitario no momento da compra.

O atributo `regiao` foi incluido em Cliente e Pedido para permitir a identificacao da localizacao dos clientes e facilitar a futura fragmentacao horizontal dos pedidos.

A entidade Produto possui atributos operacionais, como preco e estoque, e descritivos, como descricao e categoria. Essa separacao podera ser utilizada na fragmentacao vertical.

A entidade Avaliacao foi modelada separadamente para permitir que diferentes clientes avaliem os produtos, registrando notas e comentarios.

No Modelo Relacional, as chaves estrangeiras representam os relacionamentos definidos no MER.

## 4. Diagramas

### Modelo Entidade-Relacionamento (MER)

![MER do Multistore](mer.png)

### Modelo Relacional (MR)

![MR do Multistore](mr.png)

## 5. Consideracoes finais

A modelagem global foi desenvolvida com base nas entidades e nos requisitos do e-commerce multirregional. Ela servira como referencia para a definicao dos fragmentos e sua distribuicao entre PostgreSQL, MySQL e MongoDB nas proximas etapas do projeto.