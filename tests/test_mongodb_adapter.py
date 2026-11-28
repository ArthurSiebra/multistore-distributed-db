
import unittest
from unittest.mock import MagicMock

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from gateway.adapters.mongodb import MongoDBAdapter
from gateway.adapters.types import ErrorCode


class TestMongoDBAdapter(unittest.TestCase):

    def setUp(self):
        self.client = MagicMock()
        self.database = MagicMock()
        self.collection = MagicMock()

        self.client.__getitem__.return_value = self.database
        self.database.__getitem__.return_value = self.collection

        self.adapter = MongoDBAdapter(
            client_factory=lambda **kwargs: self.client
        )

        self.fragmento = "AVALIACAO"

        self.avaliacao = {
            "id_avaliacao": 1,
            "id_cliente": 10,
            "id_produto": 20,
            "nota": 5,
            "comentario": "Produto excelente",
        }

    def test_fragmento_valido(self):
        info = self.adapter._fragmento(self.fragmento)

        self.assertEqual(info["colecao"], "Avaliacao")

    def test_fragmento_inexistente(self):
        resultado = self.adapter.find("FRAGMENTO_INVALIDO")

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo,
            ErrorCode.FRAGMENT_NOT_FOUND
        )

    def test_montar_filtros(self):
        filtros = {
            "nota": {"gte": 4},
            "id_cliente": 10,
        }

        resultado = self.adapter._montar_filtros(
            filtros,
            self.adapter.FRAGMENTOS[self.fragmento]
        )

        self.assertEqual(resultado["nota"], {"$gte": 4})
        self.assertEqual(resultado["id_cliente"], 10)

    def test_operador_in(self):
        filtros = {
            "nota": {"in": [4, 5]}
        }

        resultado = self.adapter._montar_filtros(
            filtros,
            self.adapter.FRAGMENTOS[self.fragmento]
        )

        self.assertEqual(
            resultado,
            {"nota": {"$in": [4, 5]}}
        )

    def test_campo_invalido(self):
        resultado = self.adapter.find(
            self.fragmento,
            {"campo_inexistente": 10}
        )

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo,
            ErrorCode.VALIDATION_ERROR
        )

    def test_find(self):
        self.collection.find.return_value = [
            self.avaliacao.copy()
        ]

        resultado = self.adapter.find(self.fragmento)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 1)
        self.assertEqual(
            resultado.dados[0]["nota"],
            5
        )

        self.collection.find.assert_called_once_with({})

    def test_insert(self):
        object_id = ObjectId()
        self.collection.insert_one.return_value.inserted_id = object_id

        resultado = self.adapter.insert(
            self.fragmento,
            self.avaliacao
        )

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 1)
        self.assertEqual(
            resultado.dados["_id"],
            str(object_id)
        )

        self.collection.insert_one.assert_called_once()

    def test_insert_dados_invalidos(self):
        resultado = self.adapter.insert(
            self.fragmento,
            {}
        )

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo,
            ErrorCode.VALIDATION_ERROR
        )

    def test_update(self):
        self.collection.update_many.return_value.modified_count = 1

        resultado = self.adapter.update(
            self.fragmento,
            {"id_avaliacao": 1},
            {"nota": 4}
        )

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 1)
        self.assertIsNone(resultado.dados)

        self.collection.update_many.assert_called_once_with(
            {"id_avaliacao": 1},
            {"$set": {"nota": 4}}
        )

    def test_update_sem_filtro(self):
        resultado = self.adapter.update(
            self.fragmento,
            {},
            {"nota": 4}
        )

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo,
            ErrorCode.VALIDATION_ERROR
        )

    def test_delete(self):
        self.collection.delete_many.return_value.deleted_count = 1

        resultado = self.adapter.delete(
            self.fragmento,
            {"id_avaliacao": 1}
        )

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 1)

        self.collection.delete_many.assert_called_once_with(
            {"id_avaliacao": 1}
        )

    def test_delete_sem_filtro(self):
        resultado = self.adapter.delete(
            self.fragmento,
            {}
        )

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo,
            ErrorCode.VALIDATION_ERROR
        )

    def test_count(self):
        self.collection.count_documents.return_value = 5

        resultado = self.adapter.count(self.fragmento)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 5)
        self.assertIsNone(resultado.dados)

    def test_chave_duplicada(self):
        self.collection.insert_one.side_effect = DuplicateKeyError(
            "Chave duplicada"
        )

        resultado = self.adapter.insert(
            self.fragmento,
            self.avaliacao
        )

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo,
            ErrorCode.DUPLICATE_KEY
        )

    def test_conexao_fechada(self):
        self.collection.find.return_value = []

        self.adapter.find(self.fragmento)

        self.client.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
