"""
Rectangular HSS Compression Design - SI Units Version
Based on AISC Steel Construction Manual principles but using metric units
"""

from latexexpr_efficalc import Variable

from efficalc import (
    PI,
    Assumption,
    Calculation,
    Comparison,
    ComparisonStatement,
    Heading,
    Input,
    TextBlock,
    Title,
    brackets,
    maximum,
    minimum,
    sqrt,
)

# Import SI units if available
try:
    from efficalc import (
        # SI Units
        mm, cm, m, mm2, cm2, m2, 
        MPa, kPa, N, kN,
        # Conversions
        ksi_to_MPa, in_to_mm
    )
    SI_AVAILABLE = True
except ImportError:
    SI_AVAILABLE = False

def rectangular_hss_compression_design_si():
    """
    Rectangular HSS Compression Design using SI Units
    """
    
    if not SI_AVAILABLE:
        Title("Error: SI Units Not Available")
        TextBlock("This calculation requires 'forallpeople' library. Install with: pip install forallpeople")
        return
    
    Title("Rectangular HSS Compression Design (SI Units)")
    
    Assumption("Members are in pure compression")
    Assumption("AISC principles adapted for metric units")
    Assumption("Torsional unbraced length does not exceed lateral unbraced length")

    Heading("Inputs")
    Pu = Input("P_u", 45, "kN", "Ultimate compressive load")

    L = Input("L", 1.2, "m", "Member length")
    Kc = Input("k_{c}", 1.0, "", "Member effective length factor")

    # Simplified section properties (equivalent to HSS6X2X1/8)
    b = Input("b", 152, "mm", "Section width")
    h = Input("h", 51, "mm", "Section height") 
    t = Input("t", 3.2, "mm", "Wall thickness")

    Fy = Input("F_{y}", 248, "MPa", "Material yield stress")  # ~36 ksi
    Es = Input("E", 200000, "MPa", "Modulus of elasticity")   # ~29000 ksi

    Pc = Input("\\phi_c", 0.9, "", "Resistance factor for compression")

    Heading("Section Properties")
    # Calculate section properties
    Ag = Calculation("A_{g}", 
                    (b * h - (b - 2*t) * (h - 2*t)), 
                    "mm^2", 
                    "Gross cross-sectional area")
    
    # Radius of gyration calculations
    Ix = Calculation("I_x", 
                    (b * h**3 - (b - 2*t) * (h - 2*t)**3) / 12, 
                    "mm^4", 
                    "Moment of inertia about x-axis")
    
    Iy = Calculation("I_y", 
                    (h * b**3 - (h - 2*t) * (b - 2*t)**3) / 12, 
                    "mm^4", 
                    "Moment of inertia about y-axis")
    
    rx = Calculation("r_x", sqrt(Ix / Ag), "mm", "Radius of gyration about x-axis")
    ry = Calculation("r_y", sqrt(Iy / Ag), "mm", "Radius of gyration about y-axis")
    
    # Slenderness ratios
    b_t = Calculation("\\mathrm{b/t}", (b - 2*t) / (2*t), "", "Width-to-thickness ratio")
    h_t = Calculation("\\mathrm{h/t}", (h - 2*t) / (2*t), "", "Height-to-thickness ratio")

    Heading("Buckling Properties")
    yr = Calculation(
        "\\lambda_{r}",
        1.40 * sqrt(Es / Fy),
        "",
        "Element compression slenderness limit",
        reference="AISC Table B4.1a equivalent"
    )

    y_max = Calculation(
        "\\lambda_{max}", 
        maximum(b_t, h_t), 
        "", 
        "Maximum element slenderness ratio"
    )

    KLr = Calculation(
        "\\mathrm{KL/r}",
        Kc * L * 1000 / minimum(rx, ry),  # Convert m to mm
        "",
        "Member slenderness ratio"
    )

    Heading("Compressive Strength", head_level=1)
    Fe = Calculation(
        "F_e", 
        PI**2 * Es / KLr**2, 
        "MPa", 
        "Elastic buckling stress", 
        "AISC Eq. E3-4 equivalent"
    )

    Comparison(
        y_max,
        "<",
        yr,
        true_message="Non-Slender",
        false_message="Slender",
        result_check=False,
    )

    # Non-slender section
    if y_max.result() < yr.result():
        y_crit = Calculation(
            "\\lambda_{crit}", 
            4.71 * sqrt(Es / Fy), 
            "", 
            reference="AISC Section E3 equivalent"
        )
        if KLr.result() <= y_crit.result():
            ComparisonStatement(KLr, "<=", y_crit)
            TextBlock("...Inelastic buckling controls.")
            Fcr = Calculation(
                "F_{cr}",
                Fy * 0.658 ** (Fy / Fe),
                "MPa",
                "Critical compressive stress",
                "AISC Eq. E3-2 equivalent",
            )
        else:
            ComparisonStatement(KLr, ">", y_crit)
            TextBlock("...Elastic buckling controls.")
            Fcr = Calculation(
                "F_{cr}",
                0.877 * Fe,
                "MPa",
                "Critical compressive stress",
                "AISC Eq. E3-3 equivalent",
            )

        Pn = Calculation(
            "P_n",
            Fcr * Ag / 1000,  # Convert N to kN
            "kN",
            "Nominal member compressive strength",
            "AISC Eq. E3-1 equivalent",
        )

    # Slender section handling would go here...
    else:
        TextBlock("Slender section analysis not fully implemented in this SI version.")
        # For now, use conservative approach
        Fcr = Calculation("F_{cr}", 0.6 * Fy, "MPa", "Conservative critical stress")
        Pn = Calculation("P_n", Fcr * Ag / 1000, "kN", "Conservative nominal strength")

    Heading("Member Demand vs. Capacity Check", head_level=1)
    PPn = Calculation(
        "\\phi P_n",
        Pc * Pn,
        "kN",
        "Design member compressive capacity",
        result_check=True,
    )
    Comparison(
        Pu, "<=", PPn, 
        true_message="OK", 
        false_message="ERROR", 
        result_check=True
    )

if __name__ == "__main__":
    from efficalc.report_builder import ReportBuilder
    
    builder = ReportBuilder(rectangular_hss_compression_design_si)
    builder.view_report()
