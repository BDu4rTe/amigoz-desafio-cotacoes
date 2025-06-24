from abc import ABC, abstractmethod
from amigoz_desafio_cotacoes.domain.quotation import Quotation


class QuotationRepository(ABC):
    @abstractmethod
    async def get_dollar(self) -> Quotation:
        raise NotImplementedError("Implement get_dollar method")

    @abstractmethod
    async def get_euro(self) -> Quotation:
        raise NotImplementedError("Implement get_euro method")
