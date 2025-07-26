# Video Downloader API - "Grabit" Enhanced Classification System

A comprehensive FastAPI-based video downloader with intelligent format classification and visual indicators. Features enhanced yt-dlp integration with smart codec detection and quality classification.

## ✨ Enhanced Features

- **🎯 Smart Format Classification**: Visual indicators (🎬 🎵 📹) distinguish audio-only, video-only, and combined formats
- **📊 Quality Detection**: Automatic quality categorization (Best/High/Medium/Low) based on resolution and bitrate
- **🎵 Multi-Format Audio**: Extract high-quality audio (MP3, AAC, M4A) with configurable bitrates (128-320kbps)
- **🔄 Two-Phase Download Process**: Extract comprehensive metadata first, then download selected formats
- **🌐 Multi-Platform Support**: YouTube, Instagram, Facebook, Twitter with platform-specific optimizations
- **📋 Playlist Support**: Full YouTube playlist processing with batch downloads and metadata extraction
- **📡 Live Stream Detection**: Real-time identification of ongoing broadcasts
- **⚡ Batch Processing**: Concurrent downloads with configurable rate limiting
- **🎨 Enhanced Frontend**: Interactive Bootstrap UI with real-time format classification display
- **🔧 Codec Intelligence**: Advanced codec detection (AV1, VP9, H.264, H.265, Opus, AAC, MP3)

## Supported Content

📋 **[View Complete Platform Support Matrix →](PLATFORM_SUPPORT_MATRIX.md)**

### Enhanced Platform Support with Format Classification

| Platform | Videos | Audio Extract | Playlists | Live Streams | Format Types |
|----------|--------|---------------|-----------|--------------|--------------|
| **YouTube** | ✅ Up to 8K | ✅ MP3/AAC/M4A | ✅ Full Support | ⚠️ Detection | 🎬📹🎵 All |
| **Instagram** | ✅ Up to 1080p | ✅ MP3/AAC/M4A | ❌ No | ❌ No | 🎬📹🎵 All |
| **Facebook** | ✅ Up to 1080p | ✅ MP3/AAC/M4A | ❌ No | ❌ No | 🎬📹🎵 All |
| **Twitter/X** | ✅ Up to 1080p | ✅ MP3/AAC/M4A | ❌ No | ❌ No | 🎬📹🎵 All |

### Format Classification Legend
- **🎬 Combined**: Video + Audio in single file (ready to play)
- **📹 Video Only**: Video stream without audio (requires merging)  
- **🎵 Audio Only**: Audio stream without video (MP3, AAC, etc.)
- **Quality Indicators**: 🟢 Best | 🔵 High | 🟡 Medium | 🔴 Low

*All content must be publicly accessible (no login required)*

## Installation

1. **Install Dependencies**:
```bash
pip install fastapi uvicorn[standard] yt-dlp[default] python-multipart aiofiles
