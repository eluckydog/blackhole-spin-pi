#!/usr/bin/env python3
"""Test qnm package API"""

import qnm

# Print qnm package info
print("qnm version:", qnm.__version__)
print("\nAvailable functions:")
print(dir(qnm))

# Test modes_cache
print("\n\nTesting qnm.modes_cache...")
try:
    # Try to get QNM for a* = 0.67, l=2, m=2, n=0
    s = 0.67  # dimensionless spin
    l, m, n = 2, 2, 0
    
    # Check function signature
    import inspect
    sig = inspect.signature(qnm.modes_cache)
    print(f"\nmodes_cache signature: {sig}")
    
    # Try calling it
    result = qnm.modes_cache(s=s, l=l, m=m, n=n)
    print(f"\nResult type: {type(result)}")
    print(f"Result: {result}")
    
    # Try to get the complex frequency
    if hasattr(result, 'shape'):
        print(f"\nResult shape: {result.shape}")
        print(f"First element: {result[0]}")
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

# List available modes
print("\n\nTrying to list available modes...")
try:
    # Check if there's a way to list modes
    if hasattr(qnm, 'available_modes'):
        modes = qnm.available_modes()
        print("Available modes:", modes)
except Exception as e:
    print(f"Error: {e}")
