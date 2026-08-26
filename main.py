"""
Integrated Secure Data Erasure and Advanced File Recovery Tool
Main Entry Point
"""

import sys
import os
import logging

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    print("="*60)
    print("INTEGRATED SECURE DATA ERASURE AND RECOVERY TOOL")
    print("="*60)
    print(f"Python Version: {sys.version}")
    print(f"Current Directory: {os.getcwd()}")
    print("="*60)
    
    print("\n✅ Project initialized successfully!")
    print("\nAvailable modules:")
    print("  1. Core Infrastructure (Device Manager, Storage)")
    print("  2. Secure Erasure Engine")
    print("  3. File Carving & Recovery")
    print("  4. Reporting & Audit System")
    print("  5. User Interface")
    
    print("\n📦 Installed Packages:")
    try:
        import psutil
        print(f"  - psutil {psutil.__version__}")
    except ImportError:
        print("  - psutil (not installed)")
    
    try:
        import numpy
        print(f"  - numpy {numpy.__version__}")
    except ImportError:
        print("  - numpy (not installed)")
    
    try:
        import pandas
        print(f"  - pandas {pandas.__version__}")
    except ImportError:
        print("  - pandas (not installed)")
    
    try:
        import PIL
        print(f"  - Pillow {PIL.__version__}")
    except ImportError:
        print("  - Pillow (not installed)")
    
    print("\n🚀 Ready to start development!")
    print("="*60)

if __name__ == "__main__":
    main()