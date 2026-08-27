"""
Storage Interface Module
Unified interface for all storage operations
"""

from typing import Optional, List, Dict, Any
from core.common.logger import setup_logger
from core.device_manager.device_detector import DeviceDetector
from core.device_manager.device_info import DeviceInfoManager
from core.device_manager.device_locker import DeviceLocker
from core.storage.sector_reader import SectorReader
from core.storage.sector_writer import SectorWriter

logger = setup_logger(__name__)

class StorageInterface:
    """Unified storage management interface"""
    
    def __init__(self):
        self.detector = DeviceDetector()
        self.info_manager = DeviceInfoManager()
        self.locker = DeviceLocker()
        self.reader = SectorReader()
        self.writer = SectorWriter()
        logger.info("Storage Interface initialized")
    
    def list_devices(self) -> List:
        """List all connected devices"""
        return self.detector.list_devices()
    
    def get_device_info(self, device_path: str) -> Optional[Dict]:
        """Get device information"""
        info = self.info_manager.get_device_info(device_path)
        return info.to_dict() if info else None
    
    def lock_device(self, device_path: str, owner: str) -> bool:
        """Lock device for exclusive access"""
        return self.locker.acquire_lock(device_path, owner)
    
    def unlock_device(self, device_path: str, owner: str) -> bool:
        """Unlock device"""
        return self.locker.release_lock(device_path, owner)
    
    def read_sectors(self, device_path: str, start: int, count: int) -> Optional[bytes]:
        """Read sectors from device"""
        try:
            self.reader.open_device(device_path)
            data = self.reader.read_sectors(start, count)
            self.reader.close_device()
            return data
        except Exception as e:
            logger.error(f"Read operation failed: {e}")
            return None
    
    def write_pattern(self, device_path: str, sector: int, pattern: bytes) -> bool:
        """Write pattern to device"""
        try:
            self.writer.open_for_writing(device_path)
            result = self.writer.write_pattern(sector, pattern)
            self.writer.close_device()
            return result
        except Exception as e:
            logger.error(f"Write operation failed: {e}")
            return False
    
    def get_device_health(self, device_path: str) -> Dict:
        """Get device health status"""
        return self.info_manager.check_device_health(device_path)

if __name__ == "__main__":
    storage = StorageInterface()
    print("Storage Interface ready")
    
    devices = storage.list_devices()
    for device in devices:
        print(f"Found: {device.name}")