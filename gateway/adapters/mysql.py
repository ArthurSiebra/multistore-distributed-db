
import mysql.connector
from mysql.connector import Error, IntegrityError
from mysql.connector.errorcode import ER_DUP_ENTRY

from gateway.core.config import settings
from .base import DatabaseAdapter
from .exceptions import (
    AdapterException,
    ConnectionException,
    DatabaseException,
    DuplicateKeyException,
    FragmentNotFoundException,
    ValidationException,
)
from .filters import validate_filters
from .types import AdapterResult, ErrorCode, Filters, Record


class MySQLAdapter(DatabaseAdapter):

    FRAGMENTOS = {
        "CLI_SE": {
            "tabela": "CLI_SE",
            "colunas": {"id_cliente", "nome", "email", "telefone", "cidade", "estado", "regiao"},
        },
        "CLI_S": {
            "tabela": "CLI_S",
            "colunas": {"id_cliente", "nome", "email", "telefone", "cidade", "estado", "regiao"},
        },
        "PED_SE": {
            "tabela": "PED_SE",
            "colunas": {"id_pedido", "id_cliente", "data_pedido", "valor_total", "status", "regiao"},
        },
        "PED_S": {
            "tabela": "PED_S",
            "colunas": {"id_pedido", "id_cliente", "data_pedido", "valor_total", "status", "regiao"},
        },
        "ITEM_SE": {
            "tabela": "ITEM_SE",
            "colunas": {"id_item", "id_pedido", "id_produto", "quantidade", "preco_unitario"},
        },
        "ITEM_S": {
            "tabela": "ITEM_S",
            "colunas": {"id_item", "id_pedido", "id_produto", "quantidade", "preco_unitario"},
        },
        "PROD_OPERACIONAL": {
            "tabela": "PROD_OPERACIONAL",
            "colunas": {"id_produto", "descricao", "estoque"},
        },
    }

    OPERADORES = {
        "eq": "=",
        "ne": "!=",
        "gt": ">",
        "gte": ">=",
        "lt": "<",
        "lte": "<=",
    }

    def __init__(self, connection_factory=None):
        self.connection_factory = connection_factory or mysql.connector.connect

    def _conectar(self):
        try:
            return self.connection_factory(
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                database=settings.MYSQL_DATABASE,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
            )
        except Error as erro:
            raise ConnectionException(
                "Não foi possível conectar ao banco MySQL."
            ) from erro

    def _fragmento(self, fragmento):
        if fragmento not in self.FRAGMENTOS:
            raise FragmentNotFoundException(
                f"Fragmento MySQL não encontrado: {fragmento}"
            )

        return self.FRAGMENTOS[fragmento]

    def _validar_colunas(self, fragmento, campos):
        colunas_validas = fragmento["colunas"]

        for campo in campos:
            if campo not in colunas_validas:
                raise ValidationException(
                    f"Coluna inválida: {campo}"
                )

    def _montar_filtros(self, filtros, fragmento):
        validate_filters(filtros)

        if filtros is None:
            filtros = {}

        self._validar_colunas(fragmento, filtros.keys())

        condicoes = []
        parametros = []

        for campo, valor in filtros.items():
            coluna = f"`{campo}`"

            if isinstance(valor, dict):
                for operador, argumento in valor.items():

                    if operador == "in":
                        if not argumento:
                            raise ValidationException(
                                "A lista do operador in não pode ser vazia."
                            )

                        placeholders = ", ".join(["%s"] * len(argumento))
                        condicoes.append(
                            f"{coluna} IN ({placeholders})"
                        )
                        parametros.extend(argumento)

                    else:
                        sql_operador = self.OPERADORES[operador]
                        condicoes.append(
                            f"{coluna} {sql_operador} %s"
                        )
                        parametros.append(argumento)

            else:
                condicoes.append(f"{coluna} = %s")
                parametros.append(valor)

        if not condicoes:
            return "", ()

        return " WHERE " + " AND ".join(condicoes), tuple(parametros)

    def _executar(self, consulta, parametros=(), escrita=False, buscar=False):
        conexao = None
        cursor = None

        try:
            conexao = self._conectar()
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(consulta, parametros)

            if buscar:
                return cursor.fetchall()

            total = cursor.rowcount

            if escrita:
                conexao.commit()

            return total

        except AdapterException:
            if conexao:
                conexao.rollback()
            raise

        except IntegrityError as erro:
            if conexao:
                conexao.rollback()

            if erro.errno == ER_DUP_ENTRY:
                raise DuplicateKeyException(
                    "Já existe um registro com essa chave."
                ) from erro

            raise DatabaseException(
                "Erro de integridade no banco MySQL."
            ) from erro

        except Error as erro:
            if conexao:
                conexao.rollback()

            raise DatabaseException(
                "Erro durante a operação no MySQL."
            ) from erro

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def _resultado(self, operacao, *args, **kwargs):
        try:
            return operacao(*args, **kwargs)
        except AdapterException as erro:
            return erro.to_result()
        except Exception:
            return AdapterResult.failure(
                ErrorCode.DATABASE_ERROR,
                "Erro inesperado no adapter MySQL."
            )

    def find(self, fragmento: str, filtros: Filters | None = None) -> AdapterResult[list[Record]]:
        def operacao():
            info = self._fragmento(fragmento)
            where, parametros = self._montar_filtros(filtros, info)

            consulta = f"SELECT * FROM `{info['tabela']}`{where}"
            dados = self._executar(consulta, parametros, buscar=True)

            return AdapterResult.success(dados=dados, total=len(dados))

        return self._resultado(operacao)

    def insert(self, fragmento: str, dados: Record) -> AdapterResult[Record]:
        def operacao():
            info = self._fragmento(fragmento)

            if not isinstance(dados, dict) or not dados:
                raise ValidationException("Os dados para inserção são inválidos.")

            self._validar_colunas(info, dados.keys())

            colunas = list(dados.keys())
            nomes = ", ".join(f"`{campo}`" for campo in colunas)
            placeholders = ", ".join(["%s"] * len(colunas))

            consulta = (
                f"INSERT INTO `{info['tabela']}` ({nomes}) "
                f"VALUES ({placeholders})"
            )

            self._executar(
                consulta,
                tuple(dados[campo] for campo in colunas),
                escrita=True,
            )

            return AdapterResult.success(dados=dados, total=1)

        return self._resultado(operacao)

    def update(self, fragmento: str, filtros: Filters, dados: Record) -> AdapterResult[None]:
        def operacao():
            info = self._fragmento(fragmento)
            validate_filters(filtros, required=True)

            if not isinstance(dados, dict) or not dados:
                raise ValidationException("Os dados para atualização são inválidos.")

            self._validar_colunas(info, dados.keys())

            where, parametros_filtro = self._montar_filtros(filtros, info)

            atribuicoes = ", ".join(
                f"`{campo}` = %s" for campo in dados
            )

            consulta = (
                f"UPDATE `{info['tabela']}` "
                f"SET {atribuicoes}{where}"
            )

            parametros = tuple(dados.values()) + parametros_filtro
            total = self._executar(consulta, parametros, escrita=True)

            return AdapterResult.success(total=total)

        return self._resultado(operacao)

    def delete(self, fragmento: str, filtros: Filters) -> AdapterResult[None]:
        def operacao():
            info = self._fragmento(fragmento)
            validate_filters(filtros, required=True)

            where, parametros = self._montar_filtros(filtros, info)

            consulta = f"DELETE FROM `{info['tabela']}`{where}"
            total = self._executar(consulta, parametros, escrita=True)

            return AdapterResult.success(total=total)

        return self._resultado(operacao)

    def count(self, fragmento: str, filtros: Filters | None = None) -> AdapterResult[None]:
        def operacao():
            info = self._fragmento(fragmento)
            where, parametros = self._montar_filtros(filtros, info)

            consulta = f"SELECT COUNT(*) AS total FROM `{info['tabela']}`{where}"
            dados = self._executar(consulta, parametros, buscar=True)

            return AdapterResult.success(
                dados=None,
                total=dados[0]["total"],
            )

        return self._resultado(operacao)
