#!/usr/bin/env python3
"""
Spin Precession Calculator (Lense-Thirring Effect)

Computes frame-dragging precession near a rotating black hole.
Ω_LT = 2GJ/(c²r³)  (for equatorial orbit)
ϕ(t) = Ω_LT · t
One full cycle: ϕ = 2Π
"""

import argparse
import math


# Physical constants (SI units)
G = 6.67430e-11  # m³/(kg·s²) (gravitational constant)
c = 299792458.0  # m/s (speed of light)


def lense_thirring_omega(M, a_star, r):
    """
    Compute Lense-Thirring precession frequency.
    
    Parameters:
    -----------
    M : float
        Black hole mass (solar masses)
    a_star : float
        Dimensionless spin parameter (0 <= a_star <= 1)
    r : float
        Distance from black hole (Schwarzschild radii, r_s = 2GM/c²)
    
    Returns:
    --------
    Omega_LT : float
        Precession frequency (rad/s)
    f_LT : float
        Precession frequency (Hz)
    T_precess : float
        Precession period (seconds)
    """
    # Convert M to kg
    M_kg = M * 1.98847e30
    
    # Spin parameter J = a* · G M² / c
    J = a_star * G * M_kg**2 / c**2  # kg·m²/s
    
    # Schwarzschild radius
    r_s = 2.0 * G * M_kg / c**2  # meters
    
    # Distance in meters
    r_m = r * r_s
    
    # Lense-Thirring frequency (rad/s)
    Omega_LT = 2.0 * G * J / (c**2 * r_m**3)
    
    # Convert to Hz
    f_LT = Omega_LT / (2.0 * math.pi)
    
    # Precession period (seconds)
    T_precess = 2.0 * math.pi / Omega_LT if Omega_LT > 0 else float("inf")
    
    return Omega_LT, f_LT, T_precess


def precession_phase(Omega_LT, t):
    """
    Compute precession phase at time t.
    
    Parameters:
    -----------
    Omega_LT : float
        Precession frequency (rad/s)
    t : float
        Time (seconds)
    
    Returns:
    --------
    phi : float
        Phase (radians, modulo 2Π)
    """
    phi = Omega_LT * t
    phi_mod = phi % (2.0 * math.pi)  # Wrap to [0, 2Π)
    return phi_mod


def main():
    parser = argparse.ArgumentParser(
        description="Spin Precession Calculator (Lense-Thirring Effect)"
    )
    parser.add_argument(
        "--mass", type=float, default=1.0,
        help="Black hole mass (M☉, default: 1.0)"
    )
    parser.add_argument(
        "--spin", type=float, default=0.5,
        help="Dimensionless spin parameter a* (0 <= a* <= 1, default: 0.5)"
    )
    parser.add_argument(
        "--radius", type=float, default=10.0,
        help="Distance from BH (Schwarzschild radii, default: 10.0)"
    )
    parser.add_argument(
        "--time", type=float, default=1.0,
        help="Time for phase calculation (years, default: 1.0)"
    )
    parser.add_argument(
        "--scan", action="store_true",
        help="Scan radius from 3 to 100 r_s, plot Ω_LT vs r"
    )
    
    args = parser.parse_args()
    
    if args.scan:
        # Scan radius
        import numpy as np
        import matplotlib.pyplot as plt
        
        radii = np.linspace(3, 100, 500)  # r / r_s
        omegas = []
        periods = []
        
        for r in radii:
            Omega, f, T = lense_thirring_omega(args.mass, args.spin, r)
            omegas.append(Omega)
            periods.append(T)
        
        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        ax1.loglog(radii, omegas, "b-", linewidth=2)
        ax1.set_xlabel("Radius (r / r_s)", fontsize=12)
        ax1.set_ylabel("Ω_LT (rad/s)", fontsize=12)
        ax1.set_title("Lense-Thirring Frequency vs. Radius", fontsize=14)
        ax1.grid(True, alpha=0.3)
        
        ax2.loglog(radii, periods, "r-", linewidth=2)
        ax2.set_xlabel("Radius (r / r_s)", fontsize=12)
        ax2.set_ylabel("T_precess (seconds)", fontsize=12)
        ax2.set_title("Precession Period vs. Radius", fontsize=14)
        ax2.grid(True, alpha=0.3)
        
        # Mark ISCO (innermost stable circular orbit)
        # For Kerr (prograde), ISCO = 1 + sqrt(3) approx 2.73 r_s
        ax1.axvline(x=2.73, color="g", linestyle="--", label="ISCO (approx)")
        ax2.axvline(x=2.73, color="g", linestyle="--", label="ISCO (approx)")
        
        plt.tight_layout()
        plt.savefig("spin_precession.png", dpi=150)
        print(f"Plot saved: spin_precession.png")
        
    else:
        # Single calculation
        Omega, f, T = lense_thirring_omega(
            args.mass, args.spin, args.radius
        )
        
        # Phase at given time
        t_seconds = args.time * 365.25 * 24 * 3600  # years to seconds
        phi = precession_phase(Omega, t_seconds)
        
        print("=" * 60)
        print("Spin Precession Calculator (Lense-Thirring Effect)")
        print("=" * 60)
        print(f"Black hole mass M = {args.mass:.2f} M_sun")
        print(f"Spin parameter a* = {args.spin:.2f}")
        print(f"Distance r = {args.radius:.2f} r_s")
        print("-" * 60)
        print(f"Omega_LT = {Omega:.4e} rad/s")
        print(f"       = {f:.4e} Hz")
        print(f"T_precess = 2*pi/Omega_LT = {T:.4e} s")
        print(f"               = {T / (365.25 * 24 * 3600):.4e} years")
        print("-" * 60)
        print(f"Phase after {args.time:.2f} years:")
        print(f"  phi = {phi:.4f} rad")
        print(f"  phi / pi = {phi / math.pi:.4f} pi")
        print(f"  Progress: {phi / (2.0 * math.pi) * 100:.2f}% of full cycle")
        print("=" * 60)
        
        # Compare to Gravity Probe B (Earth)
        print("\nComparison to Gravity Probe B (Earth):")
        Omega_Earth, f_Earth, T_Earth = lense_thirring_omega(
            1.0e-9, 0.0, 642.0  # Earth mass ~ 1e-9 M☉, r ~ 642 km
        )
        # Actually, let me use correct Earth values:
        # M_Earth = 5.972e24 kg ~ 3e-6 M_sun
        # J_Earth = 5.86e33 kg*m^2/s
        # r_orbit = 642 km
        M_Earth = 5.972e24  # kg
        J_Earth = 5.86e33  # kg·m²/s (actual value)
        r_orbit = 642e3  # meters
        
        Omega_GPB = 2.0 * G * J_Earth / (c**2 * r_orbit**3)
        f_GPB = Omega_GPB / (2.0 * math.pi)
        T_GPB = 2.0 * math.pi / Omega_GPB
        
        print(f"  Omega_LT (Earth) = {Omega_GPB:.4e} rad/s")
        print(f"  T_precess (Earth) = {T_GPB / (365.25 * 24 * 3600):.2f} years")
        print(f"  (Gravity Probe B measured ~ 0.039 arcsec/yr)")
        print("=" * 60)


if __name__ == "__main__":
    main()
