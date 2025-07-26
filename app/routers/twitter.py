"""
Twitter video downloader router
"""

import logging
from fastapi import APIRouter, HTTPException
from app.models import ExtractRequest, DownloadRequest, ImageDownloadRequest, ExtractResponse, DownloadResponse
from app.services.downloader import downloader_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/extract/twitter", response_model=ExtractResponse)
async def extract_twitter_metadata(request: ExtractRequest):
    """
    Extract Twitter/X post metadata, handles posts with videos, images, or no media
    """
    logger.info(f"Extracting Twitter metadata for: {request.url}")
    
    try:
        response = await downloader_service.extract_twitter_metadata(str(request.url))
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error extracting Twitter metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/download/twitter", response_model=DownloadResponse)
async def download_twitter_video(request: DownloadRequest):
    """
    Download Twitter video with specific format
    """
    logger.info(f"Downloading Twitter video: {request.url} (format: {request.format_id})")
    
    try:
        response = await downloader_service.download_video(str(request.url), request.format_id)
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error downloading Twitter video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/download/twitter/images", response_model=DownloadResponse)
async def download_twitter_images(request: ImageDownloadRequest):
    """
    Download images from Twitter/X post
    """
    logger.info(f"Downloading Twitter images: {request.url}")
    
    try:
        response = await downloader_service.download_twitter_images(str(request.url))
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error downloading Twitter images: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
