"""
Core downloader service using yt-dlp
"""

import os
import asyncio
import logging
import re
from typing import Dict, Any, Optional
from pathlib import Path
import yt_dlp
import requests

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
                formats=formats,
                media_type="video" if formats else "none",
                has_media=bool(formats)
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
    
    async def extract_twitter_metadata(self, url: str) -> ExtractResponse:
        """
        Extract Twitter/X post metadata, handling posts with videos, images, or no media
        """
        try:
            ydl_opts = self._get_base_ydl_opts()
            ydl_opts['extract_flat'] = False
            ydl_opts['writeinfojson'] = True
            ydl_opts['skip_download'] = True
            ydl_opts['write_all_thumbnails'] = True  # Extract all available images/thumbnails
            ydl_opts['writethumbnail'] = True
            
            def extract_info():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    try:
                        # Try to extract video info first
                        return ydl.extract_info(url, download=False)
                    except yt_dlp.DownloadError as e:
                        if "No video could be found" in str(e):
                            # For image-only posts, try a different approach
                            try:
                                # Use a more permissive configuration
                                ydl_opts_image = self._get_base_ydl_opts()
                                ydl_opts_image.update({
                                    'skip_download': True,
                                    'extract_flat': False,
                                    'ignoreerrors': True,
                                    'no_warnings': True,
                                    'writeinfojson': False,
                                    'write_all_thumbnails': False,
                                    'writethumbnail': False,
                                    'format': 'worst',  # Try to get any available format
                                })
                                
                                with yt_dlp.YoutubeDL(ydl_opts_image) as ydl_img:
                                    try:
                                        info = ydl_img.extract_info(url, download=False)
                                        if info:
                                            return info
                                    except:
                                        pass
                                
                                # If still no luck, create basic structure with tweet ID
                                from urllib.parse import urlparse
                                path_parts = urlparse(url).path.split('/')
                                tweet_id = None
                                for i, part in enumerate(path_parts):
                                    if part == 'status' and i + 1 < len(path_parts):
                                        tweet_id = path_parts[i + 1].split('?')[0]
                                        break
                                
                                if tweet_id:
                                    # Create minimal info structure for image posts
                                    return {
                                        'id': tweet_id,
                                        'title': f'Twitter Post {tweet_id}',
                                        'webpage_url': url,
                                        'extractor': 'twitter',
                                        'formats': [],
                                        'thumbnails': [],
                                        '_type': 'url',
                                        'description': 'Twitter post - may contain images'
                                    }
                            except Exception as inner_e:
                                logger.warning(f"Failed image extraction fallback: {inner_e}")
                                pass
                        raise e
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, extract_info)
            
            if not info:
                return ExtractResponse(
                    status="error",
                    message="Could not extract post information"
                )
            
            # Process formats (if any)
            formats = []
            media_type = "none"
            images = []
            
            # Check for video formats
            for fmt in info.get('formats', []):
                if fmt.get('format_id') and fmt.get('ext'):
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
                    media_type = "video"
            
            # Check for images from multiple sources
            thumbnails = info.get('thumbnails', [])
            images = []
            
            if thumbnails:
                images.extend([thumb.get('url') for thumb in thumbnails if thumb.get('url')])
            
            # For Twitter, also check additional image fields
            if 'twitter' in info.get('extractor', '').lower():
                # Check for entries (Twitter sometimes provides multiple media entries)
                entries = info.get('entries', [])
                for entry in entries:
                    entry_thumbs = entry.get('thumbnails', [])
                    images.extend([thumb.get('url') for thumb in entry_thumbs if thumb.get('url')])
                
                # Check for any image URLs in the info structure
                if 'url' in info and any(ext in info['url'].lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                    images.append(info['url'])
            
            # Remove duplicates and filter valid URLs
            images = list(dict.fromkeys([img for img in images if img and isinstance(img, str)]))
            
            # If no images found through yt-dlp and this is a Twitter post, try web scraping fallback
            if not images and 'twitter' in info.get('extractor', '').lower():
                try:
                    images = await self._extract_twitter_images_fallback(url)
                except Exception as fallback_error:
                    logger.warning(f"Twitter image fallback failed: {fallback_error}")
            
            if images and media_type == "none":
                media_type = "image"
            
            # Determine appropriate message
            if media_type == "video":
                message = "Video metadata extracted successfully"
            elif media_type == "image":
                message = "Post contains images (no video content)"
            else:
                message = "Post contains no media content"
            
            # Create metadata object
            metadata = VideoMetadata(
                id=info.get('id', ''),
                title=info.get('title', 'Twitter Post'),
                description=info.get('description', 'Twitter/X post'),
                uploader=info.get('uploader'),
                upload_date=info.get('upload_date'),
                duration=info.get('duration'),
                view_count=info.get('view_count'),
                like_count=info.get('like_count'),
                thumbnail=info.get('thumbnail'),
                webpage_url=info.get('webpage_url', url),
                formats=formats,
                media_type=media_type,
                images=images if images else None,
                has_media=bool(formats or images)
            )
            
            return ExtractResponse(
                status="ok",
                metadata=metadata,
                message=message
            )
            
        except yt_dlp.DownloadError as e:
            logger.error(f"yt-dlp download error for {url}: {str(e)}")
            return ExtractResponse(
                status="error",
                message=f"Could not extract post information: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error extracting Twitter metadata for {url}: {str(e)}")
            return ExtractResponse(
                status="error",
                message=f"Unexpected error: {str(e)}"
            )
    
    async def download_twitter_images(self, url: str) -> DownloadResponse:
        """
        Download images from Twitter/X post
        """
        try:
            ydl_opts = self._get_base_ydl_opts()
            ydl_opts['skip_download'] = True  # Skip video download
            ydl_opts['write_all_thumbnails'] = True  # Download all images
            ydl_opts['writethumbnail'] = True
            ydl_opts['outtmpl'] = str(self.download_dir / 'images/%(title)s [%(id)s]/%(title)s.%(ext)s')
            
            downloaded_files = []
            
            def download_hook(d):
                if d['status'] == 'finished':
                    downloaded_files.append(d['filename'])
                    logger.info(f"Downloaded image: {d['filename']}")
            
            ydl_opts['progress_hooks'] = [download_hook]
            
            def download():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    try:
                        ydl.download([url])
                    except yt_dlp.DownloadError as e:
                        if "No video could be found" in str(e):
                            # This is expected for image-only posts, yt-dlp still extracts thumbnails
                            pass
                        else:
                            raise e
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, download)
            
            # Check if any image files were downloaded
            image_dir = self.download_dir / 'images'
            if image_dir.exists():
                image_files = list(image_dir.rglob('*'))
                image_files = [f for f in image_files if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']]
                
                if image_files:
                    total_size = sum(f.stat().st_size for f in image_files)
                    return DownloadResponse(
                        status="ok",
                        file_path=str(image_dir),
                        filename=f"{len(image_files)} images downloaded",
                        file_size=total_size,
                        message=f"Downloaded {len(image_files)} images successfully"
                    )
            
            return DownloadResponse(
                status="error",
                file_path=None,
                filename=None,
                file_size=None,
                message="No images were found or downloaded from this post"
            )
            
        except Exception as e:
            logger.error(f"Unexpected error downloading Twitter images for {url}: {str(e)}")
            return DownloadResponse(
                status="error",
                file_path=None,
                filename=None, 
                file_size=None,
                message=f"Unexpected error: {str(e)}"
            )
    
    async def _extract_twitter_images_fallback(self, url: str) -> list:
        """
        Fallback method to extract Twitter images using web scraping when yt-dlp fails
        """
        try:
            # Make a request to get the Twitter page HTML
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.get(url, headers=headers, timeout=10)
            )
            
            if response.status_code != 200:
                return []
            
            html_content = response.text
            
            # Look for image URLs in the HTML using regex patterns
            image_patterns = [
                r'https://pbs\.twimg\.com/media/[^"]+\.(jpg|jpeg|png|webp)',
                r'https://ton\.twitter\.com/[^"]+\.(jpg|jpeg|png|webp)', 
                r'https://video\.twimg\.com/[^"]+\.(jpg|jpeg|png|webp)',
            ]
            
            images = []
            for pattern in image_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        # Extract the full URL (match[0] would be the URL without extension)
                        full_match = re.search(pattern, html_content, re.IGNORECASE)
                        if full_match:
                            images.append(full_match.group(0))
                    else:
                        images.append(match)
            
            # Remove duplicates and return high-quality versions
            unique_images = list(dict.fromkeys(images))
            
            # Prefer larger image sizes
            quality_images = []
            for img in unique_images:
                # Convert to larger size if possible
                if ':small' in img:
                    img = img.replace(':small', ':large')
                elif ':medium' in img:
                    img = img.replace(':medium', ':large')
                elif '?format=' in img and '&name=' in img:
                    # For newer Twitter image URLs, try to get the original size
                    img = re.sub(r'&name=\w+', '&name=orig', img)
                
                quality_images.append(img)
            
            logger.info(f"Extracted {len(quality_images)} images via fallback method for {url}")
            return quality_images
            
        except Exception as e:
            logger.error(f"Twitter image fallback extraction failed: {e}")
            return []
    
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
