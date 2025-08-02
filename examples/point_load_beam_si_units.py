"""
Point Load Beam Moment and Deflection - SI Units Version
Using efficalc with SI units integration and forallpeople library
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from matplotlib import pyplot as plt

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

# Import SI units support
try:
    from efficalc.si_units import FORALLPEOPLE_AVAILABLE
    if FORALLPEOPLE_AVAILABLE:
        import forallpeople as si
        si.environment('default')  # Set up SI environment
        print("✅ SI units available with forallpeople")
    else:
        print("⚠️ forallpeople not available, using manual conversions")
        si = None
except ImportError:
    print("⚠️ SI units module not found, using manual conversions") 
    si = None
    FORALLPEOPLE_AVAILABLE = False

# Import steel sections (AISC data, we'll use for reference but convert to metric)
try:
    from efficalc.sections import get_aisc_wide_flange
    SECTIONS_AVAILABLE = True
except ImportError:
    SECTIONS_AVAILABLE = False
    print("⚠️ Steel sections not available")

def calculation():
    """Calculate beam moment and deflection using SI units"""

    Title("คาน Simply-Supported กับ Point Load (SI Units)")
    TextBlock(
        "คำนวณ moment และ deflection ของคานเหล็กด้วยระบบ SI units "
        "ตามมาตรฐาน metric สำหรับงานวิศวกรรมในประเทศไทย"
    )

    Heading("ข้อมูลนำเข้า (Inputs)")
    
    # Beam geometry in SI units
    L = Input("L", 6.0, "m", "ความยาวคาน")
    F = Input("F", 50, "kN", "แรงกระทำแบบจุด")
    x = Input("x", 2.0, "m", "ตำแหน่งแรงกระทำจากจุดรองรับซ้าย")
    
    # Steel section properties (metric equivalent of common sections)
    section_name = Input("section", "310x74", description="ขนาดหน้าตัดคาน (metric)")
    
    Heading("คำนวณ Moment")
    
    # Maximum moment calculation
    M_max = Calculation("M_{max}", (F * x * brackets(L - x)) / L, "kN*m", "โมเมนต์สูงสุด")
    
    # Create moment diagram
    if FORALLPEOPLE_AVAILABLE:
        TextBlock("สร้างแผนภาพ moment ด้วยระบบ SI units")
    
    figure = draw_moment_diagram_si(float(L), float(F), float(x))
    FigureFromMatplotlib(figure)

    Heading("คำนวณ Deflection")

    Heading("ระยะห่างจากจุดรองรับ", head_level=2)
    a = Calculation(
        "a",
        maximum(x, L - x),
        "m",
        "ระยะไกลจากตำแหน่งแรงกระทำไปยังจุดรองรับ",
    )
    b = Calculation(
        "b",
        L - a,
        "m", 
        "ระยะใกล้จากตำแหน่งแรงกระทำไปยังจุดรองรับ",
    )

    Heading("คุณสมบัติหน้าตัด (Section Properties)", head_level=2)
    
    # Steel properties in SI units
    E = Calculation("E", 200000, "MPa", "โมดูลัสความยืดหยุ่นของเหล็ก")
    
    # Section properties (approximate metric section)
    if section_name.get_value() == "310x74":
        # Approximate properties for 310x74 mm section
        d = Calculation("d", 308, "mm", "ความสูงหน้าตัด")
        bf = Calculation("b_f", 203, "mm", "ความกว้าง flange")
        tf = Calculation("t_f", 11.2, "mm", "ความหนา flange")
        tw = Calculation("t_w", 6.6, "mm", "ความหนา web")
        
        # Moment of inertia calculation (simplified)
        I_approx = 119e6  # mm^4 (approximate for 310x74)
        I = Calculation("I", I_approx, "mm^4", "โมเมนต์ความเฉื่อย")
    else:
        # Default section properties
        I = Calculation("I", 100e6, "mm^4", "โมเมนต์ความเฉื่อย (ประมาณ)")

    Heading("การคำนวณ Deflection", head_level=2)
    
    # Convert units for deflection calculation
    # Need to be consistent: F in N, dimensions in mm, E in MPa
    F_N = Calculation("F_N", F * 1000, "N", "แรงกระทำ (N)")
    L_mm = Calculation("L_mm", L * 1000, "mm", "ความยาวคาน (mm)")
    x_mm = Calculation("x_mm", x * 1000, "mm", "ตำแหน่งแรงกระทำ (mm)")
    a_mm = Calculation("a_mm", a * 1000, "mm", "ระยะไกล (mm)")
    b_mm = Calculation("b_mm", b * 1000, "mm", "ระยะใกล (mm)")
    
    # Maximum deflection calculation for simply supported beam with point load
    # delta_max = (F * a * b * (a + 2*b) * sqrt(3*a*(a + 2*b))) / (27 * E * I * L)
    delta_max = Calculation(
        "delta_{max}",
        (F_N * a_mm * b_mm * brackets(a_mm + 2 * b_mm) * sqrt(3 * a_mm * brackets(a_mm + 2 * b_mm)))
        / (27 * E * I * L_mm),
        "mm",
        "การโก่งตัวสูงสุด"
    )
    
    # Convert to more readable units
    delta_max_cm = Calculation(
        "delta_{max,cm}",
        delta_max / 10,
        "cm",
        "การโก่งตัวสูงสุด (cm)"
    )
    
    # Create deflection diagram
    deflection_figure = draw_deflection_diagram_si(
        float(L), float(F), float(x), float(E), float(I)
    )
    FigureFromMatplotlib(deflection_figure)
    
    # Design checks
    Heading("การตรวจสอบการออกแบบ", head_level=2)
    
    # Deflection limit check (L/250 is common)
    deflection_limit = Calculation("delta_{limit}", L * 1000 / 250, "mm", "ขีดจำกัดการโก่งตัว (L/250)")
    
    # Check ratio
    deflection_ratio = Calculation("อัตราส่วน", delta_max / deflection_limit, "", "อัตราส่วนการโก่งตัว")
    
    if float(deflection_ratio) <= 1.0:
        TextBlock("[OK] การโก่งตัวอยู่ในเกณฑ์ที่ยอมรับได้ (<= L/250)")
    else:
        TextBlock("[NG] การโก่งตัวเกินเกณฑ์ที่ยอมรับได้ (> L/250)")
    
    # Summary with SI units
    Heading("สรุปผลการคำนวณ", head_level=2)
    TextBlock(f"""
    ระบบหน่วย: SI Units (Metric)
    - ความยาวคาน: {float(L):.1f} m
    - แรงกระทำ: {float(F):.0f} kN
    - โมเมนต์สูงสุด: {float(M_max):.2f} kN*m
    - การโก่งตัวสูงสุด: {float(delta_max_cm):.2f} cm
    - อัตราส่วนการโก่งตัว: {float(deflection_ratio):.3f}
    """)

def draw_moment_diagram_si(beam_length_m: float, load_kN: float, load_position_m: float):
    """Draw moment diagram with SI units"""
    
    # Convert to consistent units for calculation
    beam_length = beam_length_m  # meters
    load = load_kN  # kN
    load_position = load_position_m  # meters
    
    # Define x values for the plot
    x_list = points_along_beam(beam_length, load_position, 50)

    # Calculate the moment for each plotted x position (kN*m)
    M_list = [
        (
            (load * x * (beam_length - load_position) / beam_length)
            if x <= load_position
            else (load * (beam_length - x) * load_position / beam_length)
        )
        for x in x_list
    ]

    # Plot the moment diagram
    fig, ax = set_up_plot_si(beam_length, "Moment (kN*m)")

    ax.plot(x_list, M_list, label="Moment Diagram", color="blue", linewidth=2)
    ax.fill_between(x_list, M_list, alpha=0.2, color="blue")

    # Mark the point load location
    if load_position in x_list:
        index_at_load = x_list.index(load_position)
        M_at_load = M_list[index_at_load]
        ax.plot(
            load_position, M_at_load, marker="o", markersize=8, 
            color="red", label=f"Point Load ({load:.0f} kN)"
        )

    # Add maximum moment annotation
    max_M = max(M_list)
    max_M_index = M_list.index(max_M)
    ax.annotate(f'M_max = {max_M:.2f} kN*m', 
                xy=(x_list[max_M_index], max_M),
                xytext=(x_list[max_M_index], max_M + max_M*0.2),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=10, ha='center')

    style_plots_si()
    return fig

def draw_deflection_diagram_si(
    beam_length_m: float, load_kN: float, load_position_m: float, E_MPa: float, I_mm4: float
):
    """Draw deflection diagram with SI units"""

    # Convert to consistent units (mm, N, MPa)
    beam_length = beam_length_m * 1000  # mm
    load = load_kN * 1000  # N
    load_position = load_position_m * 1000  # mm
    E = E_MPa  # MPa
    I = I_mm4  # mm^4

    # Define x values for the plot
    x_list_m = points_along_beam(beam_length_m, load_position_m, 100)
    x_list = [x * 1000 for x in x_list_m]  # Convert to mm

    # Calculate deflection using beam theory
    l = beam_length
    a = load_position
    b = l - a
    
    d_list = []
    for x in x_list:
        if x <= a:
            # Before the load
            d = -load * b * x * (l**2 - b**2 - x**2) / (6 * E * I * l)
        else:
            # After the load
            d = -load * a * (l - x) * (2 * l * x - a**2 - x**2) / (6 * E * I * l)
        d_list.append(d)  # deflection in mm

    # Convert back to meters for plotting
    d_list_m = [d / 1000 for d in d_list]  # Convert mm to m for plotting

    # Plot the deflection diagram
    fig, ax = set_up_plot_si(beam_length_m, "Deflection (mm)")

    ax.plot(x_list_m, d_list, label="Deflection", color="green", linewidth=2)
    ax.fill_between(x_list_m, d_list, alpha=0.2, color="green")

    # Mark the point load location
    if load_position_m in x_list_m:
        index_at_load = x_list_m.index(load_position_m)
        d_at_load = d_list[index_at_load]
        ax.plot(
            load_position_m, d_at_load, marker="o", markersize=8,
            color="red", label=f"Point Load Location"
        )

    # Find and annotate maximum deflection
    max_d = min(d_list)  # Most negative value (maximum downward deflection)
    max_d_index = d_list.index(max_d)
    ax.annotate(f'delta_max = {abs(max_d):.2f} mm', 
                xy=(x_list_m[max_d_index], max_d),
                xytext=(x_list_m[max_d_index], max_d - abs(max_d)*0.5),
                arrowprops=dict(arrowstyle='->', color='green'),
                fontsize=10, ha='center')

    style_plots_si()
    return fig

def set_up_plot_si(beam_length_m: float, y_label: str):
    """Set up plot with SI units"""
    fig, ax = plt.subplots(figsize=(12, 4))

    # Add a beam representation
    ax.plot([0, beam_length_m], [0, 0], color="black", label="Beam", linewidth=6)
    
    # Add support symbols
    support_height = 0.1
    ax.plot([0, 0], [0, -support_height], 'k-', linewidth=3)  # Left support
    ax.plot([beam_length_m, beam_length_m], [0, -support_height], 'k-', linewidth=3)  # Right support
    
    # Add triangular supports
    triangle_size = 0.05
    ax.plot([-triangle_size, triangle_size, 0, -triangle_size], 
            [-support_height, -support_height, -support_height-triangle_size, -support_height], 
            'k-', linewidth=2)
    ax.plot([beam_length_m-triangle_size, beam_length_m+triangle_size, beam_length_m, beam_length_m-triangle_size], 
            [-support_height, -support_height, -support_height-triangle_size, -support_height], 
            'k-', linewidth=2)

    # Style the plot
    plt.xlabel("Position along beam (m)")
    plt.ylabel(y_label)
    plt.title(f"Beam Analysis - Length: {beam_length_m:.1f} m")
    
    return fig, ax

def style_plots_si():
    """Style plots for SI units"""
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best')
    plt.tight_layout()

def points_along_beam(beam_length: float, load_position: float, n_steps: int):
    """Generate points along beam including load position"""
    step_size = beam_length / (n_steps - 1)
    x_list = [step * step_size for step in range(n_steps)]
    
    # Always include the load position for accurate plotting
    if load_position not in x_list:
        x_list.append(load_position)
    x_list.sort()
    return x_list

# Add SI units demonstration
def si_units_demo():
    """Demonstrate SI units integration"""
    print("\n" + "="*60)
    print("SI UNITS INTEGRATION DEMONSTRATION")
    print("="*60)
    
    if FORALLPEOPLE_AVAILABLE:
        print("✅ forallpeople library is available")
        
        # Demonstrate unit operations
        length = 6.0 * si.m
        force = 50000 * si.N  # 50 kN = 50,000 N
        
        print(f"Length: {length}")
        print(f"Force: {force}")
        print(f"Force value: {force.value} N")
        
        # Calculate moment
        moment = force * length / 4  # Simple moment calculation
        print(f"Moment: {moment}")
        print(f"Moment value: {moment.value} N*m")
        
        # Unit conversions
        length_mm = length.value * 1000  # Convert to mm manually
        print(f"Length in mm: {length_mm} mm")
        
        # Show that we have proper SI units
        print(f"SI environment loaded successfully!")
        print(f"Available units: m={si.m}, kg={si.kg}, N={si.N}")
        
    else:
        print("⚠️ forallpeople not available - using manual calculations")
        
        # Manual calculations
        length_m = 6.0
        force_kN = 50.0
        
        print(f"Length: {length_m} m")
        print(f"Force: {force_kN} kN")
        print(f"Force in N: {force_kN * 1000} N")
        
        moment_kNm = force_kN * length_m / 4
        print(f"Moment: {moment_kNm} kN*m")
        print(f"Moment in N*m: {moment_kNm * 1000} N*m")

if __name__ == "__main__":
    # Run SI units demonstration
    si_units_demo()
    
    # Run the calculation
    print("\nRunning beam calculation with SI units...")
    calculation()
    print("✅ SI units calculation completed!")
