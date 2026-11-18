
# Propriedades Formais da Fragmentação — MultiStore

**Projeto:** MultiStore Distributed DB  
**Issue:** #05 — Formalizar completude, reconstrução e disjunção  
**Referência:** docs/03-fragmentacao-horizontal-vertical.md  
**Status:** Especificação e demonstração formal

---

## 1. Objetivo

Demonstrar, utilizando álgebra relacional, que a estratégia
de fragmentação definida para o MultiStore satisfaz as
propriedades fundamentais de um banco de dados distribuído:

1. Completude.
2. Reconstrução.
3. Disjunção horizontal.
4. Sobreposição controlada da chave na fragmentação vertical.

As demonstrações consideram as cinco entidades do modelo
global: Cliente, Pedido, Item_Pedido, Produto e Avaliacao.

## 2. Notação

Seja:

- C = relação global Cliente.
- P = relação global Pedido.
- I = relação global Item_Pedido.
- PR = relação global Produto.
- A = relação global Avaliacao.

Operadores utilizados:

- σ = seleção de linhas por predicado.
- π = projeção de atributos.
- ∪ = união de relações.
- ∩ = interseção de relações.
- ⋈ = junção.
- ⋉ = semijunção.
- ∅ = conjunto vazio.

As relações são consideradas conjuntos para as provas
formais, com identificadores globalmente únicos.

## 3. Fragmentação horizontal de Pedido

### 3.1 Definição dos fragmentos

P_N = σ(regiao = 'Norte')(P)

P_NE = σ(regiao = 'Nordeste')(P)

P_CO = σ(regiao = 'Centro-Oeste')(P)

P_SE = σ(regiao = 'Sudeste')(P)

P_S = σ(regiao = 'Sul')(P)

### 3.2 Prova de completude

Defina o domínio permitido:

R = {
  Norte,
  Nordeste,
  Centro-Oeste,
  Sudeste,
  Sul
}

Pela regra de integridade, para todo pedido p ∈ P:

p.regiao ∈ R

Portanto, existe ao menos um fragmento P_r que contém p.

Logo, nenhum pedido válido fica fora da fragmentação.

### 3.3 Prova de disjunção

Considere duas regiões distintas r1 e r2.

Se r1 ≠ r2, um pedido não pode satisfazer simultaneamente:

p.regiao = r1

e

p.regiao = r2

Portanto:

P_r1 ∩ P_r2 = ∅

Os cinco fragmentos são mutuamente disjuntos.

### 3.4 Prova de reconstrução

Como os predicados cobrem todo o domínio R e são
mutuamente exclusivos:

P = P_N ∪ P_NE ∪ P_CO ∪ P_SE ∪ P_S

A união contém todos os pedidos e não introduz
registros adicionais.

Na implementação, UNION ALL poderá ser utilizado,
desde que a disjunção e a unicidade global sejam
preservadas.

## 4. Fragmentação horizontal de Cliente

### 4.1 Definição

C_N = σ(regiao = 'Norte')(C)

C_NE = σ(regiao = 'Nordeste')(C)

C_CO = σ(regiao = 'Centro-Oeste')(C)

C_SE = σ(regiao = 'Sudeste')(C)

C_S = σ(regiao = 'Sul')(C)

### 4.2 Completude

Todo cliente válido possui uma região pertencente
ao domínio R.

Assim:

C = C_N ∪ C_NE ∪ C_CO ∪ C_SE ∪ C_S

### 4.3 Disjunção

Como cada cliente possui exatamente uma região:

C_r1 ∩ C_r2 = ∅, para r1 ≠ r2.

### 4.4 Mudança de região

Se um cliente alterar sua região, ele deverá ser
removido do fragmento anterior e inserido no novo.

A operação deve preservar id_cliente e impedir
duplicação entre fragmentos após sua conclusão.

## 5. Fragmentação horizontal derivada de Item_Pedido

### 5.1 Definição

Para cada região r:

I_r = I ⋉(I.id_pedido = P_r.id_pedido) P_r

Ou, de forma equivalente:

I_r = σ(
  id_pedido ∈ π(id_pedido)(P_r)
)(I)

### 5.2 Completude

Todo item i ∈ I referencia exatamente um pedido
existente por meio de id_pedido.

Como todo pedido pertence a um fragmento regional,
todo item pertence ao fragmento derivado correspondente.

Assim:

I = I_N ∪ I_NE ∪ I_CO ∪ I_SE ∪ I_S

### 5.3 Disjunção

Cada item referencia um único pedido.

Como os fragmentos de Pedido são disjuntos e
id_pedido é globalmente único, um item não pode
pertencer a dois fragmentos derivados.

Portanto:

I_r1 ∩ I_r2 = ∅, para r1 ≠ r2.

### 5.4 Reconstrução

A união dos cinco fragmentos derivados recupera
todos os registros da entidade Item_Pedido.

A integridade referencial de id_pedido é uma
pré-condição necessária para essa propriedade.

## 6. Fragmentação vertical de Produto

