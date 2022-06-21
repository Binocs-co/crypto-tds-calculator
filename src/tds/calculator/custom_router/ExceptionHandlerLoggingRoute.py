from typing import Callable, List

from fastapi import HTTPException, Request, Response, status
from fastapi.routing import APIRoute
from tds.calculator.common.logger import get_logger

logger = get_logger(__name__)


class ExceptionHandlerLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except HTTPException as http_except:
                logger.exception(http_except)
                raise http_except
            except Exception as exce:
                logger.exception(exce)
                detail = {"errors": str(exce)}
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

        return custom_route_handler
