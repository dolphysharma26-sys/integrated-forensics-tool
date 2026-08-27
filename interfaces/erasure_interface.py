"""
Erasure Module Interface
Defines how erasure module communicates with other modules
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

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
    def erase_folder(self, folder_path: str) -> Dict:
        """Securely erase folder"""
        pass
    
    @abstractmethod
    def verify_erasure(self, device_path: str) -> Dict:
        """Verify erasure was successful"""
        pass
    
    @abstractmethod
    def get_erasure_status(self, operation_id: str) -> Dict:
        """Get erasure operation status"""
        pass