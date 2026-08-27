"""
Custom Exceptions for Integrated Forensics Tool
"""

class ForensicsError(Exception):
    """Base exception for all errors"""
    pass

class DeviceError(ForensicsError):
    """Raised when device operations fail"""
    pass

class DeviceNotFoundError(DeviceError):
    """Raised when device is not found"""
    pass

class DeviceAccessError(DeviceError):
    """Raised when device access is denied"""
    pass

class DeviceLockedError(DeviceError):
    """Raised when device is locked"""
    pass

class StorageError(ForensicsError):
    """Raised when storage operations fail"""
    pass

class SectorReadError(StorageError):
    """Raised when sector read fails"""
    pass

class SectorWriteError(StorageError):
    """Raised when sector write fails"""
    pass

class ErasureError(ForensicsError):
    """Raised when erasure fails"""
    pass

class VerificationError(ForensicsError):
    """Raised when verification fails"""
    pass

class RecoveryError(ForensicsError):
    """Raised when recovery fails"""
    pass

class ReportingError(ForensicsError):
    """Raised when reporting fails"""
    pass

class DatabaseError(ForensicsError):
    """Raised when database operations fail"""
    pass

class IntegrationError(ForensicsError):
    """Raised when module integration fails"""
    pass