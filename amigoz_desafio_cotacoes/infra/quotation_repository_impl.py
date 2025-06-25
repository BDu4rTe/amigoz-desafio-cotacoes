import httpx
import logging
import os

from amigoz_desafio_cotacoes.domain.quotation import Quotation
from amigoz_desafio_cotacoes.domain.quotation_repository import (
    QuotationRepository,
)
from amigoz_desafio_cotacoes.exceptions.quotation_exceptions import (
    QuotationTimeoutException,
)

logger: logging.Logger = logging.getLogger(__file__)


class QuotationRepositoryImpl(QuotationRepository):
    def __init__(self):
        self._service_host: str = os.getenv(
            "QUOTATION_SERVICE_HOST",
            "http://localhost",
        )
        self._service_port: str = os.getenv(
            "QUOTATION_SERVICE_PORT",
            "3000"
        )
        self._base_url: str = self._service_host + ":" + self._service_port
        self._timeout: float = 5.0
        self._dollar_route: str = f"{self._base_url}/cotacao/dolar"
        self._euro_route: str = f"{self._base_url}/cotacao/euro"

    async def get_dollar(self) -> Quotation:
        """
        Get dollar quotation.
        """
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                logger.info(f"Request {self._dollar_route}")

                response: httpx.Response = await client.get(self._dollar_route)
                response.raise_for_status()
                data = response.json()
                return Quotation(
                    name=data["currency_name"],
                    kind=data["currency_kind"],
                    price=int(data["currency_price"]),
                )
        except httpx.HTTPStatusError as err:
            err_msg: str = f"HTTP error on get dollar quotation: {str(err)}"
            logger.error(err_msg)
            raise ValueError(err_msg)
        except httpx.ReadTimeout as err:
            url: str = str(err.request.url)
            err_msg: str = f"Timeout on get dollar quotation: {url}"
            logger.error(err_msg)
            raise QuotationTimeoutException(err_msg)
        except httpx.RequestError as err:
            err_msg: str = f"Network error: {str(err)}"
            logger.error(err_msg)
            raise ValueError(err)

    async def get_euro(self) -> Quotation:
        """
        Get euro quotation.
        """
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                logger.info(f"Request {self._euro_route}")

                response: httpx.Response = await client.get(self._euro_route)
                response.raise_for_status()
                data = response.json()
                return Quotation(
                    name=data["cotacao"]["moeda"],
                    kind=data["cotacao"]["sigla"],
                    price=int(data["cotacao"]["valor_comercial"] * 100),
                )
        except httpx.HTTPStatusError as err:
            err_msg: str = f"HTTP error on get euro quotation: {str(err)}"
            logger.error(err_msg)
            raise ValueError(err_msg)
        except httpx.ReadTimeout as err:
            url: str = str(err.request.url)
            err_msg: str = f"Timeout on get euro quotation in: {url}"
            logger.error(err_msg)
            raise QuotationTimeoutException(err_msg)
        except httpx.RequestError as err:
            err_msg: str = f"Network error: {str(err)}"
            logger.error(err_msg)
            raise ValueError(err_msg)
