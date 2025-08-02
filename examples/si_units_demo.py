"""
Simple demonstration of SI Units integration with efficalc
Using forallpeople for comprehensive units handling
"""

from efficalc import (
    Calculation, 
    Comparison, 
    Heading, 
    Input, 
    TextBlock, 
    Title,
    Assumption,
    maximum
)

# Test SI units import
try:
    import forallpeople as si
    si.environment('default')
    SI_AVAILABLE = True
    print("✓ forallpeople (SI Units) is available")
except ImportError:
    SI_AVAILABLE = False
    print("✗ forallpeople not available")

def simple_si_example():
    """
    Simple concrete beam example using SI units
    """
    
    Title("SI Units Demo with efficalc")
    TextBlock("This example demonstrates the integration of SI units using the forallpeople library.")
    
    if not SI_AVAILABLE:
        TextBlock("WARNING: forallpeople library not available. Install with: pip install forallpeople")
        return
    
    Heading("Material Properties (SI Units)")
    
    # Concrete strength in MPa (typical SI unit)
    fc = Input(
        "f'_c", 
        25, 
        "MPa", 
        "Concrete compressive strength"
    )
    
    # Steel yield strength in MPa
    fy = Input(
        "f_y", 
        420, 
        "MPa", 
        "Steel yield strength"
    )
    
    # Steel modulus in GPa
    Es = Input(
        "E_s",
        200,
        "GPa", 
        "Steel modulus of elasticity"
    )
    
    Heading("Geometric Properties (SI Units)")
    
    # Beam width in mm (common in metric design)
    b = Input(
        "b", 
        300, 
        "mm", 
        "Beam width"
    )
    
    # Effective depth in mm
    d = Input(
        "d", 
        500, 
        "mm", 
        "Effective depth"
    )
    
    # Reinforcement area in mm^2
    As = Input(
        "A_s", 
        1500, 
        "mm^2", 
        "Tension reinforcement area"
    )
    
    Heading("Design Calculations")
    
    # Convert units for calculations (demonstrating unit awareness)
    fc_Pa = Calculation(
        "f'_{c,Pa}",
        fc * 1e6,  # Convert MPa to Pa
        "Pa",
        "Concrete strength in base SI units (Pa)"
    )
    
    fy_Pa = Calculation(
        "f_{y,Pa}",
        fy * 1e6,  # Convert MPa to Pa  
        "Pa",
        "Steel yield in base SI units (Pa)"
    )
    
    # Steel ratio
    rho = Calculation(
        "\\rho",
        As / (b * d),
        "",
        "Reinforcement ratio"
    )
    
    # Balanced reinforcement ratio (simplified)
    rho_b = Calculation(
        "\\rho_b",
        0.85 * 0.85 * fc / fy * 600 / (600 + fy),
        "",
        "Balanced reinforcement ratio"
    )
    
    Heading("Design Checks")
    
    # Check if section is tension controlled
    Comparison(
        rho,
        "<=",
        0.75 * rho_b,
        "Tension-controlled section",
        "Compression-controlled section", 
        "Section classification check"
    )
    
    # Minimum reinforcement check using maximum function properly
    term1 = Calculation("term1", 1.4 / fy, "", "First term for minimum reinforcement")
    term2 = Calculation("term2", 0.25 * (fc**0.5) / fy, "", "Second term for minimum reinforcement")
    
    rho_min = Calculation(
        "\\rho_{min}",
        maximum(term1, term2),
        "",
        "Minimum reinforcement ratio"
    )
    
    Comparison(
        rho,
        ">=",
        rho_min,
        "Minimum reinforcement OK",
        "Insufficient reinforcement",
        "Minimum reinforcement check"
    )
    
    Heading("Unit Conversion Example")
    
    # Show conversion between Imperial and SI
    TextBlock(
        "This section demonstrates conversion between Imperial (US) and SI (Metric) units."
    )
    
    # Conversion factors
    psi_to_Pa = Calculation(
        "psi_{to}Pa",
        6895,
        "Pa/psi",
        "Pressure conversion factor"
    )
    
    in_to_mm = Calculation(
        "in_{to}mm", 
        25.4,
        "mm/in",
        "Length conversion factor"
    )
    
    # Example conversions
    fc_psi = Calculation(
        "f'_{c,psi}",
        fc * 1e6 / psi_to_Pa,  # Convert MPa to psi
        "psi",
        "Concrete strength in Imperial units"
    )
    
    b_in = Calculation(
        "b_{in}",
        b / in_to_mm,  # Convert mm to inches
        "in", 
        "Beam width in Imperial units"
    )
    
    Heading("Summary")
    
    TextBlock(
        "This example shows how efficalc can work with SI units (metric system) "
        "alongside the forallpeople library for comprehensive units handling. "
        "The calculations demonstrate typical concrete design parameters in "
        "both SI and Imperial units for international compatibility."
    )


if __name__ == "__main__":
    from efficalc.report_builder import ReportBuilder
    
    builder = ReportBuilder(simple_si_example)
    builder.view_report()
