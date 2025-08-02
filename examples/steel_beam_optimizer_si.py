"""
Steel Beam Optimizer - SI Units Version
Find the lightest beam section that meets the moment demand using metric units
"""

from efficalc import clear_saved_objects, Title, TextBlock, Heading, Input, Calculation, Comparison, Symbolic

# Import the SI beam strength calculation
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

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

def steel_beam_optimizer_si():
    """
    Steel Beam Optimizer using SI Units
    Find the lightest W-shape beam that can carry the specified moment
    """
    
    if not SI_AVAILABLE:
        Title("Error: SI Units Not Available")
        TextBlock("This calculation requires 'forallpeople' library. Install with: pip install forallpeople")
        return
    
    Title("Steel Beam Size Optimizer (SI Units)")
    TextBlock("Automatically selects the lightest W-shape beam section that can carry the applied moment.")
    
    Heading("Design Parameters")
    Mu = Input("M_u", 80, "kN*m", "Required moment capacity")
    Lbu = Input("L_b", 4.0, "m", "Unbraced length")
    Fy = Input("F_y", 345, "MPa", "Steel yield strength")
    
    # Simplified beam database with SI equivalent sections
    beam_sections = get_si_beam_database()
    
    Heading("Optimization Process")
    TextBlock("Testing beam sections from lightest to heaviest...")
    
    # Find the optimal beam
    selected_beam = None
    final_capacity = 0
    for beam_data in beam_sections:
        section_name = beam_data['name']
        capacity = calculate_beam_capacity_si(beam_data, Lbu.get_value(), Fy.get_value())
        
        TextBlock(f"Testing {section_name}: Capacity = {capacity:.1f} kN⋅m")
        
        if capacity >= Mu.get_value():
            selected_beam = beam_data
            final_capacity = capacity
            break
    
    if selected_beam:
        Heading("Selected Beam Section")
        Symbolic("Selected_Section", selected_beam['name'], "Optimal beam size", result_check=True)
        Calculation("Section_Weight", selected_beam['weight'], "kg/m", "Weight per meter")
        Calculation("Moment_Capacity", final_capacity, "kN*m", "Design moment capacity")
        
        utilization = Mu.get_value() / final_capacity
        Calculation("Utilization", utilization * 100, "%", "Capacity utilization")
        
        Comparison(Mu, "<=", final_capacity, true_message="✅ ADEQUATE", false_message="❌ INADEQUATE", result_check=True)
        
        TextBlock(f"The {selected_beam['name']} beam weighs {selected_beam['weight']:.1f} kg/m and provides {final_capacity:.1f} kN⋅m capacity.")
        
    else:
        TextBlock("❌ No suitable beam found in the database. Consider a larger section or reduce the moment demand.")

def calculate_beam_capacity_si(beam_data, Lb, Fy):
    """
    Simplified beam capacity calculation for SI units
    This is a simplified version - actual calculations would be more complex
    """
    import math
    
    Zx = beam_data['Zx']  # mm³
    Es = 200000  # MPa
    
    # Plastic moment
    Mp = Fy * Zx / 1e6  # kN⋅m
    
    # Simplified lateral-torsional buckling check
    ry = beam_data['ry']  # mm
    Lp = 1.76 * ry * math.sqrt(Es / Fy) / 1000  # m
    
    if Lb <= Lp:
        # No LTB - full plastic capacity
        Mn = Mp
    else:
        # Simplified LTB reduction
        reduction_factor = max(0.7, Lp / Lb)
        Mn = Mp * reduction_factor
    
    # Apply resistance factor
    phi_b = 0.9
    design_capacity = phi_b * Mn
    
    return design_capacity

