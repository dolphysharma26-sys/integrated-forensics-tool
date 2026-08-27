"""
Device Locking Module
Prevents concurrent access to devices during operations
"""

import threading
from typing import Dict, Optional
from core.common.logger import setup_logger
from core.common.exceptions import DeviceLockedError, DeviceError

logger = setup_logger(__name__)

class DeviceLocker:
    """Manages device locks for exclusive access"""
    
    def __init__(self):
        self._locks: Dict[str, threading.Lock] = {}
        self._owners: Dict[str, str] = {}
        self._lock_manager = threading.Lock()
        logger.info("Device Locker initialized")
    
    def acquire_lock(self, device_path: str, owner: str, timeout: int = 30) -> bool:
        """
        Acquire lock on device
        
        Args:
            device_path: Device to lock
            owner: Who is locking
            timeout: Max wait time in seconds
        
        Returns:
            True if lock acquired, False otherwise
        """
        with self._lock_manager:
            if device_path not in self._locks:
                self._locks[device_path] = threading.Lock()
            
            lock = self._locks[device_path]
        
        acquired = lock.acquire(timeout=timeout)
        
        if acquired:
            with self._lock_manager:
                self._owners[device_path] = owner
            logger.info(f"Device locked: {device_path} by {owner}")
            return True
        else:
            logger.warning(f"Failed to lock device: {device_path}")
            return False
    
    def release_lock(self, device_path: str, owner: str) -> bool:
        """
        Release lock on device
        
        Args:
            device_path: Device to unlock
            owner: Who is unlocking
        
        Returns:
            True if released, False otherwise
        """
        with self._lock_manager:
            if device_path not in self._locks:
                logger.warning(f"Device not locked: {device_path}")
                return False
            
            if self._owners.get(device_path) != owner:
                logger.warning(f"Lock owner mismatch for {device_path}")
                return False
            
            lock = self._locks[device_path]
            del self._owners[device_path]
        
        lock.release()
        logger.info(f"Device unlocked: {device_path}")
        return True
    
    def is_locked(self, device_path: str) -> bool:
        """Check if device is locked"""
        with self._lock_manager:
            return device_path in self._owners
    
    def get_owner(self, device_path: str) -> Optional[str]:
        """Get lock owner"""
        with self._lock_manager:
            return self._owners.get(device_path)
    
    def get_all_locks(self) -> Dict[str, str]:
        """Get all active locks"""
        with self._lock_manager:
            return self._owners.copy()
    
    def force_unlock(self, device_path: str) -> bool:
        """Force unlock a device"""
        with self._lock_manager:
            if device_path not in self._locks:
                return False
            
            lock = self._locks[device_path]
            owner = self._owners.pop(device_path, None)
        
        lock.release()
        logger.info(f"Force unlocked: {device_path} (was locked by {owner})")
        return True

if __name__ == "__main__":
    locker = DeviceLocker()
    print("Device Locker ready")