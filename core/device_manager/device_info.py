"""
Device Information Module
Provides detailed information about storage devices
"""

import psutil
import platform
from dataclasses import dataclass
from typing import Optional, Dict, Any
from core.common.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class DeviceInfo:
    """Detailed device information"""
    name: str
    path: str
    size_bytes: int
    size_gb: float
    filesystem: str
    mountpoint: str
    device_type: str
    manufacturer: str = "Unknown"
    model: str = "Unknown"
    serial_number: str = "Unknown"
    interface: str = "Unknown"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "path": self.path,
            "size_bytes": self.size_bytes,
            "size_gb": self.size_gb,
            "filesystem": self.filesystem,
            "mountpoint": self.mountpoint,
            "device_type": self.device_type,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "serial_number": self.serial_number,
            "interface": self.interface
        }

class DeviceInfoManager:
    """Manages device information"""
    
    def __init__(self):
        self.system = platform.system()
        logger.info(f"Device Info Manager initialized on {self.system}")
    
    def get_device_info(self, device_path: str) -> Optional[DeviceInfo]:
        """Get detailed information about a device"""
        try:
            # Get basic partition info
            partitions = psutil.disk_partitions(all=False)
            
            for partition in partitions:
                if partition.device == device_path:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    return DeviceInfo(
                        name=partition.device,
                        path=partition.device,
                        size_bytes=usage.total,
                        size_gb=round(usage.total / (1024**3), 2),
                        filesystem=partition.fstype or "Unknown",
                        mountpoint=partition.mountpoint,
                        device_type=self._detect_type(partition.device)
                    )
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get device info: {e}")
            return None
    
    def _detect_type(self, device_path: str) -> str:
        """Detect device type from path"""
        device_lower = device_path.lower()
        
        if "nvme" in device_lower:
            return "SSD_NVME"
        elif "ssd" in device_lower:
            return "SSD"
        elif "usb" in device_lower or "removable" in device_lower:
            return "USB"
        elif "sd" in device_lower or "hd" in device_lower:
            return "HDD"
        else:
            return "UNKNOWN"
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "system": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": platform.node()
        }
    
    def check_device_health(self, device_path: str) -> Dict[str, Any]:
        """Check device health status"""
        try:
            usage = psutil.disk_usage(device_path)
            
            health_percent = round((usage.used / usage.total) * 100, 2)
            
            status = "GOOD"
            if health_percent > 90:
                status = "CRITICAL"
            elif health_percent > 75:
                status = "WARNING"
            
            return {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent_used": health_percent,
                "status": status
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "UNKNOWN",
                "error": str(e)
            }

if __name__ == "__main__":
    manager = DeviceInfoManager()
    print(manager.get_system_info())