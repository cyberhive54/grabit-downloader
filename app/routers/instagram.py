"""
Instagram video downloader router
"""

import logging
from fastapi import APIRouter, HTTPException
from app.models import ExtractRequest, DownloadRequest, ExtractResponse, DownloadResponse
from app.services.downloader import downloader_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/extract/instagram", response_model=ExtractResponse)
async def extract_instagram_metadata(request: ExtractRequest):
    """
    Extract Instagram video metadata without downloading
    """
    logger.info(f"Extracting Instagram metadata for: {request.url}")
    
    try:
        response = await downloader_service.extract_metadata(str(request.url))
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error extracting Instagram metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/download/instagram", response_model=DownloadResponse)
async def download_instagram_video(request: DownloadRequest):
    """
    Download Instagram video with specific format
    """
    logger.info(f"Downloading Instagram video: {request.url} (format: {request.format_id})")
    
    try:
        response = await downloader_service.download_video(str(request.url), request.format_id)
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error downloading Instagram video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
