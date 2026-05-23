#!/usr/bin/env python3
"""Test qnm package API v3 - correctly extract QNM frequency for given spin"""

import qnm
import numpy as np

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
        Angular harmonic indices
    n : int
        Overtone index
    
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
    omega_complex = seq.omega[idx]  # complex number
    
    # Convert to physical units
    M_sun = 1.9885e30  # kg
    G = 6.67430e-11   # m³/(kg·s²)
    c = 299792458.0     # m/s
    
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


# Test with GW150914 final BH (M = 62 M☉, a* = 0.67)
M_test = 62.0
a_test = 0.67

print("=" * 60)
print("QNM Frequency Calculation (using qnm package)")
print("=" * 60)
print(f"Mass M = {M_test:.2f} M_sun")
print(f"Spin a* = {a_test:.2f}")
print("-" * 60)

f_R, f_I, T_osc, tau = get_qnm_frequency(M_test, a_test)

print(f"f_R = {f_R:.2f} Hz  (oscillation frequency)")
print(f"f_I = {f_I:.2f} Hz  (damping rate)")
print(f"T_osc = {T_osc:.6f} s  (oscillation period)")
print(f"tau = {tau:.3f} s  (damping time)")
print("-" * 60)

# Compare to LIGO observation (GW150914 ringdown ~ 235 Hz)
print(f"\nComparison to LIGO GW150914:")
print(f"  Observed ringdown frequency ~ 235 Hz")
print(f"  Calculated f_R = {f_R:.2f} Hz")
print(f"  (Note: fitting formula approximation, actual QNM frequency")
print(f"   depends on l,m,n mode and BH parameters)")
print("=" * 60)
