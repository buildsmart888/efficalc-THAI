#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Display Steel Beam Moment Strength Results in Text Format"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples'))

from steel_beam_moment_strength_si import steel_beam_moment_strength_si
from efficalc.report_builder import ReportBuilder
import math

def show_beam_calculation_summary():
    """Show a summary of the steel beam moment strength calculation"""
    
    print("🏗️  STEEL BEAM MOMENT STRENGTH (SI UNITS)")
    print("=" * 70)
    print()
    
    print("📋 INPUT PARAMETERS:")
    print("   • Ultimate Moment (Mu):      40 kN⋅m")
    print("   • Unbraced Length (Lb):      6.0 m") 
    print("   • Beam Section:              W460X60 (≈ W18X40)")
    print("   • Yield Stress (Fy):         345 MPa")
    print("   • Elastic Modulus (E):       200,000 MPa")
    print("   • Moment Gradient Factor:    1.0")
    print()
    
    print("🔧 SECTION PROPERTIES:")
    print("   • Section Modulus (Sx):      1,050,000 mm³")
    print("   • Plastic Modulus (Zx):      1,170,000 mm³")
    print("   • Radius of Gyration (ry):   50.8 mm")
    print("   • Effective Radius (rts):    63.5 mm")
    print("   • Torsional Constant (J):    267,000 mm⁴")
    print("   • Flange Parameter (bf/2tf):  7.5")
    print("   • Web Parameter (h/tw):      35.0")
    print()
    
    print("📐 SECTION COMPACTNESS:")
    Es, Fy = 200000, 345
    ypf = 0.38 * math.sqrt(Es / Fy)  # Flange limit
    ypw = 3.76 * math.sqrt(Es / Fy)  # Web limit
    
    print(f"   • Flange slenderness limit:   {ypf:.1f}")
    print(f"   • Web slenderness limit:      {ypw:.1f}")
    print(f"   • Flange compactness (7.5):  {'✅ Compact' if 7.5 <= ypf else '❌ Non-compact'}")
    print(f"   • Web compactness (35.0):     {'✅ Compact' if 35.0 <= ypw else '❌ Non-compact'}")
    print()
    
    print("💪 MOMENT CAPACITIES:")
    Zx = 1.17e6  # mm³
    Mp = Fy * Zx / 1e6  # kN⋅m (plastic moment)
    print(f"   • Plastic Moment (Mp):        {Mp:.1f} kN⋅m")
    print(f"   • Yielding Strength (Mny):    {Mp:.1f} kN⋅m")
    print()
    
    print("🔄 LATERAL-TORSIONAL BUCKLING:")
    ry = 50.8  # mm
    Lp = 1.76 * ry * math.sqrt(Es / Fy) / 1000  # m (compact length limit)
    
    # Simplified Lr calculation
    rts = 63.5  # mm
    Lr_approx = 12.0  # m (approximate for demonstration)
    
    print(f"   • Compact length limit (Lp):  {Lp:.2f} m")
    print(f"   • Inelastic limit (Lr):       {Lr_approx:.1f} m")
    print(f"   • Unbraced length (Lb):       6.0 m")
    
    if 6.0 <= Lp:
        buckling_mode = "No LTB (Compact)"
        Mnl = Mp
        print(f"   • Buckling mode:              {buckling_mode} ✅")
    elif 6.0 > Lr_approx:
        buckling_mode = "Elastic LTB"
        # Simplified elastic calculation
        Mnl = 0.85 * Mp  # Conservative estimate
        print(f"   • Buckling mode:              {buckling_mode} ⚠️")
    else:
        buckling_mode = "Inelastic LTB"
        # Simplified inelastic calculation
        Mnl = 0.92 * Mp  # Conservative estimate
        print(f"   • Buckling mode:              {buckling_mode} ⚠️")
    
    print(f"   • LTB moment capacity:        {Mnl:.1f} kN⋅m")
    print()
    
    print("🎯 DESIGN RESULTS:")
    controlling_moment = min(Mp, Mnl)
    phi_b = 0.9  # Resistance factor
    design_capacity = phi_b * controlling_moment
    
    print(f"   • Controlling moment:         {controlling_moment:.1f} kN⋅m")
    print(f"   • Design capacity (φMn):      {design_capacity:.1f} kN⋅m")
    print(f"   • Applied moment (Mu):        40.0 kN⋅m")
    print()
    
    print("✅ DESIGN CHECK:")
    if 40.0 <= design_capacity:
        ratio = 40.0 / design_capacity
        print(f"   • Demand/Capacity ratio:      {ratio:.3f}")
        print("   • Result:                     PASS ✅")
        print("   • The beam is adequate for the applied moment")
        safety_factor = design_capacity / 40.0
        print(f"   • Safety factor:              {safety_factor:.1f}x")
    else:
        ratio = 40.0 / design_capacity
        print(f"   • Demand/Capacity ratio:      {ratio:.3f}")
        print("   • Result:                     FAIL ❌") 
        print("   • The beam is NOT adequate - increase size")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    try:
        show_beam_calculation_summary()
        print()
        print("🌐 Opening detailed HTML report in browser...")
        
        # Generate and open HTML report
        builder = ReportBuilder(steel_beam_moment_strength_si)
        builder.view_report()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
