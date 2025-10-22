from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes import analysis
from app.config import settings
from app.logger import setup_logging, get_logger
from app.exceptions import ValidationError, BalanceSheetError, CalculationError
import time

# Set up logging first thing
setup_logging(log_level=settings.log_level, log_file=settings.log_file)
logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="API para análise financeira empresarial com rácios portugueses",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every request that comes in, with timing information."""
    start_time = time.time()
    
    logger.info(f"Request started: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    logger.info(
        f"Request completed: {request.method} {request.url.path} "
        f"- Status: {response.status_code} - Duration: {duration:.3f}s"
    )
    
    return response


# Global exception handlers
@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    """Handle validation errors with proper error response."""
    logger.warning(f"Validation error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": "validation_error"}
    )


@app.exception_handler(BalanceSheetError)
async def balance_sheet_error_handler(request: Request, exc: BalanceSheetError):
    """Handle balance sheet errors."""
    logger.warning(f"Balance sheet error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": "balance_sheet_error"}
    )


@app.exception_handler(CalculationError)
async def calculation_error_handler(request: Request, exc: CalculationError):
    """Handle calculation errors."""
    logger.error(f"Calculation error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": "calculation_error"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch any other unexpected errors."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor. Por favor, tente novamente mais tarde.",
            "type": "internal_error"
        }
    )


@app.on_event("startup")
async def startup_event():
    """Run when the API starts up."""
    import os
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"PORT: {os.getenv('PORT', 'not set')}")
    logger.info(f"Allowed origins: {settings.cors_origins}")
    logger.info("API startup complete - ready to accept requests")


@app.on_event("shutdown")
async def shutdown_event():
    """Run when the API shuts down."""
    logger.info(f"Shutting down {settings.app_name}")

# Include routers
app.include_router(analysis.router, prefix="/api", tags=["analysis"])

@app.get("/")
async def root():
    """Root endpoint - basic API information."""
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "status": "online",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/health")
async def simple_health():
    """Simple health check without API prefix."""
    return {"status": "ok"}


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.
    Used by monitoring tools to make sure the API is alive.
    """
    import os
    return {
        "status": "healthy",
        "service": "janua-financial-api",
        "version": settings.app_version,
        "port": os.getenv("PORT", "not_set"),
        "timestamp": time.time()
    }
