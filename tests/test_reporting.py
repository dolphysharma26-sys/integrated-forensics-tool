"""
Tests for Reporting Module
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

def test_report_generator():
    """Test report generator"""
    from modules.reporting.report_generator import ReportGenerator
    rg = ReportGenerator()
    report = rg.generate_report("test")
    assert "report_id" in report
    assert "timestamp" in report
    print(f"Generated report: {report['report_id']}")
