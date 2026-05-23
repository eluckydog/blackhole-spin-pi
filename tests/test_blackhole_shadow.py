"""
Unit tests for code/blackhole_shadow.py
"""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from blackhole_shadow import shadow_radius, angular_diameter, compare_with_eht


def test_shadow_radius_schwarzschild():
    """Test shadow radius for non-spinning black hole (a*=0)."""
    M_kg = 10.0 * 1.9885e30  # 10 solar masses in kg
    a_star = 0.0
    
    r_shadow = shadow_radius(M_kg, a_star, theta_o=0.0)
    
    # Schwarzschild approximation: r_shadow = sqrt(27) * G*M/c^2
    expected = math.sqrt(27.0) * 6.67430e-11 * M_kg / (299792458.0**2)
    
    assert abs(r_shadow - expected) / expected < 1e-6, \
        f"Expected {expected}, got {r_shadow}"


def test_shadow_radius_spin_correction():
    """Test that spin correction reduces shadow radius."""
    M_kg = 6.5e9 * 1.9885e30  # M87* mass in kg
    
    r_nospin = shadow_radius(M_kg, 0.0, theta_o=0.0)
    r_spin = shadow_radius(M_kg, 0.9, theta_o=0.0)
    
    # Spin correction should reduce shadow radius (empirical)
    assert r_spin < r_nospin, \
        f"Spin correction should reduce shadow: {r_spin} >= {r_nospin}"


def test_angular_diameter_basic():
    """Test angular diameter calculation."""
    r_shadow = 1.0e13  # meters (approximate for SMBH)
    D_m = 16.8e6 * 3.086e16  # 16.8 Mpc to meters
    
    theta_muas = angular_diameter(r_shadow, D_m)
    
    # Should be positive and finite
    assert theta_muas > 0.0, f"Theta should be positive, got {theta_muas}"
    assert math.isfinite(theta_muas), f"Theta should be finite, got {theta_muas}"
    
    # Rough check: for M87*, theta ~ 40 μas
    # This is just a sanity check, not precise
    assert 1.0 < theta_muas < 1000.0, f"Theta out of range: {theta_muas}"


def test_angular_diameter_increases_with_shadow():
    """Test that angular diameter increases with shadow radius."""
    D_m = 1.0e20  # fixed distance
    
    theta_small = angular_diameter(1.0e12, D_m)
    theta_large = angular_diameter(2.0e12, D_m)
    
    assert theta_large > theta_small, \
        f"Larger shadow should give larger angular diameter: {theta_large} <= {theta_small}"


def test_angular_diameter_decreases_with_distance():
    """Test that angular diameter decreases with distance."""
    r_shadow = 1.0e13  # fixed shadow radius
    
    theta_near = angular_diameter(r_shadow, 1.0e20)
    theta_far = angular_diameter(r_shadow, 2.0e20)
    
    assert theta_far < theta_near, \
        f"Farther distance should give smaller angular diameter: {theta_far} >= {theta_near}"


def test_shadow_radius_order_of_magnitude():
    """Test that shadow radius is reasonable for astrophysical BH."""
    # M87*: M ~ 6.5e9 M_sun
    M_kg = 6.5e9 * 1.9885e30
    r_shadow = shadow_radius(M_kg, 0.0, theta_o=0.0)
    
    # r_shadow should be ~ sqrt(27) * G*M/c^2 ~ 10^13 m for SMBH
    assert 1.0e12 < r_shadow < 1.0e14, \
        f"Shadow radius out of range: {r_shadow}"


def test_compare_with_eht_m87():
    """Test compare_with_eht() for M87*."""
    result = compare_with_eht(
        M_solar=6.5e9,
        a_star=0.9,
        D_Mpc=16.8,
        name="M87*"
    )
    
    # Check result structure
    assert "name" in result
    assert "theta_calc_muas" in result
    assert "theta_obs_muas" in result
    
    # Check values are finite
    assert math.isfinite(result["theta_calc_muas"])
    assert result["theta_obs_muas"] == 42.0  # EHT observed


def test_compare_with_eht_sgr():
    """Test compare_with_eht() for Sgr A*."""
    result = compare_with_eht(
        M_solar=4.3e6,
        a_star=0.5,
        D_Mpc=8.2,
        name="Sgr A*"
    )
    
    assert result["name"] == "Sgr A*"
    assert result["theta_obs_muas"] == 48.0  # EHT observed


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
