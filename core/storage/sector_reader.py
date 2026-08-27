"""
Sector Reader Module
Reads raw sectors from storage devices
"""

import os
import logging
from typing import Optional, List, BinaryIO
from core.common.logger import setup_logger
from core.common.constants import SECTOR_SIZE
from core.common.exceptions import SectorReadError, DeviceAccessError

logger = setup_logger(__name__)

class SectorReader:
    """Reads raw sectors from storage devices"""
    
    def __init__(self, sector_size: int = SECTOR_SIZE):
        self.sector_size = sector_size
        self._handle: Optional[BinaryIO] = None
        self._device_path: Optional[str] = None
        logger.info(f"Sector Reader initialized (sector size: {sector_size})")
    
    def open_device(self, device_path: str, mode: str = 'rb') -> bool:
        """
        Open device for reading
        
        Args:
            device_path: Path to device
            mode: File mode ('rb' for read-only)
        
        Returns:
            True if opened successfully
        """
        try:
            self._handle = open(device_path, mode)
            self._device_path = device_path
            logger.info(f"Opened device: {device_path}")
            return True
        except PermissionError:
            logger.error(f"Permission denied: {device_path}")
            raise DeviceAccessError(f"Permission denied: {device_path}")
        except Exception as e:
            logger.error(f"Failed to open device: {e}")
            raise DeviceAccessError(f"Failed to open device: {e}")
    
    def read_sector(self, sector_number: int) -> Optional[bytes]:
        """
        Read a single sector
        
        Args:
            sector_number: Sector to read
        
        Returns:
            Sector data or None if failed
        """
        if not self._handle:
            raise SectorReadError("Device not opened")
        
        try:
            self._handle.seek(sector_number * self.sector_size)
            data = self._handle.read(self.sector_size)
            
            if len(data) != self.sector_size:
                logger.warning(f"Incomplete sector read: {len(data)} bytes")
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to read sector {sector_number}: {e}")
            raise SectorReadError(f"Failed to read sector {sector_number}")
    
    def read_sectors(self, start_sector: int, count: int) -> Optional[bytes]:
        """
        Read multiple consecutive sectors
        
        Args:
            start_sector: First sector to read
            count: Number of sectors
        
        Returns:
            Combined sector data
        """
        if not self._handle:
            raise SectorReadError("Device not opened")
        
        try:
            self._handle.seek(start_sector * self.sector_size)
            data = self._handle.read(count * self.sector_size)
            return data
            
        except Exception as e:
            logger.error(f"Failed to read {count} sectors from {start_sector}: {e}")
            raise SectorReadError(f"Failed to read sectors")
    
    def get_device_size(self) -> int:
        """Get device size in bytes"""
        if not self._handle:
            return 0
        
        try:
            current_pos = self._handle.tell()
            self._handle.seek(0, 2)  # Seek to end
            size = self._handle.tell()
            self._handle.seek(current_pos)  # Restore position
            return size
        except Exception as e:
            logger.error(f"Failed to get device size: {e}")
            return 0
    
    def get_total_sectors(self) -> int:
        """Get total number of sectors"""
        return self.get_device_size() // self.sector_size
    
    def close_device(self):
        """Close device handle"""
        if self._handle:
            self._handle.close()
            logger.info(f"Closed device: {self._device_path}")
            self._handle = None
            self._device_path = None

if __name__ == "__main__":
    reader = SectorReader()
    print("Sector Reader ready")