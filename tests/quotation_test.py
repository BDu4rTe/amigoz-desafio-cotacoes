import pytest

from amigoz_desafio_cotacoes.domain.quotation import Quotation
from tests.conftest import (
    dollar_620,
    euro_570,
)


def test_quotation_name(dollar_620):
    assert dollar_620.name == "dollar"


def test_quotation_kind(dollar_620):
    assert dollar_620.kind == "USD"


def test_quotation_price(dollar_620):
    assert dollar_620.price == 620


@pytest.mark.errors
def test_quotation_with_negative_price():
    with pytest.raises(ValueError):
        Quotation(
            name="dollar",
            kind="USD",
            price=-1,
        )


@pytest.mark.errors
def test_quotation_with_zero_price():
    with pytest.raises(ValueError):
        Quotation(
            name="dollar",
            kind="USD",
            price=0,
        )
