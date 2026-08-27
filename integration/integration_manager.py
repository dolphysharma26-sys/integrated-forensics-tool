"""
Integration Manager Module
Connects all modules together
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, Optional
from core.common.logger import setup_logger

logger = setup_logger(__name__)

class IntegrationManager:
    """Manages integration between all modules"""
    
    def __init__(self):
        self.modules = {}
        self.connections = {}
        logger.info("Integration Manager initialized")
    
    def register_module(self, name: str, module: Any):
        """Register a module"""
        self.modules[name] = module
        logger.info(f"Module registered: {name}")
    
    def get_module(self, name: str) -> Optional[Any]:
        """Get registered module"""
        return self.modules.get(name)
    
    def connect_modules(self, source: str, target: str):
        """Connect two modules"""
        if source not in self.modules:
            logger.error(f"Source module not found: {source}")
            return False
        
        if target not in self.modules:
            logger.error(f"Target module not found: {target}")
            return False
        
        self.connections[f"{source}->{target}"] = True
        logger.info(f"Connected: {source} -> {target}")
        return True
    
    def execute_cross_module(self, source: str, method: str, **kwargs):
        """Execute method on a module"""
        module = self.get_module(source)
        if not module:
            logger.error(f"Module not found: {source}")
            return None
        
        if hasattr(module, method):
            return getattr(module, method)(**kwargs)
        else:
            logger.error(f"Method not found: {source}.{method}")
            return None

if __name__ == "__main__":
    im = IntegrationManager()
    print("Integration Manager ready")
    im.register_module("test", {"name": "test_module"})
    print(f"Registered modules: {list(im.modules.keys())}")