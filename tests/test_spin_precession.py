"""
Unit tests for code/spin_precession.py
"""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from spin_precession import lense_thirring_omega


def test_lense_thirring_omega_basic():
    """Test Lense-Thirring frequency for basic case."""
    M_solar = 10.0  # 10 solar masses
    a_star = 0.5
    r = 10.0  # 10 Schwarzschild radii
    
    Omega_LT, f_LT, T_precess = lense_thirring_omega(M_solar, a_star, r)
    
    # Check outputs are finite
    assert math.isfinite(Omega_LT), f"Omega_LT should be finite, got {Omega_LT}"
    assert math.isfinite(f_LT), f"f_LT should be finite, got {f_LT}"
    assert math.isfinite(T_precess), f"T_precess should be finite, got {T_precess}"
    
    # Check signs (Omega_LT should be positive for prograde orbit)
    assert Omega_LT > 0.0, f"Omega_LT should be positive, got {Omega_LT}"
    assert f_LT > 0.0, f"f_LT should be positive, got {f_LT}"
    assert T_precess > 0.0, f"T_precess should be positive, got {T_precess}"


def test_lense_thirring_omega_scaling():
    """Test that precession frequency scales correctly with distance."""
    M_solar = 10.0
    a_star = 0.5
    
    # Closer distance should give higher precession frequency
    Omega_LT_10, _, _ = lense_thirring_omega(M_solar, a_star, 10.0)
    Omega_LT_100, _, _ = lense_thirring_omega(M_solar, a_star, 100.0)
    
    assert Omega_LT_10 > Omega_LT_100, \
        f"Closer orbit should precess faster: {Omega_LT_10} vs {Omega_LT_100}"


def test_lense_thirring_omega_spin_dependence():
    """Test that precession frequency depends on spin."""
    M_solar = 10.0
    r = 10.0
    
    Omega_LT_0, _, _ = lense_thirring_omega(M_solar, 0.0, r)
    Omega_LT_099, _, _ = lense_thirring_omega(M_solar, 0.99, r)
    
    # Higher spin should give higher precession frequency
    assert Omega_LT_099 > Omega_LT_0, \
        f"Higher spin should give higher precession: {Omega_LT_099} vs {Omega_LT_0}"


def test_lense_thirring_omega_mass_scaling():
    """Test that precession frequency scales with mass."""
    a_star = 0.5
    r = 10.0
    
    Omega_LT_10, _, _ = lense_thirring_omega(10.0, a_star, r)
    Omega_LT_100, _, _ = lense_thirring_omega(100.0, a_star, r)
    
    # More massive BH gives LOWER precession frequency (Omega_LT ∝ 1/M)
    assert Omega_LT_100 < Omega_LT_10, \
        f"More massive BH should give lower precession: {Omega_LT_100} vs {Omega_LT_10}"


def test_precession_period_reasonableness():
    """Test that precession period is reasonable for astrophysical BH."""
    # For M = 1e6 M_sun (SMBH), a* = 0.9, r = 10 r_s
    M_solar = 1e6
    a_star = 0.9
    r = 10.0
    
    _, _, T_precess = lense_thirring_omega(M_solar, a_star, r)
    
    # Period should be positive and finite
    assert T_precess > 0.0, f"T_precess should be positive, got {T_precess}"
    # For SMBH, period could be years to centuries
    assert T_precess < 1e20, f"T_precess suspiciously large: {T_precess}"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
