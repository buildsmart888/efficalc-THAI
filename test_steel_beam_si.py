#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Steel Beam Moment Strength with SI Units"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples'))

try:
    from steel_beam_moment_strength_si import steel_beam_moment_strength_si
    from efficalc.report_builder import ReportBuilder
    
    print("🔧 Running Steel Beam Moment Strength (SI Units)")
    print("=" * 60)
    
    builder = ReportBuilder(steel_beam_moment_strength_si)
    html_content = builder.get_html_as_str()
    
    print(f"✅ Report generated successfully!")
    print(f"📊 HTML report size: {len(html_content)} characters")
    
    # Save to file for viewing
    with open("steel_beam_si_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("💾 Report saved as: steel_beam_si_report.html")
    print("🌐 You can open this file in your web browser")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("SI units may not be available")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
