"""
Tests for Recovery Module
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

def test_signature_carver():
    """Test signature carver"""
    from modules.recovery.signature_carver import SignatureCarver
    carver = SignatureCarver()
    assert len(carver.signatures) > 0
    print(f"Loaded {len(carver.signatures)} signatures")

def test_jpeg_signature():
    """Test JPEG signature exists"""
    from modules.recovery.signature_carver import SignatureCarver
    carver = SignatureCarver()
    signatures = [s.name for s in carver.signatures]
    assert "JPEG" in signatures
    print("JPEG signature found")