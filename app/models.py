"""
Pydantic models for request/response validation
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl, Field

class ExtractRequest(BaseModel):
    """Request model for metadata extraction"""
    url: HttpUrl = Field(..., description="Video URL to extract metadata from")

class DownloadRequest(BaseModel):
    """Request model for video download"""
    url: HttpUrl = Field(..., description="Video URL to download")
    format_id: str = Field(..., description="Format ID from metadata extraction")
    audio_only: bool = Field(default=False, description="Extract audio only")
    audio_format: Optional[str] = Field(default="mp3", description="Audio format (mp3, aac, m4a, etc.)")
    audio_quality: Optional[str] = Field(default="192", description="Audio bitrate (128, 192, 256, 320)")

class ImageDownloadRequest(BaseModel):
    """Request model for image download"""
    url: HttpUrl = Field(..., description="Post URL to download images from")
    download_all: bool = Field(default=True, description="Download all available images")

class PlaylistRequest(BaseModel):
    """Request model for playlist processing"""
    url: HttpUrl = Field(..., description="Playlist URL to process")
    download_all: bool = Field(default=False, description="Download all videos in playlist")
    max_downloads: Optional[int] = Field(default=None, description="Maximum number of videos to download")
    start_index: Optional[int] = Field(default=1, description="Start downloading from this index")
    end_index: Optional[int] = Field(default=None, description="Stop downloading at this index")

class BatchDownloadRequest(BaseModel):
    """Request model for batch downloads"""
    urls: List[HttpUrl] = Field(..., description="List of URLs to download")
    format_preference: Optional[str] = Field(default="best", description="Format preference for all videos")
    audio_only: bool = Field(default=False, description="Extract audio only for all videos")
    max_concurrent: Optional[int] = Field(default=3, description="Maximum concurrent downloads")

class VideoFormat(BaseModel):
    """Video format information"""
    format_id: str = Field(..., description="Unique format identifier")
    format_note: Optional[str] = Field(None, description="Human-readable format description")
    ext: str = Field(..., description="File extension")
    resolution: Optional[str] = Field(None, description="Video resolution (e.g., '1920x1080')")
    height: Optional[int] = Field(None, description="Video height in pixels")
    width: Optional[int] = Field(None, description="Video width in pixels")
    fps: Optional[float] = Field(None, description="Frames per second")
    vcodec: Optional[str] = Field(None, description="Video codec")
    acodec: Optional[str] = Field(None, description="Audio codec")
    filesize: Optional[int] = Field(None, description="Approximate file size in bytes")
    filesize_approx: Optional[int] = Field(None, description="Approximate file size in bytes")
    tbr: Optional[float] = Field(None, description="Total bitrate")
    vbr: Optional[float] = Field(None, description="Video bitrate")
    abr: Optional[float] = Field(None, description="Audio bitrate")
    quality: Optional[float] = Field(None, description="Quality rating")
    
    # Enhanced format classification
    format_type: Optional[str] = Field(None, description="Format type: 'audio-only', 'video-only', 'combined'")
    format_category: Optional[str] = Field(None, description="Quality category: 'best', 'high', 'medium', 'low'")
    visual_indicator: Optional[str] = Field(None, description="Visual indicator for frontend")
    codec_info: Optional[str] = Field(None, description="Human-readable codec description")

class VideoMetadata(BaseModel):
    """Complete video metadata"""
    id: str = Field(..., description="Video ID")
    title: str = Field(..., description="Video title")
    description: Optional[str] = Field(None, description="Video description")
    uploader: Optional[str] = Field(None, description="Video uploader/channel")
    upload_date: Optional[str] = Field(None, description="Upload date (YYYYMMDD)")
    duration: Optional[float] = Field(None, description="Duration in seconds")
    view_count: Optional[int] = Field(None, description="View count")
    like_count: Optional[int] = Field(None, description="Like count")
    thumbnail: Optional[str] = Field(None, description="Thumbnail URL")
    webpage_url: str = Field(..., description="Original webpage URL")
    formats: List[VideoFormat] = Field(default_factory=list, description="Available video formats")
    media_type: Optional[str] = Field(None, description="Type of media: 'video', 'image', 'none', 'playlist', 'live'")
    images: Optional[List[str]] = Field(None, description="List of image URLs if post contains images")
    has_media: bool = Field(True, description="Whether the post contains any media")
    is_live: bool = Field(False, description="Whether this is a live stream")
    playlist_count: Optional[int] = Field(None, description="Number of videos in playlist")
    entries: Optional[List['VideoMetadata']] = Field(None, description="Playlist entries")

class ExtractResponse(BaseModel):
    """Response model for metadata extraction"""
    status: str = Field(..., description="Response status")
    metadata: Optional[VideoMetadata] = Field(None, description="Video metadata")
    message: Optional[str] = Field(None, description="Status message")

class DownloadResponse(BaseModel):
    """Response model for video download"""
    status: str = Field(..., description="Response status")
    file_path: Optional[str] = Field(None, description="Downloaded file path")
    filename: Optional[str] = Field(None, description="Downloaded filename")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    message: Optional[str] = Field(None, description="Status message")
    download_type: Optional[str] = Field(None, description="Type of download: 'video', 'audio', 'playlist', 'batch'")
    files_downloaded: Optional[List[str]] = Field(None, description="List of downloaded files for batch/playlist")
    total_files: Optional[int] = Field(None, description="Total number of files processed")
    success_count: Optional[int] = Field(None, description="Number of successful downloads")
    error_count: Optional[int] = Field(None, description="Number of failed downloads")

class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = Field(default="error", description="Error status")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
