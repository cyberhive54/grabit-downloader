"""
Configuration settings for the Video Downloader API
"""

import os
from pathlib import Path

class Settings:
    """Application settings"""
    
    # Download configuration
    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")
    DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", "300"))  # 5 minutes
    
    # yt-dlp configuration
    MAX_FILESIZE = os.getenv("MAX_FILESIZE", "500M")  # 500MB max
    
    # API configuration
    MAX_CONCURRENT_DOWNLOADS = int(os.getenv("MAX_CONCURRENT_DOWNLOADS", "3"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    def __init__(self):
        # Ensure download directory exists
        Path(self.DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

# Global settings instance
settings = Settings()
