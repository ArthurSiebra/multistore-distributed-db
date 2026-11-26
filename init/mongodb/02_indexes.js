const database = db.getSiblingDB(
    process.env.MONGO_INITDB_DATABASE || "multistore"
);

database.Avaliacao.createIndex(
    { id_avaliacao: 1 },
    {
        unique: true,
        name: "idx_avaliacao_id"
    }
);

database.Avaliacao.createIndex(
    { id_cliente: 1 },
    {
        name: "idx_avaliacao_cliente"
    }
);

database.Avaliacao.createIndex(
    { id_produto: 1 },
    {
        name: "idx_avaliacao_produto"
    }
);

print("Indices da colecao Avaliacao criados com sucesso.");