#!/usr/bin/env python3
"""
Quasi-Normal Mode (QNM) Calculator

Computes QNM frequencies for Kerr black holes.
Uses fitting formulas from the literature (Echeverria 1989, etc.)

ω = ω_R + i·ω_I
T_osc = 2Π / ω_R
τ = 2Π / |ω_I|
"""

import argparse
import math
import numpy as np


# Fundamental QNM frequency for Schwarzschild (l=m=2, n=0)
# From Echeverria (1989), Table I
W_R_SCHW = 1.525  # rad/s (in units of c³/GM)
W_I_SCHW = -1.1566  # rad/s (in units of c³/GM)


def qnm_frequency_kerr(M, a_star, l=2, m=2, n=0):
    """
    Compute QNM frequency for Kerr black hole.
    
    Uses approximate fitting formula:
    ω_R(M, a*) ≈ ω_R(0) + Δω_R(a*)
    ω_I(M, a*) ≈ ω_I(0) + Δω_I(a*)
    
    Parameters:
    -----------
    M : float
        Black hole mass (solar masses)
    a_star : float
        Dimensionless spin parameter (0 <= a_star <= 1)
    l, m : int
        Angular harmonic indices (default: l=m=2)
    n : int
        Overtone index (default: n=0, fundamental)
    
    Returns:
    --------
    w_R : float
        Real part (oscillation frequency) in Hz
    w_I : float
        Imaginary part (damping rate) in Hz
    T_osc : float
        Oscillation period (seconds)
    tau : float
        Damping time (seconds)
    """
    # Convert M to kg
    M_kg = M * 1.98847e30
    
    # Constants
    G = 6.67430e-11  # m³/(kg·s²)
    c = 299792458.0  # m/s
    
    # Geometric factor (c³/GM)
    factor = c**3 / (G * M_kg)  # rad/s
    
    # Fitting formula for Kerr (simplified)
    # From Leaver (1985), see 
    # For l=m=2, n=0:
    if l == 2 and m == 2 and n == 0:
        # Real part (oscillation frequency)
        # W_R(a*) = W_R(0) * (1 + 0.1 * a_star + 0.2 * a_star²)
        w_R_geo = W_R_SCHW * (1.0 + 0.1 * a_star + 0.2 * a_star**2)
        
        # Imaginary part (damping rate)
        # W_I(a*) = W_I(0) * (1 + 0.15 * a_star + 0.3 * a_star²)
        w_I_geo = W_I_SCHW * (1.0 + 0.15 * a_star + 0.3 * a_star**2)
    else:
        # Generic (use Schwarzschild as approximation)
        w_R_geo = W_R_SCHW
        w_I_geo = W_I_SCHW
    
    # Convert to physical units (Hz)
    w_R_Hz = w_R_geo * factor / (2.0 * math.pi)  # Hz (f = ω/2Π)
    w_I_Hz = w_I_geo * factor / (2.0 * math.pi)  # Hz
    
    # Oscillation period and damping time
    T_osc = 2.0 * math.pi / (w_R_geo * factor)  # seconds
    tau = 2.0 * math.pi / abs(w_I_geo * factor)  # seconds
    
    return w_R_Hz, w_I_Hz, T_osc, tau


def main():
    parser = argparse.ArgumentParser(
        description="Quasi-Normal Mode (QNM) Calculator"
    )
    parser.add_argument(
        "--mass", type=float, default=62.0,
        help="Black hole mass (M☉, default: 62.0, GW150914 final mass)"
    )
    parser.add_argument(
        "--spin", type=float, default=0.67,
        help="Dimensionless spin parameter a* (0 <= a* <= 1, default: 0.67)"
    )
    parser.add_argument(
        "--mode", type=str, default="220",
        help="QNM mode (format: lmn, e.g., '220' = l=2,m=2,n=0, default: '220')"
    )
    parser.add_argument(
        "--scan", action="store_true",
        help="Scan spin from 0 to 0.99, plot ω_R and |ω_I| vs a*"
    )
    
    args = parser.parse_args()
    
    # Parse mode
    if len(args.mode) == 3:
        l = int(args.mode[0])
        m = int(args.mode[1])
        n = int(args.mode[2])
    else:
        l, m, n = 2, 2, 0  # Default: (2,2,0)
    
    if args.scan:
        # Scan spin parameter
        import matplotlib.pyplot as plt
        
        a_stars = np.linspace(0, 0.99, 100)
        w_Rs = []
        w_Is = []
        
        for a in a_stars:
            w_R, w_I, _, _ = qnm_frequency_kerr(args.mass, a, l, m, n)
            w_Rs.append(w_R)
            w_Is.append(abs(w_I))
        
        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        ax1.plot(a_stars, w_Rs, "b-", linewidth=2)
        ax1.set_xlabel("Dimensionless spin a*", fontsize=12)
        ax1.set_ylabel("ω_R (Hz)", fontsize=12)
        ax1.set_title(f"QNM oscillation frequency (l={l},m={m},n={n})", fontsize=14)
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(a_stars, w_Is, "r-", linewidth=2)
        ax2.set_xlabel("Dimensionless spin a*", fontsize=12)
        ax2.set_ylabel("|ω_I| (Hz)", fontsize=12)
        ax2.set_title(f"QNM damping rate (l={l},m={m},n={n})", fontsize=14)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig("qnm_frequency.png", dpi=150)
        print(f"Plot saved: qnm_frequency.png")
        
    else:
        # Single calculation
        w_R, w_I, T_osc, tau = qnm_frequency_kerr(
            args.mass, args.spin, l, m, n
        )
        
        print("=" * 60)
        print("Quasi-Normal Mode (QNM) Calculator")
        print("=" * 60)
        print(f"Mass M = {args.mass:.2f} M☉")
        print(f"Spin a* = {args.spin:.2f}")
        print(f"Mode (l,m,n) = ({l},{m},{n})")
        print("-" * 60)
        print(f"ω_R = {w_R:.4f} Hz  (oscillation frequency)")
        print(f"ω_I = {w_I:.4f} Hz  (damping rate)")
        print(f"T_osc = 2Π/ω_R = {T_osc:.6f} s  (oscillation period)")
        print(f"τ = 2Π/|ω_I| = {tau:.6f} s  (damping time)")
        print("-" * 60)
        
        # Quality factor
        Q = w_R * T_osc / (2.0 * math.pi)  # Q = ω_R / (2|ω_I|)
        Q_alt = abs(w_R / (2.0 * w_I))
        print(f"Quality factor Q = {Q_alt:.2f}")
        print(f"  (Q > 1 means underdamped oscillation)")
        print("=" * 60)
        
        # Compare to GW150914
        if args.mass == 62.0 and abs(args.spin - 0.67) < 0.01:
            print("\nComparison to GW150914 (LIGO first detection):")
            print(f"  Final mass = 62 M☉, spin = 0.67")
            print(f"  Observed ringdown frequency ~ 235 Hz")
            print(f"  This calculation: ω_R = {w_R:.1f} Hz")
            print(f"  (Fitting formula approximation)")


if __name__ == "__main__":
    main()
