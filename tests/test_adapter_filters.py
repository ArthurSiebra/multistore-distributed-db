import unittest

from gateway.adapters.filters import validate_filters
from gateway.adapters.exceptions import ValidationException


class TestAdapterFilters(unittest.TestCase):

    def test_filtro_simples(self):
        validate_filters({"id_cliente": 1})

    def test_operadores_validos(self):
        for operador in ["eq", "ne", "gt", "gte", "lt", "lte"]:
            with self.subTest(operador=operador):
                validate_filters({"preco": {operador: 50}})

    def test_multiplos_operadores(self):
        validate_filters({
            "preco": {"gte": 50, "lte": 200}
        })

    def test_operador_in(self):
        validate_filters({
            "regiao": {"in": ["Sul", "Norte"]}
        })

    def test_operador_invalido(self):
        with self.assertRaises(ValidationException):
            validate_filters({"preco": {"abc": 50}})

    def test_in_sem_lista(self):
        with self.assertRaises(ValidationException):
            validate_filters({"regiao": {"in": "Sul"}})

    def test_filtro_vazio_obrigatorio(self):
        with self.assertRaises(ValidationException):
            validate_filters({}, required=True)

    def test_filtro_nulo_obrigatorio(self):
        with self.assertRaises(ValidationException):
            validate_filters(None, required=True)

    def test_filtro_opcional(self):
        validate_filters(None)
        validate_filters({})

    def test_tipo_invalido(self):
        with self.assertRaises(ValidationException):
            validate_filters("filtro invalido")

    def test_campo_invalido(self):
        with self.assertRaises(ValidationException):
            validate_filters({"": 1})

    def test_operadores_vazios(self):
        with self.assertRaises(ValidationException):
            validate_filters({"preco": {}})


if __name__ == "__main__":
    unittest.main()
