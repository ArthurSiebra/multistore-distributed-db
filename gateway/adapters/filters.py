from .types import Filters, FilterOperator
from .exceptions import ValidationException


def validate_filters(
    filtros: Filters | None,
    required: bool = False
) -> None:

    if filtros is None:
        if required:
            raise ValidationException(
                "Os filtros sao obrigatorios."
            )
        return

    if not isinstance(filtros, dict):
        raise ValidationException(
            "Os filtros devem ser um dicionario."
        )

    if required and not filtros:
        raise ValidationException(
            "Filtros vazios nao sao permitidos."
        )

    operadores_validos = {
        operador.value for operador in FilterOperator
    }

    for campo, valor in filtros.items():

        if not isinstance(campo, str) or not campo.strip():
            raise ValidationException(
                "Nome de campo invalido."
            )

        if isinstance(valor, dict):

            if not valor:
                raise ValidationException(
                    f"Filtro vazio para o campo {campo}."
                )

            for operador, argumento in valor.items():

                if operador not in operadores_validos:
                    raise ValidationException(
                        f"Operador invalido: {operador}"
                    )

                if operador == "in":
                    if not isinstance(argumento, list):
                        raise ValidationException(
                            "O operador in exige uma lista."
                        )
