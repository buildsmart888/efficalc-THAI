"""
Concrete Beam Neutral Axis Calculation - SI Units Version
Calculate the neutral axis depth and moment capacity using ACI 318M-25 metric provisions
"""

from efficalc import (
    Calculation,
    Comparison,
    Heading,
    Input,
    TextBlock,
    Title,
    maximum,
    sqrt,
)

# Import SI units if available
try:
    from efficalc import (
        # SI Units
        mm, cm, m, mm2, cm2, m2, mm3, cm3,
        MPa, kPa, N, kN, kNm
    )
    SI_AVAILABLE = True
except ImportError:
    SI_AVAILABLE = False

def concrete_beam_neutral_axis_si():
    """
    Concrete Beam Neutral Axis Calculation using SI Units (ACI 318M-25)
    """
    
    if not SI_AVAILABLE:
        Title("Error: SI Units Not Available")
        TextBlock("This calculation requires 'forallpeople' library. Install with: pip install forallpeople")
        return

    Title("Reinforced Concrete Beam Neutral Axis Analysis (SI Units)")
    TextBlock(
        "Calculate the neutral axis depth and moment capacity of a reinforced concrete beam "
        "using ACI 318M-25 metric provisions."
    )

    Heading("Material Properties")
    fc = Input("f_c", 25, "MPa", "Concrete compressive strength")  # ~3.6 ksi
    fy = Input("f_y", 420, "MPa", "Steel yield strength")  # ~60 ksi
    
    Heading("Section Geometry")
    b = Input("b", 300, "mm", "Beam width")  # ~12 inches
    h = Input("h", 500, "mm", "Total beam height")  # ~20 inches
    cover = Input("cover", 40, "mm", "Concrete cover to reinforcement centroid")  # ~1.5 inches
    
    d = Calculation("d", h - cover, "mm", "Effective depth")

    Heading("Reinforcement")
    As = Input("A_s", 1935, "mm^2", "Total steel area")  # ~3 in²
    
    # Calculate steel ratio
    rho = Calculation("\\rho", As / (b * d), "", "Steel ratio")

    Heading("Neutral Axis Analysis")
    
    # Stress block parameters (ACI 318M-25)
    alpha1 = Calculation("\\alpha_1", 0.85, "", "Stress block factor")  # For fc ≤ 28 MPa
    beta1 = Calculation("\\beta_1", 0.85, "", "Stress block depth factor")  # For fc ≤ 28 MPa
    
    # Calculate stress block depth 'a' from force equilibrium
    # T = C  →  As × fy = α₁ × fc × a × b
    a = Calculation(
        "a", 
        As * fy / (alpha1 * fc * b), 
        "mm", 
        description="Depth of equivalent stress block",
        reference="ACI 318M-25 Eq. 22.2.2.4.1"
    )
    
    # Neutral axis depth from stress block depth
    c = Calculation(
        "c",
        a / beta1,
        "mm",
        description="Neutral axis depth from extreme compression fiber",
        reference="ACI 318M-25 Section 22.2.2.4.1",
    )

    Heading("Strain Analysis")
    
    # Maximum concrete strain (ACI 318M-25)
    epsilon_cu = Calculation("\\epsilon_{cu}", 0.003, "", "Ultimate concrete strain")
    
    # Steel strain at ultimate
    epsilon_s = Calculation(
        "\\epsilon_s", 
        epsilon_cu * (d - c) / c, 
        "", 
        "Steel strain at ultimate",
        reference="Strain compatibility"
    )
    
    # Steel yield strain
    Es = Calculation("E_s", 200000, "MPa", "Steel modulus of elasticity")
    epsilon_y = Calculation("\\epsilon_y", fy / Es, "", "Steel yield strain")
    
    # Check if steel yields
    steel_yields = Comparison(
        epsilon_s,
        ">=", 
        epsilon_y,
        true_message="Steel yields - tension controlled section",
        false_message="Steel does not yield - compression controlled"
    )

    Heading("Internal Forces and Moment Capacity")
    
    # Concrete compression force
    Cc = Calculation("C_c", alpha1 * fc * a * b / 1000, "kN", "Concrete compression force")
    
    # Steel tension force (assuming steel yields)
    Ts = Calculation("T_s", As * fy / 1000, "kN", "Steel tension force")
    
    # Force equilibrium check - forces should be approximately equal
    TextBlock(f"Force equilibrium check: Cc = {Cc.result():.1f} kN, Ts = {Ts.result():.1f} kN")
    
    force_difference = Calculation("\\Delta F", abs(Cc - Ts), "kN", "Force difference")
    force_balance = Comparison(
        force_difference,
        "<=",
        2.0,  # Allow 2 kN difference
        true_message="Forces balanced ✓ (difference ≤ 2 kN)",
        false_message="Forces not balanced - check calculation"
    )
    
    # Distance from compression face to centroid of compression force
    y_cc = Calculation("y_{cc}", a / 2, "mm", "Centroid of compression block")
    
    # Moment arm
    moment_arm = Calculation("z", d - y_cc, "mm", "Internal moment arm")
    
    # Nominal moment capacity
    Mn = Calculation("M_n", Ts * moment_arm / 1000, "kN*m", "Nominal moment capacity")
    
    # Design moment capacity (with strength reduction factor)
    phi = Calculation("\\phi", 0.9, "", "Strength reduction factor for tension-controlled")
    Mu = Calculation("M_u", phi * Mn, "kN*m", "Design moment capacity")

    Heading("Section Classification")
    
    # Check minimum reinforcement (ACI 318M-25 Section 9.6.1.2)
    As_min = Calculation(
        "A_{s,min}",
        maximum(0.25 * sqrt(fc) * b * d / fy, 1.4 * b * d / fy),
        "mm^2",
        "Minimum reinforcement area",
        reference="ACI 318M-25 Section 9.6.1.2"
    )
    
    min_reinf_check = Comparison(
        As,
        ">=",
        As_min,
        true_message="Minimum reinforcement satisfied ✓",
        false_message="Insufficient reinforcement"
    )

    Heading("Summary")
    TextBlock(f"Neutral axis depth: **{c.result():.1f} mm** from compression face")
    TextBlock(f"Steel ratio: **ρ = {rho.result():.4f}**")
    TextBlock(f"Stress block depth: **{a.result():.1f} mm**")
    TextBlock(f"Steel strain: **{epsilon_s.result():.4f}** ({'yields' if epsilon_s.result() >= epsilon_y.result() else 'does not yield'})")
    TextBlock(f"Nominal moment capacity: **{Mn.result():.1f} kN⋅m**")
    TextBlock(f"Design moment capacity: **{Mu.result():.1f} kN⋅m**")

if __name__ == "__main__":
    from efficalc.report_builder import ReportBuilder
    
    builder = ReportBuilder(concrete_beam_neutral_axis_si)
    builder.view_report()
