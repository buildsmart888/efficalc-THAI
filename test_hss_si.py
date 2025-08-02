#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test HSS Compression Design with SI Units"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples'))

try:
    from rectangular_hss_compression_design_si import rectangular_hss_compression_design_si
    from efficalc.report_builder import ReportBuilder
    
    print("🔧 Running Rectangular HSS Compression Design (SI Units)")
    print("=" * 60)
    
    builder = ReportBuilder(rectangular_hss_compression_design_si)
    html_content = builder.get_html_as_str()
    
    print(f"✅ Report generated successfully!")
    print(f"📊 HTML report size: {len(html_content)} characters")
    
    # Save to file for viewing
    with open("hss_compression_si_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("💾 Report saved as: hss_compression_si_report.html")
    print("🌐 You can open this file in your web browser")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("SI units may not be available")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
