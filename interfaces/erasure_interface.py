"""
Erasure Module Interface
Defines how erasure module communicates with core
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod
from typing import Dict, Any

class IErasureModule(ABC):
    """Interface for erasure module"""
    
    @abstractmethod
    def erase_drive(self, device_path: str, standard: str) -> Dict:
        """Securely erase entire drive"""
        pass
    
    @abstractmethod
    def erase_file(self, file_path: str) -> Dict:
        """Securely erase single file"""
        pass
    
    @abstractmethod
    def verify_erasure(self, device_path: str) -> Dict:
        """Verify erasure was successful"""
        pass

print("Erasure Interface defined")