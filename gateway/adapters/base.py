from abc import ABC, abstractmethod

from .types import AdapterResult, Record, Filters


class DatabaseAdapter(ABC):

    @abstractmethod
    def find(
        self,
        fragmento: str,
        filtros: Filters | None = None
    ) -> AdapterResult[list[Record]]:
        """Buscar registros em um fragmento."""
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        fragmento: str,
        dados: Record
    ) -> AdapterResult[Record]:
        """Inserir um registro em um fragmento."""
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        fragmento: str,
        filtros: Filters,
        dados: Record
    ) -> AdapterResult[None]:
        """Atualizar registros de um fragmento."""
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        fragmento: str,
        filtros: Filters
    ) -> AdapterResult[None]:
        """Excluir registros de um fragmento."""
        raise NotImplementedError

    @abstractmethod
    def count(
        self,
        fragmento: str,
        filtros: Filters | None = None
    ) -> AdapterResult[None]:
        """Contar registros de um fragmento."""
        raise NotImplementedError
