"""
Recovery Module Interface
Defines how recovery module communicates with core
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod
from typing import Dict, List, Any

class IRecoveryModule(ABC):
    """Interface for recovery module"""
    
    @abstractmethod
    def carve_files(self, device_path: str) -> List[Dict]:
        """Carve files from device"""
        pass
    
    @abstractmethod
    def recover_deleted(self, device_path: str) -> List[Dict]:
        """Recover deleted files"""
        pass
    
    @abstractmethod
    def classify_files(self, files: List[Dict]) -> List[Dict]:
        """Classify recovered files"""
        pass

print("Recovery Interface defined")