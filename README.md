# Video Downloader API - Two-Phase System

A FastAPI-based video downloader that provides a two-phase approach: first extract metadata, then download selected formats using yt-dlp.

## Features

- **Two-Phase Download Process**: Extract metadata first, then download specific quality/format
- **Multi-Platform Support**: YouTube, Instagram, Facebook, Twitter via yt-dlp
- **Comprehensive Metadata**: Title, thumbnail, duration, file sizes, available qualities/formats
- **Selective Downloads**: Choose specific quality (720p, 1080p, audio-only, etc.)
- **Async FastAPI**: Better performance with async/await
- **Interactive Frontend**: Complete HTML interface demonstrating the workflow
- **Enhanced Twitter Support**: Image extraction with web scraping fallback
- **No Authentication Required**: Works with all public content without login

## Supported Content

📋 **[View Complete Platform Support Matrix →](PLATFORM_SUPPORT_MATRIX.md)**

### Quick Reference
| Platform | Videos | Images | Playlists | Live Streams |
|----------|--------|--------|-----------|--------------|
| **YouTube** | ✅ Up to 8K | ❌ | ✅ Public | ⚠️ Experimental |
| **Instagram** | ✅ Up to 1080p | ✅ Posts | ❌ | ❌ |
| **Facebook** | ✅ Up to 1080p | ⚠️ Limited | ❌ | ❌ |
| **Twitter/X** | ✅ Up to 1080p | ✅ Enhanced | ❌ | ❌ |

*All content must be publicly accessible (no login required)*

## Installation

1. **Install Dependencies**:
```bash
pip install fastapi uvicorn[standard] yt-dlp[default] python-multipart aiofiles
