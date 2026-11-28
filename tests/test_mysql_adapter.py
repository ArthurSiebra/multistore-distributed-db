
import unittest
from unittest.mock import MagicMock

from gateway.adapters.mysql import MySQLAdapter
from gateway.adapters.types import ErrorCode


class TestMySQLAdapter(unittest.TestCase):

    def setUp(self):
        self.conexao = MagicMock()
        self.cursor = MagicMock()

        self.conexao.cursor.return_value = self.cursor

        self.adapter = MySQLAdapter(
            connection_factory=MagicMock(return_value=self.conexao)
        )

    def test_fragmento_mysql_valido(self):
        resultado = self.adapter._fragmento("CLI_SE")

        self.assertEqual(resultado["tabela"], "CLI_SE")

    def test_fragmento_inexistente(self):
        resultado = self.adapter.find("CLI_NE")

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo,
            ErrorCode.FRAGMENT_NOT_FOUND
        )

    def test_find(self):
        self.cursor.fetchall.return_value = [
            {"id_cliente": 1, "nome": "Maria"}
        ]

        resultado = self.adapter.find("CLI_SE")

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 1)
        self.assertEqual(resultado.dados[0]["nome"], "Maria")
        self.cursor.execute.assert_called_once_with(
            "SELECT * FROM `CLI_SE`",
            ()
        )

    def test_find_com_filtro(self):
        self.cursor.fetchall.return_value = [
            {"id_cliente": 1, "nome": "Maria"}
        ]

        resultado = self.adapter.find(
            "CLI_SE",
            {"regiao": "Sudeste"}
        )

        self.assertTrue(resultado.sucesso)
        self.cursor.execute.assert_called_once_with(
            "SELECT * FROM `CLI_SE` WHERE `regiao` = %s",
            ("Sudeste",)
        )

    def test_insert(self):
        dados = {
            "id_cliente": 100,
            "nome": "Lucas",
            "email": "lucas@teste.com",
            "cidade": "São Paulo",
            "estado": "SP",
            "regiao": "Sudeste"
        }

        resultado = self.adapter.insert("CLI_SE", dados)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 1)
        self.assertEqual(resultado.dados, dados)
        self.conexao.commit.assert_called_once()

    def test_update(self):
        resultado = self.adapter.update(
            "CLI_SE",
            {"id_cliente": 100},
            {"nome": "Lucas Atualizado"}
        )

        self.assertTrue(resultado.sucesso)
        self.cursor.execute.assert_called_once_with(
            "UPDATE `CLI_SE` SET `nome` = %s WHERE `id_cliente` = %s",
            ("Lucas Atualizado", 100)
        )
        self.conexao.commit.assert_called_once()

    def test_delete(self):
        resultado = self.adapter.delete(
            "CLI_SE",
            {"id_cliente": 100}
        )

        self.assertTrue(resultado.sucesso)
        self.cursor.execute.assert_called_once_with(
            "DELETE FROM `CLI_SE` WHERE `id_cliente` = %s",
            (100,)
        )
        self.conexao.commit.assert_called_once()

    def test_count(self):
        self.cursor.fetchall.return_value = [{"total": 5}]

        resultado = self.adapter.count("CLI_SE")

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 5)
        self.assertIsNone(resultado.dados)

    def test_count_com_filtro(self):
        self.cursor.fetchall.return_value = [{"total": 2}]

        resultado = self.adapter.count(
            "CLI_SE",
            {"regiao": "Sudeste"}
        )

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 2)

    def test_filtro_com_operadores(self):
        filtros = {
            "estoque": {
                "gte": 10,
                "lte": 100
            }
        }

        info = self.adapter._fragmento("PROD_OPERACIONAL")

        where, parametros = self.adapter._montar_filtros(
            filtros,
            info
        )

        self.assertEqual(
            where,
            " WHERE `estoque` >= %s AND `estoque` <= %s"
        )
        self.assertEqual(parametros, (10, 100))

    def test_filtro_in(self):
        info = self.adapter._fragmento("CLI_SE")

        where, parametros = self.adapter._montar_filtros(
            {"estado": {"in": ["SP", "RJ"]}},
            info
        )

        self.assertEqual(
            where,
            " WHERE `estado` IN (%s, %s)"
        )
        self.assertEqual(parametros, ("SP", "RJ"))

    def test_coluna_invalida(self):
        resultado = self.adapter.find(
            "CLI_SE",
            {"senha": "123"}
        )

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo,
            ErrorCode.VALIDATION_ERROR
        )

    def test_update_sem_filtros(self):
        resultado = self.adapter.update(
            "CLI_SE",
            {},
            {"nome": "Teste"}
        )

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo,
            ErrorCode.VALIDATION_ERROR
        )

    def test_delete_sem_filtros(self):
        resultado = self.adapter.delete("CLI_SE", {})

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo,
            ErrorCode.VALIDATION_ERROR
        )

    def test_insert_sem_dados(self):
        resultado = self.adapter.insert("CLI_SE", {})

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo,
            ErrorCode.VALIDATION_ERROR
        )


if __name__ == "__main__":
    unittest.main()
