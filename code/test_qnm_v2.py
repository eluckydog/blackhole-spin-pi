#!/usr/bin/env python3
"""Test qnm package API v2 - extract complex frequency"""

import qnm
import numpy as np

# Get QNM sequence for l=2, m=2, n=0
l, m, n = 2, 2, 0
seq = qnm.modes_cache(s=0.67, l=l, m=m, n=n)

print("Type:", type(seq))
print("\nAttributes:")
for attr in dir(seq):
    if not attr.startswith('_'):
        print(f"  {attr}")

# Check if seq has 'omega' attribute (complex frequency Mω)
if hasattr(seq, 'omega'):
    omega_list = seq.omega  # This is a list of complex numbers
    omega_arr = np.array(omega_list)  # Convert to numpy array
    
    print("\n\nseq.omega shape:", omega_arr.shape)
    print("seq.omega[0]:", omega_arr[0])  # Should be complex
    print("seq.a shape:", seq.a.shape)
    print("seq.a[0:5]:", seq.a[0:5])
    
    # Find index closest to s=0.67
    idx = np.argmin(np.abs(seq.a - 0.67))
    print(f"\nIndex for s=0.67: {idx}")
    print(f"a[{idx}] = {seq.a[idx]}")
    print(f"omega[{idx}] = {omega_arr[idx]} (complex Mω)")
    
    # Convert to physical frequency (Hz)
    # omega is Mω (dimensionless)
    # Physical ω = (omega / M) in geometric units
    # M (geometric) = G*M/c³ (seconds)
    # f = Re(ω) / (2π) (Hz)
    
    M_sun = 1.9885e30  # kg
    G = 6.67430e-11   # m³/(kg·s²)
    c = 299792458.0     # m/s
    
    M_kg = 62.0 * M_sun  # GW150914 final BH mass
    M_geo = G * M_kg / c**3  # geometric mass (seconds)
    
    omega_complex = seq.omega[idx]  # dimensionless Mω
    omega_phys = omega_complex / M_geo  # physical ω (rad/s)
    
    f_R = np.real(omega_phys) / (2.0 * np.pi)  # Hz
    f_I = np.imag(omega_phys) / (2.0 * np.pi)  # damping rate (Hz)
    
    print(f"\nFor M = 62 M☉:")
    print(f"  Re(ω) = {f_R:.2f} Hz")
    print(f"  Im(ω) = {f_I:.2f} Hz")
    print(f"  T_osc = {1.0/f_R:.6f} s")
    print(f"  τ = {1.0/abs(f_I):.6f} s")
    
else:
    print("\n\nNo 'omega' attribute found")
    print("Available attributes:", [a for a in dir(seq) if not a.startswith('_')])
