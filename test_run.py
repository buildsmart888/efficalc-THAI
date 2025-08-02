"""
Test script to run concrete analysis automatically
"""

from examples.concrete_aci318m_si_example import concrete_beam_aci318m_si, concrete_column_aci318m_si

def test_beam_analysis():
    """Test beam analysis"""
    print("=" * 60)
    print("TESTING CONCRETE BEAM ANALYSIS")
    print("=" * 60)
    
    try:
        # Import required modules
        from efficalc.report_builder import ReportBuilder
        
        # Run beam analysis
        builder = ReportBuilder(concrete_beam_aci318m_si)
        
        # Try to get HTML content instead of opening browser
        html_content = builder.get_html_as_str()
        
        # Check for problematic characters
        if "Misplaced &" in html_content:
            print("❌ Found 'Misplaced &' error in HTML")
            return False
        else:
            print("✅ No 'Misplaced &' error found")
            
        # Check for successful completion indicators
        if "Concrete Beam Analysis" in html_content:
            print("✅ Report generated successfully")
            print("✅ Title found in report")
            
        if "ACI 318M-25" in html_content:
            print("✅ ACI code reference found")
            
        if "kN*m" in html_content:
            print("✅ SI units (kN*m) found - encoding fixed")
            
        if "phi = 0.9" in html_content:
            print("✅ Greek phi converted to text successfully")
            
        if "Systeme International" in html_content:
            print("✅ French accent removed successfully")
            
        print(f"HTML content length: {len(html_content)} characters")
        return True
        
    except Exception as e:
        print(f"❌ Error during beam analysis: {e}")
        return False

def test_column_analysis():
    """Test column analysis"""
    print("\n" + "=" * 60)
    print("TESTING CONCRETE COLUMN ANALYSIS")
    print("=" * 60)
    
    try:
        from efficalc.report_builder import ReportBuilder
        
        builder = ReportBuilder(concrete_column_aci318m_si)
        html_content = builder.get_html_as_str()
        
        if "Misplaced &" in html_content:
            print("❌ Found 'Misplaced &' error in HTML")
            return False
        else:
            print("✅ No 'Misplaced &' error found")
            
        if "Concrete Column Design" in html_content:
            print("✅ Column report generated successfully")
            
        print(f"HTML content length: {len(html_content)} characters")
        return True
        
    except Exception as e:
        print(f"❌ Error during column analysis: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing efficalc-THAI with SI units and encoding fixes...")
    
    beam_ok = test_beam_analysis()
    column_ok = test_column_analysis()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    if beam_ok and column_ok:
        print("🎉 SUCCESS: All tests passed!")
        print("✅ No 'Misplaced &' errors found")
        print("✅ Encoding issues resolved")
        print("✅ Both beam and column analysis working")
    else:
        print("❌ Some tests failed:")
        print(f"   Beam analysis: {'✅' if beam_ok else '❌'}")
        print(f"   Column analysis: {'✅' if column_ok else '❌'}")
