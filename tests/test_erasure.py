"""
Tests for Erasure Module
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

def test_pattern_generator():
    """Test pattern generator"""
    from modules.erasure.pattern_generator import PatternGenerator
    pg = PatternGenerator()
    patterns = pg.get_patterns("DoD_5220_22_M")
    assert len(patterns) == 3
    print(f"Generated {len(patterns)} patterns")

def test_zero_pattern():
    """Test zero pattern"""
    from modules.erasure.pattern_generator import PatternGenerator
    pg = PatternGenerator()
    pattern = pg.get_zero_pattern()
    assert len(pattern) == 512
    assert all(b == 0 for b in pattern)
    print("Zero pattern correct")