"""
TSK Loader Module
Loads and manages The Sleuth Kit library
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.common.logger import setup_logger

logger = setup_logger(__name__)

class TSKLoader:
    """Loads TSK and related forensic libraries"""
    
    def __init__(self):
        self.tsk = None
        self.tsk_available = False
        self.ewf_available = False
        self._load_libraries()
    
    def _load_libraries(self):
        """Load TSK and libewf"""
        
        # Load TSK
        try:
            import pytsk3
            self.tsk = pytsk3
            self.tsk_available = True
            logger.info("Sleuth Kit loaded successfully")
        except ImportError:
            logger.warning("Sleuth Kit not available")
        
        # Load libewf
        try:
            import pyewf
            self.ewf = pyewf
            self.ewf_available = True
            logger.info("libewf loaded successfully")
        except ImportError:
            logger.warning("libewf not available")
    
    def is_available(self):
        """Check if TSK is ready"""
        return self.tsk_available
    
    def get_tsk(self):
        """Get TSK module"""
        return self.tsk
    
    def get_status(self):
        """Get library status"""
        return {
            "tsk": self.tsk_available,
            "ewf": self.ewf_available
        }

if __name__ == "__main__":
    loader = TSKLoader()
    status = loader.get_status()
    print(f"TSK Available: {status['tsk']}")
    print(f"EWF Available: {status['ewf']}")
