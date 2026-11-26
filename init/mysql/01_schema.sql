
-- MultiStore Distributed DB
-- Issue #11 - Esquema MySQL

USE multistore;


CREATE TABLE IF NOT EXISTS CLI_SE (
    id_cliente BIGINT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    regiao VARCHAR(20) NOT NULL,

    CONSTRAINT chk_cli_se_regiao
        CHECK (regiao = 'Sudeste')
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS CLI_S (
    id_cliente BIGINT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    regiao VARCHAR(20) NOT NULL,

    CONSTRAINT chk_cli_s_regiao
        CHECK (regiao = 'Sul')
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS PROD_OPERACIONAL (
    id_produto BIGINT PRIMARY KEY,
    descricao TEXT,
    estoque INT NOT NULL DEFAULT 0,

    CONSTRAINT chk_prod_estoque
        CHECK (estoque >= 0)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS PED_SE (
    id_pedido BIGINT PRIMARY KEY,
    id_cliente BIGINT NOT NULL,
    data_pedido TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    regiao VARCHAR(20) NOT NULL,

    CONSTRAINT chk_ped_se_regiao
        CHECK (regiao = 'Sudeste'),

    CONSTRAINT chk_ped_se_valor
        CHECK (valor_total >= 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS PED_S (
    id_pedido BIGINT PRIMARY KEY,
    id_cliente BIGINT NOT NULL,
    data_pedido TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    regiao VARCHAR(20) NOT NULL,

    CONSTRAINT chk_ped_s_regiao
        CHECK (regiao = 'Sul'),

    CONSTRAINT chk_ped_s_valor
        CHECK (valor_total >= 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ITEM_SE (
    id_item BIGINT PRIMARY KEY,
    id_pedido BIGINT NOT NULL,
    id_produto BIGINT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(12,2) NOT NULL,

    CONSTRAINT chk_item_se_quantidade
        CHECK (quantidade > 0),

    CONSTRAINT chk_item_se_preco
        CHECK (preco_unitario >= 0),

    CONSTRAINT fk_item_se_pedido
        FOREIGN KEY (id_pedido)
        REFERENCES PED_SE(id_pedido)
        ON DELETE RESTRICT,

    CONSTRAINT fk_item_se_produto
        FOREIGN KEY (id_produto)
        REFERENCES PROD_OPERACIONAL(id_produto)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ITEM_S (
    id_item BIGINT PRIMARY KEY,
    id_pedido BIGINT NOT NULL,
    id_produto BIGINT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(12,2) NOT NULL,

    CONSTRAINT chk_item_s_quantidade
        CHECK (quantidade > 0),

    CONSTRAINT chk_item_s_preco
        CHECK (preco_unitario >= 0),

    CONSTRAINT fk_item_s_pedido
        FOREIGN KEY (id_pedido)
        REFERENCES PED_S(id_pedido)
        ON DELETE RESTRICT,

    CONSTRAINT fk_item_s_produto
        FOREIGN KEY (id_produto)
        REFERENCES PROD_OPERACIONAL(id_produto)
        ON DELETE RESTRICT
) ENGINE=InnoDB;
