#!/usr/bin/env python3
"""
Black Hole Shadow Calculator

Calculates shadow angular diameter for Kerr black holes.
Uses Schwarzschild approximation (r_shadow = sqrt(27) * G*M/c^2).
"""

import argparse
import math
import json
import os
import sys


# Constants
M_sun = 1.9885e30  # kg
G = 6.67430e-11    # m³/(kg·s²)
c = 299792458.0      # m/s

# Micro-arcsecond conversion
muas_per_rad = 180.0 * 3600.0 * 1e6 / math.pi  # μas/rad


def shadow_radius(M_kg, a_star=0.0, theta_o=0.0):
    """
    Calculate shadow radius (Schwarzschild approximation).
    
    Parameters:
    -----------
    M_kg : float
        Black hole mass (kg)
    a_star : float
        Dimensionless spin parameter (default: 0.0 = Schwarzschild)
    theta_o : float
        Observer viewing angle (radians, default: 0.0 = face-on)
    
    Returns:
    --------
    r_shadow : float
        Shadow radius (meters)
    """
    # Schwarzschild approximation (no spin correction)
    # r_shadow = sqrt(27) * G*M/c^2
    r_g = G * M_kg / c**2  # gravitational radius (meters)
    r_shadow = math.sqrt(27.0) * r_g
    
    # Spin correction (face-on approximation from EHT 2019)
    # For a* > 0, shadow shrinks slightly
    if a_star > 0.0 and theta_o == 0.0:
        # Empirical correction (from EHT papers)
        # Shadow radius decreases with a*
        correction = 1.0 - 0.1 * a_star  # Approximate
        r_shadow *= correction
    
    return r_shadow


def angular_diameter(r_shadow, D_m):
    """
    Calculate angular diameter (μas).
    
    Parameters:
    -----------
    r_shadow : float
        Shadow radius (meters)
    D_m : float
        Distance to observer (meters)
    
    Returns:
    --------
    theta_muas : float
        Angular diameter (micro-arcseconds)
    """
    # Angular radius (rad)
    theta_rad = r_shadow / D_m
    
    # Convert to micro-arcseconds
    theta_muas = 2.0 * theta_rad * muas_per_rad  # diameter
    
    return theta_muas


