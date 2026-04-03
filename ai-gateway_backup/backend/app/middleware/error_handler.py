from fastapi import Request
from fastapi.responses import JSONResponse
import structlog
from app.core.exceptions import AIGatewayException

logger = structlog.get_logger(__name__)

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, AIGatewayException):
        logger.warning(
            "Application error", 
            error_code=exc.error_code, 
            message=exc.message
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message
                }
            }
        )

    logger.error("Unhandled exception", error=str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred."
            }
        }
    )
