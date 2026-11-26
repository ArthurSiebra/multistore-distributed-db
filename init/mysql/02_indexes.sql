
-- MultiStore Distributed DB
-- Issue #11 - Indices MySQL

USE multistore;

CREATE INDEX idx_ped_se_cliente
    ON PED_SE(id_cliente);

CREATE INDEX idx_ped_se_data
    ON PED_SE(data_pedido);

CREATE INDEX idx_ped_s_cliente
    ON PED_S(id_cliente);

CREATE INDEX idx_ped_s_data
    ON PED_S(data_pedido);

CREATE INDEX idx_prod_operacional_estoque
    ON PROD_OPERACIONAL(estoque);
