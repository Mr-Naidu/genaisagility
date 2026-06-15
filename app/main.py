from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import get_settings
from app.api.endpoints import router as api_router
from app.core.logging import logger

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Microservice to classify and rewrite emails using Generative AI.",
    version="1.0.0",
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error processing request {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal server error occurred. Please try again later."}
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def serve_frontend():
    """Serves the frontend UI."""
    return FileResponse("app/static/index.html")

@app.get("/health")
async def health_check():
    """Simple health check endpoint to verify the API is running."""
    logger.info("Health check endpoint called.")
    return {"status": "healthy"}
