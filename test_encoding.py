#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test file to check encoding issues
"""

def test_encoding():
    """Test various characters that might cause LaTeX/HTML issues"""
    
    # Test basic ASCII
    print("ASCII text: OK")
    
    # Test LaTeX symbols that should work
    symbols = {
        "phi": r"\phi",
        "beta": r"\beta", 
        "epsilon": r"\epsilon",
        "rho": r"\rho"
    }
    
    print("LaTeX symbols:")
    for name, symbol in symbols.items():
        print(f"  {name}: {symbol}")
    
    # Test units that should be safe
    units = ["MPa", "kN*m", "mm^2", "mm"]
    print("Units:")
    for unit in units:
        print(f"  {unit}")
    
    # Test phrases that caused issues before
    phrases = [
        "Tension-controlled section (phi = 0.9)",
        "SI units (Systeme International) used throughout",
        "Minimum reinforcement satisfied"
    ]
    
    print("Test phrases:")
    for phrase in phrases:
        print(f"  {phrase}")
    
    print("Encoding test completed successfully!")

if __name__ == "__main__":
    test_encoding()
