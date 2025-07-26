# Video Downloader API - Two-Phase System

A FastAPI-based video downloader that provides a two-phase approach: first extract metadata, then download selected formats using yt-dlp.

## Features

- **Two-Phase Download Process**: Extract metadata first, then download specific quality/format
- **Multi-Platform Support**: YouTube, Instagram, Facebook, Twitter via yt-dlp
- **Comprehensive Metadata**: Title, thumbnail, duration, file sizes, available qualities/formats
- **Selective Downloads**: Choose specific quality (720p, 1080p, audio-only, etc.)
- **Async FastAPI**: Better performance with async/await
- **Interactive Frontend**: Complete HTML interface demonstrating the workflow

## Installation

1. **Install Dependencies**:
```bash
pip install fastapi uvicorn[standard] yt-dlp[default] python-multipart aiofiles
