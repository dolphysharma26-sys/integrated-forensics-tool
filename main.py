"""
Integrated Secure Data Erasure and Advanced File Recovery Tool
Main Entry Point
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.common.logger import setup_logger
from core.common.database import Database
from core.storage.storage_interface import StorageInterface
from integration.workflow.task_queue import TaskQueue

logger = setup_logger('main')

def main():
    print("="*60)
    print("INTEGRATED SECURE DATA ERASURE AND RECOVERY TOOL")
    print("Core Infrastructure - Member 1")
    print("="*60)
    
    # Step 1: Database
    print("\n[1/5] Initializing database...")
    db = Database()
    db.connect()
    db.create_tables()
    print("✅ Database ready")
    
    # Step 2: Storage
    print("\n[2/5] Initializing storage interface...")
    storage = StorageInterface()
    print("✅ Storage interface ready")
    
    # Step 3: Task Queue
    print("\n[3/5] Initializing task queue...")
    tq = TaskQueue(max_workers=2)
    print("✅ Task queue ready")
    
    # Step 4: TSK
    print("\n[4/5] Checking TSK availability...")
    try:
        from integration.tsk_wrapper.tsk_loader import TSKLoader
        tsk_loader = TSKLoader()
        status = tsk_loader.get_status()
        
        if status['tsk']:
            print("✅ Sleuth Kit available for forensic analysis")
        else:
            print("⚠️ TSK not available")
        
        if status['ewf']:
            print("✅ EWF (E01) image support ready")
    except Exception as e:
        print(f"⚠️ TSK check failed: {e}")
    
    # Step 5: Devices
    print("\n[5/5] Detecting devices...")
    devices = storage.list_devices()
    
    if devices:
        print(f"\n📀 Found {len(devices)} device(s):")
        for i, device in enumerate(devices, 1):
            print(f"\n  {i}. {device.name}")
            print(f"     Size: {device.size_gb} GB")
            print(f"     Type: {device.device_type}")
            print(f"     Filesystem: {device.filesystem}")
    else:
        print("\n⚠️ No devices detected")
    
    print("\n" + "="*60)
    print("✅ Core Infrastructure + TSK Integration Ready")
    print("="*60)
    
    db.close()

if __name__ == "__main__":
    main()