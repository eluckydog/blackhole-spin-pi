"""
Unit tests for code/hawking_radiation.py
Fixed unit issues: functions expect M in kg, not solar masses.
"""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from hawking_radiation import (
    schwarzschild_horizon,
    kerr_horizon,
    hawking_temperature,
    evaporation_power,
    evaporation_time,
)


def test_schwarzschild_horizon():
    """Test Schwarzschild horizon radius."""
    M_kg = 10.0 * 1.98847e30  # 10 solar masses in kg
    r_s = schwarzschild_horizon(M_kg)
    
    # r_s = 2GM/c^2
    expected = 2.0 * 6.67430e-11 * M_kg / (299792458.0**2)
    
    assert abs(r_s - expected) < 1e-10, f"Expected {expected}, got {r_s}"


def test_kerr_horizon_non_spinning():
    """Test Kerr horizon for non-spinning case (should match Schwarzschild)."""
    M_kg = 10.0 * 1.98847e30
    a_star = 0.0
    
    r_plus, r_minus = kerr_horizon(M_kg, a_star)
    
    # For a*=0, r_plus = 2GM/c^2 (Schwarzschild)
    expected_r_plus = 2.0 * 6.67430e-11 * M_kg / (299792458.0**2)
    
    assert r_plus is not None, "r_plus should not be None for a*=0"
    assert abs(r_plus - expected_r_plus) < 1e-10, f"Expected {expected_r_plus}, got {r_plus}"
    assert r_minus is not None, "r_minus should not be None for a*=0"
    assert abs(r_minus - 0.0) < 1e-10, f"Expected r_minus=0, got {r_minus}"


def test_kerr_horizon_extreme():
    """Test Kerr horizon for extreme spin (a*=1)."""
    M_kg = 10.0 * 1.98847e30
    a_star = 1.0
    
    r_plus, r_minus = kerr_horizon(M_kg, a_star)
    
    # For a*=1, r_plus = GM/c^2 (half of Schwarzschild)
    expected_r_plus = 6.67430e-11 * M_kg / (299792458.0**2)
    
    assert r_plus is not None
    assert abs(r_plus - expected_r_plus) < 1e-10, f"Expected {expected_r_plus}, got {r_plus}"


def test_hawking_temperature_schwarzschild():
    """Test Hawking temperature for Schwarzschild black hole."""
    M_kg = 10.0 * 1.98847e30  # 10 solar masses in kg
    a_star = 0.0
    
    T = hawking_temperature(M_kg, a_star)
    
    # T = ħ c^3 / (8π G M k_B)
    expected = (1.054571817e-34 * 299792458.0**3) / (8.0 * math.pi * 6.67430e-11 * M_kg * 1.380649e-23)
    
    assert abs(T - expected) / expected < 1e-6, f"Expected {expected}, got {T}"


def test_hawking_temperature_decreases_with_mass():
    """Test that Hawking temperature decreases as mass increases."""
    T_1 = hawking_temperature(1.0 * 1.98847e30, 0.0)   # 1 solar mass
    T_10 = hawking_temperature(10.0 * 1.98847e30, 0.0)  # 10 solar masses
    
    assert T_1 > T_10, "Temperature should decrease with mass"


def test_hawking_evaporation_power():
    """Test Hawking evaporation power (should be very small for stellar-mass BH)."""
    M_kg = 10.0 * 1.98847e30
    a_star = 0.0
    
    T = hawking_temperature(M_kg, a_star)
    P = evaporation_power(M_kg, T)
    
    # Power should be positive and very small
    assert P > 0.0, "Evaporation power should be positive"
    assert P < 1e10, "Evaporation power should be very small for stellar-mass BH"


def test_hawking_lifetime():
    """Test Hawking evaporation lifetime (should be very long for stellar-mass BH)."""
    M_kg = 10.0 * 1.98847e30
    a_star = 0.0
    
    T = hawking_temperature(M_kg, a_star)
    tau = evaporation_time(M_kg, T)
    
    # Lifetime should be positive and very long
    assert tau > 0.0, "Lifetime should be positive"
    assert tau > 1e60, "Lifetime should be very long for stellar-mass BH (>> age of universe)"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
