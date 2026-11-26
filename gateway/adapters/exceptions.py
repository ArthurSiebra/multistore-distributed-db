from .types import AdapterResult, ErrorCode


class AdapterException(Exception):

    def __init__(self, codigo: ErrorCode, mensagem: str):
        self.codigo = codigo
        self.mensagem = mensagem
        super().__init__(mensagem)

    def to_result(self) -> AdapterResult:
        return AdapterResult.failure(
            codigo=self.codigo,
            mensagem=self.mensagem
        )


class ConnectionException(AdapterException):

    def __init__(self, mensagem: str):
        super().__init__(ErrorCode.CONNECTION_ERROR, mensagem)


class FragmentNotFoundException(AdapterException):

    def __init__(self, mensagem: str):
        super().__init__(ErrorCode.FRAGMENT_NOT_FOUND, mensagem)


class ValidationException(AdapterException):

    def __init__(self, mensagem: str):
        super().__init__(ErrorCode.VALIDATION_ERROR, mensagem)


class DuplicateKeyException(AdapterException):

    def __init__(self, mensagem: str):
        super().__init__(ErrorCode.DUPLICATE_KEY, mensagem)


class RecordNotFoundException(AdapterException):

    def __init__(self, mensagem: str):
        super().__init__(ErrorCode.RECORD_NOT_FOUND, mensagem)


class DatabaseException(AdapterException):

    def __init__(self, mensagem: str):
        super().__init__(ErrorCode.DATABASE_ERROR, mensagem)


class PartialFailureException(AdapterException):

    def __init__(self, mensagem: str):
        super().__init__(ErrorCode.PARTIAL_FAILURE, mensagem)
