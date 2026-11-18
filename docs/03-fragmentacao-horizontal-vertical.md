
# Fragmentação Horizontal e Vertical — MultiStore

**Projeto:** MultiStore Distributed DB  
**Issue:** #04 — Definir fragmentação horizontal e vertical  
**Referência:** docs/modelagem/decisoes-modelagem.md  
**Status:** Especificação técnica proposta

---

## 1. Objetivo

Definir as estratégias de fragmentação horizontal e vertical
do banco de dados distribuído MultiStore.

O sistema utilizará cinco entidades:

- Cliente
- Produto
- Pedido
- Item_Pedido
- Avaliacao

A fragmentação deverá garantir:

- Completude dos dados.
- Disjunção dos fragmentos horizontais.
- Reconstrução das entidades originais.
- Preservação dos identificadores.
- Integridade dos relacionamentos.
- Distribuição coerente entre os SGBDs.

## 2. Estratégia geral

| Entidade | Estratégia |
|---|---|
| Cliente | Horizontal primária por região |
| Pedido | Horizontal primária por região |
| Item_Pedido | Horizontal derivada de Pedido |
| Produto | Vertical por atributos |
| Avaliacao | Armazenamento documental no MongoDB |

A fragmentação lógica será independente da alocação física.

O sistema representará cinco regiões brasileiras:

1. Norte
2. Nordeste
3. Centro-Oeste
4. Sudeste
5. Sul

## 3. Fragmentação horizontal de Pedido

### 3.1 Estrutura global

A entidade Pedido possui:

- id_pedido (PK)
- data_pedido
- valor_total
- status
- regiao
- id_cliente (FK)

### 3.2 Predicados

Os pedidos serão divididos conforme a região da compra.

| Fragmento | Predicado |
|---|---|
| PED_N | regiao = 'Norte' |
| PED_NE | regiao = 'Nordeste' |
| PED_CO | regiao = 'Centro-Oeste' |
| PED_SE | regiao = 'Sudeste' |
| PED_S | regiao = 'Sul' |

### 3.3 Completude

Todo pedido deverá possuir uma região válida.

O atributo regiao será obrigatório e limitado aos cinco
valores definidos.

Portanto, cada pedido pertencerá a pelo menos um fragmento.

### 3.4 Disjunção

Como cada pedido possui uma única região, os predicados
são mutuamente exclusivos.

Nenhum pedido poderá pertencer simultaneamente a dois
fragmentos horizontais.

### 3.5 Reconstrução

A relação global será reconstruída pela união:

Pedido = PED_N ∪ PED_NE ∪ PED_CO ∪ PED_SE ∪ PED_S

Como os fragmentos são disjuntos, poderá ser utilizada
a operação UNION ALL.

### 3.6 Exemplo SQL

```sql
SELECT *
FROM Pedido
WHERE regiao = 'Nordeste';
```

A consulta deverá acessar somente o fragmento
correspondente à região solicitada.

## 4. Fragmentação horizontal de Cliente

### 4.1 Estrutura global

A entidade Cliente possui:

- id_cliente (PK)
- nome
- email
- telefone
- cidade
- estado
- regiao

### 4.2 Predicados

| Fragmento | Predicado |
|---|---|
| CLI_N | regiao = 'Norte' |
| CLI_NE | regiao = 'Nordeste' |
| CLI_CO | regiao = 'Centro-Oeste' |
| CLI_SE | regiao = 'Sudeste' |
| CLI_S | regiao = 'Sul' |

### 4.3 Completude e disjunção

O atributo regiao será obrigatório e deverá corresponder
à região brasileira associada ao estado cadastrado.

Cada cliente deverá pertencer a exatamente um fragmento.

### 4.4 Reconstrução

Cliente = CLI_N ∪ CLI_NE ∪ CLI_CO ∪ CLI_SE ∪ CLI_S

### 4.5 Mudança de região

Caso o cliente altere seu estado para outro pertencente
a uma região diferente:

1. O sistema identifica a nova região.
2. Localiza o fragmento de destino.
3. Migra o registro do cliente.
4. Preserva o identificador id_cliente.
5. Atualiza o catálogo de localização.

Os pedidos existentes manterão a região registrada
no momento da compra.

A migração deverá prever recuperação em caso de falha.

## 5. Fragmentação horizontal derivada de Item_Pedido

### 5.1 Estrutura global

A entidade Item_Pedido possui:

