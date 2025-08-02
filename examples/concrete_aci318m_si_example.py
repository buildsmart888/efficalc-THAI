"""
ACI 318M-25 Concrete Beam Analysis Example with SI Units
Using efficalc with forallpeople for comprehensive SI units support
"""

from efficalc import (
    Calculation, 
    Comparison, 
    Heading, 
    Input, 
    TextBlock, 
    Title,
    Assumption,
    sqrt,
    maximum  # Add this for max function
)

# Import SI units and ACI constants
try:
    from efficalc import (
        # SI Units
        mm, cm, m, mm2, cm2, m2, 
        MPa, kPa, N, kN,
        # ACI Constants
        ACI318M_Constants,
        # Conversions (if needed)
        ksi_to_MPa, in2_to_mm2, in_to_mm
    )
    SI_AVAILABLE = True
except ImportError:
    SI_AVAILABLE = False


def concrete_beam_aci318m_si():
    """
    Concrete beam neutral axis calculation using ACI 318M-25 and SI units
    """
    
    if not SI_AVAILABLE:
        Title("Error: SI Units Not Available")
        TextBlock("This calculation requires 'forallpeople' library. Install with: pip install forallpeople")
        return
    
    Title("Concrete Beam Analysis - ACI 318M-25 (SI Units)")
    TextBlock("Determination of neutral axis depth for singly reinforced concrete beam using metric units.")
    
    Heading("Code References", numbered=False)
    Assumption("ACI 318M-25 Building Code Requirements for Structural Concrete (Metric)")
    Assumption("SI units (Systeme International) used throughout")
    Assumption("Normal weight concrete assumed")
    
    Heading("Material Properties")
    
    # Concrete properties
    fc = Input(
        "f_{c}^{\\prime}", 
        30, 
        "MPa", 
        "Specified compressive strength of concrete",
        reference="ACI 318M-25 19.2.1.1"
    )
    
    # Steel properties  
    fy = Input(
        "f_y", 
        420, 
        "MPa", 
        "Specified yield strength of reinforcement",
        reference="ACI 318M-25 20.2.2.1"
    )
    
    Es = Calculation(
        "E_s",
        200000,
        "MPa",
        "Modulus of elasticity of steel",
        reference="ACI 318M-25 20.2.2.2"
    )
    
    Heading("Geometric Properties")
    
    # Beam dimensions
    b = Input(
        "b", 
        300, 
        "mm", 
        "Width of compression face of beam"
    )
    
    h = Input(
        "h", 
        600, 
        "mm", 
        "Overall depth of beam"
    )
    
    cover = Input(
        "cover",
        40,
        "mm", 
        "Concrete cover to reinforcement center",
        reference="ACI 318M-25 Table 20.5.1.3.1"
    )
    
    d = Calculation(
        "d",
        h - cover,
        "mm",
        "Effective depth to tension reinforcement"
    )
    
    # Reinforcement
    As = Input(
        "A_s", 
        2000, 
        "mm^2", 
        "Area of tension reinforcement"
    )
    
    Heading("Stress Block Parameters")
    
    # Beta1 factor for stress block (ACI 318M-25 22.2.2.4.3)
    beta1_calc = Calculation(
        "\\beta_1",
        0.85,  # Simplified - for fc <= 28 MPa
        "",
        "Stress block factor",
        reference="ACI 318M-25 Table 22.2.2.4.3"
    )
    
    Heading("Neutral Axis Calculation")
    
    # Depth of stress block
    a = Calculation(
        "a",
        As * fy / (0.85 * fc * b),
        "mm",
        "Depth of equivalent rectangular stress block",
        result_check=True
    )
    
    # Neutral axis depth
    c = Calculation(
        "c",
        a / beta1_calc,
        "mm",
        "Distance from extreme compression fiber to neutral axis",
        reference="ACI 318M-25 22.2.2.4.1",
        result_check=True
    )
    
    Heading("Strain Compatibility Check")
    
    # Maximum concrete strain
    epsilon_cu = Calculation(
        "\\epsilon_{cu}",
        0.003,
        "",
        "Maximum usable strain in concrete",
        reference="ACI 318M-25 22.2.2.1"
    )
    
    # Steel strain
    epsilon_s = Calculation(
        "\\epsilon_s",
        epsilon_cu * (d - c) / c,
        "",
        "Strain in tension reinforcement"
    )
    
    # Yield strain
    epsilon_y = Calculation(
        "\\epsilon_y",
        fy / Es,
        "",
        "Yield strain of reinforcement"
    )
    
    Heading("Section Classification")
    
    # Check if steel yields (tension-controlled)
    Comparison(
        epsilon_s,
        ">=",
        epsilon_y,
        "Tension-controlled section (phi = 0.9)",
        "Compression-controlled or transition",
        "Steel yield check",
        reference="ACI 318M-25 21.2.2"
    )
    
    # Minimum reinforcement check
    As_min = Calculation(
        "A_{s,min}",
        maximum(0.25 * sqrt(fc) * b * d / fy, 1.4 * b * d / fy),
        "mm^2",
        "Minimum required reinforcement",
        reference="ACI 318M-25 9.6.1.2"
    )
    
    Comparison(
        As,
        ">=",
        As_min,
        "OK - Minimum reinforcement satisfied",
        "NG - Insufficient reinforcement",
        "Minimum reinforcement check"
    )
    
    Heading("Nominal Moment Capacity")
    
    # Nominal moment strength
    Mn = Calculation(
        "M_n",
        As * fy * (d - a/2) / 1e6,  # Convert to kN*m
        "kN*m",
        "Nominal flexural strength",
        reference="ACI 318M-25 22.2.2.4.1",
        result_check=True
    )
    
    # Design moment strength
    phi = Calculation(
        "\\phi",
        0.9,
        "",
        "Strength reduction factor for flexure",
        reference="ACI 318M-25 21.2.1"
    )
    
    Md = Calculation(
        "M_d",
        phi * Mn,
        "kN*m",
        "Design flexural strength",
        result_check=True
    )
    
    Heading("Summary")
    
    TextBlock(
        "This analysis demonstrates ACI 318M-25 compliance using SI units. "
        "The neutral axis depth and moment capacity have been calculated according to "
        "metric building code requirements."
    )


