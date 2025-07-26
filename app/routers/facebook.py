"""
Facebook video downloader router
"""

import logging
from fastapi import APIRouter, HTTPException
from app.models import ExtractRequest, DownloadRequest, ExtractResponse, DownloadResponse
from app.services.downloader import downloader_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/extract/facebook", response_model=ExtractResponse)
async def extract_facebook_metadata(request: ExtractRequest):
    """
    Extract Facebook video metadata without downloading
    """
    logger.info(f"Extracting Facebook metadata for: {request.url}")
    
    try:
        response = await downloader_service.extract_metadata(str(request.url))
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error extracting Facebook metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/download/facebook", response_model=DownloadResponse)
async def download_facebook_video(request: DownloadRequest):
    """
    Download Facebook video with specific format, supports audio-only extraction
    """
    logger.info(f"Downloading Facebook video: {request.url} (format: {request.format_id}, audio_only: {request.audio_only})")
    
    try:
        response = await downloader_service.download_video(
            str(request.url), 
            request.format_id,
            audio_only=request.audio_only,
            audio_format=request.audio_format or "mp3",
            audio_quality=request.audio_quality or "192"
        )
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error downloading Facebook video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
