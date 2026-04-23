from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.utils.logger import setup_logging
from app.middleware.logging import StructlogMiddleware
from app.middleware.error_handler import global_exception_handler
from app.api.v1.api import api_router
from app.core.observability import setup_prometheus_metrics, setup_opentelemetry
import structlog

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging(settings.LOGGING_LEVEL)
    logger = structlog.get_logger(__name__)
    logger.info("Application starting up", app_name=settings.APP_NAME)
    
    # Configuration Validation & DB check
    logger.info("Configuration validated. Testing DB connection...")
    try:
        from app.db.session import engine
        from sqlalchemy import text
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection successful.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise e # Fail fast
    
    # Initialize observability
    setup_prometheus_metrics(app)
    setup_opentelemetry(app)
    
    yield
    
    # Shutdown
    logger.info("Application shutting down")
    
app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    version="0.1.0"
)

# Exception handlers
app.add_exception_handler(Exception, global_exception_handler)

# Middleware
app.add_middleware(StructlogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Routers
app.include_router(api_router, prefix="/api/v1")

# Root
@app.get("/")
async def root():
    return {"message": "Welcome to Enterprise AI Gateway"}

# Prometheus metrics
from prometheus_client import make_asgi_app
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
