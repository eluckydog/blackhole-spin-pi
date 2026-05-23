"""
Unit tests for code/qnm_calculator_v2.py
"""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

import numpy as np
from qnm_calculator_v2 import get_qnm_frequency


def test_qnm_frequency_known_values():
    """Test QNM frequency for known case (GW150914-like parameters)."""
    M_solar = 62.0  # solar masses
    a_star = 0.67   # dimensionless spin
    
    f_R, f_I, T_osc, tau = get_qnm_frequency(M_solar, a_star, l=2, m=2, n=0)
    
    # Check that frequencies are positive
    assert f_R > 0.0, f"f_R should be positive, got {f_R}"
    assert f_I < 0.0, f"f_I should be negative (damping), got {f_I}"
    
    # Check that period and damping time are positive
    assert T_osc > 0.0, f"T_osc should be positive, got {T_osc}"
    assert tau > 0.0, f"tau should be positive, got {tau}"
    
    # Rough check: for M=62, a*=0.67, f_R should be around 300-400 Hz
    assert 200.0 < f_R < 500.0, f"f_R out of expected range: {f_R}"


def test_qnm_frequency_spin_dependence():
    """Test that QNM frequency changes with spin."""
    M_solar = 10.0
    
    f_R_0, _, _, _ = get_qnm_frequency(M_solar, 0.0, l=2, m=2, n=0)
    f_R_099, _, _, _ = get_qnm_frequency(M_solar, 0.99, l=2, m=2, n=0)
    
    # Frequency should change with spin (not necessarily monotonic)
    assert abs(f_R_0 - f_R_099) > 1e-6, "f_R should depend on spin"


def test_qnm_frequency_mass_dependence():
    """Test that QNM frequency scales with mass (f ∝ 1/M)."""
    a_star = 0.5
    
    f_R_10, _, _, _ = get_qnm_frequency(10.0, a_star, l=2, m=2, n=0)
    f_R_20, _, _, _ = get_qnm_frequency(20.0, a_star, l=2, m=2, n=0)
    
    # f_R should scale roughly as 1/M
    ratio = f_R_10 / f_R_20
    expected_ratio = 20.0 / 10.0  # = 2.0
    assert abs(ratio - expected_ratio) / expected_ratio < 0.1, f"Mass scaling wrong: ratio={ratio}, expected ~{expected_ratio}"


def test_qnm_frequency_overtone():
    """Test that overtone n=1 has different frequency from n=0."""
    M_solar = 10.0
    a_star = 0.5
    
    f_R_n0, f_I_n0, _, _ = get_qnm_frequency(M_solar, a_star, l=2, m=2, n=0)
    f_R_n1, f_I_n1, _, _ = get_qnm_frequency(M_solar, a_star, l=2, m=2, n=1)
    
    # Overtone frequency should be different
    assert abs(f_R_n0 - f_R_n1) > 1e-6, "Overtone should have different f_R"
    assert abs(f_I_n0 - f_I_n1) > 1e-6, "Overtone should have different f_I"


def test_qnm_frequency_lm_indices():
    """Test that different (l,m) indices give different frequencies."""
    M_solar = 10.0
    a_star = 0.5
    
    f_R_22, _, _, _ = get_qnm_frequency(M_solar, a_star, l=2, m=2, n=0)
    f_R_33, _, _, _ = get_qnm_frequency(M_solar, a_star, l=3, m=3, n=0)
    
    # Different (l,m) should give different frequencies
    assert abs(f_R_22 - f_R_33) > 1e-6, "Different (l,m) should have different f_R"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