def get_si_beam_database():
    """
    Database of common W-shape beams with SI properties
    Sorted by weight (lightest first)
    """
    beams = [
        # Format: name, weight (kg/m), Zx (mm³), ry (mm)
        {'name': 'W200×15', 'weight': 15.0, 'Zx': 206000, 'ry': 26.2},    # ≈ W8×10
        {'name': 'W250×18', 'weight': 17.9, 'Zx': 311000, 'ry': 33.3},    # ≈ W10×12
        {'name': 'W310×21', 'weight': 20.9, 'Zx': 455000, 'ry': 39.9},    # ≈ W12×14
        {'name': 'W310×24', 'weight': 23.8, 'Zx': 544000, 'ry': 40.4},    # ≈ W12×16
        {'name': 'W310×28', 'weight': 28.3, 'Zx': 715000, 'ry': 41.1},    # ≈ W12×19
        {'name': 'W250×28', 'weight': 28.4, 'Zx': 567000, 'ry': 34.5},    # ≈ W10×19
        {'name': 'W250×33', 'weight': 32.7, 'Zx': 692000, 'ry': 35.3},    # ≈ W10×22
        {'name': 'W310×33', 'weight': 32.7, 'Zx': 872000, 'ry': 41.9},    # ≈ W12×22
        {'name': 'W360×33', 'weight': 32.9, 'Zx': 1020000, 'ry': 48.3},   # ≈ W14×22
        {'name': 'W310×39', 'weight': 38.8, 'Zx': 1050000, 'ry': 42.4},   # ≈ W12×26
        {'name': 'W360×39', 'weight': 38.8, 'Zx': 1250000, 'ry': 49.1},   # ≈ W14×26
        {'name': 'W410×39', 'weight': 38.8, 'Zx': 1430000, 'ry': 54.9},   # ≈ W16×26
        {'name': 'W360×45', 'weight': 44.5, 'Zx': 1450000, 'ry': 50.0},   # ≈ W14×30
        {'name': 'W410×46', 'weight': 46.1, 'Zx': 1690000, 'ry': 55.9},   # ≈ W16×31
        {'name': 'W360×51', 'weight': 50.7, 'Zx': 1680000, 'ry': 51.1},   # ≈ W14×34
        {'name': 'W460×52', 'weight': 52.0, 'Zx': 2040000, 'ry': 61.7},   # ≈ W18×35
        {'name': 'W410×60', 'weight': 59.5, 'Zx': 2290000, 'ry': 57.4},   # ≈ W16×40
        {'name': 'W460×60', 'weight': 60.0, 'Zx': 2520000, 'ry': 62.5},   # ≈ W18×40
        {'name': 'W530×66', 'weight': 65.4, 'Zx': 3210000, 'ry': 70.9},   # ≈ W21×44
        {'name': 'W530×72', 'weight': 71.4, 'Zx': 3630000, 'ry': 71.6},   # ≈ W21×48
        {'name': 'W530×74', 'weight': 74.4, 'Zx': 3800000, 'ry': 72.1},   # ≈ W21×50
        {'name': 'W460×82', 'weight': 81.6, 'Zx': 3960000, 'ry': 64.5},   # ≈ W18×55
        {'name': 'W530×82', 'weight': 82.0, 'Zx': 4730000, 'ry': 73.4},   # ≈ W21×55
        {'name': 'W610×82', 'weight': 82.0, 'Zx': 5210000, 'ry': 79.2},   # ≈ W24×55
        {'name': 'W530×92', 'weight': 92.4, 'Zx': 5570000, 'ry': 74.7},   # ≈ W21×62
        {'name': 'W610×92', 'weight': 92.4, 'Zx': 6140000, 'ry': 80.5},   # ≈ W24×62
        {'name': 'W530×101', 'weight': 101.0, 'Zx': 6370000, 'ry': 76.0}, # ≈ W21×68
        {'name': 'W610×101', 'weight': 101.0, 'Zx': 7060000, 'ry': 81.8}, # ≈ W24×68
        {'name': 'W610×113', 'weight': 113.0, 'Zx': 8200000, 'ry': 83.3}, # ≈ W24×76
        {'name': 'W610×125', 'weight': 125.0, 'Zx': 9380000, 'ry': 84.8}, # ≈ W24×84
        {'name': 'W690×125', 'weight': 125.0, 'Zx': 10800000, 'ry': 91.4}, # ≈ W27×84
        {'name': 'W760×134', 'weight': 134.0, 'Zx': 13400000, 'ry': 98.0}, # ≈ W30×90
        {'name': 'W760×147', 'weight': 147.0, 'Zx': 15200000, 'ry': 99.3}, # ≈ W30×99
        {'name': 'W760×161', 'weight': 161.0, 'Zx': 17100000, 'ry': 100.6}, # ≈ W30×108
        {'name': 'W760×173', 'weight': 173.0, 'Zx': 19000000, 'ry': 101.6}, # ≈ W30×116
        {'name': 'W840×176', 'weight': 176.0, 'Zx': 22600000, 'ry': 108.2}, # ≈ W33×118
        {'name': 'W840×193', 'weight': 193.0, 'Zx': 25600000, 'ry': 109.7}, # ≈ W33×130
        {'name': 'W920×201', 'weight': 201.0, 'Zx': 29200000, 'ry': 116.1}, # ≈ W36×135
        {'name': 'W840×210', 'weight': 210.0, 'Zx': 30100000, 'ry': 111.8}, # ≈ W33×141
        {'name': 'W1000×222', 'weight': 222.0, 'Zx': 37700000, 'ry': 124.7}, # ≈ W40×149
        {'name': 'W920×238', 'weight': 238.0, 'Zx': 37900000, 'ry': 118.9}, # ≈ W36×160
        {'name': 'W1000×249', 'weight': 249.0, 'Zx': 42100000, 'ry': 126.2}, # ≈ W40×167
    ]
    
    # Sort by weight to ensure lightest first
    return sorted(beams, key=lambda x: x['weight'])

if __name__ == "__main__":
    from efficalc.report_builder import ReportBuilder
    
    builder = ReportBuilder(steel_beam_optimizer_si)
    builder.view_report()
