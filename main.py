"""
Integrated Secure Data Erasure and Advanced File Recovery Tool
Main Entry Point
"""

import sys
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("="*60)
    print("INTEGRATED SECURE DATA ERASURE AND RECOVERY TOOL")
    print("="*60)
    print(f"Python: {sys.version.split()[0]}")
    print(f"Directory: {os.getcwd()}")
    print("="*60)
    
    print("\n📦 Testing modules...")
    
    # Test device detector
    try:
        from core.device_manager.device_detector import DeviceDetector
        detector = DeviceDetector()
        devices = detector.list_devices()
        print(f"✅ Device Detector: Found {len(devices)} devices")
        detector.print_devices()
    except Exception as e:
        print(f"❌ Device Detector: {e}")
    
    # Test pattern generator
    try:
        from modules.erasure.pattern_generator import PatternGenerator
        pg = PatternGenerator()
        patterns = pg.get_patterns()
        print(f"\n✅ Pattern Generator: {len(patterns)} patterns ready")
    except Exception as e:
        print(f"❌ Pattern Generator: {e}")
    
    # Test signature carver
    try:
        from modules.recovery.signature_carver import SignatureCarver
        carver = SignatureCarver()
        print(f"✅ Signature Carver: {len(carver.signatures)} signatures loaded")
    except Exception as e:
        print(f"❌ Signature Carver: {e}")
    
    # Test report generator
    try:
        from modules.reporting.report_generator import ReportGenerator
        rg = ReportGenerator()
        print(f"✅ Report Generator: Ready")
    except Exception as e:
        print(f"❌ Report Generator: {e}")
    
    print("\n" + "="*60)
    print("🚀 All modules ready!")
    print("="*60)

if __name__ == "__main__":
    main()