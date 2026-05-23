"""
Unit tests for code/kerr_horizon.py
"""

import sys
import os
import math

# Add parent directory to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from kerr_horizon import kerr_horizon_area


def test_schwarzschild_horizon_area():
    """Test horizon area for non-spinning black hole (a*=0)."""
    M = 1.0
    a_star = 0.0
    A, r_outer = kerr_horizon_area(M, a_star)
    
    # For a*=0: r_outer = M + sqrt(M^2 - 0) = 2M
    # A = 8π M r_outer = 8π M * 2M = 16π M^2
    expected_A = 16.0 * math.pi * M**2
    expected_r = 2.0 * M
    
    assert abs(A - expected_A) < 1e-10, f"Expected A={expected_A}, got {A}"
    assert abs(r_outer - expected_r) < 1e-10, f"Expected r_outer={expected_r}, got {r_outer}"


def test_kerr_horizon_area_spin():
    """Test horizon area for spinning black hole (a*=0.5)."""
    M = 1.0
    a_star = 0.5
    A, r_outer = kerr_horizon_area(M, a_star)
    
    # r_outer = M + sqrt(M^2 - (a_star*M)^2) = 1 + sqrt(1 - 0.25) = 1 + sqrt(0.75)
    expected_r = 1.0 + math.sqrt(1.0 - 0.25)
    expected_A = 8.0 * math.pi * M * expected_r
    
    assert abs(r_outer - expected_r) < 1e-10, f"Expected r_outer={expected_r}, got {r_outer}"
    assert abs(A - expected_A) < 1e-10, f"Expected A={expected_A}, got {A}"


def test_extreme_kerr_horizon():
    """Test horizon area for extreme Kerr black hole (a*=1)."""
    M = 1.0
    a_star = 1.0
    A, r_outer = kerr_horizon_area(M, a_star)
    
    # For a*=1: r_outer = M + sqrt(M^2 - M^2) = M
    expected_r = M
    expected_A = 8.0 * math.pi * M * expected_r
    
    assert abs(r_outer - expected_r) < 1e-10, f"Expected r_outer={expected_r}, got {r_outer}"
    assert abs(A - expected_A) < 1e-10, f"Expected A={expected_A}, got {A}"


def test_horizon_area_decreases_with_spin():
    """Test that horizon area decreases as spin increases."""
    M = 1.0
    areas = []
    for a_star in [0.0, 0.5, 0.8, 0.99]:
        A, _ = kerr_horizon_area(M, a_star)
        areas.append(A)
    
    # Check that area decreases monotonically
    for i in range(len(areas) - 1):
        assert areas[i] > areas[i+1], f"Area should decrease with spin: {areas[i]} <= {areas[i+1]}"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
