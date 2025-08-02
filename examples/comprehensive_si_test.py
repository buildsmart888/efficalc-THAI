"""
Comprehensive SI Units Test - All Examples
Run all available SI unit examples and generate summary report
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from efficalc.report_builder import ReportBuilder
from efficalc import Title, Heading, TextBlock
import importlib

def run_comprehensive_si_test():
    """Run all SI unit examples and create comprehensive report"""
    
    Title("Comprehensive SI Units Engineering Calculations")
    TextBlock("Complete collection of structural engineering calculations using metric (SI) units")
    
    # List of all SI examples
    si_examples = [
        ("concrete_aci318m_si_example", "ACI 318M-25 Concrete Design"),
        ("rectangular_hss_compression_design_si", "Steel HSS Column Compression Design"),
        ("steel_beam_moment_strength_si", "Steel Beam Flexural Strength"),
        ("steel_beam_optimizer_si", "Steel Beam Optimization"),
        ("concrete_beam_neutral_axis_si_complete", "Concrete Beam Neutral Axis Analysis"),
        ("point_load_beam_moment_deflection_si", "Point Load Beam Analysis")
    ]
    
    successful_runs = []
    failed_runs = []
    
    for module_name, description in si_examples:
        Heading(f"{description}", head_level=1)
        
        try:
            # Import the module
            module = importlib.import_module(module_name)
            
            # Find the main function (should be module_name without _si suffix)
            function_name = module_name.replace('_si', '_si').replace('_si_complete', '_si')
            if hasattr(module, function_name):
                calculation_function = getattr(module, function_name)
            else:
                # Try variations
                possible_names = [
                    f"{module_name.replace('_si', '')}_si",
                    module_name,
                    f"{module_name}_calculation"
                ]
                calculation_function = None
                for name in possible_names:
                    if hasattr(module, name):
                        calculation_function = getattr(module, name)
                        break
                
                if not calculation_function:
                    raise AttributeError(f"No suitable function found in {module_name}")
            
            # Run the calculation
            calculation_function()
            successful_runs.append((module_name, description))
            TextBlock(f"✅ **{description}** completed successfully")
            
        except Exception as e:
            failed_runs.append((module_name, description, str(e)))
            TextBlock(f"❌ **{description}** failed: {str(e)}")
    
    # Summary section
    Heading("Execution Summary", head_level=1)
    TextBlock(f"**Total examples:** {len(si_examples)}")
    TextBlock(f"**Successful:** {len(successful_runs)}")
    TextBlock(f"**Failed:** {len(failed_runs)}")
    
    if successful_runs:
        Heading("Successful Calculations", head_level=2)
        for module_name, description in successful_runs:
            TextBlock(f"• {description} (`{module_name}.py`)")
    
    if failed_runs:
        Heading("Failed Calculations", head_level=2)
        for module_name, description, error in failed_runs:
            TextBlock(f"• {description} (`{module_name}.py`) - Error: {error}")
    
    # Technical specifications
    Heading("Technical Specifications", head_level=1)
    TextBlock("**Units System:** SI (International System of Units)")
    TextBlock("**Force Units:** kN (kilonewtons)")
    TextBlock("**Moment Units:** kN⋅m (kilonewton-meters)")
    TextBlock("**Stress Units:** MPa (megapascals)")
    TextBlock("**Length Units:** mm (millimeters), m (meters)")
    TextBlock("**Area Units:** mm² (square millimeters)")
    
    Heading("Design Standards", head_level=1)
    TextBlock("**Concrete Design:** ACI 318M-25 (Building Code Requirements for Structural Concrete - Metric)")
    TextBlock("**Steel Design:** AISC principles adapted for metric units")
    TextBlock("**Material Properties:** Metric material strengths and moduli")

if __name__ == "__main__":
    builder = ReportBuilder(run_comprehensive_si_test)
    builder.view_report()
