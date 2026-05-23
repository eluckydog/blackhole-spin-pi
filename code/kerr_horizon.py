#!/usr/bin/env python3
"""
Kerr Black Hole Horizon Area Calculator

Computes the event horizon area of a Kerr black hole.
A = 8π M r₊  (geometric units G = c = 1)
"""

import argparse
import math


def kerr_horizon_area(M, a_star):
    """
    Compute Kerr black hole horizon area.
    
    Parameters:
    -----------
    M : float
        Black hole mass (solar masses or geometric units)
    a_star : float
        Dimensionless spin parameter (0 <= a_star <= 1)
    
    Returns:
    --------
    A : float
        Horizon area (in units of M², times π)
    r_outer : float
        Outer horizon radius r₊
    """
    a = a_star * M  # spin parameter (dimensional)
    
    # Outer horizon radius
    r_outer = M + math.sqrt(M**2 - a**2)
    
    # Horizon area: A = 8π M r₊
    A = 8.0 * math.pi * M * r_outer
    
    return A, r_outer


def main():
    parser = argparse.ArgumentParser(
        description="Kerr Black Hole Horizon Area Calculator"
    )
    parser.add_argument(
        "--mass", type=float, default=1.0,
        help="Black hole mass (solar masses or geometric units, default: 1.0)"
    )
    parser.add_argument(
        "--spin", type=float, default=0.0,
        help="Dimensionless spin parameter a* (0 <= a* <= 1, default: 0.0)"
    )
    parser.add_argument(
        "--scan", action="store_true",
        help="Scan spin from 0 to 0.99, plot A vs a*"
    )
    
    args = parser.parse_args()
    
    if args.scan:
        # Scan spin parameter
        import numpy as np
        import matplotlib.pyplot as plt
        
        a_stars = np.linspace(0, 0.99, 100)
        areas = []
        
        for a in a_stars:
            A, r = kerr_horizon_area(args.mass, a)
            areas.append(A)
        
        # Plot
        plt.figure(figsize=(8, 6))
        plt.plot(a_stars, areas, "b-", linewidth=2)
        plt.axvline(x=1.0, color="r", linestyle="--", label="Extremal Kerr (a*=1)")
        plt.xlabel("Dimensionless spin a*", fontsize=12)
        plt.ylabel("Horizon area A / M²", fontsize=12)
        plt.title("Kerr black hole horizon area vs. spin", fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig("kerr_horizon_area.png", dpi=150)
        print(f"Plot saved: kerr_horizon_area.png")
        
    else:
        # Single calculation
        A, r_outer = kerr_horizon_area(args.mass, args.spin)
        
        print("=" * 60)
        print("Kerr Black Hole Horizon Area")
        print("=" * 60)
        print(f"Mass M = {args.mass:.4f}")
        print(f"Spin a* = {args.spin:.4f}")
        print(f"Outer horizon r_outer = {r_outer:.4f} (geometric units)")
        print(f"Horizon area A = {A:.4f} * M^2")
        print(f"                   = {A:.4f} * (G^2 M^2 / c^4)  (SI units)")
        print("=" * 60)
        
        # Compare to Schwarzschild (a* = 0)
        A_sch, r_sch = kerr_horizon_area(args.mass, 0.0)
        print(f"\nComparison to Schwarzschild (a* = 0):")
        print(f"  A_Schwarzschild = {A_sch:.4f} * M^2")
        print(f"  A_Kerr / A_Sch = {A / A_sch:.4f}")
        print("=" * 60)


if __name__ == "__main__":
    main()
