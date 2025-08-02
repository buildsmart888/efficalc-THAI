#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Display Steel Beam Optimizer Results"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples'))

from steel_beam_optimizer_si import steel_beam_optimizer_si, get_si_beam_database, calculate_beam_capacity_si
from efficalc.report_builder import ReportBuilder

def show_optimization_results():
    """Show beam optimization results in text format"""
    
    print("🔍 STEEL BEAM SIZE OPTIMIZER (SI UNITS)")
    print("=" * 70)
    print()
    
    # Design parameters
    Mu_target = 80.0  # kN⋅m
    Lb = 4.0  # m  
    Fy = 345  # MPa
    
    print("🎯 DESIGN REQUIREMENTS:")
    print(f"   • Required moment capacity:   {Mu_target} kN⋅m")
    print(f"   • Unbraced length:            {Lb} m")
    print(f"   • Steel yield strength:       {Fy} MPa")
    print()
    
    print("🔍 TESTING BEAM SECTIONS (lightest to heaviest):")
    print("-" * 70)
    
    beam_sections = get_si_beam_database()
    selected_beam = None
    final_capacity = 0
    
    for i, beam_data in enumerate(beam_sections[:15]):  # Show first 15 beams
        section_name = beam_data['name']
        weight = beam_data['weight']
        capacity = calculate_beam_capacity_si(beam_data, Lb, Fy)
        
        status = "✅ ADEQUATE" if capacity >= Mu_target else "❌ TOO SMALL"
        print(f"{i+1:2d}. {section_name:<12} | {weight:6.1f} kg/m | {capacity:6.1f} kN⋅m | {status}")
        
        if capacity >= Mu_target and selected_beam is None:
            selected_beam = beam_data
            final_capacity = capacity
            break
    
    print("-" * 70)
    print()
    
    if selected_beam:
        print("🎉 OPTIMIZATION RESULTS:")
        print(f"   • Selected beam:              {selected_beam['name']}")
        print(f"   • Weight per meter:           {selected_beam['weight']:.1f} kg/m")
        print(f"   • Design moment capacity:     {final_capacity:.1f} kN⋅m")
        
        utilization = (Mu_target / final_capacity) * 100
        print(f"   • Capacity utilization:       {utilization:.1f}%")
        
        # Calculate efficiency metrics
        total_weight_4m = selected_beam['weight'] * 4.0  # For 4m beam
        strength_to_weight = final_capacity / selected_beam['weight']
        
        print()
        print("📊 EFFICIENCY METRICS:")
        print(f"   • Total beam weight (4m):     {total_weight_4m:.1f} kg")
        print(f"   • Strength-to-weight ratio:   {strength_to_weight:.2f} kN⋅m per kg/m")
        print(f"   • Safety factor:              {final_capacity/Mu_target:.2f}x")
        
        # Show comparison with next few heavier options
        print()
        print("🔍 ALTERNATIVE OPTIONS (heavier beams):")
        for j in range(1, 4):  # Show next 3 options
            if len(beam_sections) > beam_sections.index(selected_beam) + j:
                alt_beam = beam_sections[beam_sections.index(selected_beam) + j]
                alt_capacity = calculate_beam_capacity_si(alt_beam, Lb, Fy)
                alt_utilization = (Mu_target / alt_capacity) * 100
                weight_increase = ((alt_beam['weight'] - selected_beam['weight']) / selected_beam['weight']) * 100
                
                print(f"   {j}. {alt_beam['name']:<12} | {alt_beam['weight']:6.1f} kg/m | {alt_capacity:6.1f} kN⋅m | {alt_utilization:5.1f}% | +{weight_increase:4.1f}% weight")
        
        print()
        print("✅ RECOMMENDATION:")
        print(f"   Use {selected_beam['name']} beam for optimal weight efficiency.")
        if utilization < 50:
            print("   ⚠️  Low utilization - consider reducing safety factors or loads if possible.")
        elif utilization > 85:
            print("   ⚠️  High utilization - consider next heavier section for safety margin.")
        else:
            print("   ✅ Good utilization ratio for structural design.")
            
    else:
        print("❌ NO SUITABLE BEAM FOUND:")
        print("   • All beams in database are too small")
        print("   • Consider custom sections or reduce moment demand")
        print("   • Check if moment includes appropriate load factors")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    try:
        show_optimization_results()
        print()
        print("🌐 Opening detailed HTML report in browser...")
        
        # Generate and open HTML report
        builder = ReportBuilder(steel_beam_optimizer_si)
        builder.view_report()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
