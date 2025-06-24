import asyncio
import logging
from amigoz_desafio_cotacoes.domain.quotation import Quotation
from amigoz_desafio_cotacoes.domain.quotation_repository import QuotationRepository
from typing import List


logger: logging.Logger = logging.getLogger(__file__)


class QuotationService:
    def __init__(self, repository: QuotationRepository):
        self.__repo = repository

    async def _fetch_quotation(self, method, name: str) -> Quotation:
        """
        ...
        """
        try:
            quotation = await method()
            logger.debug(f"Quotation obtained for {name}: {quotation}")
            return quotation
        except Exception as e:
            logger.error(f"Failed to get quotation from {name}: {str(e)}")
            raise ValueError(f"Failed to get quotation from {name}: {str(e)}")

    async def find_best_quotation(self) -> Quotation:
        """
        ...
        """
        dollar_task = self._fetch_quotation(
            self.__repo.get_dollar,
            "dollar",
        )

        euro_task = self._fetch_quotation(self.__repo.get_euro, "euro")
        quotations: List[Quotation] = await asyncio.gather(
            dollar_task,
            euro_task,
        )

        best_quotation: Quotation = min(quotations, key=lambda q: q.price)
        logger.info(f"Best quotation found: {best_quotation}")
        return best_quotation
