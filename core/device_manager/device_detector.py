"""
Device Detection Module
Detects connected storage devices on the system
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import psutil
import logging
import platform
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)

@dataclass
class Device:
    """Represents a storage device"""
    name: str
    path: str
    size_gb: float
    filesystem: str
    mountpoint: str
    device_type: str

class DeviceDetector:
    """Detects and manages storage devices"""
    
    def __init__(self):
        self.devices: List[Device] = []
        logger.info("Device Detector initialized")
    
    def list_devices(self) -> List[Device]:
        """List all connected storage devices"""
        self.devices = []
        
        try:
            partitions = psutil.disk_partitions(all=False)
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    device_type = self._detect_device_type(partition.device)
                    
                    device = Device(
                        name=partition.device,
                        path=partition.device,
                        size_gb=round(usage.total / (1024**3), 2),
                        filesystem=partition.fstype or "Unknown",
                        mountpoint=partition.mountpoint,
                        device_type=device_type
                    )
                    
                    self.devices.append(device)
                    logger.info(f"Detected device: {device.name} ({device.size_gb} GB)")
                    
                except PermissionError:
                    logger.warning(f"Permission denied for {partition.device}")
                except Exception as e:
                    logger.error(f"Error accessing {partition.device}: {e}")
        
        except Exception as e:
            logger.error(f"Device detection failed: {e}")
        
        return self.devices
    
    def _detect_device_type(self, device_path: str) -> str:
        """Detect device type"""
        system = platform.system()
        
        if system == "Windows":
            # Windows: C:\ is system drive
            if device_path == "C:\\":
                return "System Drive (SSD)"
            else:
                return "Local Disk"
        else:
            # Linux/macOS
            device_lower = device_path.lower()
            
            if "nvme" in device_lower:
                return "SSD (NVMe)"
            elif "usb" in device_lower:
                return "USB Drive"
            elif "sd" in device_lower:
                return "HDD"
            else:
                return "Unknown"
    
    def get_device_by_name(self, name: str) -> Optional[Device]:
        """Get device by its name/path"""
        for device in self.devices:
            if device.name == name:
                return device
        return None
    
    def print_devices(self):
        """Display all detected devices"""
        if not self.devices:
            print("\nNo devices detected!")
            return
        
        print("\n" + "="*60)
        print("DETECTED STORAGE DEVICES")
        print("="*60)
        
        for i, device in enumerate(self.devices, 1):
            print(f"\n{i}. Device: {device.name}")
            print(f"   Type: {device.device_type}")
            print(f"   Size: {device.size_gb} GB")
            print(f"   File System: {device.filesystem}")
            print(f"   Mount Point: {device.mountpoint}")
        
        print("\n" + "="*60)

# Test the module
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    detector = DeviceDetector()
    devices = detector.list_devices()
    detector.print_devices()