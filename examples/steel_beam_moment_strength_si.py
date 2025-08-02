"""
Steel Beam Moment Strength - SI Units Version
Based on AISC Steel Construction Manual principles but using metric units
"""

from efficalc import (
    PI,
    Assumption,
    Calculation,
    Comparison,
    ComparisonStatement,
    Heading,
    Input,
    Symbolic,
    TextBlock,
    Title,
    brackets,
    minimum,
    sqrt,
)

# Import SI units if available
try:
    from efficalc import (
        # SI Units
        mm, cm, m, mm2, cm2, m2, mm3, cm3,
        MPa, kPa, N, kN, kNm,
        # Conversions
        ksi_to_MPa, in_to_mm
    )
    SI_AVAILABLE = True
except ImportError:
    SI_AVAILABLE = False

def steel_beam_moment_strength_si():
    """
    Steel Beam Moment Strength using SI Units
    """
    
    if not SI_AVAILABLE:
        Title("Error: SI Units Not Available")
        TextBlock("This calculation requires 'forallpeople' library. Install with: pip install forallpeople")
        return
    
    Title("Steel Beam Moment Strength (SI Units)")
    
    TextBlock("Flexural design strength of a steel wide-flange beam section using metric units.")

    Heading("Assumptions", numbered=False)
    Assumption("AISC principles adapted for metric units")
    Assumption("Beam web is unstiffened")
    Assumption("Beam design is not controlled by deflection requirements")

    Heading("Inputs", numbered=False)

    Mu = Input("M_u", 40, "kN*m", "Beam ultimate moment demand")
    Lbu = Input("L_b", 6.0, "m", "Beam unbraced length")

    # Simplified W18X40 equivalent section properties in SI
    section_name = Input("section", "W460X60", "", "Beam section (W18X40 equivalent)")
    
    Fy = Input("F_y", 345, "MPa", "Steel yield strength")  # ~50 ksi
    Es = Input("E", 200000, "MPa", "Modulus of elasticity")  # ~29000 ksi

    Cb = Input(
        "C_b",
        1.0,
        "",
        "Lateral-torsional buckling modification factor",
        reference="AISC F1(3) equivalent"
    )

    Heading("Section Properties", numbered=False)
    Symbolic("section", "W460X60 (equivalent to W18X40)", result_check=True)
    
    # W18X40 properties converted to SI (approximate)
    Sx = Calculation("S_x", 1.05e6, "mm^3", "Section modulus")  # ~64.7 in³
    Zx = Calculation("Z_x", 1.17e6, "mm^3", "Plastic section modulus")  # ~72.9 in³
    ry = Calculation("r_{y}", 50.8, "mm", "Radius of gyration about y-axis")  # ~2.0 in
    rts = Calculation("r_{ts}", 63.5, "mm", "Effective radius of gyration")  # ~2.5 in
    J = Calculation("J", 2.67e5, "mm^4", "Torsional constant")  # ~0.65 in⁴
    ho = Calculation("h_o", 430, "mm", "Distance between flange centroids")  # ~17.0 in
    bf_2tf = Calculation("b_f/2t_f", 7.5, "", "Flange local buckling parameter")
    h_tw = Calculation("h/t_w", 35.0, "", "Web local buckling parameter")

    Heading("Beam Flexural Capacity", head_level=1)
    Pb = Calculation(
        "\\phi_{b}", 0.9, "", "Flexural resistance factor", reference="AISC F1(1) equivalent"
    )

    Heading("Section Compactness", head_level=2)
    ypf = Calculation(
        "\\lambda_{pf}", 0.38 * sqrt(Es / Fy), "", reference="AISC Table B4.1b(10) equivalent"
    )
    Comparison(
        bf_2tf,
        "<=",
        ypf,
        true_message="CompactFlange",
        false_message="ERROR:NotCompactFlange",
        result_check=False,
    )

    ypw = Calculation(
        "\\lambda_{pw}", 3.76 * sqrt(Es / Fy), "", reference="AISC Table B4.1b(15) equivalent"
    )
    Comparison(
        h_tw,
        "<=",
        ypw,
        true_message="CompactWeb",
        false_message="ERROR:NotCompactWeb",
        result_check=False,
    )

    Heading("Plastic Moment Strength", head_level=2)
    Mp = Calculation(
        "M_{p}",
        Fy * Zx / 1e6,  # Convert N*mm to kN*m
        "kN*m",
        "Nominal plastic moment strength",
        reference="AISC Eq. F2-1 equivalent",
    )

    Heading("Yielding Strength", head_level=2)
    Mny = Calculation("M_{ny}", Mp, "kN*m", reference="AISC Eq. F2-1 equivalent")

    Heading("Lateral-Torsional Buckling", head_level=2)
    Lp = Calculation(
        "L_{p}", 
        1.76 * ry * sqrt(Es / Fy) / 1000,  # Convert mm to m
        "m", 
        reference="AISC Eq. F2-5 equivalent"
    )
    
    cc = Calculation("c", 1.0, "", reference="AISC Eq. F2-8a equivalent")
    
    Lr = Calculation(
        "L_{r}",
        (1.95 * rts / 1000 * Es / (0.7 * Fy))  # Convert mm to m
        * sqrt(
            J * cc / (Sx * ho)
            + sqrt((J * cc / (Sx * ho)) ** 2 + 6.76 * (0.7 * Fy / Es) ** 2)
        ),
        "m",
        reference="AISC Eq. F2-6 equivalent",
    )

    # Convert result() calls to get_value() for proper comparison
    Lbu_val = Lbu.get_value()
    Lp_val = Lp.result()
    Lr_val = Lr.result()

    if Lbu_val <= Lp_val:
        ComparisonStatement(Lbu, "<=", Lp)
        Mnl = Calculation(
            "M_{nltb}",
            Mp,
            "kN*m",
            "The limit state of lateral-torsional buckling does not apply",
            reference="AISC F2.2(a) equivalent",
        )
    elif Lbu_val > Lr_val:
        ComparisonStatement(Lbu, ">", Lr)
        Fcr = Calculation(
            "F_{cr}",
            Cb * PI**2 * Es / (Lbu * 1000 / rts) ** 2  # Convert m to mm
            * sqrt(1 + 0.078 * J * cc / (Sx * ho) * (Lbu * 1000 / rts) ** 2),
            "MPa",
            reference="AISC Eq. F2-4 equivalent",
        )
        Mncr = Calculation(
            "M_{ncr}", Fcr * Sx / 1e6, "kN*m", reference="AISC F2.2(c) equivalent"
        )
        Mnl = Calculation(
            "M_{nltb}", minimum(Mncr, Mp), "kN*m", reference="AISC Eq. F2-3 equivalent"
        )
    else:
        ComparisonStatement(Lp, "<", Lbu, "<=", Lr)
        Mncr = Calculation(
            "M_{ncr}",
            Cb
            * brackets(
                Mp - brackets(Mp - 0.7 * Fy * Sx / 1e6) * (Lbu - Lp) / (Lr - Lp)
            ),
            "kN*m",
            reference="AISC F2.2(b) equivalent",
        )
        Mnl = Calculation(
            "M_{nltb}", minimum(Mncr, Mp), "kN*m", reference="AISC Eq. F2-2 equivalent"
        )

    Heading("Controlling Strength", head_level=2)
    PMn = Calculation(
        "\\phi M_n",
        Pb * minimum(Mny, Mnl),
        "kN*m",
        "Design flexural strength of the section",
        result_check=True,
    )
    Comparison(Mu, "<=", PMn, true_message="OK", false_message="ERROR", result_check=True)

    return {"design_strength": PMn.result(), "demand": Mu.get_value()}

if __name__ == "__main__":
    from efficalc.report_builder import ReportBuilder
    
    builder = ReportBuilder(steel_beam_moment_strength_si)
    builder.view_report()
