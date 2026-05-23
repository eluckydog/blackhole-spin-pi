#!/usr/bin/env python3
"""
Quasi-Normal Mode (QNM) Calculator v2

Computes QNM frequencies for Kerr black holes.
Uses qnm package (v0.4.4) to solve Teukolsky equation.
"""

import argparse
import math
import numpy as np
import qnm


# Constants
M_sun = 1.9885e30  # kg
G = 6.67430e-11     # m³/(kg·s²)
c = 299792458.0       # m/s


def get_qnm_frequency(M_solar, a_star, l=2, m=2, n=0):
    """
    Get QNM frequency for Kerr black hole using qnm package.
    
    Parameters:
    -----------
    M_solar : float
        Black hole mass (solar masses)
    a_star : float
        Dimensionless spin parameter (0 <= a_star <= 1)
    l, m : int
        Angular harmonic indices (default: l=m=2)
    n : int
        Overtone index (default: n=0, fundamental)
    
    Returns:
    --------
    f_R : float
        Real part (oscillation frequency) in Hz
    f_I : float
        Imaginary part (damping rate) in Hz
    T_osc : float
        Oscillation period (seconds)
    tau : float
        Damping time (seconds)
    """
    # Get QNM sequence (covers spin range 0.0 to 0.99)
    seq = qnm.modes_cache(s=0.0, l=l, m=m, n=n)
    
    # Convert seq.a (list) to numpy array
    a_arr = np.array(seq.a)
    
    # Find index closest to a_star
    idx = np.argmin(np.abs(a_arr - a_star))
    
    # Get complex frequency Mω (dimensionless)
    omega_complex = seq.omega[idx]
    
    # Convert to physical units (Hz)
    M_kg = M_solar * M_sun
    M_geo = G * M_kg / c**3  # geometric mass (seconds)
    
    # Physical ω = (Mω) / M_geo (rad/s)
    omega_phys = omega_complex / M_geo  # complex (rad/s)
    
    # Convert to Hz
    f_R = np.real(omega_phys) / (2.0 * np.pi)  # Hz
    f_I = np.imag(omega_phys) / (2.0 * np.pi)  # Hz
    
    # Period and damping time
    T_osc = 1.0 / f_R  # seconds
    tau = 1.0 / np.abs(f_I)  # seconds
    
    return f_R, f_I, T_osc, tau


def main():
    parser = argparse.ArgumentParser(
        description="Quasi-Normal Mode (QNM) Calculator v2 (uses qnm package)"
    )
    parser.add_argument(
        "--mass", type=float, default=62.0,
        help="Black hole mass (solar masses, default: 62.0 = GW150914 final BH)"
    )
    parser.add_argument(
        "--spin", type=float, default=0.67,
        help="Dimensionless spin parameter a* (0 <= a* <= 1, default: 0.67)"
    )
    parser.add_argument(
        "--l", type=int, default=2,
        help="Angular harmonic index l (default: 2)"
    )
    parser.add_argument(
        "--m", type=int, default=2,
        help="Angular harmonic index m (default: 2)"
    )
    parser.add_argument(
        "--n", type=int, default=0,
        help="Overtone index n (default: 0 = fundamental)"
    )
    parser.add_argument(
        "--scan", action="store_true",
        help="Scan spin from 0.0 to 0.99, plot f_R and f_I"
    )
    
    args = parser.parse_args()
    
    if args.scan:
        # Scan spin
        import matplotlib.pyplot as plt
        
        # Get QNM sequence
        seq = qnm.modes_cache(s=0.0, l=args.l, m=args.m, n=args.n)
        a_arr = np.array(seq.a)
        omega_arr = np.array(seq.omega)
        
        # Convert to physical units (for M = args.mass)
        M_kg = args.mass * M_sun
        M_geo = G * M_kg / c**3
        
        omega_phys = omega_arr / M_geo  # complex (rad/s)
        f_R_arr = np.real(omega_phys) / (2.0 * np.pi)  # Hz
        f_I_arr = np.imag(omega_phys) / (2.0 * np.pi)  # Hz
        
        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        ax1.plot(a_arr, f_R_arr, "b-", linewidth=2)
        ax1.set_xlabel("Spin a*", fontsize=12)
        ax1.set_ylabel("f_R (Hz)", fontsize=12)
        ax1.set_title(f"QNM Oscillation Frequency (M = {args.mass:.1f} M_sun)", fontsize=14)
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(a_arr, np.abs(f_I_arr), "r-", linewidth=2)
        ax2.set_xlabel("Spin a*", fontsize=12)
        ax2.set_ylabel("|f_I| (Hz)", fontsize=12)
        ax2.set_title(f"QNM Damping Rate (M = {args.mass:.1f} M_sun)", fontsize=14)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig("qnm_frequency_v2.png", dpi=150)
        print(f"Plot saved: qnm_frequency_v2.png")
        
    else:
        # Single calculation
        f_R, f_I, T_osc, tau = get_qnm_frequency(
            args.mass, args.spin, args.l, args.m, args.n
        )
        
        print("=" * 60)
        print("Quasi-Normal Mode (QNM) Calculator v2")
        print("=" * 60)
        print(f"Mass M = {args.mass:.2f} M_sun")
        print(f"Spin a* = {args.spin:.2f}")
        print(f"Mode (l,m,n) = ({args.l},{args.m},{args.n})")
        print("-" * 60)
        print(f"f_R = {f_R:.4f} Hz  (oscillation frequency)")
        print(f"f_I = {f_I:.4f} Hz  (damping rate)")
        print(f"T_osc = {T_osc:.6f} s  (oscillation period)")
        print(f"tau = {tau:.6f} s  (damping time)")
        print("-" * 60)
        
        # Quality factor
        Q = 2.0 * np.pi * f_R / np.abs(f_I)
        print(f"Quality factor Q = {Q:.2f}")
        print(f"  (Q > 1 means underdamped oscillation)")
        print("=" * 60)
        
        # Comparison to observations
        if abs(args.mass - 62.0) < 1.0 and abs(args.spin - 0.67) < 0.01:
            print("\nComparison to GW150914 (LIGO first detection):")
            print(f"  Final mass = 62 M_sun, spin = 0.67")
            print(f"  Observed ringdown frequency ~ 235 Hz")
            print(f"  This calculation: f_R = {f_R:.2f} Hz")
            print(f"  (Using qnm package v0.4.4)")
        print("=" * 60)


if __name__ == "__main__":
    main()
