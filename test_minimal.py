"""
Minimal test to check for encoding issues
"""

# Simple test without dependencies
def main():
    # Test all the potentially problematic strings
    test_strings = [
        "Tension-controlled section (phi = 0.9)",
        "SI units (Systeme International) used throughout",
        "beta_1 = 0.85",
        "epsilon_cu = 0.003",
        "A_s,min calculation",
        "rho_g,min = 0.01",
        "f'_c = 30 MPa",
        "M_n = 245 kN*m",
        "phi_c = 0.65"
    ]
    
    print("Testing potentially problematic strings:")
    print("-" * 50)
    
    for i, string in enumerate(test_strings, 1):
        print(f"{i:2d}. {string}")
    
    print("-" * 50)
    print("Test completed - no encoding errors detected")
    
    # Test LaTeX-like expressions that might cause issues
    latex_expressions = [
        r"\beta_1",
        r"\epsilon_{cu}",  
        r"\epsilon_s",
        r"\epsilon_y",
        r"\phi",
        r"\rho_g",
        r"\rho_{g,min}",
        r"\rho_{g,max}",
        r"\phi_c"
    ]
    
    print("\nTesting LaTeX expressions:")
    print("-" * 50)
    
    for i, expr in enumerate(latex_expressions, 1):
        print(f"{i:2d}. {expr}")
    
    print("-" * 50)
    print("LaTeX expressions test completed")

if __name__ == "__main__":
    main()
