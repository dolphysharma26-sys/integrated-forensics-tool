"""
Reporting Module Interface
Defines how reporting module communicates with core
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod
from typing import Dict, Any

class IReportingModule(ABC):
    """Interface for reporting module"""
    
    @abstractmethod
    def generate_report(self, operation_type: str, data: Dict) -> Dict:
        """Generate report"""
        pass
    
    @abstractmethod
    def log_audit(self, action: str, details: Dict) -> bool:
        """Log audit entry"""
        pass

print("Reporting Interface defined")