"""Main application entry point for iframe-server."""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.config import settings
from app.database import init_database, close_database
from app.api import projects, files, static
from app.models import HealthResponse


# Track application start time for uptime
start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    await init_database(settings.db_path)
    yield
    # Shutdown
    await close_database()


# Create FastAPI application
app = FastAPI(
    title="iframe-server",
    description="Lightweight iframe hosting service for markdown embeds",
    version="0.1.0",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint (before routers to ensure it's accessible)
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        uptime=time.time() - start_time
    )


# Register API routers
app.include_router(projects.router)
app.include_router(files.router)
app.include_router(static.router)


# Mount static files for web UI (must be last to not override API routes)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


def main():
    """Run the application."""
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=False
    )


if __name__ == "__main__":
    main()