- id_item (PK)
- quantidade
- preco_unitario
- id_pedido (FK)
- id_produto (FK)

### 5.2 Estratégia

Item_Pedido será fragmentada conforme a região
do pedido ao qual cada item pertence.

Para cada região R:

ITEM_R = Item_Pedido ⋉ PED_R

A operação representa um semijoin pela condição:

Item_Pedido.id_pedido = PED_R.id_pedido

### 5.3 Fragmentos

| Fragmento | Pedido correspondente |
|---|---|
| ITEM_N | PED_N |
| ITEM_NE | PED_NE |
| ITEM_CO | PED_CO |
| ITEM_SE | PED_SE |
| ITEM_S | PED_S |

### 5.4 Regras de integridade

- Cada item pertence a um único pedido.
- Cada pedido possui um identificador global.
- Cada item acompanha o fragmento de seu pedido.
- O id_produto referencia logicamente um Produto.
- A quantidade deverá ser maior que zero.
- O preco_unitario deverá ser não negativo.
- Um pedido confirmado deverá possuir pelo menos um item.

### 5.5 Reconstrução

Item_Pedido = ITEM_N ∪ ITEM_NE ∪ ITEM_CO
              ∪ ITEM_SE ∪ ITEM_S

A reconstrução será realizada por união dos fragmentos.

## 6. Fragmentação vertical de Produto

### 6.1 Estrutura global

A entidade Produto possui:

- id_produto (PK)
- nome
- descricao
- preco
- estoque
- categoria

### 6.2 Fragmento comercial

Nome: PROD_COMERCIAL

Atributos:

- id_produto
- nome
- categoria
- preco

Esse fragmento concentra informações frequentemente
utilizadas nas consultas de catálogo.

### 6.3 Fragmento operacional

Nome: PROD_OPERACIONAL

Atributos:

- id_produto
- descricao
- estoque

Esse fragmento concentra a descrição e a quantidade
disponível em estoque.

### 6.4 Repetição da chave primária

O atributo id_produto será repetido nos dois fragmentos.

A repetição permite associar os atributos comerciais
e operacionais ao mesmo produto.

Para cada id_produto, deverá existir exatamente um
registro em cada fragmento.

### 6.5 Completude

Todos os atributos da entidade Produto estão presentes
na união dos conjuntos de atributos dos fragmentos.

Nenhum atributo original é perdido.

### 6.6 Disjunção dos atributos

O único atributo compartilhado será id_produto,
necessário à reconstrução.

Os demais atributos não serão repetidos entre
os fragmentos.

### 6.7 Reconstrução

Produto = PROD_COMERCIAL
          JOIN PROD_OPERACIONAL
          USING (id_produto)

Exemplo SQL conceitual:

```sql
SELECT
    c.id_produto,
    c.nome,
    o.descricao,
    c.categoria,
    c.preco,
    o.estoque
FROM PROD_COMERCIAL c
INNER JOIN PROD_OPERACIONAL o
    ON c.id_produto = o.id_produto;
```

Caso os fragmentos estejam em SGBDs diferentes,
a junção será realizada pelo gateway FastAPI.

### 6.8 Integridade

- id_produto deverá ser globalmente único.
- O preço deverá ser não negativo.
- O estoque não poderá ser negativo.
- A criação deverá contemplar ambos os fragmentos.
- A exclusão deverá considerar ambos os fragmentos.
- Falhas parciais deverão ser detectadas e tratadas.

## 7. Armazenamento de Avaliacao

### 7.1 Estrutura global

A entidade Avaliacao possui:

- id_avaliacao (PK)
- nota
- comentario
- data_avaliacao
- id_cliente (FK lógica)
- id_produto (FK lógica)

### 7.2 Estratégia

As avaliações serão armazenadas no MongoDB,
utilizando documentos BSON.

Exemplo:

```json
{
  "id_avaliacao": 1,
  "nota": 5,
  "comentario": "Excelente produto",
  "data_avaliacao": "2026-11-18",
  "id_cliente": 10,
  "id_produto": 25
}
```

### 7.3 Integridade

O gateway deverá verificar a existência do cliente
e do produto antes de registrar uma avaliação.

A nota deverá ser um número inteiro entre 1 e 5.

O armazenamento documental não constitui, por si só,
fragmentação horizontal ou vertical.

## 8. Proposta de alocação física

A seguinte distribuição é proposta para os três SGBDs.

### 8.1 PostgreSQL

Armazenará:

