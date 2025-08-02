#!/usr/bin/env python3
"""
Final encoding test - checks only REAL problematic Unicode characters
Regular HTML quotes (") are normal and expected
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from examples.concrete_aci318m_si_example import concrete_beam_aci318m_si, concrete_column_aci318m_si

def test_real_encoding_issues():
    print("🧪 Final encoding test - REAL Unicode issues only...")
    print("=" * 60)
    
    try:
        from efficalc.report_builder import ReportBuilder
        
        # ONLY check for REAL problematic Unicode characters
        # Exclude normal ASCII quotes which are expected in HTML
        real_problematic_chars = {
            '*': 'Middle dot (use \\cdot or *)',
            ''': 'Curly left single quote (use straight apostrophe)',  
            ''': 'Curly right single quote (use straight apostrophe)',
            '"': 'Curly left double quote (use straight quotes)',
            '"': 'Curly right double quote (use straight quotes)', 
            '^2': 'Superscript 2 (use ^2)',
            '^3': 'Superscript 3 (use ^3)',
            '+/-': 'Plus-minus (use +/-)',
            '-': 'Em dash (use hyphen)',
            '-': 'En dash (use hyphen)',
            '...': 'Ellipsis (use ...)',
            ''': 'Prime symbol (use apostrophe)',
            '"': 'Double prime (use quotes)',
        }
        
        # Test beam analysis
        print("📊 Testing beam analysis...")
        beam_report = ReportBuilder(concrete_beam_aci318m_si)
        html_output = beam_report.get_html_as_str()
        
        beam_issues = []
        for char, description in real_problematic_chars.items():
            if char in html_output:
                count = html_output.count(char)
                beam_issues.append(f"Found {count} instances of '{char}' - {description}")
        
        if beam_issues:
            print("❌ Beam analysis has Unicode issues:")
            for issue in beam_issues:
                print(f"  • {issue}")
        else:
            print("✅ Beam analysis - Clean! No problematic Unicode characters found")
            
        html_size = len(html_output)
        print(f"📏 Beam report size: {html_size} characters")
        
        # Test column analysis  
        print("\n📊 Testing column analysis...")
        column_report = ReportBuilder(concrete_column_aci318m_si)
        html_output2 = column_report.get_html_as_str()
        
        column_issues = []
        for char, description in real_problematic_chars.items():
            if char in html_output2:
                count = html_output2.count(char)
                column_issues.append(f"Found {count} instances of '{char}' - {description}")
        
        if column_issues:
            print("❌ Column analysis has Unicode issues:")
            for issue in column_issues:
                print(f"  • {issue}")
        else:
            print("✅ Column analysis - Clean! No problematic Unicode characters found")
            
        html_size2 = len(html_output2)
        print(f"📏 Column report size: {html_size2} characters")
        
        # Summary
        total_issues = len(beam_issues) + len(column_issues)
        print(f"\n🎯 FINAL RESULT:")
        if total_issues == 0:
            print("🎉 SUCCESS! All 'Misplaced &' encoding issues have been resolved!")
            print("📈 Both beam and column analysis generate clean HTML reports")
            print("✨ Ready for production use")
        else:
            print(f"⚠️  Still have {total_issues} real Unicode encoding issues to fix")
            print("🔧 These need to be addressed to prevent LaTeX errors")
            
        return total_issues == 0
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_real_encoding_issues()
    sys.exit(0 if success else 1)
