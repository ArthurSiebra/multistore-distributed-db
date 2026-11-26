const database = db.getSiblingDB(
    process.env.MONGO_INITDB_DATABASE || "multistore"
);

database.createCollection("Avaliacao", {
    validator: {
        $jsonSchema: {
            bsonType: "object",

            required: [
                "id_avaliacao",
                "id_cliente",
                "id_produto",
                "nota",
                "data_avaliacao"
            ],

            properties: {
                id_avaliacao: {
                    bsonType: ["int", "long"],
                    description: "Identificador global da avaliacao"
                },

                id_cliente: {
                    bsonType: ["int", "long"],
                    description: "Identificador do cliente"
                },

                id_produto: {
                    bsonType: ["int", "long"],
                    description: "Identificador do produto"
                },

                nota: {
                    bsonType: ["int", "long"],
                    minimum: 1,
                    maximum: 5,
                    description: "Nota inteira entre 1 e 5"
                },

                comentario: {
                    bsonType: "string",
                    description: "Comentario do cliente"
                },

                data_avaliacao: {
                    bsonType: "date",
                    description: "Data da avaliacao"
                }
            }
        }
    },

    validationLevel: "strict",
    validationAction: "error"
});

print("Colecao Avaliacao criada com sucesso.");