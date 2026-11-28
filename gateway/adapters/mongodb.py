
from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    DuplicateKeyError,
    PyMongoError,
)

from bson import ObjectId

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


class MongoDBAdapter(DatabaseAdapter):

    FRAGMENTOS = {
        "AVALIACAO": {
            "colecao": "Avaliacao",
            "campos": {
                "id_avaliacao",
                "id_cliente",
                "id_produto",
                "nota",
                "comentario",
                "data_avaliacao",
            },
        },
    }

    OPERADORES = {
        "eq": "$eq",
        "ne": "$ne",
        "gt": "$gt",
        "gte": "$gte",
        "lt": "$lt",
        "lte": "$lte",
        "in": "$in",
    }

    def __init__(self, client_factory=None):
        self.client_factory = client_factory or MongoClient

    def _conectar(self):
        cliente = None

        try:
            cliente = self.client_factory(
                host=settings.MONGO_HOST,
                port=settings.MONGO_PORT,
                username=settings.MONGO_USER,
                password=settings.MONGO_PASSWORD,
                authSource=settings.MONGO_AUTH_SOURCE,
                serverSelectionTimeoutMS=5000,
            )

            cliente.admin.command("ping")

            return cliente

        except ConnectionFailure as erro:
            if cliente:
                cliente.close()

            raise ConnectionException(
                "Não foi possível conectar ao banco MongoDB."
            ) from erro

        except PyMongoError as erro:
            if cliente:
                cliente.close()

            raise ConnectionException(
                "Erro ao estabelecer conexão com o MongoDB."
            ) from erro

    def _fragmento(self, fragmento):
        if fragmento not in self.FRAGMENTOS:
            raise FragmentNotFoundException(
                f"Fragmento MongoDB não encontrado: {fragmento}"
            )

        return self.FRAGMENTOS[fragmento]

    def _validar_campos(self, fragmento, campos):
        campos_validos = fragmento["campos"]

        for campo in campos:
            if campo not in campos_validos:
                raise ValidationException(
                    f"Campo inválido: {campo}"
                )

    def _montar_filtros(self, filtros, fragmento):
        validate_filters(filtros)

        if filtros is None:
            return {}

        self._validar_campos(fragmento, filtros.keys())

        consulta = {}

        for campo, valor in filtros.items():

            if isinstance(valor, dict):
                condicoes = {}

                for operador, argumento in valor.items():
                    if operador == "in" and not argumento:
                        raise ValidationException(
                            "A lista do operador in não pode ser vazia."
                        )

                    condicoes[self.OPERADORES[operador]] = argumento

                consulta[campo] = condicoes

            else:
                consulta[campo] = valor

        return consulta

    def _normalizar_dados(self, dados):
        if isinstance(dados, ObjectId):
            return str(dados)

        if isinstance(dados, list):
            return [
                self._normalizar_dados(item)
                for item in dados
            ]

        if isinstance(dados, dict):
            return {
                chave: self._normalizar_dados(valor)
                for chave, valor in dados.items()
            }

        return dados

    def _executar(self, info, operacao):
        cliente = None

        try:
            cliente = self._conectar()

            banco = cliente[settings.MONGO_DATABASE]
            colecao = banco[info["colecao"]]

            return operacao(colecao)

        except AdapterException:
            raise

        except DuplicateKeyError as erro:
            raise DuplicateKeyException(
                "Já existe um registro com essa chave."
            ) from erro

        except ConnectionFailure as erro:
            raise ConnectionException(
                "Falha na conexão com o MongoDB."
            ) from erro

        except PyMongoError as erro:
            raise DatabaseException(
                "Erro durante a operação no MongoDB."
            ) from erro

        finally:
            if cliente:
                cliente.close()

    def _resultado(self, operacao):
        try:
            return operacao()

        except AdapterException as erro:
            return erro.to_result()

        except Exception:
            return AdapterResult.failure(
                ErrorCode.DATABASE_ERROR,
                "Erro inesperado no adapter MongoDB."
            )

    def find(
        self,
        fragmento: str,
        filtros: Filters | None = None
    ) -> AdapterResult[list[Record]]:

        def operacao():
            info = self._fragmento(fragmento)
            consulta = self._montar_filtros(filtros, info)

            dados = self._executar(
                info,
                lambda colecao: list(colecao.find(consulta))
            )

            dados = self._normalizar_dados(dados)

            return AdapterResult.success(
                dados=dados,
                total=len(dados)
            )

        return self._resultado(operacao)

    def insert(
        self,
        fragmento: str,
        dados: Record
    ) -> AdapterResult[Record]:

        def operacao():
            info = self._fragmento(fragmento)

            if not isinstance(dados, dict) or not dados:
                raise ValidationException(
                    "Os dados para inserção são inválidos."
                )

            self._validar_campos(info, dados.keys())

            documento = dados.copy()

            resultado = self._executar(
                info,
                lambda colecao: colecao.insert_one(documento)
            )

            documento["_id"] = resultado.inserted_id

            return AdapterResult.success(
                dados=self._normalizar_dados(documento),
                total=1
            )

        return self._resultado(operacao)

    def update(
        self,
        fragmento: str,
        filtros: Filters,
        dados: Record
    ) -> AdapterResult[None]:

        def operacao():
            info = self._fragmento(fragmento)

            validate_filters(filtros, required=True)

            if not isinstance(dados, dict) or not dados:
                raise ValidationException(
                    "Os dados para atualização são inválidos."
                )

            self._validar_campos(info, dados.keys())

            consulta = self._montar_filtros(filtros, info)

            resultado = self._executar(
                info,
                lambda colecao: colecao.update_many(
                    consulta,
                    {"$set": dados}
                )
            )

            return AdapterResult.success(
                total=resultado.modified_count
            )

        return self._resultado(operacao)

    def delete(
        self,
        fragmento: str,
        filtros: Filters
    ) -> AdapterResult[None]:

        def operacao():
            info = self._fragmento(fragmento)

            validate_filters(filtros, required=True)

            consulta = self._montar_filtros(filtros, info)

            resultado = self._executar(
                info,
                lambda colecao: colecao.delete_many(consulta)
            )

            return AdapterResult.success(
                total=resultado.deleted_count
            )

        return self._resultado(operacao)

    def count(
        self,
        fragmento: str,
        filtros: Filters | None = None
    ) -> AdapterResult[None]:

        def operacao():
            info = self._fragmento(fragmento)
            consulta = self._montar_filtros(filtros, info)

            total = self._executar(
                info,
                lambda colecao: colecao.count_documents(consulta)
            )

            return AdapterResult.success(
                dados=None,
                total=total
            )

        return self._resultado(operacao)
