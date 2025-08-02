"""
Concrete Beam Neutral Axis - SI Units Version
Determine neutral axis depth using metric units (ACI 318M-25)
"""

from efficalc import Calculation, Comparison, Heading, Input, TextBlock, Title

# Import SI units if available
try:
    from efficalc import (
        # SI Units
        mm, cm, m, mm2, cm2, m2,
        MPa, kPa, N, kN
    )
    SI_AVAILABLE = True
except ImportError:
    SI_AVAILABLE = False

def concrete_beam_neutral_axis_si():
    """
    Concrete Beam Neutral Axis using SI Units
    """
    
    if not SI_AVAILABLE:
        Title("Error: SI Units Not Available")
        TextBlock("This calculation requires 'forallpeople' library. Install with: pip install forallpeople")
        return

    Title("Concrete Beam Neutral Axis (SI Units)")
    TextBlock("Determine the neutral axis depth in a singly reinforced concrete beam using metric units.")

    Heading("Inputs")
    As = Input("A_s", 1935, "mm^2", description="Area of reinforcing steel")  # ~3 in²
    fy = Input("f_y", 420, "MPa", "Yield strength of reinforcing steel")  # ~60 ksi
    fc = Input("f_{c}^{\\prime}", 25, "MPa", "Concrete compressive strength")  # ~3.6 ksi
    b = Input("b", 300, "mm", "Beam width")  # ~12 in
    B1 = Input("\\beta_1", 0.85, "", description="Compressive stress block ratio")

    Heading("Calculations")
    a = Calculation(
        "a", 
        As * fy / (0.85 * fc * b), 
        "mm", 
        result_check=True,
        description="Depth of equivalent stress block",
        reference="ACI 318M-25 Eq. 22.2.2.4.1"
    )
    
    c = Calculation(
        "c",
        a / B1,
        "mm",
        result_check=True,
        description="Neutral axis depth from extreme compression fiber",
        reference="ACI 318M-25 Section 22.2.2.4.1",
    )

    # Check minimum depth requirement (converted from 3.5 in to mm)
    min_depth = 89  # mm (≈ 3.5 in)
    Comparison(
        c, 
        ">", 
        min_depth, 
        true_message="Adequate depth", 
        false_message="Insufficient depth",
        result_check=True
    )

    Heading("Summary")
    TextBlock(f"The neutral axis is located {c.result():.1f} mm from the extreme compression fiber.")
    
    # Calculate additional parameters
    d = Input("d", 450, "mm", "Effective depth to tension reinforcement")  # ~18 in
    
    strain_ratio = Calculation(
        "\\varepsilon_s/\\varepsilon_c",
        (d - c) / c,
        "",
        description="Strain ratio (tension/compression)",
        reference="ACI 318M-25 strain compatibility"
    )
    
    # Check if section is tension-controlled
    Comparison(
        strain_ratio,
        ">=",
        1.4,  # Corresponds to εs ≥ 0.005 when εc = 0.003
        true_message="Tension-controlled section",
        false_message="Compression-controlled section",
        result_check=False
    )

if __name__ == "__main__":
    from efficalc.report_builder import ReportBuilder
    
    builder = ReportBuilder(concrete_beam_neutral_axis_si)
    builder.view_report()
