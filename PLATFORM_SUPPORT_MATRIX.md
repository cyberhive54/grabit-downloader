# Platform Support Matrix for Grabit Video Downloader API

## Overview
This document outlines all supported content types across different platforms using yt-dlp. The API supports content that can be accessed without authentication (cookies/login).

---

## 🎬 **YOUTUBE**

### ✅ **Fully Supported (No Login Required)**
| Content Type | Description | Quality Options | Notes |
|--------------|-------------|-----------------|-------|
| **Regular Videos** | Public videos | All available formats | yt-dlp handles format detection |
| **YouTube Shorts** | Short-form videos | All available formats | Standard video extraction |
| **Unlisted Videos** | Videos with direct links | All available | Requires direct URL |
| **Age-Restricted** | Most age-restricted content | All available | Handled by yt-dlp automatically |

### ⚠️ **Limited/Experimental Support**
| Content Type | Description | Limitations | Notes |
|--------------|-------------|-------------|-------|
| **Format Selection** | Choose video quality/format | Basic format picker | Limited quality filtering |

### 🚧 **Planned Features (Not Yet Implemented)**
| Content Type | Description | Status | Priority |
|--------------|-------------|--------|----------|
| **Public Playlists** | Downloadable playlists | Not implemented | High |
| **Audio Only** | Extract audio tracks | Not implemented | High |
| **Live Streams** | Ongoing broadcasts | Not implemented | Medium |
| **Batch Downloads** | Multiple URLs at once | Not implemented | Medium |

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
| **Public Posts** | Videos in feed posts | All available formats | Single videos only |
| **Public Reels** | Short-form videos | All available formats | Standard extraction |

### ⚠️ **Limited Support (Depends on yt-dlp)**
| Content Type | Limitation | Requirements |
|--------------|------------|--------------|
| **IGTV Videos** | No special handling | Public content only |
| **Story Highlights** | Uncertain reliability | Public accounts only |
| **Recent Stories** | May require login | Limited success |
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
| **Public Videos** | Videos in public posts | All available formats | Public pages and profiles |

### ⚠️ **Limited Support (Depends on yt-dlp)**
| Content Type | Limitation | Requirements |
|--------------|------------|--------------|
| **Public Page Videos** | No special handling | Public content only |
| **Shared Public Videos** | Basic extraction | Must be public |

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

| Platform | Public Videos | Private Content | Images | Playlists | Audio Extract | Special Features |
|----------|---------------|-----------------|--------|-----------|---------------|------------------|
| **YouTube** | ✅ Full | ❌ No | ❌ No | 🚧 Planned | 🚧 Planned | Community post detection |
| **Instagram** | ✅ Full | ❌ No | ⚠️ Basic | ❌ No | ❌ No | Single video extraction |
| **Facebook** | ✅ Full | ❌ No | ⚠️ Basic | ❌ No | ❌ No | Public content only |
| **Twitter/X** | ✅ Full | ❌ No | ✅ Enhanced | ❌ No | ❌ No | Image fallback + web scraping |

---

## 🔄 **LAST UPDATED**
**Date**: July 26, 2025  
**yt-dlp Version**: 2025.7.21  
**API Version**: 1.0  

*This matrix is updated regularly as platform support and yt-dlp capabilities evolve.*