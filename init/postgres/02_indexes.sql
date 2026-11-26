-- Índices dos fragmentos de Pedido

CREATE INDEX IF NOT EXISTS idx_ped_n_cliente ON PED_N(id_cliente);
CREATE INDEX IF NOT EXISTS idx_ped_n_data ON PED_N(data_pedido);

CREATE INDEX IF NOT EXISTS idx_ped_ne_cliente ON PED_NE(id_cliente);
CREATE INDEX IF NOT EXISTS idx_ped_ne_data ON PED_NE(data_pedido);

CREATE INDEX IF NOT EXISTS idx_ped_co_cliente ON PED_CO(id_cliente);
CREATE INDEX IF NOT EXISTS idx_ped_co_data ON PED_CO(data_pedido);

-- Índices dos fragmentos de Item_Pedido

CREATE INDEX IF NOT EXISTS idx_item_n_pedido ON ITEM_N(id_pedido);
CREATE INDEX IF NOT EXISTS idx_item_n_produto ON ITEM_N(id_produto);

CREATE INDEX IF NOT EXISTS idx_item_ne_pedido ON ITEM_NE(id_pedido);
CREATE INDEX IF NOT EXISTS idx_item_ne_produto ON ITEM_NE(id_produto);

CREATE INDEX IF NOT EXISTS idx_item_co_pedido ON ITEM_CO(id_pedido);
CREATE INDEX IF NOT EXISTS idx_item_co_produto ON ITEM_CO(id_produto);

-- Índices do fragmento comercial de Produto

CREATE INDEX IF NOT EXISTS idx_prod_comercial_nome
    ON PROD_COMERCIAL(nome);

CREATE INDEX IF NOT EXISTS idx_prod_comercial_categoria
    ON PROD_COMERCIAL(categoria);
