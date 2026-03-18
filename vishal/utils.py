"""
VISHAL Utility Functions
"""
import os
import sys
import time
import json
import hashlib
import platform
import subprocess
from datetime import datetime
from pathlib import Path
import socket
import getpass

class Utils:
    """Utility Functions Class"""
    
    @staticmethod
    def get_system_info():
        """Get complete system information"""
        info = {
            "timestamp": datetime.now().isoformat(),
            "hostname": platform.node(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "username": getpass.getuser(),
            "home": str(Path.home()),
            "cwd": os.getcwd(),
            "pid": os.getpid(),
            "python": sys.version,
            "platform": sys.platform,
            "ip_addresses": Utils.get_ip_addresses(),
            "termux": Utils.is_termux(),
            "android": Utils.is_android(),
            "storage_info": Utils.get_storage_info()
        }
        return info
    
    @staticmethod
    def get_ip_addresses():
        """Get all IP addresses"""
        ips = []
        try:
            hostname = socket.gethostname()
            ips.append(socket.gethostbyname(hostname))
            
            # Get all interfaces
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ips.append(s.getsockname()[0])
            s.close()
        except:
            pass
        return list(set(ips))
    
    @staticmethod
    def is_termux():
        """Check if running in Termux"""
        return os.path.exists('/data/data/com.termux')
    
    @staticmethod
    def is_android():
        """Check if running on Android"""
        return 'android' in platform.platform().lower()
    
    @staticmethod
    def get_storage_info():
        """Get storage information"""
        storage = {}
        paths = ['/', '/sdcard', '/storage', '/data']
        
        for path in paths:
            if os.path.exists(path):
                try:
                    stat = os.statvfs(path)
                    total = stat.f_frsize * stat.f_blocks
                    free = stat.f_frsize * stat.f_bfree
                    used = total - free
                    
                    storage[path] = {
                        "total": Utils.format_size(total),
                        "used": Utils.format_size(used),
                        "free": Utils.format_size(free),
                        "percent": f"{(used/total)*100:.1f}%"
                    }
                except:
                    continue
        
        return storage
    
    @staticmethod
    def format_size(size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    
    @staticmethod
    def get_file_hash(filepath):
        """Get file hash"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    @staticmethod
    def get_file_info(filepath):
        """Get detailed file information"""
        try:
            stat = os.stat(filepath)
            return {
                "path": filepath,
                "name": os.path.basename(filepath),
                "size": stat.st_size,
                "size_fmt": Utils.format_size(stat.st_size),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                "extension": os.path.splitext(filepath)[1],
                "hash": Utils.get_file_hash(filepath)
            }
        except:
            return None
    
    @staticmethod
    def run_command(cmd):
        """Run system command"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def save_cache(data, filename):
        """Save data to cache"""
        try:
            cache_dir = Path.home() / '.vishal_cache'
            cache_dir.mkdir(exist_ok=True)
            cache_file = cache_dir / filename
            
            with open(cache_file, 'w') as f:
                json.dump(data, f)
            return True
        except:
            return False
    
    @staticmethod
    def load_cache(filename):
        """Load data from cache"""
        try:
            cache_file = Path.home() / '.vishal_cache' / filename
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return None