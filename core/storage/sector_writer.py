"""
Sector Writer Module
Writes raw sectors to storage devices for secure erasure
"""

import os
from typing import Optional, BinaryIO
from core.common.logger import setup_logger
from core.common.constants import SECTOR_SIZE
from core.common.exceptions import SectorWriteError, DeviceAccessError

logger = setup_logger(__name__)

class SectorWriter:
    """Writes raw sectors to storage devices"""
    
    def __init__(self, sector_size: int = SECTOR_SIZE):
        self.sector_size = sector_size
        self._handle: Optional[BinaryIO] = None
        self._device_path: Optional[str] = None
        logger.info(f"Sector Writer initialized (sector size: {sector_size})")
    
    def open_for_writing(self, device_path: str) -> bool:
        """
        Open device for writing
        
        Args:
            device_path: Path to device
        
        Returns:
            True if opened successfully
        """
        try:
            self._handle = open(device_path, 'wb')
            self._device_path = device_path
            logger.info(f"Opened device for writing: {device_path}")
            return True
        except PermissionError:
            logger.error(f"Permission denied: {device_path}")
            raise DeviceAccessError(f"Permission denied: {device_path}")
        except Exception as e:
            logger.error(f"Failed to open device: {e}")
            raise DeviceAccessError(f"Failed to open device: {e}")
    
    def write_sector(self, sector_number: int, data: bytes) -> bool:
        """
        Write data to a single sector
        
        Args:
            sector_number: Sector to write
            data: Data to write (should be sector_size bytes)
        
        Returns:
            True if written successfully
        """
        if not self._handle:
            raise SectorWriteError("Device not opened for writing")
        
        try:
            if len(data) != self.sector_size:
                logger.warning(f"Data size {len(data)} != sector size {self.sector_size}")
                # Pad or truncate to sector size
                data = data[:self.sector_size].ljust(self.sector_size, b'\x00')
            
            self._handle.seek(sector_number * self.sector_size)
            self._handle.write(data)
            return True
            
        except Exception as e:
            logger.error(f"Failed to write sector {sector_number}: {e}")
            raise SectorWriteError(f"Failed to write sector {sector_number}")
    
    def write_pattern(self, sector_number: int, pattern: bytes) -> bool:
        """Write a pattern to a sector"""
        return self.write_sector(sector_number, pattern)
    
    def write_sectors(self, start_sector: int, count: int, pattern: bytes) -> int:
        """
        Write pattern to multiple sectors
        
        Returns:
            Number of sectors written successfully
        """
        successful = 0
        
        for sector in range(start_sector, start_sector + count):
            if self.write_pattern(sector, pattern):
                successful += 1
        
        return successful
    
    def flush(self):
        """Flush write buffer to disk"""
        if self._handle:
            self._handle.flush()
            os.fsync(self._handle.fileno())
    
    def close_device(self):
        """Close device handle"""
        if self._handle:
            self.flush()
            self._handle.close()
            logger.info(f"Closed device: {self._device_path}")
            self._handle = None
            self._device_path = None

if __name__ == "__main__":
    writer = SectorWriter()
    print("Sector Writer ready")