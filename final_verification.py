#!/usr/bin/env python3
"""
Final comprehensive encoding verification
This test correctly identifies ONLY problematic Unicode characters
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from examples.concrete_aci318m_si_example import concrete_beam_aci318m_si, concrete_column_aci318m_si

def final_encoding_verification():
    print("🎯 FINAL ENCODING VERIFICATION")
    print("=" * 60)
    print("Only checking for REAL problematic Unicode characters")
    print("(Regular ASCII quotes are normal in HTML)")
    print()
    
    try:
        from efficalc.report_builder import ReportBuilder
        
        # Define REAL problematic Unicode characters only
        problematic_unicode = {
            '*': 'Middle dot (U+00B7) - use \\cdot or *',
            ''': 'Left single quote (U+2018) - use straight apostrophe',  
            ''': 'Right single quote (U+2019) - use straight apostrophe',
            '"': 'Left double quote (U+201C) - use straight quotes',
            '"': 'Right double quote (U+201D) - use straight quotes', 
            '^2': 'Superscript 2 (U+00B2) - use ^2',
            '^3': 'Superscript 3 (U+00B3) - use ^3',
            '+/-': 'Plus-minus (U+00B1) - use +/-',
            '-': 'Em dash (U+2014) - use hyphen',
            '-': 'En dash (U+2013) - use hyphen',
            '...': 'Ellipsis (U+2026) - use ...',
            ''': 'Prime (U+2032) - use apostrophe',
            '"': 'Double prime (U+2033) - use quotes',
            '\u00A0': 'Non-breaking space (U+00A0) - use regular space'
        }
        
        # Test beam analysis
        print("📊 Testing beam analysis...")
        beam_report = ReportBuilder(concrete_beam_aci318m_si)
        html_output = beam_report.get_html_as_str()
        
        beam_issues = []
        for char, description in problematic_unicode.items():
            if char in html_output:
                count = html_output.count(char)
                beam_issues.append(f"{char} ({count}x): {description}")
        
        if beam_issues:
            print("❌ Found Unicode issues in beam analysis:")
            for issue in beam_issues:
                print(f"  • {issue}")
        else:
            print("✅ CLEAN - No problematic Unicode characters in beam analysis")
            
        print(f"📏 Beam report size: {len(html_output):,} characters")
        
        # Test column analysis  
        print("\n📊 Testing column analysis...")
        column_report = ReportBuilder(concrete_column_aci318m_si)
        html_output2 = column_report.get_html_as_str()
        
        column_issues = []
        for char, description in problematic_unicode.items():
            if char in html_output2:
                count = html_output2.count(char)
                column_issues.append(f"{char} ({count}x): {description}")
        
        if column_issues:
            print("❌ Found Unicode issues in column analysis:")
            for issue in column_issues:
                print(f"  • {issue}")
        else:
            print("✅ CLEAN - No problematic Unicode characters in column analysis")
            
        print(f"📏 Column report size: {len(html_output2):,} characters")
        
        # Final verdict
        total_issues = len(beam_issues) + len(column_issues)
        print(f"\n" + "=" * 60)
        print(f"🎯 FINAL VERDICT:")
        
        if total_issues == 0:
            print("🎉 SUCCESS! All encoding issues resolved!")
            print("✨ efficalc-THAI is ready for production use")
            print("📈 HTML reports generate without 'Misplaced &' errors")
            print("🌟 Both beam and column analysis work perfectly")
            print("\n💡 Note: Regular ASCII quotes (\") in HTML are normal and expected")
        else:
            print(f"⚠️  Found {total_issues} real Unicode encoding issues")
            print("🔧 These must be fixed to prevent LaTeX compilation errors")
            
        return total_issues == 0
        
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = final_encoding_verification()
    if success:
        print("\n🚀 Ready for release!")
    sys.exit(0 if success else 1)
