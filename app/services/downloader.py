"""
Core downloader service using yt-dlp
"""

import os
import asyncio
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import yt_dlp

from config import settings
from app.models import VideoMetadata, VideoFormat, ExtractResponse, DownloadResponse

logger = logging.getLogger(__name__)

class VideoDownloaderService:
    """Service for video metadata extraction and downloading"""
    
    def __init__(self):
        self.download_dir = Path(settings.DOWNLOAD_DIR)
        self.download_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_base_ydl_opts(self) -> Dict[str, Any]:
        """Get base yt-dlp options"""
        return {
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
            'format': 'best',
            'outtmpl': str(self.download_dir / '%(title)s [%(id)s].%(ext)s'),
            'writeinfojson': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'ignoreerrors': False,
            'socket_timeout': settings.DOWNLOAD_TIMEOUT,
        }
    
    async def extract_metadata(self, url: str) -> ExtractResponse:
        """
        Extract video metadata without downloading
        """
        try:
            ydl_opts = self._get_base_ydl_opts()
            
            def extract_info():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extract info without downloading
                    return ydl.extract_info(url, download=False)
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, extract_info)
            
            if not info:
                return ExtractResponse(
                    status="error",
                    message="Could not extract video information"
                )
            
            # Process formats
            formats = []
            for fmt in info.get('formats', []):
                video_format = VideoFormat(
                    format_id=fmt.get('format_id', ''),
                    format_note=fmt.get('format_note'),
                    ext=fmt.get('ext', 'unknown'),
                    resolution=fmt.get('resolution'),
                    height=fmt.get('height'),
                    width=fmt.get('width'),
                    fps=fmt.get('fps'),
                    vcodec=fmt.get('vcodec'),
                    acodec=fmt.get('acodec'),
                    filesize=fmt.get('filesize'),
                    filesize_approx=fmt.get('filesize_approx'),
                    tbr=fmt.get('tbr'),
                    vbr=fmt.get('vbr'),
                    abr=fmt.get('abr'),
                    quality=fmt.get('quality')
                )
                formats.append(video_format)
            
            # Create metadata object
            metadata = VideoMetadata(
                id=info.get('id', ''),
                title=info.get('title', 'Unknown Title'),
                description=info.get('description'),
                uploader=info.get('uploader'),
                upload_date=info.get('upload_date'),
                duration=info.get('duration'),
                view_count=info.get('view_count'),
                like_count=info.get('like_count'),
                thumbnail=info.get('thumbnail'),
                webpage_url=info.get('webpage_url', url),
                formats=formats
            )
            
            return ExtractResponse(
                status="ok",
                metadata=metadata,
                message="Metadata extracted successfully"
            )
            
        except yt_dlp.DownloadError as e:
            logger.error(f"yt-dlp download error for {url}: {str(e)}")
            return ExtractResponse(
                status="error",
                message=f"Download error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error extracting metadata for {url}: {str(e)}")
            return ExtractResponse(
                status="error",
                message=f"Unexpected error: {str(e)}"
            )
    
    async def download_video(self, url: str, format_id: str) -> DownloadResponse:
        """
        Download video with specific format
        """
        try:
            ydl_opts = self._get_base_ydl_opts()
            ydl_opts['format'] = format_id
            
            downloaded_files = []
            
            def download_hook(d):
                if d['status'] == 'finished':
                    downloaded_files.append(d['filename'])
                    logger.info(f"Downloaded: {d['filename']}")
            
            ydl_opts['progress_hooks'] = [download_hook]
            
            def download():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, download)
            
            if not downloaded_files:
                return DownloadResponse(
                    status="error",
                    message="No files were downloaded"
                )
            
            # Get info about the downloaded file
            file_path = downloaded_files[0]
            file_stat = os.stat(file_path)
            filename = os.path.basename(file_path)
            
            return DownloadResponse(
                status="ok",
                file_path=file_path,
                filename=filename,
                file_size=file_stat.st_size,
                message="Video downloaded successfully"
            )
            
        except yt_dlp.DownloadError as e:
            logger.error(f"yt-dlp download error for {url} (format: {format_id}): {str(e)}")
            return DownloadResponse(
                status="error",
                message=f"Download error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error downloading {url}: {str(e)}")
            return DownloadResponse(
                status="error",
                message=f"Unexpected error: {str(e)}"
            )

# Global service instance
downloader_service = VideoDownloaderService()