- CLI_N
- CLI_NE
- CLI_CO
- PED_N
- PED_NE
- PED_CO
- ITEM_N
- ITEM_NE
- ITEM_CO
- PROD_COMERCIAL

### 8.2 MySQL

Armazenará:

- CLI_SE
- CLI_S
- PED_SE
- PED_S
- ITEM_SE
- ITEM_S
- PROD_OPERACIONAL

### 8.3 MongoDB

Armazenará:

- Coleção Avaliacao

### 8.4 Justificativa

A distribuição utiliza PostgreSQL e MySQL para
armazenar os fragmentos relacionais.

Os dados de pedidos e seus respectivos itens
permanecerão no mesmo SGBD regional.

Os atributos de Produto serão divididos entre
PostgreSQL e MySQL, permitindo demonstrar uma
reconstrução vertical distribuída.

O MongoDB será responsável pelas avaliações,
demonstrando integração entre bancos relacionais
e documentais.

Essa alocação é uma proposta de implementação,
sujeita à validação pela equipe.

## 9. Consultas distribuídas

### 9.1 Consulta regional

Consultar pedidos de uma região específica.

O gateway identifica o fragmento correspondente
e acessa somente o SGBD necessário.

### 9.2 Consulta global

Consultar todos os pedidos do MultiStore.

O gateway acessa os fragmentos regionais
e consolida os resultados.

### 9.3 Reconstrução vertical

Consultar todas as informações de um produto.

O gateway recupera os atributos comerciais
no PostgreSQL e os operacionais no MySQL.

Os resultados são associados por id_produto.

### 9.4 Consulta de pedido e itens

Consultar um pedido e todos os seus itens.

O gateway utiliza id_pedido para localizar
o fragmento regional correspondente.

### 9.5 Consulta de produto e avaliações

Consultar um produto e suas avaliações.

O gateway recupera os dados do Produto nos
SGBDs relacionais e as avaliações no MongoDB.

### 9.6 Agregação regional

Calcular o valor total de pedidos por região.

Os resultados parciais são agregados pelo gateway.

## 10. Regras de integridade distribuída

### 10.1 Identificadores globais

Os identificadores deverão ser únicos em todo o sistema.

O formato e a estratégia de geração serão definidos
na implementação.

### 10.2 Relacionamentos

Os seguintes relacionamentos deverão ser preservados:

- Cliente 1:N Pedido
- Pedido 1:N Item_Pedido
- Produto 1:N Item_Pedido
- Cliente 1:N Avaliacao
- Produto 1:N Avaliacao

### 10.3 Integridade entre SGBDs

Quando entidades relacionadas estiverem em bancos
distintos, a integridade referencial deverá ser
validada pela aplicação.

Chaves estrangeiras locais não garantem integridade
referencial entre PostgreSQL, MySQL e MongoDB.

### 10.4 Falhas distribuídas

Operações que envolvam múltiplos SGBDs deverão prever:

- Detecção de falhas parciais.
- Registro de erros.
- Recuperação ou compensação.
- Prevenção de registros inconsistentes.

A estratégia transacional será detalhada
nas Issues de implementação.

## 11. Verificação dos critérios de fragmentação

### 11.1 Completude

Todos os registros de Cliente, Pedido e Item_Pedido
deverão pertencer a algum fragmento horizontal.

Todos os atributos de Produto deverão estar presentes
nos fragmentos verticais.

### 11.2 Disjunção

Os fragmentos horizontais serão mutuamente exclusivos.

Na fragmentação vertical, somente a chave id_produto
será repetida.

### 11.3 Reconstrução

As entidades deverão ser reconstruídas por:

- UNION ALL para fragmentação horizontal.
- JOIN por id_produto para fragmentação vertical.
- Associação por id_pedido para recuperar itens.

## 12. Critérios de aceitação da Issue #04

- [x] Predicados horizontais definidos.
- [x] Completude e disjunção especificadas.
- [x] Fragmentos verticais definidos.
- [x] Chave id_produto repetida corretamente.
- [x] Distribuição de Cliente especificada.
- [x] Distribuição derivada de Item_Pedido especificada.
- [x] Proposta de alocação física documentada.
- [x] Regras de reconstrução especificadas.
- [ ] Validar a alocação com a equipe.
- [ ] Executar testes de reconstrução na implementação.
- [ ] Revisar e integrar a documentação à branch dev.

---

**Documento vinculado à Issue #04 — MultiStore Distributed DB.**
