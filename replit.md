# Video Downloader API

## Overview

This is a FastAPI-based video downloader service that implements a two-phase approach for downloading videos from multiple platforms (YouTube, Instagram, Facebook, Twitter). The system first extracts video metadata and available formats, then allows users to download specific quality/format combinations using yt-dlp as the core extraction engine.

## User Preferences

Preferred communication style: Simple, everyday language.

### Recent Request (July 26, 2025)
- Enhanced Twitter/X support to handle posts without videos
- Show appropriate responses for posts with images or no media
- Display media type badges and handle different content types
- Added comprehensive YouTube content type support analysis
- Implemented better error handling for unsupported YouTube content types
- Added web scraping fallback for Twitter image extraction
- Created detailed platform support matrix documenting all supported content types

## System Architecture

### Backend Framework
- **FastAPI**: Chosen for its async capabilities, automatic API documentation, and built-in request/response validation
- **Python 3.10+**: Modern Python features with type hints and async/await support
- **Async Architecture**: All operations are asynchronous to handle multiple concurrent requests efficiently

### Two-Phase Design Philosophy
The application implements a two-phase workflow:
1. **Metadata Extraction Phase**: Extract video information, available formats, and quality options without downloading
2. **Selective Download Phase**: Download specific format based on user selection

This approach provides better user experience by allowing format selection and prevents unnecessary downloads.

## Key Components

### API Layer (`app/routers/`)
- **Platform-Specific Routers**: Separate routers for YouTube, Instagram, Facebook, and Twitter
- **Unified Interface**: All platforms expose the same two endpoints (`/extract/{platform}` and `/download/{platform}`)
- **Error Handling**: Comprehensive exception handling with proper HTTP status codes

### Service Layer (`app/services/downloader.py`)
- **VideoDownloaderService**: Core service that wraps yt-dlp functionality
- **Async Operations**: All yt-dlp operations are wrapped in async functions using thread executors
- **Configuration Management**: Centralized yt-dlp options and download settings

### Data Models (`app/models.py`)
- **Pydantic Models**: Strong typing for request/response validation
- **VideoMetadata**: Comprehensive metadata structure including formats, thumbnails, duration
- **VideoFormat**: Detailed format information with codec, resolution, and file size data

### Configuration (`config.py`)
- **Environment-Based Settings**: Configurable download directory, timeouts, file size limits
- **Resource Limits**: Concurrent download limits and maximum file sizes
- **Directory Management**: Automatic creation of download directories

### Frontend Interface (`static/index.html`)
- **Interactive Demo**: Complete HTML interface demonstrating the two-phase workflow
- **Bootstrap UI**: Modern responsive interface with format selection capabilities
- **AJAX Integration**: Real-time communication with the API endpoints

## Data Flow

### Metadata Extraction Flow
1. Client sends POST request to `/api/extract/{platform}` with video URL
2. VideoDownloaderService calls yt-dlp to extract metadata without downloading
3. Raw yt-dlp data is transformed into structured VideoMetadata response
4. Available formats are parsed and presented with quality/codec information

### Download Flow
1. Client sends POST request to `/api/download/{platform}` with URL and selected format_id
2. VideoDownloaderService configures yt-dlp for specific format download
3. File is downloaded to configured directory with structured naming
4. Download response includes file path and metadata

## External Dependencies

### Core Dependencies
- **yt-dlp**: Primary video extraction and download engine
- **FastAPI**: Web framework for API endpoints
- **Uvicorn**: ASGI server for FastAPI application
- **Pydantic**: Data validation and serialization
- **aiofiles**: Async file operations

### Platform Integration
- **yt-dlp Extractors**: Handles platform-specific extraction logic for YouTube, Instagram, Facebook, Twitter
- **No Direct API Keys**: Uses web scraping approach through yt-dlp, avoiding platform API limitations

## Deployment Strategy

### Development Setup
- **Local Development**: Run with `uvicorn main:app --reload`
- **Environment Variables**: Configurable through environment variables or defaults
- **Static File Serving**: FastAPI serves static HTML interface

### Production Considerations
- **Async Concurrency**: Handles multiple concurrent requests efficiently
- **Resource Management**: Configurable limits on concurrent downloads and file sizes
- **Logging**: Structured logging for monitoring and debugging
- **File Management**: Organized download directory structure

### Scalability Features
- **Async Architecture**: Non-blocking operations for better throughput
- **Configurable Limits**: Prevents resource exhaustion through download limits
- **Modular Design**: Easy to add new platforms by creating new router modules
- **Stateless Design**: No database dependency, making horizontal scaling simpler

The architecture prioritizes simplicity, reliability, and user experience while maintaining the flexibility to support multiple video platforms through a unified interface.