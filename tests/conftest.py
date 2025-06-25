from pytest import fixture

from amigoz_desafio_cotacoes.domain.quotation import Quotation


@fixture
def dollar_620() -> Quotation:
    return Quotation(
        name="dollar",
        kind="USD",
        price=620,
    )


@fixture
def euro_570() -> Quotation:
    return Quotation(
        name="euro",
        kind="EUR",
        price=570,
    )
