import logging
import os
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)

from amigoz_desafio_cotacoes.domain.quotation import Quotation
from amigoz_desafio_cotacoes.domain.quotation_repository import (
    QuotationRepository,
)
from amigoz_desafio_cotacoes.domain.quotation_service import QuotationService
from amigoz_desafio_cotacoes.infra.quotation_repository_impl import (
    QuotationRepositoryImpl,
)
from amigoz_desafio_cotacoes.exceptions.quotation_exceptions import (
    QuotationTimeoutException,
)

level = os.getenv("LOG_LEVEL", logging.DEBUG)
logging.basicConfig(
    level=level,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)

logger: logging.Logger = logging.getLogger(__file__)

app = FastAPI(
    title="Quotation API",
    description="Evaluates the best quotation between dollar and euro",
)


def get_quotation_service() -> QuotationService:
    """
    DI for QuotationService.
    """
    repository: QuotationRepository = QuotationRepositoryImpl()
    return QuotationService(repository)


@app.get("/cotacao", response_model=Quotation)
async def get_best_quotation(
    service: QuotationService = Depends(get_quotation_service),
):
    """
    Return best quotation between dollar and euro.
    """
    try:
        best_quotation: Quotation = await service.find_best_quotation()
        logger.info(
            f"Best quotation found: {best_quotation.kind} "
            f"{best_quotation.price} {best_quotation.name}s"
        )
        return best_quotation
    except ValueError as err:
        logger.error(f"Error on get best quotation: {str(err)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(err),
        )
    except QuotationTimeoutException as err:
        logger.error(f"Error on get best quotation: {str(err)}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=str(err),
        )

