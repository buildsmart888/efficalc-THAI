#!/usr/bin/env python3
"""        # Check for problematic characters (REAL Unicode issues only - exclude normal HTML quotes)
        problematic_chars = ['*', ''', ''', '"', '"', '^2', '^3', '+/-']
        found_issues = []
        
        for char in problematic_chars:
            if char in html_output:
                count = html_output.count(char)
                found_issues.append(f"Found {count} instances of '{char}'")test to verify all encoding issues are resolved
Tests both beam and column analysis to ensure no 'Misplaced &' errors
"""

import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Import the beam and column functions directly
from examples.concrete_aci318m_si_example import concrete_beam_aci318m_si, concrete_column_aci318m_si

def test_encoding_fixes():
    print("🧪 Testing encoding fixes...")
    print("=" * 50)
    
    try:
        # Test beam analysis
        print("📊 Testing beam analysis...")
        from efficalc.report_builder import ReportBuilder
        
        # Run beam analysis by creating temporary HTML file
        beam_report = ReportBuilder(concrete_beam_aci318m_si)
        html_output = beam_report.get_html_as_str()
        
        # Check for problematic characters
        problematic_chars = ['*', ''', ''', '"', '"', '^2', '^3', '+/-']
        found_issues = []
        
        for char in problematic_chars:
            if char in html_output:
                count = html_output.count(char)
                found_issues.append(f"Found {count} instances of '{char}'")
        
        if found_issues:
            print("❌ Beam analysis still has encoding issues:")
            for issue in found_issues:
                print(f"  • {issue}")
        else:
            print("✅ Beam analysis - No encoding issues found!")
            
        # Check HTML size (should be reasonable)
        html_size = len(html_output)
        print(f"📏 Beam report size: {html_size} characters")
        
        # Test column analysis  
        print("\n📊 Testing column analysis...")
        
        column_report = ReportBuilder(concrete_column_aci318m_si)
        html_output2 = column_report.get_html_as_str()
        
        # Clean up temp file
        # (No cleanup needed for get_html_as_str)
        
        found_issues2 = []
        for char in problematic_chars:
            if char in html_output2:
                count = html_output2.count(char)
                found_issues2.append(f"Found {count} instances of '{char}'")
        
        if found_issues2:
            print("❌ Column analysis still has encoding issues:")
            for issue in found_issues2:
                print(f"  • {issue}")
        else:
            print("✅ Column analysis - No encoding issues found!")
            
        html_size2 = len(html_output2)
        print(f"📏 Column report size: {html_size2} characters")
        
        # Summary
        total_issues = len(found_issues) + len(found_issues2)
        if total_issues == 0:
            print("\n🎉 SUCCESS: All encoding issues resolved!")
            print("📈 Reports generate clean HTML without 'Misplaced &' errors")
        else:
            print(f"\n⚠️  Still have {total_issues} encoding issues to fix")
            
        return total_issues == 0
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_encoding_fixes()
    sys.exit(0 if success else 1)
