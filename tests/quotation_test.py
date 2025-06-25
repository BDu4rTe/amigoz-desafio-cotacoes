from unittest.mock import AsyncMock

import pytest

from amigoz_desafio_cotacoes.domain.quotation import Quotation
from amigoz_desafio_cotacoes.domain.quotation_repository import (
    QuotationRepository,
)
from amigoz_desafio_cotacoes.domain.quotation_service import QuotationService
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


@pytest.mark.errors
def test_quotation_with_float_price():
    with pytest.raises(ValueError):
        Quotation(
            name="dollar",
            kind="USD",
            price=6.20,
        )


@pytest.mark.asyncio
async def test_find_best_quotation_succ(dollar_620, euro_570):
    repository = AsyncMock(spec=QuotationRepository)
    repository.get_dollar.return_value = dollar_620
    repository.get_euro.return_value = euro_570
    service = QuotationService(repository)
    best_quotation = await service.find_best_quotation()

    assert best_quotation == euro_570

    repository.get_dollar.assert_called_once()
    repository.get_euro.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.errors
async def test_find_best_quotation_dollar_fail(euro_570):
    repository = AsyncMock(spec=QuotationRepository)
    repository.get_dollar.side_effect = Exception("Timeout")
    repository.get_euro.return_value = euro_570

    service = QuotationService(repository)

    with pytest.raises(ValueError):  # match ??
        await service.find_best_quotation()


@pytest.mark.asyncio
@pytest.mark.errors
async def test_find_best_quotation_euro_fail(dollar_620):
    repository = AsyncMock(spec=QuotationRepository)
    repository.get_dollar.return_value = dollar_620
    repository.get_euro.side_effect = Exception("Timeout")

    service = QuotationService(repository)

    with pytest.raises(ValueError):  # match ??
        await service.find_best_quotation()
