"""
FastAPI Video Downloader - Two-Phase API
Supports metadata extraction and selective downloads using yt-dlp
"""

import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

from app.routers import youtube, instagram, facebook, twitter
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    os.makedirs(settings.DOWNLOAD_DIR, exist_ok=True)
    logger.info(f"Download directory created/verified: {settings.DOWNLOAD_DIR}")
    logger.info("FastAPI Video Downloader API started")
    
    yield
    
    # Shutdown
    logger.info("FastAPI Video Downloader API shutting down")

# Initialize FastAPI app
app = FastAPI(
    title="Video Downloader API",
    description="Two-phase video downloader: extract metadata first, then download selected formats",
    version="1.0.0",
    lifespan=lifespan
)

# Include platform routers
app.include_router(youtube.router, prefix="/api", tags=["YouTube"])
app.include_router(instagram.router, prefix="/api", tags=["Instagram"])
app.include_router(facebook.router, prefix="/api", tags=["Facebook"])
app.include_router(twitter.router, prefix="/api", tags=["Twitter"])

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML interface"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Frontend interface not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Video Downloader API is running",
        "download_dir": settings.DOWNLOAD_DIR,
        "supported_platforms": ["youtube", "instagram", "facebook", "twitter"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
