#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final verification for Unicode encoding in efficalc-THAI"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples'))

# Import the concrete example
from concrete_aci318m_si_example import Calculation
calculation = Calculation()

# Define problematic characters we want to avoid
PROBLEMATIC_CHARS = {
    '\u201c': 'Left double quote (U+201C)',  # "
    '\u201d': 'Right double quote (U+201D)', # "
    '\u2018': 'Left single quote (U+2018)',  # '
    '\u2019': 'Right single quote (U+2019)', # '
}

def check_html_for_unicode_issues(html_content, test_name):
    """Check HTML content for problematic Unicode characters"""
    print(f"\n🔍 Testing {test_name}")
    print(f"   HTML size: {len(html_content)} characters")
    
    issues_found = False
    for char, description in PROBLEMATIC_CHARS.items():
        count = html_content.count(char)
        if count > 0:
            print(f"   ❌ Found {count} instances of {description}")
            issues_found = True
    
    if not issues_found:
        print(f"   ✅ {test_name} HTML is clean!")
    
    return not issues_found

def main():
    print("🎯 Final Unicode Verification Test")
    print("=" * 50)
    
    all_clean = True
    
    try:
        # Generate HTML reports
        print("📊 Generating HTML reports...")
        
        # Test beam analysis
        html_content = calculation.beam_analysis.to_html()
        beam_clean = check_html_for_unicode_issues(html_content, "Beam Analysis")
        all_clean = all_clean and beam_clean
        
        # Test column analysis
        html_content = calculation.column_analysis.to_html()
        column_clean = check_html_for_unicode_issues(html_content, "Column Analysis")
        all_clean = all_clean and column_clean
        
    except Exception as e:
        print(f"❌ Error during HTML generation: {e}")
        all_clean = False
    
    print("\n" + "=" * 50)
    if all_clean:
        print("🎉 SUCCESS: All HTML reports are clean of problematic Unicode!")
        print("✅ The 'Misplaced &' LaTeX errors should be resolved.")
    else:
        print("❌ ISSUES FOUND: Some HTML reports still contain problematic Unicode characters.")
        print("   This may cause 'Misplaced &' errors in LaTeX/PDF generation.")
    
    return all_clean

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