def compare_with_eht(M_solar, a_star, D_Mpc, name="M87*"):
    """
    Compare calculation with EHT observation.
    
    Parameters:
    -----------
    M_solar : float
        Black hole mass (solar masses)
    a_star : float
        Dimensionless spin parameter
    D_Mpc : float
        Distance (Mpc)
    name : str
        Black hole name (for output)
    
    Returns:
    --------
    result : dict
        Comparison result
    """
    # Convert to SI
    M_kg = M_solar * M_sun
    D_m = D_Mpc * 3.086e22  # Mpc to meters
    
    # Calculate shadow radius
    r_shadow = shadow_radius(M_kg, a_star, theta_o=0.0)
    
    # Calculate angular diameter
    theta_calc = angular_diameter(r_shadow, D_m)
    
    # EHT observed values
    if "M87" in name:
        theta_obs = 42.0  # μas
        theta_err = 3.0
    elif "Sgr" in name:
        theta_obs = 48.0  # μas
        theta_err = 7.0
    else:
        theta_obs = None
        theta_err = None
    
    # Result
    result = {
        "name": name,
        "M_solar": M_solar,
        "a_star": a_star,
        "D_Mpc": D_Mpc,
        "r_shadow_m": r_shadow,
        "theta_calc_muas": theta_calc,
        "theta_obs_muas": theta_obs,
        "theta_obs_err": theta_err
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Black Hole Shadow Calculator"
    )
    parser.add_argument(
        "--mass", type=float, default=6.5e9,
        help="Black hole mass (solar masses, default: 6.5e9 = M87*)"
    )
    parser.add_argument(
        "--spin", type=float, default=0.9,
        help="Dimensionless spin parameter a* (0 <= a* <= 1, default: 0.9)"
    )
    parser.add_argument(
        "--distance", type=float, default=16.8,
        help="Distance (Mpc, default: 16.8 = M87*)"
    )
    parser.add_argument(
        "--viewing-angle", type=float, default=0.0,
        help="Viewing angle (degrees, 0=face-on, 90=edge-on, default: 0.0)"
    )
    parser.add_argument(
        "--compare-eht", action="store_true",
        help="Compare with EHT observations (M87* and Sgr A*)"
    )
    
    args = parser.parse_args()
    
    if args.compare_eht:
        # Compare with EHT data
        print("=" * 80)
        print("Black Hole Shadow — Comparison with EHT Observations")
        print("=" * 80)
        
        # M87*
        print("\n1. M87* (EHT 2019):")
        res_m87 = compare_with_eht(
            M_solar=6.5e9,
            a_star=0.9,
            D_Mpc=16.8,
            name="M87*"
        )
        print(f"   Mass M = {res_m87['M_solar']:.1e} M_sun")
        print(f"   Spin a* = {res_m87['a_star']:.2f}")
        print(f"   Distance D = {res_m87['D_Mpc']:.1f} Mpc")
        print(f"   Calculated shadow radius r_shadow = {res_m87['r_shadow_m']:.2e} m")
        print(f"   Calculated angular diameter θ = {res_m87['theta_calc_muas']:.2f} μas")
        print(f"   EHT observed θ = {res_m87['theta_obs_muas']:.2f} ± {res_m87['theta_obs_err']:.2f} μas")
        if res_m87['theta_obs_muas']:
            diff = res_m87['theta_calc_muas'] - res_m87['theta_obs_muas']
            print(f"   Difference = {diff:.2f} μas")
        
        # Sgr A*
        print("\n2. Sgr A* (EHT 2022):")
        res_sgr = compare_with_eht(
            M_solar=4.3e6,
            a_star=0.5,
            D_Mpc=8.2e-3,  # 8.2 kpc = 8.2e-3 Mpc
            name="Sgr A*"
        )
        print(f"   Mass M = {res_sgr['M_solar']:.1e} M_sun")
        print(f"   Spin a* = {res_sgr['a_star']:.2f}")
        print(f"   Distance D = {res_sgr['D_Mpc']:.4f} Mpc")
        print(f"   Calculated shadow radius r_shadow = {res_sgr['r_shadow_m']:.2e} m")
        print(f"   Calculated angular diameter θ = {res_sgr['theta_calc_muas']:.2f} μas")
        print(f"   EHT observed θ = {res_sgr['theta_obs_muas']:.2f} ± {res_sgr['theta_obs_err']:.2f} μas")
        if res_sgr['theta_obs_muas']:
            diff = res_sgr['theta_calc_muas'] - res_sgr['theta_obs_muas']
            print(f"   Difference = {diff:.2f} μas")
        
        print("\n" + "=" * 80)
        
    else:
        # Single calculation
        M_kg = args.mass * M_sun
        D_m = args.distance * 3.086e22  # Mpc to meters
        theta_o = math.radians(args.viewing_angle)
        
        r_shadow = shadow_radius(M_kg, args.spin, theta_o)
        theta = angular_diameter(r_shadow, D_m)
        
        print("=" * 80)
        print("Black Hole Shadow Calculator")
        print("=" * 80)
        print(f"Mass M = {args.mass:.2e} M_sun")
        print(f"Spin a* = {args.spin:.2f}")
        print(f"Distance D = {args.distance:.2f} Mpc")
        print(f"Viewing angle = {args.viewing_angle:.2f} deg")
        print("-" * 80)
        print(f"Shadow radius r_shadow = {r_shadow:.2e} m")
        print(f"Angular diameter θ = {theta:.2f} μas")
        print("-" * 80)
        print("=" * 80)


if __name__ == "__main__":
    main()
