"""
Tests for Core Infrastructure
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

def test_device_detector():
    """Test device detector works"""
    from core.device_manager.device_detector import DeviceDetector
    detector = DeviceDetector()
    devices = detector.list_devices()
    assert isinstance(devices, list)
    assert len(devices) > 0
    print(f"Found {len(devices)} devices")

def test_database():
    """Test database initialization"""
    from core.common.database import Database
    db = Database("data/test.db")
    db.connect()
    db.create_tables()
    db.close()
    assert True

def test_logger():
    """Test logger setup"""
    from core.common.logger import setup_logger
    logger = setup_logger("test")
    logger.info("Test log message")
    assert logger is not None

def test_constants():
    """Test constants"""
    from core.common.constants import SECTOR_SIZE
    assert SECTOR_SIZE == 512

def test_tsk_loader():
    """Test TSK loader"""
    from integration.tsk_wrapper.tsk_loader import TSKLoader
    loader = TSKLoader()
    status = loader.get_status()
    assert "tsk" in status
    assert "ewf" in status
    print(f"TSK: {status['tsk']}, EWF: {status['ewf']}")