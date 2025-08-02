#!/usr/bin/env python3
"""
Runner script for point load beam moment and deflection example
"""

import sys
import os

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the calculation function
from examples.point_load_beam_moment_and_deflection import calculation

try:
    from efficalc.report_builder import ReportBuilder
except ImportError:
    try:
        from efficalc import ReportBuilder
    except ImportError:
        print("ReportBuilder not found, running calculation only...")
        ReportBuilder = None

def main():
    """Run the point load beam calculation and generate report"""
    
    print("=" * 60)
    print("POINT LOAD BEAM MOMENT AND DEFLECTION CALCULATION")
    print("=" * 60)
    
    try:
        # Run the calculation
        print("Running calculation...")
        
        if ReportBuilder:
            # Generate and view report
            print("Generating HTML report...")
            builder = ReportBuilder(calculation)
            builder.view_report()
            print("✅ Report generated and opened in browser")
        else:
            # Just run the calculation
            calculation()
            print("✅ Calculation completed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\nCalculation Summary:")
    print("- Steel beam with point load")
    print("- Moment and deflection analysis")
    print("- AISC wide flange section")
    print("- Imperial units (ft, kips, ksi)")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
