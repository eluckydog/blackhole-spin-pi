#!/usr/bin/env python3
"""
Hawking Radiation Calculator

Computes Hawking temperature and evaporation power for Schwarzschild/Kerr black holes.
T = ħc³/(8ΠGMk_B)  (Schwarzschild)
T = ħc³(r₊ - r_-) / [4Πk_B G M (r₊² + a²)]  (Kerr)
"""

import argparse
import math


# Physical constants (SI units)
hbar = 1.054571817e-34  # J·s (reduced Planck constant)
c = 299792458.0  # m/s (speed of light)
G = 6.67430e-11  # m³/(kg·s²) (gravitational constant)
k_B = 1.380649e-23  # J/K (Boltzmann constant)
sigma = 5.670374419e-8  # W/(m²·K⁴) (Stefan-Boltzmann constant)
M_sun = 1.98847e30  # kg (solar mass)


def schwarzschild_horizon(M):
    """Event horizon radius for Schwarzschild black hole."""
    return 2.0 * G * M / c**2


def kerr_horizon(M, a):
    """Inner and outer horizon radii for Kerr black hole."""
    M_geo = G * M / c**2  # Convert M to geometric length (meters)
    a_geo = a  # a is already in meters (J/M = kg·m²/s / kg = m²/s)
    # Actually, a = J/M (dimensionless spin parameter a* times M)
    # Let me use dimensionless a* = J/M²
    # Then a_geo = a_star * G * M / c²
    a_geo = a * G * M / c**2
    
    discriminant = M_geo**2 - a_geo**2
    if discriminant < 0:
        return None, None  # Extremal or naked singularity
    
    r_plus = M_geo + math.sqrt(discriminant)  # Outer horizon
    r_minus = M_geo - math.sqrt(discriminant)  # Inner horizon
    
    return r_plus, r_minus


def hawking_temperature(M, a_star=0.0):
    """
    Compute Hawking temperature.
    
    Parameters:
    -----------
    M : float
        Black hole mass (kg)
    a_star : float
        Dimensionless spin parameter (0 <= a_star <= 1)
    
    Returns:
    --------
    T : float
        Temperature (Kelvin)
    """
    if a_star == 0.0:
        # Schwarzschild
        T = hbar * c**3 / (8.0 * math.pi * G * M * k_B)
    else:
        # Kerr (approximate formula)
        M_geo = G * M / c**2
        a_geo = a_star * M_geo
        
        r_plus, r_minus = kerr_horizon(M, a_star)
        if r_plus is None:
            return None
        
        numerator = hbar * c**3 * (r_plus - r_minus)
        denominator = 4.0 * math.pi * k_B * G * M * (r_plus**2 + a_geo**2)
        
        T = numerator / denominator
    
    return T


def evaporation_power(M, T):
    """
    Compute Hawking radiation power (Stefan-Boltzmann).
    
    P = σ A T⁴
    
    Parameters:
    -----------
    M : float
        Black hole mass (kg)
    T : float
        Temperature (Kelvin)
    
    Returns:
    --------
    P : float
        Power (Watts)
    """
    # Horizon area (Schwarzschild approximation)
    r_s = 2.0 * G * M / c**2
    A = 4.0 * math.pi * r_s**2
    
    # Power
    P = sigma * A * T**4
    
    return P


def evaporation_time(M, T):
    """
    Compute evaporation time (approximate).
    
    τ ∝ M³  (from dM/dt ∝ -1/M²)
    
    Parameters:
    -----------
    M : float
        Black hole mass (kg)
    T : float
        Temperature (Kelvin)
    
    Returns:
    --------
    tau : float
        Evaporation time (seconds)
    """
    # Approximation: τ ≈ 5120Π G² M³ / (ħ c⁴)
    tau = 5120.0 * math.pi * G**2 * M**3 / (hbar * c**4)
    return tau


def main():
    parser = argparse.ArgumentParser(
        description="Hawking Radiation Calculator"
    )
    parser.add_argument(
        "--mass", type=float, default=1.0,
        help="Black hole mass (solar masses, default: 1.0)"
    )
    parser.add_argument(
        "--spin", type=float, default=0.0,
        help="Dimensionless spin parameter a* (0 <= a* <= 1, default: 0.0)"
    )
    parser.add_argument(
        "--scan", action="store_true",
        help="Scan mass from 10¹² kg to 10³⁰ kg, plot T and τ"
    )
    
    args = parser.parse_args()
    
    if args.scan:
        # Scan mass
        import numpy as np
        import matplotlib.pyplot as plt
        
        masses = np.logspace(12, 30, 100)  # 10¹² to 10³⁰ kg
        temperatures = []
        lifetimes = []
        
        for M in masses:
            T = hawking_temperature(M, args.spin)
            tau = evaporation_time(M, T)
            temperatures.append(T)
            lifetimes.append(tau)
        
        # Convert to numpy arrays for plotting
        temperatures = np.array(temperatures)
        lifetimes = np.array(lifetimes)
        
        # Plot 1: Temperature vs Mass
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        ax1.loglog(masses / M_sun, temperatures, "b-", linewidth=2)
        ax1.set_xlabel("Mass (M☉)", fontsize=12)
        ax1.set_ylabel("Temperature (K)", fontsize=12)
        ax1.set_title("Hawking Temperature vs. Mass", fontsize=14)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Lifetime vs Mass
        ax2.loglog(masses / M_sun, lifetimes / (365.25 * 24 * 3600), "r-", linewidth=2)
        ax2.set_xlabel("Mass (M☉)", fontsize=12)
        ax2.set_ylabel("Lifetime (years)", fontsize=12)
        ax2.set_title("Evaporation Time vs. Mass", fontsize=14)
        ax2.grid(True, alpha=0.3)
        
        # Mark primordial black hole (M ~ 10¹² kg)
        ax2.axvline(x=10**12 / M_sun, color="g", linestyle="--", label="Primordial BH")
        
        plt.tight_layout()
        plt.savefig("hawking_radiation.png", dpi=150)
        print(f"Plot saved: hawking_radiation.png")
        
    else:
        # Single calculation
        M_kg = args.mass * M_sun
        T = hawking_temperature(M_kg, args.spin)
        
        if T is None:
            print("Error: Invalid spin parameter (extremal or naked singularity)")
            return
        
        P = evaporation_power(M_kg, T)
        tau = evaporation_time(M_kg, T)
        
        print("=" * 60)
        print("Hawking Radiation Calculator")
        print("=" * 60)
        print(f"Mass M = {args.mass:.4f} M☉ = {M_kg:.4e} kg")
        print(f"Spin a* = {args.spin:.4f}")
        print(f"Temperature T = {T:.4e} K")
        print(f"Power P = {P:.4e} W")
        print(f"Evaporation time τ = {tau:.4e} s")
        print(f"                  = {tau / (365.25 * 24 * 3600):.4e} years")
        print("=" * 60)
        
        # Compare to solar mass black hole
        T_sun = hawking_temperature(M_sun, 0.0)
        print(f"\nComparison to solar mass (M = M☉, a* = 0):")
        print(f"  T☉ = {T_sun:.4e} K")
        print(f"  T / T☉ = {T / T_sun:.4f}")
        print("=" * 60)


if __name__ == "__main__":
    main()
