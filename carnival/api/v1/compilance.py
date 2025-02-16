from carnival.api.deps import get_compilance_service
from carnival.api.v1.schemas import CheckCompilancePayload
from carnival.services.compilance_service import ComplianceService, CompliantReport
from carnival.core.logger import logger
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import Annotated

router = APIRouter(tags=["Compilance Service"], prefix="/compilance")


@router.post("/", response_model=CompliantReport)
async def check_optimizaiton_compilance(
    body: CheckCompilancePayload,
    compilance_service: Annotated[ComplianceService, Depends(get_compilance_service)],
):
    try:
        compilance_report = await compilance_service.check_optimization_compliance(
            departure_port=body.departure_port, arrival_port=body.arrival_port
        )
        return compilance_report
    except Exception as e:
        logger.error(
            f"COMPILANCE ROUTE:  failed to generate compilance report: >> \n {e} "
        )
        raise HTTPException(
            detail=str(e), status_code=500
        )  # TODO:: customize this status code accordingly