def concrete_column_aci318m_si():
    """
    Simple concrete column analysis using ACI 318M-25 and SI units
    """
    
    if not SI_AVAILABLE:
        Title("Error: SI Units Not Available")
        TextBlock("This calculation requires 'forallpeople' library. Install with: pip install forallpeople")
        return
    
    Title("Concrete Column Design - ACI 318M-25 (SI Units)")
    TextBlock("Axial capacity calculation for tied concrete column using metric units.")
    
    Heading("Code References", numbered=False)
    Assumption("ACI 318M-25 Building Code Requirements for Structural Concrete (Metric)")
    Assumption("Tied column with Grade 420 reinforcement")
    Assumption("Normal weight concrete")
    
    Heading("Material Properties")
    
    fc = Input(
        "f_{c}^{\\prime}", 
        25, 
        "MPa", 
        "Specified compressive strength of concrete"
    )
    
    fy = Input(
        "f_y", 
        420, 
        "MPa", 
        "Specified yield strength of reinforcement"
    )
    
    Heading("Column Geometry")
    
    # Column dimensions
    h = Input("h", 400, "mm", "Column dimension")
    b = Input("b", 400, "mm", "Column dimension") 
    
    Ag = Calculation(
        "A_g",
        h * b,
        "mm^2",
        "Gross area of column"
    )
    
    # Reinforcement
    As = Input(
        "A_s", 
        3200, 
        "mm^2", 
        "Total area of longitudinal reinforcement"
    )
    
    # Reinforcement ratio
    rho_g = Calculation(
        "\\rho_g",
        As / Ag,
        "",
        "Gross reinforcement ratio"
    )
    
    Heading("Reinforcement Limits Check")
    
    # Minimum reinforcement (ACI 318M-25 10.6.1.1)
    rho_min = Calculation(
        "\\rho_{g,min}",
        0.01,
        "",
        "Minimum gross reinforcement ratio",
        reference="ACI 318M-25 10.6.1.1"
    )
    
    # Maximum reinforcement (ACI 318M-25 10.6.1.1)  
    rho_max = Calculation(
        "\\rho_{g,max}",
        0.08,
        "",
        "Maximum gross reinforcement ratio",
        reference="ACI 318M-25 10.6.1.1"
    )
    
    Comparison(
        rho_g,
        ">=",
        rho_min,
        "OK - Minimum reinforcement satisfied",
        "NG - Insufficient reinforcement",
        "Minimum reinforcement check"
    )
    
    Comparison(
        rho_g,
        "<=", 
        rho_max,
        "OK - Maximum reinforcement satisfied",
        "NG - Excessive reinforcement",
        "Maximum reinforcement check"
    )
    
    Heading("Nominal Axial Strength")
    
    # Nominal axial strength for tied column (ACI 318M-25 22.4.2.2)
    Pn = Calculation(
        "P_n",
        0.8 * (0.85 * fc * (Ag - As) + fy * As) / 1000,  # Convert to kN
        "kN",
        "Nominal axial strength",
        reference="ACI 318M-25 22.4.2.2"
    )
    
    # Design strength
    phi_c = Calculation(
        "\\phi_c",
        0.65,
        "",
        "Strength reduction factor for tied column",
        reference="ACI 318M-25 21.2.1"
    )
    
    Pd = Calculation(
        "P_d",
        phi_c * Pn,
        "kN", 
        "Design axial strength",
        result_check=True
    )
    
    Heading("Summary")
    
    TextBlock(
        "Column design completed using ACI 318M-25 metric provisions. "
        "All calculations performed in SI units for international compatibility."
    )


if __name__ == "__main__":
    from efficalc.report_builder import ReportBuilder
    
    # Choose which calculation to run
    print("Choose calculation:")
    print("1. Concrete Beam Analysis")
    print("2. Concrete Column Design")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        builder = ReportBuilder(concrete_beam_aci318m_si)
    elif choice == "2":
        builder = ReportBuilder(concrete_column_aci318m_si)
    else:
        print("Running beam analysis by default...")
        builder = ReportBuilder(concrete_beam_aci318m_si)
    
    builder.view_report()
