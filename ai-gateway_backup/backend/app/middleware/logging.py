import time
import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import uuid

logger = structlog.get_logger(__name__)

class StructlogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            endpoint=request.url.path,
            method=request.method,
        )

        start_time = time.time()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            status_code = response.status_code
            
            # Note: user_id would typically be extracted from auth middleware and bound there
            logger.info(
                "Request completed",
                latency=process_time,
                status=status_code,
            )
            
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            return response
            
        except Exception as exc:
            process_time = time.time() - start_time
            logger.error(
                "Request failed",
                latency=process_time,
                status=500,
                error=str(exc)
            )
            raise
