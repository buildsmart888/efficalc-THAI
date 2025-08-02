"""
This module provides a sample usage for the efficalc package with a calculation for visually testing the package.
Updated to include SI Units and ACI 318M-25 support.
"""

from efficalc import (
    Assumption,
    Calculation,
    Comparison,
    ComparisonStatement,
    FigureFromFile,
    Heading,
    Input,
    TextBlock,
    Title,
    brackets,
)
from efficalc.report_builder import ReportBuilder
from efficalc.sections import get_aisc_wide_flange
# from examples.simple.concrete_beam_neutral_axis import calculation as example_calc

# Try to import SI units - show if available
try:
    from efficalc import MPa, mm, kN
    from efficalc.si_units import FORALLPEOPLE_AVAILABLE
    SI_AVAILABLE = FORALLPEOPLE_AVAILABLE
except ImportError:
    SI_AVAILABLE = False


def calculation():
    FigureFromFile(r".\docs_src\efficalc.png")

    Title("Welcome to efficalc calculations")

    Assumption('You\'ve read the "Quickstart" guide in the project README.')
    Assumption("You've seen that we have a full documentation site.")
    Assumption("You want to make better calculations")
    
    # Show SI Units status
    if SI_AVAILABLE:
        Assumption("SI Units support is available (forallpeople library installed)")
        TextBlock("This version includes support for SI units and ACI 318M-25 metric standards!")
    else:
        Assumption("SI Units support not available (install forallpeople for metric units)")

    Heading("Inputs (Imperial Units - Original)")

    a = Input(
        "a^2_v",
        5,
        description="Names with sub and superscripts",
    )
    b = Input(
        "b_{var}",
        0.2,
        "in^2",
        "Units can also have sub and superscripts",
    )
    f = Input(
        "F_y",
        50,
        "ksi",
        "This input includes a code reference",
        reference="AISC Eq. F.2.2",
    )

    section_name = Input(
        "WF \\ Section \\ Name",
        "W18X40",
        description="Choose beam section size as your input, get the section properties below",
    )

    Heading("Section Properties")
    TextBlock("These are automatically fetched from our shapes database.")
    chosen_section_props = get_aisc_wide_flange(str(section_name.get_value()))
    Sx = Calculation("S_x", chosen_section_props.Sx, "in^3")
    Zx = Calculation("Z_x", chosen_section_props.Zx, "in^3")
    ry = Calculation("r_{y}", chosen_section_props.ry, "in")

    Heading("Calculations")

    num = Calculation(
        "num", a, "in", 'A "calculated" constant with a code reference', "AISC ref1"
    )
    short = Calculation(
        "c", a * b, "in^2", description="This is a product", result_check=True
    )
    long = Calculation(
        "long",
        a - f + brackets(b * a * f) + b - Sx - Zx - b,
        "mm^2",
        "A long calculation should still display well",
        "ASCE 7-16 Ch.8",
    )

    Heading("Comparisons (Design Checks)")

    Comparison(
        a,
        ">=",
        b,
        "Good",
        "Bad",
        "Compare two variables as a design check indicator",
        "ACI 318",
    )

    Comparison(
        f,
        "<=",
        ry,
        "Good",
        "Bad",
        "Checking that the comparison is not true (BAD)",
    )

    TextBlock("This is some text before we show a comparison statement that num=b.")
    ComparisonStatement(num, "=", b, reference="any ref 123")

    TextBlock(
        "Now we'll show that short is not long but long is greater than a. Even text blocks can have references.",
        reference="idk",
    )
    ComparisonStatement(short, "!=", long, ">", a)
    
    # Add SI Units demonstration if available
    if SI_AVAILABLE:
        si_units_demo()


def si_units_demo():
    """
    Demonstrate SI Units capabilities
    """
    Heading("SI Units Demonstration")
    
    TextBlock(
        "The following section demonstrates SI units integration with ACI 318M-25 support. "
        "This enables international compatibility and modern metric-based design."
    )
    
    Heading("Material Properties (SI Units)", head_level=2)
    
    # Concrete strength in MPa
    fc_si = Input(
        "f'_{c,SI}",
        25,
        "MPa", 
        "Concrete compressive strength (SI units)"
    )
    
    # Steel yield in MPa  
    fy_si = Input(
        "f_{y,SI}",
        420,
        "MPa",
        "Steel yield strength (SI units)"
    )
    
    Heading("Unit Conversions", head_level=2)
    
    # Show conversions
    TextBlock("Demonstrate conversion between Imperial and SI units:")
    
    # Convert ksi to MPa
    f_imperial = Input("F_{y,imp}", 60, "ksi", "Steel yield (Imperial)")
    f_metric = Calculation(
        "F_{y,metric}",
        f_imperial * 6.895,  # ksi to MPa conversion
        "MPa",
        "Steel yield converted to SI",
        reference="1 ksi = 6.895 MPa"
    )
    
    # Length conversion  
    width_imperial = Input("w_{imp}", 12, "in", "Width (Imperial)")
    width_metric = Calculation(
        "w_{metric}",
        width_imperial * 25.4,  # inches to mm
        "mm",
        "Width converted to SI",
        reference="1 in = 25.4 mm"
    )
    
    Heading("ACI 318M-25 Example", head_level=2)
    
    TextBlock("Simple reinforcement ratio calculation using metric standards:")
    
    # Basic reinforcement ratio calculation
    b_beam = Input("b_{beam}", 300, "mm", "Beam width")
    d_beam = Input("d_{beam}", 500, "mm", "Effective depth") 
    As_beam = Input("A_{s,beam}", 1500, "mm^2", "Steel area")
    
    rho_steel = Calculation(
        "\\rho_{steel}",
        As_beam / (b_beam * d_beam),
        "",
        "Steel reinforcement ratio",
        reference="ACI 318M-25 Basic principles"
    )
    
    # Check against typical minimum
    Comparison(
        rho_steel,
        ">=", 
        0.002,
        "Adequate reinforcement",
        "Check minimum requirements",
        "Minimum steel ratio check",
        reference="ACI 318M-25 guidelines"
    )


if __name__ == "__main__":
    # builder = ReportBuilder(example_calc)
    builder = ReportBuilder(calculation)
    builder.view_report()
