# Platform Support Matrix for Grabit Video Downloader API

## Overview
This document outlines all supported content types across different platforms using yt-dlp. The API supports content that can be accessed without authentication (cookies/login).

---

## 🎬 **YOUTUBE**

### ✅ **Fully Supported (No Login Required)**
| Content Type | Description | Quality Options | Notes |
|--------------|-------------|-----------------|-------|
| **Regular Videos** | Public videos | 144p to 8K/4K | All formats: MP4, WebM, etc. |
| **YouTube Shorts** | Short-form videos | Up to 1080p | Full metadata extraction |
| **Public Playlists** | Downloadable playlists | Varies by video | Batch download support |
| **Unlisted Videos** | Videos with direct links | All available | Requires direct URL |
| **Age-Restricted** | Most age-restricted content | All available | Some may require verification |
| **Live Streams** | Ongoing broadcasts | Source quality | Experimental support |
| **Audio Only** | Extract audio tracks | MP3, AAC, OGG | Various bitrates |

### ❌ **Not Supported**
| Content Type | Reason | Alternative |
|--------------|--------|-------------|
| **Community Posts** | Text/image content, not video | Use official YouTube app |
| **Members-Only Videos** | Requires channel membership | Subscribe to channel |
| **Private Videos** | Requires owner permission | Get direct access from owner |
| **Premium Content** | Requires YouTube Premium | Use YouTube Premium |
| **Live Chat** | Not video content | Use specialized chat tools |

---

## 📱 **INSTAGRAM**

### ✅ **Fully Supported (No Login Required)**
| Content Type | Description | Quality Options | Notes |
|--------------|-------------|-----------------|-------|
| **Public Posts** | Videos in feed posts | Up to 1080p | Single videos and carousels |
| **Public Reels** | Short-form videos | Up to 1080p | Full metadata extraction |
| **IGTV Videos** | Longer-form content | Up to 1080p | If publicly accessible |
| **Story Highlights** | Saved public stories | Up to 1080p | Public accounts only |

### ⚠️ **Limited Support**
| Content Type | Limitation | Requirements |
|--------------|------------|--------------|
| **Recent Stories** | May require login | Public accounts preferred |
| **Newer Content** | Instagram's restrictions | May work intermittently |

### ❌ **Not Supported**
| Content Type | Reason |
|--------------|--------|
| **Private Account Content** | Requires following/login |
| **Protected Stories** | Account privacy settings |
| **Live Streams** | Real-time content restrictions |

---

## 🔵 **FACEBOOK**

### ✅ **Fully Supported (No Login Required)**
| Content Type | Description | Quality Options | Notes |
|--------------|-------------|-----------------|-------|
| **Public Videos** | Videos in public posts | Up to 1080p | Public pages and profiles |
| **Public Page Videos** | Business/creator content | Up to 1080p | Embedded or direct links |
| **Shared Public Videos** | Publicly shared content | Varies | Must be public |

### ❌ **Not Supported**
| Content Type | Reason |
|--------------|--------|
| **Private Group Videos** | Requires group membership |
| **Friends-Only Content** | Privacy restrictions |
| **Facebook Live** | Authentication required |
| **Private Profile Videos** | Account privacy settings |

---

## 🐦 **TWITTER/X**

### ✅ **Fully Supported (No Login Required)**
| Content Type | Description | Quality Options | Notes |
|--------------|-------------|-----------------|-------|
| **Video Tweets** | Videos in public tweets | Up to 1080p | All video formats |
| **Image Tweets** | Images in public posts | Original quality | Enhanced extraction with fallback |
| **GIF Tweets** | Animated content | Original quality | MP4 format conversion |
| **Thread Videos** | Videos in tweet threads | Up to 1080p | Individual tweet extraction |

### ⚠️ **Enhanced Features**
| Feature | Description | Implementation |
|---------|-------------|----------------|
| **Image Extraction** | Fallback web scraping | When yt-dlp fails to detect images |
| **Multiple Images** | Download all images from post | Batch download to organized folders |
| **Quality Enhancement** | Convert to larger sizes | :small → :large, &name=orig |

### ❌ **Not Supported**
| Content Type | Reason |
|--------------|--------|
| **Protected Accounts** | Account privacy settings |
| **Private/DM Media** | Requires authentication |
| **Twitter Spaces** | Audio-only live content |
| **Fleet Content** | Discontinued feature |

---

## 🎵 **ADDITIONAL PLATFORMS**

### ✅ **Other Supported Platforms**
The API supports 1000+ additional platforms through yt-dlp, including:

| Platform Category | Examples | Content Types |
|------------------|----------|---------------|
| **Video Platforms** | Vimeo, Dailymotion, Twitch | Videos, clips, VODs |
| **News Sites** | BBC, CNN, Reuters | News videos, reports |
| **Educational** | Khan Academy, Coursera | Course videos, lectures |
| **Entertainment** | TikTok, Reddit | Short videos, clips |

---

## 🔧 **TECHNICAL SPECIFICATIONS**

### **Quality Options Available**
- **Video**: 144p, 240p, 360p, 480p, 720p (HD), 1080p (FHD), 1440p (2K), 2160p (4K), 4320p (8K)
- **Audio**: 32kbps to 320kbps, various formats (MP3, AAC, OGG, M4A)
- **Formats**: MP4, WebM, MKV, AVI, MOV, FLV

### **Metadata Extraction**
- Video title and description
- Upload date and duration
- View count and engagement metrics
- Thumbnail images (multiple sizes)
- Subtitle/caption files
- Channel/uploader information

### **Download Features**
- **Two-Phase Process**: Metadata extraction → Selective download
- **Format Selection**: Choose quality and format before downloading
- **Batch Processing**: Multiple URLs in playlists
- **Progress Tracking**: Real-time download status
- **Error Handling**: Detailed error messages for unsupported content

---

## 🚫 **GLOBAL LIMITATIONS**

### **Content Requiring Authentication**
- Private/protected accounts across all platforms
- Membership-only content (YouTube, Patreon, etc.)
- Age-restricted content requiring account verification
- Live streams requiring subscription
- Platform-specific premium content

### **Technical Limitations**
- DRM-protected content (Netflix, Disney+, etc.)
- Real-time live streams (limited support)
- Very large files (configurable size limits)
- Rate limiting by platforms
- Geo-restricted content

### **Legal Considerations**
- Respect platform terms of service
- Consider copyright restrictions
- Personal use vs. redistribution
- Fair use guidelines
- Platform-specific policies

---

## 📊 **SUPPORT SUMMARY**

| Platform | Public Videos | Private Content | Images | Live Streams | Special Features |
|----------|---------------|-----------------|--------|--------------|------------------|
| **YouTube** | ✅ Full | ❌ No | ❌ No | ⚠️ Limited | Playlist support |
| **Instagram** | ✅ Full | ❌ No | ✅ Yes | ❌ No | Story highlights |
| **Facebook** | ✅ Full | ❌ No | ⚠️ Limited | ❌ No | Page content |
| **Twitter/X** | ✅ Full | ❌ No | ✅ Enhanced | ❌ No | Image fallback |

---

## 🔄 **LAST UPDATED**
**Date**: July 26, 2025  
**yt-dlp Version**: 2025.7.21  
**API Version**: 1.0  

*This matrix is updated regularly as platform support and yt-dlp capabilities evolve.*