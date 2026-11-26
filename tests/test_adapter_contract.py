import unittest

from gateway.adapters.base import DatabaseAdapter
from gateway.adapters.types import AdapterResult, ErrorCode
from gateway.adapters.exceptions import ConnectionException


class FakeAdapter(DatabaseAdapter):

    def __init__(self):
        self.registros = []

    def find(self, fragmento, filtros=None):
        registros = [
            registro.copy()
            for registro in self.registros
            if self.matches(registro, filtros)
        ]

        return AdapterResult.success(
            dados=registros,
            total=len(registros)
        )

    def insert(self, fragmento, dados):
        self.registros.append(dados.copy())

        return AdapterResult.success(
            dados=dados.copy(),
            total=1
        )

    def update(self, fragmento, filtros, dados):
        total = 0

        for registro in self.registros:
            if self.matches(registro, filtros):
                registro.update(dados)
                total += 1

        return AdapterResult.success(total=total)

    def delete(self, fragmento, filtros):
        total_anterior = len(self.registros)

        self.registros = [
            registro
            for registro in self.registros
            if not self.matches(registro, filtros)
        ]

        return AdapterResult.success(
            total=total_anterior - len(self.registros)
        )

    def count(self, fragmento, filtros=None):
        total = self.find(fragmento, filtros).total
        return AdapterResult.success(total=total)

    @staticmethod
    def matches(registro, filtros):
        return all(
            registro.get(campo) == valor
            for campo, valor in (filtros or {}).items()
        )


class TestAdapterContract(unittest.TestCase):

    def setUp(self):
        self.adapter = FakeAdapter()
        self.fragmento = "CLI_NE"

        self.cliente = {
            "id_cliente": 1,
            "nome": "Maria",
            "regiao": "Nordeste"
        }

    def test_interface_abstrata(self):
        with self.assertRaises(TypeError):
            DatabaseAdapter()

    def test_adapter_incompleto(self):
        class AdapterIncompleto(DatabaseAdapter):
            pass

        with self.assertRaises(TypeError):
            AdapterIncompleto()

    def test_insert(self):
        resultado = self.adapter.insert(
            self.fragmento, self.cliente
        )

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 1)
        self.assertEqual(resultado.dados, self.cliente)
        self.assertIsNone(resultado.erro)

    def test_find(self):
        self.adapter.insert(self.fragmento, self.cliente)

        resultado = self.adapter.find(
            self.fragmento, {"id_cliente": 1}
        )

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 1)
        self.assertEqual(resultado.dados[0]["nome"], "Maria")

    def test_find_sem_resultados(self):
        resultado = self.adapter.find(
            self.fragmento, {"id_cliente": 999}
        )

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 0)
        self.assertEqual(resultado.dados, [])

    def test_update(self):
        self.adapter.insert(self.fragmento, self.cliente)

        resultado = self.adapter.update(
            self.fragmento,
            {"id_cliente": 1},
            {"nome": "Ana"}
        )

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 1)
        self.assertIsNone(resultado.dados)

        consulta = self.adapter.find(
            self.fragmento, {"id_cliente": 1}
        )

        self.assertEqual(consulta.dados[0]["nome"], "Ana")

    def test_delete(self):
        self.adapter.insert(self.fragmento, self.cliente)

        resultado = self.adapter.delete(
            self.fragmento, {"id_cliente": 1}
        )

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 1)
        self.assertIsNone(resultado.dados)
        self.assertEqual(
            self.adapter.count(self.fragmento).total, 0
        )

    def test_count(self):
        self.adapter.insert(self.fragmento, self.cliente)

        resultado = self.adapter.count(self.fragmento)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.total, 1)
        self.assertIsNone(resultado.dados)

    def test_count_com_filtro(self):
        self.adapter.insert(self.fragmento, self.cliente)

        resultado = self.adapter.count(
            self.fragmento, {"regiao": "Nordeste"}
        )

        self.assertEqual(resultado.total, 1)

        resultado = self.adapter.count(
            self.fragmento, {"regiao": "Sul"}
        )

        self.assertEqual(resultado.total, 0)

    def test_resultado_de_erro(self):
        resultado = AdapterResult.failure(
            ErrorCode.DATABASE_ERROR,
            "Erro no banco de dados"
        )

        self.assertFalse(resultado.sucesso)
        self.assertIsNone(resultado.dados)
        self.assertEqual(resultado.total, 0)
        self.assertEqual(
            resultado.erro.codigo, ErrorCode.DATABASE_ERROR
        )

    def test_conversao_de_excecao(self):
        erro = ConnectionException("Banco indisponivel")
        resultado = erro.to_result()

        self.assertFalse(resultado.sucesso)
        self.assertEqual(
            resultado.erro.codigo, ErrorCode.CONNECTION_ERROR
        )
        self.assertEqual(
            resultado.erro.mensagem, "Banco indisponivel"
        )


if __name__ == "__main__":
    unittest.main()
