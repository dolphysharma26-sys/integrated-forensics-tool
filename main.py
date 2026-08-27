"""
Integrated Secure Data Erasure and Advanced File Recovery Tool
Main Entry Point - Member 1: Core Infrastructure
"""

import sys
import os
from core.common.logger import setup_logger
from core.common.database import Database
from core.storage.storage_interface import StorageInterface
from integration.workflow.task_queue import TaskQueue

logger = setup_logger('main')

def main():
    print("="*60)
    print("INTEGRATED SECURE DATA ERASURE AND RECOVERY TOOL")
    print("Core Infrastructure by Member 1")
    print("="*60)
    
    # Initialize database
    logger.info("Initializing database...")
    db = Database()
    db.connect()
    db.create_tables()
    print("✅ Database initialized")
    
    # Initialize storage interface
    logger.info("Initializing storage interface...")
    storage = StorageInterface()
    print("✅ Storage interface ready")
    
    # Initialize task queue
    logger.info("Initializing task queue...")
    tq = TaskQueue(max_workers=2)
    print("✅ Task queue ready")
    
    # List devices
    print("\n📀 Detecting devices...")
    devices = storage.list_devices()
    
    if devices:
        print(f"Found {len(devices)} devices:\n")
        for i, device in enumerate(devices, 1):
            print(f"{i}. {device.name}")
            print(f"   Size: {device.size_gb} GB")
            print(f"   Type: {device.device_type}")
            print(f"   Filesystem: {device.filesystem}")
            print()
    else:
        print("No devices detected")
    
    print("="*60)
    print("✅ Core Infrastructure ready for module integration")
    print("="*60)
    
    # Close database
    db.close()

if __name__ == "__main__":
    main()