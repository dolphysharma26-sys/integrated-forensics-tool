"""
Global Constants for Integrated Forensics Tool
"""

# Sector size in bytes
SECTOR_SIZE = 512

# Operation types
OPERATION_TYPES = {
    "DRIVE_ERASE": "Secure Drive Erasure",
    "FILE_ERASE": "Secure File Erasure",
    "FOLDER_ERASE": "Secure Folder Erasure",
    "FILE_RECOVERY": "File Recovery",
    "FILE_CARVING": "File Carving",
    "VERIFICATION": "Erasure Verification",
    "REPORTING": "Report Generation"
}

# Status codes
STATUS = {
    "PENDING": "PENDING",
    "IN_PROGRESS": "IN_PROGRESS",
    "COMPLETED": "COMPLETED",
    "FAILED": "FAILED",
    "CANCELLED": "CANCELLED"
}

# Erasure standards
ERASURE_STANDARDS = {
    "DoD_5220_22_M": {
        "passes": 3,
        "description": "3-pass overwrite (zeros, ones, random)"
    },
    "DoD_5220_22_M_7PASS": {
        "passes": 7,
        "description": "7-pass overwrite (3x random, zeros, 3x random)"
    },
    "NIST_800_88": {
        "passes": 1,
        "description": "Single pass overwrite"
    },
    "GUTMANN": {
        "passes": 35,
        "description": "35-pass overwrite"
    }
}

# Device types
DEVICE_TYPES = {
    "HDD": "Hard Disk Drive",
    "SSD": "Solid State Drive",
    "SSD_NVME": "NVMe SSD",
    "USB": "USB Drive",
    "MEMORY_CARD": "Memory Card",
    "NETWORK": "Network Storage",
    "UNKNOWN": "Unknown Device"
}

# File signatures for carving
FILE_SIGNATURES = {
    "JPEG": {"header": b'\xFF\xD8\xFF', "footer": b'\xFF\xD9'},
    "PNG": {"header": b'\x89PNG\r\n\x1a\n', "footer": b'IEND\xaeB`\x82'},
    "GIF": {"header": b'GIF8', "footer": b'\x00;'},
    "PDF": {"header": b'%PDF', "footer": b'%%EOF'},
    "ZIP": {"header": b'PK\x03\x04', "footer": b'PK\x05\x06'},
    "RAR": {"header": b'Rar!\x1a\x07', "footer": None},
    "7Z": {"header": b'7z\xbc\xaf\x27\x1c', "footer": None},
    "MP3": {"header": b'ID3', "footer": None},
    "MP4": {"header": b'\x00\x00\x00\x18ftyp', "footer": None}
}

# Buffer sizes
BUFFER_SIZE = 1024 * 1024  # 1MB
CHUNK_SIZE = 10 * 1024 * 1024  # 10MB

# Timeouts
DEVICE_TIMEOUT = 30  # seconds
OPERATION_TIMEOUT = 3600  # 1 hour