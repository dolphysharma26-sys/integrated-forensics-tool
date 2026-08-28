"""
Complete Test Suite for Integrated Forensics Tool
Tests all modules and files
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_header(title):
    """Print test header"""
    print("\n" + "="*60)
    print(f"TESTING: {title}")
    print("="*60)

def test_result(name, success, details=""):
    """Print test result"""
    if success:
        print(f"✅ PASS: {name} {details}")
    else:
        print(f"❌ FAIL: {name} {details}")
    return success

def main():
    results = []
    
    # ============================================
    # TEST 1: Core Common Modules
    # ============================================
    test_header("CORE COMMON MODULES")
    
    # Test Logger
    try:
        from core.common.logger import setup_logger
        logger = setup_logger('test')
        results.append(test_result("Logger", True))
    except Exception as e:
        results.append(test_result("Logger", False, f"- {e}"))
    
    # Test Constants
    try:
        from core.common.constants import SECTOR_SIZE, ERASURE_STANDARDS
        results.append(test_result("Constants", True, f"(Sector: {SECTOR_SIZE}, Standards: {len(ERASURE_STANDARDS)})"))
    except Exception as e:
        results.append(test_result("Constants", False, f"- {e}"))
    
    # Test Exceptions
    try:
        from core.common.exceptions import ForensicsError, DeviceError
        results.append(test_result("Exceptions", True))
    except Exception as e:
        results.append(test_result("Exceptions", False, f"- {e}"))
    
    # Test Database
    try:
        from core.common.database import Database
        db = Database("data/test.db")
        db.connect()
        db.create_tables()
        db.close()
        results.append(test_result("Database", True))
    except Exception as e:
        results.append(test_result("Database", False, f"- {e}"))
    
    # ============================================
    # TEST 2: Device Manager
    # ============================================
    test_header("DEVICE MANAGER")
    
    # Test Device Detector
    try:
        from core.device_manager.device_detector import DeviceDetector
        detector = DeviceDetector()
        devices = detector.list_devices()
        results.append(test_result("Device Detector", True, f"(Found {len(devices)} devices)"))
        
        if devices:
            for device in devices:
                print(f"         - {device.name}: {device.size_gb} GB ({device.device_type})")
    except Exception as e:
        results.append(test_result("Device Detector", False, f"- {e}"))
    
    # Test Device Info
    try:
        from core.device_manager.device_info import DeviceInfoManager
        info_manager = DeviceInfoManager()
        system_info = info_manager.get_system_info()
        results.append(test_result("Device Info", True, f"(System: {system_info.get('system')})"))
    except Exception as e:
        results.append(test_result("Device Info", False, f"- {e}"))
    
    # Test Device Locker
    try:
        from core.device_manager.device_locker import DeviceLocker
        locker = DeviceLocker()
        locker.acquire_lock("test_device", "test_owner")
        is_locked = locker.is_locked("test_device")
        locker.release_lock("test_device", "test_owner")
        results.append(test_result("Device Locker", is_locked))
    except Exception as e:
        results.append(test_result("Device Locker", False, f"- {e}"))
    
    # ============================================
    # TEST 3: Storage Layer
    # ============================================
    test_header("STORAGE LAYER")
    
    # Test Sector Reader
    try:
        from core.storage.sector_reader import SectorReader
        reader = SectorReader()
        results.append(test_result("Sector Reader", True))
    except Exception as e:
        results.append(test_result("Sector Reader", False, f"- {e}"))
    
    # Test Sector Writer
    try:
        from core.storage.sector_writer import SectorWriter
        writer = SectorWriter()
        results.append(test_result("Sector Writer", True))
    except Exception as e:
        results.append(test_result("Sector Writer", False, f"- {e}"))
    
    # Test Storage Interface
    try:
        from core.storage.storage_interface import StorageInterface
        storage = StorageInterface()
        devices = storage.list_devices()
        results.append(test_result("Storage Interface", True, f"(Devices: {len(devices)})"))
    except Exception as e:
        results.append(test_result("Storage Interface", False, f"- {e}"))
    
    # ============================================
    # TEST 4: Integration Layer
    # ============================================
    test_header("INTEGRATION LAYER")
    
    # Test TSK Loader
    try:
        from integration.tsk_wrapper.tsk_loader import TSKLoader
        tsk_loader = TSKLoader()
        status = tsk_loader.get_status()
        results.append(test_result("TSK Loader", True, f"(TSK: {status['tsk']}, EWF: {status['ewf']})"))
    except Exception as e:
        results.append(test_result("TSK Loader", False, f"- {e}"))
    
    # Test TSK File System Parser
    try:
        from integration.tsk_wrapper.tsk_fs_parser import TSKFileSystemParser
        tsk_parser = TSKFileSystemParser()
        results.append(test_result("TSK Parser", True))
    except Exception as e:
        results.append(test_result("TSK Parser", False, f"- {e}"))
    
    # Test Task Queue
    try:
        from integration.workflow.task_queue import TaskQueue, Task, TaskStatus
        tq = TaskQueue(max_workers=1)
        results.append(test_result("Task Queue", True))
    except Exception as e:
        results.append(test_result("Task Queue", False, f"- {e}"))
    
    # Test Workflow Manager
    try:
        from integration.workflow.workflow_manager import WorkflowManager, WorkflowType
        wm = WorkflowManager()
        results.append(test_result("Workflow Manager", True))
    except Exception as e:
        results.append(test_result("Workflow Manager", False, f"- {e}"))
    
    # Test Integration Manager
    try:
        from integration.integration_manager import IntegrationManager
        im = IntegrationManager()
        results.append(test_result("Integration Manager", True))
    except Exception as e:
        results.append(test_result("Integration Manager", False, f"- {e}"))
    
    # ============================================
    # TEST 5: Module Interfaces
    # ============================================
    test_header("MODULE INTERFACES")
    
    # Test Erasure Interface
    try:
        from interfaces.erasure_interface import IErasureModule
        results.append(test_result("Erasure Interface", True))
    except Exception as e:
        results.append(test_result("Erasure Interface", False, f"- {e}"))
    
    # Test Recovery Interface
    try:
        from interfaces.recovery_interface import IRecoveryModule
        results.append(test_result("Recovery Interface", True))
    except Exception as e:
        results.append(test_result("Recovery Interface", False, f"- {e}"))
    
    # Test Reporting Interface
    try:
        from interfaces.reporting_interface import IReportingModule
        results.append(test_result("Reporting Interface", True))
    except Exception as e:
        results.append(test_result("Reporting Interface", False, f"- {e}"))
    
    # ============================================
    # TEST 6: Modules (Starter Code)
    # ============================================
    test_header("MODULES (STARTER CODE)")
    
    # Test Pattern Generator
    try:
        from modules.erasure.pattern_generator import PatternGenerator
        pg = PatternGenerator()
        patterns = pg.get_patterns("DoD_5220_22_M")
        results.append(test_result("Pattern Generator", True, f"({len(patterns)} patterns)"))
    except Exception as e:
        results.append(test_result("Pattern Generator", False, f"- {e}"))
    
    # Test Signature Carver
    try:
        from modules.recovery.signature_carver import SignatureCarver
        carver = SignatureCarver()
        results.append(test_result("Signature Carver", True, f"({len(carver.signatures)} signatures)"))
    except Exception as e:
        results.append(test_result("Signature Carver", False, f"- {e}"))
    
    # Test Report Generator
    try:
        from modules.reporting.report_generator import ReportGenerator
        rg = ReportGenerator()
        results.append(test_result("Report Generator", True))
    except Exception as e:
        results.append(test_result("Report Generator", False, f"- {e}"))
    
    # ============================================
    # SUMMARY
    # ============================================
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n⚠️ SOME TESTS FAILED - Check above for details")
    
    print("="*60)

if __name__ == "__main__":
    main()