"""
YouTube video downloader router
"""

import logging
from fastapi import APIRouter, HTTPException
from app.models import ExtractRequest, DownloadRequest, PlaylistRequest, BatchDownloadRequest, ExtractResponse, DownloadResponse
from app.services.downloader import downloader_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/extract/youtube", response_model=ExtractResponse)
async def extract_youtube_metadata(request: ExtractRequest):
    """
    Extract YouTube video metadata without downloading
    """
    logger.info(f"Extracting YouTube metadata for: {request.url}")
    
    try:
        response = await downloader_service.extract_metadata(str(request.url))
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error extracting YouTube metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/download/youtube", response_model=DownloadResponse)
async def download_youtube_video(request: DownloadRequest):
    """
    Download YouTube video with specific format, supports audio-only extraction
    """
    logger.info(f"Downloading YouTube video: {request.url} (format: {request.format_id}, audio_only: {request.audio_only})")
    
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
        logger.error(f"Error downloading YouTube video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/extract/youtube/playlist", response_model=ExtractResponse)
async def extract_youtube_playlist(request: ExtractRequest):
    """
    Extract YouTube playlist metadata without downloading videos
    """
    logger.info(f"Extracting YouTube playlist metadata for: {request.url}")
    
    try:
        response = await downloader_service.extract_playlist_metadata(str(request.url))
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error extracting YouTube playlist metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/download/youtube/playlist", response_model=DownloadResponse)
async def download_youtube_playlist(request: PlaylistRequest):
    """
    Download YouTube playlist videos
    """
    logger.info(f"Downloading YouTube playlist: {request.url}")
    
    try:
        response = await downloader_service.download_playlist(
            str(request.url),
            max_downloads=request.max_downloads,
            start_index=request.start_index or 1,
            end_index=request.end_index,
            audio_only=False  # Can be extended later to support audio-only playlists
        )
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error downloading YouTube playlist: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/download/batch", response_model=DownloadResponse)
async def batch_download_videos(request: BatchDownloadRequest):
    """
    Download multiple videos from various platforms in batch
    """
    logger.info(f"Batch downloading {len(request.urls)} videos")
    
    try:
        response = await downloader_service.batch_download(
            [str(url) for url in request.urls],
            format_preference=request.format_preference or "best",
            audio_only=request.audio_only,
            max_concurrent=request.max_concurrent or 3
        )
        
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error in batch download: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
