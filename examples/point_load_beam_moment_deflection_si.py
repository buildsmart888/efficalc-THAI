"""
Point Load Beam Moment and Deflection - SI Units Version
Calculate moment and deflection of simply-supported steel beam using metric units
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from matplotlib import pyplot as plt
import numpy as np

from efficalc import (
    Calculation,
    FigureFromMatplotlib,
    Heading,
    Input,
    TextBlock,
    Title,
    brackets,
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

def point_load_beam_moment_deflection_si():
    """
    Point Load Beam Analysis using SI Units
    """
    
    if not SI_AVAILABLE:
        Title("Error: SI Units Not Available")
        TextBlock("This calculation requires 'forallpeople' library. Install with: pip install forallpeople")
        return

    Title("Beam Moment and Deflection with Point Load (SI Units)")
    TextBlock(
        "Calculate the moment and deflection demands of a simply-supported steel beam due to a point load using metric units."
    )

    Heading("Inputs")
    L = Input("L", 6.0, "m", "Beam length")  # ~20 ft
    F = Input("F", 67, "kN", "Point load force")  # ~15 kips
    x = Input("x", 1.2, "m", "Point load position along the beam")  # ~4 ft
    
    # Simplified W12×40 equivalent section properties in SI
    section_name = Input("section", "W310×60", "", "Beam section (W12×40 equivalent)")

    Heading("Moment Demand")
    M_max = Calculation(
        "M_{max}", 
        (F * x * brackets(L - x)) / L, 
        "kN*m",
        "Maximum moment in beam",
        result_check=True
    )
    
    # Create moment diagram
    figure = draw_moment_diagram_si(L.get_value(), F.get_value(), x.get_value())
    FigureFromMatplotlib(figure)

    Heading("Deflection Analysis")

    Heading("Beam and Load Dimensions", head_level=2)
    a = Calculation(
        "a",
        maximum(x, L - x),
        "m",
        "Distance from support to load (larger value)",
    )
    
    b = Calculation(
        "b",
        L - a,
        "m", 
        "Distance from load to other support",
    )

    Heading("Section Properties", head_level=2)
    # W12×40 equivalent properties in SI units
    I = Calculation("I", 162.7e6, "mm^4", "Moment of inertia")  # ~391 in⁴
    E = Calculation("E", 200000, "MPa", "Modulus of elasticity")  # ~29000 ksi

    Heading("Maximum Deflection", head_level=2)
    
    # Deflection calculation for point load on simply supported beam
    # δ = (F*a*b*(L²-a²-b²))/(6*E*I*L) when load is not at center
    
    delta_max = Calculation(
        "\\delta_{max}",
        (F * 1000 * a * 1000 * b * 1000 * (L**2 - a**2 - b**2) * 1000**2) / 
        (6 * E * I * L * 1000),  # Convert all to consistent units (N, mm)
        "mm",
        "Maximum deflection of beam",
        reference="Standard beam deflection formula",
        result_check=True
    )

    Heading("Deflection Check", head_level=2)
    # Typical deflection limit L/360 for live loads
    deflection_limit = Calculation(
        "\\delta_{limit}",
        L * 1000 / 360,  # Convert m to mm
        "mm",
        "Deflection limit (L/360)",
        reference="Typical structural limit"
    )
    
    from efficalc import Comparison
    Comparison(
        delta_max,
        "<=",
        deflection_limit,
        true_message="Deflection OK",
        false_message="Excessive deflection",
        result_check=True
    )

    Heading("Summary")
    TextBlock(f"Maximum moment: {M_max.result():.1f} kN⋅m")
    TextBlock(f"Maximum deflection: {delta_max.result():.2f} mm")
    TextBlock(f"Deflection limit: {deflection_limit.result():.1f} mm")

def draw_moment_diagram_si(L, F, x):
    """Draw moment diagram for point load on simply supported beam (SI units)"""
    
    # Calculate reactions
    R1 = F * (L - x) / L  # Reaction at left support
    R2 = F * x / L        # Reaction at right support
    
    # Create position array
    positions = np.linspace(0, L, 100)
    moments = np.zeros_like(positions)
    
    # Calculate moments
    for i, pos in enumerate(positions):
        if pos <= x:
            moments[i] = R1 * pos
        else:
            moments[i] = R1 * pos - F * (pos - x)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot moment diagram
    ax.plot(positions, moments, 'b-', linewidth=2, label='Moment')
    ax.fill_between(positions, moments, alpha=0.3, color='blue')
    
    # Mark maximum moment point
    max_moment = F * x * (L - x) / L
    ax.plot(x, max_moment, 'ro', markersize=8, label=f'Max M = {max_moment:.1f} kN⋅m')
    
    # Add labels and formatting
    ax.set_xlabel('Position along beam (m)')
    ax.set_ylabel('Moment (kN⋅m)')
    ax.set_title('Bending Moment Diagram')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Add load and support annotations
    ax.annotate(f'F = {F} kN', xy=(x, max_moment), xytext=(x, max_moment + max_moment*0.2),
                arrowprops=dict(arrowstyle='->', color='red'), 
                ha='center', fontsize=10, color='red')
    
    # Mark supports
    ax.plot([0, L], [0, 0], 'ks', markersize=8, label='Supports')
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    from efficalc.report_builder import ReportBuilder
    
    builder = ReportBuilder(point_load_beam_moment_deflection_si)
    builder.view_report()
