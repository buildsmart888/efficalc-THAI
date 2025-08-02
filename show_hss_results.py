#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Display HSS Compression Design Results in Text Format"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples'))

from rectangular_hss_compression_design_si import rectangular_hss_compression_design_si
from efficalc.report_builder import ReportBuilder

def show_calculation_summary():
    """Show a summary of the HSS compression design calculation"""
    
    print("🏗️  RECTANGULAR HSS COMPRESSION DESIGN (SI UNITS)")
    print("=" * 70)
    print()
    
    print("📋 INPUT PARAMETERS:")
    print("   • Ultimate Load (Pu):        45 kN")
    print("   • Member Length (L):         1.2 m") 
    print("   • Effective Length Factor:   1.0")
    print("   • Section Width (b):         152 mm")
    print("   • Section Height (h):        51 mm")
    print("   • Wall Thickness (t):        3.2 mm")
    print("   • Yield Stress (Fy):         248 MPa")
    print("   • Elastic Modulus (E):       200,000 MPa")
    print("   • Resistance Factor (φc):    0.9")
    print()
    
    print("🔧 SECTION PROPERTIES:")
    # Manual calculations to show results
    b, h, t = 152, 51, 3.2
    Ag = (b * h - (b - 2*t) * (h - 2*t))  # mm²
    
    Ix = (b * h**3 - (b - 2*t) * (h - 2*t)**3) / 12  # mm⁴
    Iy = (h * b**3 - (h - 2*t) * (b - 2*t)**3) / 12  # mm⁴
    
    rx = (Ix / Ag) ** 0.5  # mm
    ry = (Iy / Ag) ** 0.5  # mm
    
    print(f"   • Gross Area (Ag):           {Ag:.1f} mm²")
    print(f"   • Moment of Inertia (Ix):    {Ix:.0f} mm⁴")
    print(f"   • Moment of Inertia (Iy):    {Iy:.0f} mm⁴")
    print(f"   • Radius of Gyration (rx):   {rx:.1f} mm")
    print(f"   • Radius of Gyration (ry):   {ry:.1f} mm")
    print()
    
    print("📐 SLENDERNESS RATIOS:")
    b_t = (b - 2*t) / (2*t)
    h_t = (h - 2*t) / (2*t)
    KLr = 1.0 * 1.2 * 1000 / min(rx, ry)  # dimensionless
    
    print(f"   • Width-to-thickness (b/t):  {b_t:.1f}")
    print(f"   • Height-to-thickness (h/t): {h_t:.1f}")
    print(f"   • Member slenderness (KL/r): {KLr:.1f}")
    print()
    
    print("🔍 BUCKLING ANALYSIS:")
    Es, Fy = 200000, 248
    yr = 1.40 * (Es / Fy) ** 0.5  # Element slenderness limit
    y_max = max(b_t, h_t)
    
    print(f"   • Element slenderness limit (λr): {yr:.1f}")
    print(f"   • Maximum element slenderness:     {y_max:.1f}")
    
    if y_max < yr:
        print("   • Section classification:          Non-Slender ✅")
        
        y_crit = 4.71 * (Es / Fy) ** 0.5
        print(f"   • Critical slenderness (λcrit):    {y_crit:.1f}")
        
        Fe = 3.14159**2 * Es / KLr**2
        print(f"   • Elastic buckling stress (Fe):   {Fe:.1f} MPa")
        
        if KLr <= y_crit:
            print("   • Buckling mode:                   Inelastic")
            Fcr = Fy * 0.658 ** (Fy / Fe)
        else:
            print("   • Buckling mode:                   Elastic")
            Fcr = 0.877 * Fe
            
        print(f"   • Critical stress (Fcr):           {Fcr:.1f} MPa")
    else:
        print("   • Section classification:          Slender ⚠️")
        Fcr = 0.6 * Fy  # Conservative
        print(f"   • Conservative critical stress:    {Fcr:.1f} MPa")
    
    print()
    
    print("💪 CAPACITY RESULTS:")
    Pn = Fcr * Ag / 1000  # kN
    Pc = 0.9
    PPn = Pc * Pn  # kN
    
    print(f"   • Nominal strength (Pn):      {Pn:.1f} kN")
    print(f"   • Design capacity (φPn):      {PPn:.1f} kN")
    print(f"   • Applied load (Pu):          45.0 kN")
    print()
    
    print("✅ DESIGN CHECK:")
    if 45.0 <= PPn:
        print(f"   • Demand/Capacity ratio:      {45.0/PPn:.3f}")
        print("   • Result:                     PASS ✅")
        print("   • The member is adequate for the applied load")
    else:
        print(f"   • Demand/Capacity ratio:      {45.0/PPn:.3f}")
        print("   • Result:                     FAIL ❌") 
        print("   • The member is NOT adequate - increase size")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    try:
        show_calculation_summary()
        print()
        print("🌐 Opening detailed HTML report in browser...")
        
        # Generate and open HTML report
        builder = ReportBuilder(rectangular_hss_compression_design_si)
        builder.view_report()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
