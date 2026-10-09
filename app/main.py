import os
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import tasks, dashboard
from app.schemas import HealthCheckResponse, ErrorResponse

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartTask API",
    description=(
        "SmartTask is a modern, feature-rich Task Management & Productivity REST API "
        "built with Python 3.11+, FastAPI, SQLAlchemy, and Pydantic. It provides full task CRUD, "
        "advanced filtering, search, pagination, smart task categorization, and real-time dashboard analytics."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)

# Mount static files and frontend root handler
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
def serve_frontend():
    """Serve interactive web dashboard interface."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to SmartTask API. Documentation at /docs"}


# Register API Routers
app.include_router(tasks.router)
app.include_router(dashboard.router)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """Custom exception handler to return consistent error response payloads."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom validation exception handler for clear error messages."""
    error_msg = "Validation error"
    if exc.errors():
        first_err = exc.errors()[0]
        field_parts = [str(loc) for loc in first_err.get("loc", []) if loc != "body"]
        field = " -> ".join(field_parts)
        msg = first_err.get("msg", "Invalid input")
        error_msg = f"Validation error in '{field}': {msg}" if field else f"Validation error: {msg}"

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": error_msg, "status_code": 422},
    )


@app.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    tags=["Health"],
    summary="API Health Check",
    description="Returns service status to ensure API health and uptime.",
)
def health_check():
    """Health check endpoint for service monitoring."""
    return {"status": "healthy", "service": "SmartTask API"}
