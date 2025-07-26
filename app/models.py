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

class ImageDownloadRequest(BaseModel):
    """Request model for image download"""
    url: HttpUrl = Field(..., description="Post URL to download images from")
    download_all: bool = Field(default=True, description="Download all available images")

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
    media_type: Optional[str] = Field(None, description="Type of media: 'video', 'image', 'none'")
    images: Optional[List[str]] = Field(None, description="List of image URLs if post contains images")
    has_media: bool = Field(True, description="Whether the post contains any media")

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

class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = Field(default="error", description="Error status")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
