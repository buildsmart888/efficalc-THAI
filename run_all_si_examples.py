#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run All efficalc-THAI SI Units Examples"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples'))

def run_all_si_examples():
    """Run all SI unit examples in the project"""
    
    print("🏗️  EFFICALC-THAI PROJECT - ALL SI UNITS EXAMPLES")
    print("=" * 80)
    print()
    
    examples = [
        {
            'name': 'Concrete Beam & Column Analysis (ACI 318M-25)',
            'description': 'Concrete beam moment capacity and column design',
            'module': 'concrete_aci318m_si_example',
            'function': 'concrete_beam_aci318m_si'
        },
        {
            'name': 'Steel HSS Compression Design',
            'description': 'Rectangular HSS column compression capacity',
            'module': 'rectangular_hss_compression_design_si',
            'function': 'rectangular_hss_compression_design_si'
        },
        {
            'name': 'Steel Beam Moment Strength',
            'description': 'W-shape beam flexural capacity analysis',
            'module': 'steel_beam_moment_strength_si',
            'function': 'steel_beam_moment_strength_si'
        },
        {
            'name': 'Steel Beam Size Optimizer',
            'description': 'Automatic selection of optimal beam size',
            'module': 'steel_beam_optimizer_si',
            'function': 'steel_beam_optimizer_si'
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['name']}")
        print(f"   Description: {example['description']}")
        
        try:
            # Import and run the example
            module = __import__(example['module'])
            func = getattr(module, example['function'])
            
            from efficalc.report_builder import ReportBuilder
            
            builder = ReportBuilder(func)
            html_content = builder.get_html_as_str()
            
            # Save HTML report
            filename = f"{example['module']}_report.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            print(f"   Status: ✅ SUCCESS")
            print(f"   Report: {filename}")
            print(f"   Size: {len(html_content):,} characters")
            
        except ImportError:
            print(f"   Status: ❌ MODULE NOT FOUND")
        except Exception as e:
            print(f"   Status: ❌ ERROR - {str(e)}")
        
        print()
    
    print("📊 SUMMARY:")
    print("   All SI unit examples completed!")
    print("   Check the generated HTML reports for detailed calculations.")
    print()
    print("🌐 Generated Reports:")
    for example in examples:
        filename = f"{example['module']}_report.html"
        if os.path.exists(filename):
            print(f"   • {filename}")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    run_all_si_examples()
