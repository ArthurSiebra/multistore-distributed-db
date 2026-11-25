-- Fragmentos de Cliente

CREATE TABLE IF NOT EXISTS CLI_N (
    id_cliente BIGINT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    regiao VARCHAR(20) NOT NULL CHECK (regiao = 'Norte')
);

CREATE TABLE IF NOT EXISTS CLI_NE (
    id_cliente BIGINT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    regiao VARCHAR(20) NOT NULL CHECK (regiao = 'Nordeste')
);

CREATE TABLE IF NOT EXISTS CLI_CO (
    id_cliente BIGINT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    regiao VARCHAR(20) NOT NULL CHECK (regiao = 'Centro-Oeste')
);

-- Fragmento comercial de Produto

CREATE TABLE IF NOT EXISTS PROD_COMERCIAL (
    id_produto BIGINT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    preco NUMERIC(12,2) NOT NULL CHECK (preco >= 0)
);

-- Fragmentos de Pedido

CREATE TABLE IF NOT EXISTS PED_N (
    id_pedido BIGINT PRIMARY KEY,
    data_pedido TIMESTAMP NOT NULL,
    valor_total NUMERIC(12,2) NOT NULL CHECK (valor_total >= 0),
    status VARCHAR(30) NOT NULL,
    regiao VARCHAR(20) NOT NULL CHECK (regiao = 'Norte'),
    id_cliente BIGINT NOT NULL,
    CONSTRAINT fk_ped_n_cliente
        FOREIGN KEY (id_cliente) REFERENCES CLI_N(id_cliente)
);

CREATE TABLE IF NOT EXISTS PED_NE (
    id_pedido BIGINT PRIMARY KEY,
    data_pedido TIMESTAMP NOT NULL,
    valor_total NUMERIC(12,2) NOT NULL CHECK (valor_total >= 0),
    status VARCHAR(30) NOT NULL,
    regiao VARCHAR(20) NOT NULL CHECK (regiao = 'Nordeste'),
    id_cliente BIGINT NOT NULL,
    CONSTRAINT fk_ped_ne_cliente
        FOREIGN KEY (id_cliente) REFERENCES CLI_NE(id_cliente)
);

CREATE TABLE IF NOT EXISTS PED_CO (
    id_pedido BIGINT PRIMARY KEY,
    data_pedido TIMESTAMP NOT NULL,
    valor_total NUMERIC(12,2) NOT NULL CHECK (valor_total >= 0),
    status VARCHAR(30) NOT NULL,
    regiao VARCHAR(20) NOT NULL CHECK (regiao = 'Centro-Oeste'),
    id_cliente BIGINT NOT NULL,
    CONSTRAINT fk_ped_co_cliente
        FOREIGN KEY (id_cliente) REFERENCES CLI_CO(id_cliente)
);

-- Fragmentos de Item_Pedido

CREATE TABLE IF NOT EXISTS ITEM_N (
    id_item BIGINT PRIMARY KEY,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario NUMERIC(12,2) NOT NULL CHECK (preco_unitario >= 0),
    id_pedido BIGINT NOT NULL,
    id_produto BIGINT NOT NULL,
    CONSTRAINT fk_item_n_pedido
        FOREIGN KEY (id_pedido) REFERENCES PED_N(id_pedido)
);

CREATE TABLE IF NOT EXISTS ITEM_NE (
    id_item BIGINT PRIMARY KEY,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario NUMERIC(12,2) NOT NULL CHECK (preco_unitario >= 0),
    id_pedido BIGINT NOT NULL,
    id_produto BIGINT NOT NULL,
    CONSTRAINT fk_item_ne_pedido
        FOREIGN KEY (id_pedido) REFERENCES PED_NE(id_pedido)
);

CREATE TABLE IF NOT EXISTS ITEM_CO (
    id_item BIGINT PRIMARY KEY,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario NUMERIC(12,2) NOT NULL CHECK (preco_unitario >= 0),
    id_pedido BIGINT NOT NULL,
    id_produto BIGINT NOT NULL,
    CONSTRAINT fk_item_co_pedido
        FOREIGN KEY (id_pedido) REFERENCES PED_CO(id_pedido)
);
