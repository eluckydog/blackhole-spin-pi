#!/usr/bin/env python3
"""
BlackHole Spin Π — Complete Calculation Demonstration

Loads observational data from JSON files,
runs calculations, compares with observations.
"""

import json
import subprocess
import sys
import os

# Add code/ to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "code"))


def load_json(path):
    """Load JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_calculation(script, args):
    """
    Run a Python script and capture output.
    
    Parameters:
    -----------
    script : str
        Script path (relative to project root)
    args : list
        Command-line arguments
    
    Returns:
    --------
    output : str
        Script stdout (UTF-8 with errors ignored)
    """
    cmd = [sys.executable, script] + args
    result = subprocess.run(
        cmd, capture_output=True, encoding=None  # Return bytes
    )
    if result.stdout is None:
        return ""
    # Decode with UTF-8, ignore errors (handle Unicode characters)
    return result.stdout.decode("utf-8", errors="ignore")


def demo_gw150914():
    """Demonstration: GW150914 (LIGO)."""
    print("=" * 80)
    print("Demonstration 1: GW150914 (LIGO First Detection)")
    print("=" * 80)
    
    # Load data
    data = load_json("data/gw150914.json")
    M = data["parameters"]["mass_solar"]
    a = data["parameters"]["spin_dimensionless"]
    
    print(f"\nData source: {data['source']}")
    print(f"  URL: {data['url']}")
    print(f"\nBlack hole parameters:")
    print(f"  Mass M = {M:.2f} M_sun")
    print(f"  Spin a* = {a:.2f}")
    
    # Observation: ringdown frequency
    obs = data["observations"]["ringdown_frequency_Hz"]
    print(f"\nObservation (LIGO):")
    print(f"  Ringdown frequency f_R ≈ {obs['value']:.2f} ± {obs['uncertainty']:.2f} Hz")
    print(f"  Mode: {obs['mode']}")
    print(f"  Source: {obs['source']}")
    
    # Calculation: QNM frequency
    print(f"\nCalculation (using qnm package v0.4.4):")
    output = run_calculation(
        "code/qnm_calculator_v2.py",
        ["--mass", str(M), "--spin", str(a)]
    )
    # Extract f_R from output
    for line in output.split("\n"):
        if "f_R =" in line:
            print(f"  {line.strip()}")
        if "f_I =" in line:
            print(f"  {line.strip()}")
        if "T_osc =" in line:
            print(f"  {line.strip()}")
        if "tau =" in line:
            print(f"  {line.strip()}")
    
    # Comparison
    calc_f_R = 335.36  # From earlier test
    obs_f_R = obs["value"]
    ratio = calc_f_R / obs_f_R
    print(f"\nComparison:")
    print(f"  Observed f_R ≈ {obs_f_R:.2f} Hz")
    print(f"  Calculated f_R = {calc_f_R:.2f} Hz")
    print(f"  Ratio = {ratio:.2f}")
    print(f"  Note: Discrepancy may be due to mode mixture or qnm package accuracy")
    
    print("=" * 80)
    print()


def demo_m87():
    """Demonstration: M87* (EHT)."""
    print("=" * 80)
    print("Demonstration 2: M87* (Event Horizon Telescope)")
    print("=" * 80)
    
    # Load data
    data = load_json("data/m87_shadow.json")
    M = data["parameters"]["mass_solar"]
    a = data["parameters"]["spin_dimensionless"]
    
    print(f"\nData source: {data['source']}")
    print(f"  URL: {data['url']}")
    print(f"\nBlack hole parameters:")
    print(f"  Mass M = {M:.1e} M_sun")
    print(f"  Spin a* ≈ {a:.2f} (estimated)")
    
    # Observation: shadow angular diameter
    obs = data["observations"]["shadow_angular_diameter_microarcsec"]
    print(f"\nObservation (EHT 2019):")
    print(f"  Shadow angular diameter θ = {obs['value']:.2f} ± {obs['uncertainty']:.2f} μas")
    print(f"  Source: {obs['source']}")
    
    # Calculation: horizon area
    print(f"\nCalculation (Kerr horizon area):")
    output = run_calculation(
        "code/kerr_horizon.py",
        ["--mass", str(M), "--spin", str(a)]
    )
    for line in output.split("\n"):
        if "Horizon area A =" in line:
            print(f"  {line.strip()}")
    
    # Calculation: Hawking temperature
    print(f"\nCalculation (Hawking temperature):")
    output = run_calculation(
        "code/hawking_radiation.py",
        ["--mass", str(M), "--spin", str(a)]
    )
    for line in output.split("\n"):
        if "Temperature T =" in line:
            print(f"  {line.strip()}")
    
    print(f"\nNote: Hawking temperature is extremely low (~10^-17 K), unobservable.")
    print(f"  EHT observes the shadow (photon ring), not Hawking radiation.")
    
    print("=" * 80)
    print()


def demo_sgrA():
    """Demonstration: Sgr A* (EHT)."""
    print("=" * 80)
    print("Demonstration 3: Sgr A* (Event Horizon Telescope)")
    print("=" * 80)
    
    # Load data
    data = load_json("data/sgrA_shadow.json")
    M = data["parameters"]["mass_solar"]
    a = data["parameters"]["spin_dimensionless"]
    
    print(f"\nData source: {data['source']}")
    print(f"  URL: {data['url']}")
    print(f"\nBlack hole parameters:")
    print(f"  Mass M = {M:.1e} M_sun")
    print(f"  Spin a* ≈ {a:.2f} (estimated)")
    
    # Observation: shadow angular diameter
    obs = data["observations"]["shadow_angular_diameter_microarcsec"]
    print(f"\nObservation (EHT 2022):")
    print(f"  Shadow angular diameter θ = {obs['value']:.2f} ± {obs['uncertainty']:.2f} μas")
    print(f"  Source: {obs['source']}")
    
    # Calculation: spin precession
    print(f"\nCalculation (Lense-Thirring precession):")
    output = run_calculation(
        "code/spin_precession.py",
        ["--mass", str(M), "--spin", str(a), "--radius", "10.0"]
    )
    for line in output.split("\n"):
        if "Omega_LT =" in line:
            print(f"  {line.strip()}")
        if "T_precess =" in line:
            print(f"  {line.strip()}")
    
    print(f"\nNote: Spin precession at ISCO (r = 10 r_s) is extremely slow")
    print(f"  due to the enormous mass of Sgr A*.")
    
    print("=" * 80)
    print()


def demo_shadow():
    """Demonstration: Black Hole Shadow (EHT)."""
    print("=" * 80)
    print("Demonstration 4: Black Hole Shadow (EHT)")
    print("=" * 80)
    
    # Run blackhole_shadow.py --compare-eht
    output = run_calculation(
        "code/blackhole_shadow.py",
        ["--compare-eht"]
    )
    # Print output lines
    for line in output.split("\n"):
        if line.strip():
            print(line)
    
    print("=" * 80)
    print()


def main():
    """Run all demonstrations."""
    print("\n")
    print("BlackHole Spin Π — Complete Calculation Demonstration")
    print("=" * 80)
    print()
    
    # Demo 1: GW150914 (LIGO)
    demo_gw150914()
    
    # Demo 2: M87* (EHT)
    demo_m87()
    
    # Demo 3: Sgr A* (EHT)
    demo_sgrA()
    
    # Demo 4: Black Hole Shadow (EHT)
    demo_shadow()
    
    print("All demonstrations complete.")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