### 6.1 Relação global

PR(
  id_produto,
  nome,
  descricao,
  categoria,
  preco,
  estoque
)

### 6.2 Fragmento comercial

PR_C = π(
  id_produto,
  nome,
  categoria,
  preco
)(PR)

### 6.3 Fragmento operacional

PR_O = π(
  id_produto,
  descricao,
  estoque
)(PR)

### 6.4 Completude dos atributos

Sejam:

A_C = {
  id_produto,
  nome,
  categoria,
  preco
}

A_O = {
  id_produto,
  descricao,
  estoque
}

A união dos conjuntos de atributos é:

A_C ∪ A_O = atributos(PR)

Portanto, todos os atributos da relação global
estão representados nos fragmentos.

### 6.5 Sobreposição controlada

A interseção dos conjuntos de atributos é:

A_C ∩ A_O = {id_produto}

O único atributo repetido é a chave primária.

Essa repetição é intencional e necessária para
reconstruir os registros completos.

### 6.6 Prova de reconstrução

Como id_produto identifica unicamente cada produto,
e ambos os fragmentos são projeções da mesma
relação global:

PR = PR_C ⋈(PR_C.id_produto = PR_O.id_produto) PR_O

A junção é sem perda de informação porque:

1. Cada produto possui id_produto único.
2. Cada identificador aparece nos dois fragmentos.
3. Os demais atributos são preservados integralmente.
4. A junção pelo identificador associa somente
   atributos pertencentes ao mesmo produto.

A prova pressupõe que os dois fragmentos sejam
mantidos sincronizados e completos.

### 6.7 Disjunção vertical

A disjunção vertical é aplicada aos atributos
não identificadores.

Portanto, não se exige interseção vazia entre
os conjuntos completos de atributos, pois a chave
id_produto deve estar presente em ambos.

## 7. Avaliacao no MongoDB

A entidade Avaliacao será armazenada em uma coleção
documental no MongoDB.

Essa decisão, isoladamente, não constitui uma
fragmentação horizontal ou vertical.

Assim, as provas anteriores não se aplicam à
coleção enquanto ela não for subdividida em
fragmentos.

A integridade de id_cliente e id_produto deverá
ser validada pela aplicação.

## 8. Exemplo de validação conceitual

Considere quatro pedidos:

| id_pedido | regiao |
|---|---|
| 1 | Nordeste |
| 2 | Sul |
| 3 | Norte |
| 4 | Nordeste |

A fragmentação produz:

- P_NE = {1, 4}
- P_S = {2}
- P_N = {3}
- P_CO = {}
- P_SE = {}

### 8.1 Completude

A união dos identificadores resulta em:

{1, 4} ∪ {2} ∪ {3} ∪ {} ∪ {} = {1, 2, 3, 4}

Todos os pedidos originais foram recuperados.

### 8.2 Disjunção

Nenhum identificador aparece em dois fragmentos.

Logo, as interseções entre fragmentos distintos
são vazias.

### 8.3 Reconstrução vertical

Considere:

PR_C = {
  (10, 'Notebook', 'Eletronicos', 3500)
}

PR_O = {
  (10, '16 GB RAM', 15)
}

A junção por id_produto = 10 produz:

{
  id_produto: 10,
  nome: 'Notebook',
  descricao: '16 GB RAM',
  categoria: 'Eletronicos',
  preco: 3500,
  estoque: 15
}

Todos os atributos do produto foram reconstruídos.

Esses exemplos são validações conceituais,
não resultados de testes executados nos SGBDs.

## 9. Condições necessárias

As propriedades demonstradas dependem de:

- Região obrigatória e pertencente ao domínio R.
- Identificadores globalmente únicos.
- Integridade de id_pedido em Item_Pedido.
- Presença de id_produto em ambos os fragmentos.
- Sincronização dos fragmentos verticais.
- Ausência de perda de dados durante migrações.
- Ausência de duplicações indevidas entre fragmentos.

Falhas de implementação podem violar essas
propriedades, mesmo que a especificação lógica
esteja correta.

## 10. Conclusão

A fragmentação proposta para o MultiStore satisfaz
formalmente as propriedades de completude,
reconstrução e disjunção horizontal, considerando
as restrições de integridade estabelecidas.

A fragmentação vertical de Produto permite
reconstrução sem perda por junção na chave
id_produto.

A validade prática dessas propriedades deverá ser
confirmada durante a implementação e os testes
de integração do sistema.

## 11. Checklist da Issue #05

- [x] Expressões de seleção σ definidas.
- [x] Expressões de projeção π definidas.
- [x] Completude horizontal demonstrada.
- [x] Reconstrução por união demonstrada.
- [x] Reconstrução por junção demonstrada.
- [x] Disjunção horizontal demonstrada.
- [x] Sobreposição da chave vertical explicada.
- [x] Exemplo conceitual documentado.
- [ ] Revisão pela equipe.
- [ ] Integração na branch dev.

---

Documento vinculado à Issue #05.
