#!/usr/bin/env python3
"""
Run All SI Unit Examples - Complete Project
Execute all engineering calculations in SI units and generate comprehensive reports
"""

import subprocess
import sys
import os
from pathlib import Path

def run_python_script(script_path):
    """Run a Python script and capture output"""
    try:
        # Use the virtual environment Python if available
        python_exe = Path("D:/OneDrive - Thaniyagroup/GitHub/efficalc-THAI/.venv/Scripts/python.exe")
        if python_exe.exists():
            cmd = [str(python_exe), str(script_path)]
        else:
            cmd = [sys.executable, str(script_path)]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(script_path)
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    """Run all SI unit examples"""
    
    examples_dir = Path(__file__).parent
    
    # All SI unit examples
    si_examples = [
        "concrete_aci318m_si_example.py",
        "rectangular_hss_compression_design_si.py", 
        "steel_beam_moment_strength_si.py",
        "steel_beam_optimizer_si.py",
        "concrete_beam_neutral_axis_si_complete.py",
        "point_load_beam_moment_deflection_si.py"
    ]
    
    print("=" * 80)
    print("EFFICALC-THAI PROJECT - SI UNITS COMPREHENSIVE TEST")
    print("=" * 80)
    print()
    
    successful = []
    failed = []
    
    for i, example in enumerate(si_examples, 1):
        script_path = examples_dir / example
        
        print(f"[{i}/{len(si_examples)}] Running {example}...")
        
        if not script_path.exists():
            print(f"   ❌ File not found: {script_path}")
            failed.append((example, "File not found"))
            continue
        
        success, stdout, stderr = run_python_script(script_path)
        
        if success:
            print(f"   ✅ {example} completed successfully")
            successful.append(example)
        else:
            print(f"   ❌ {example} failed")
            if stderr:
                print(f"      Error: {stderr.strip()}")
            failed.append((example, stderr.strip() if stderr else "Unknown error"))
        
        print()
    
    # Summary
    print("=" * 80)
    print("EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Total examples: {len(si_examples)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print()
    
    if successful:
        print("✅ SUCCESSFUL CALCULATIONS:")
        for example in successful:
            print(f"   • {example}")
        print()
    
    if failed:
        print("❌ FAILED CALCULATIONS:")
        for example, error in failed:
            print(f"   • {example}")
            if error:
                print(f"     Error: {error}")
        print()
    
    # Technical summary
    print("📊 TECHNICAL SUMMARY:")
    print("   • Units System: SI (International System)")
    print("   • Force: kN (kilonewtons)")  
    print("   • Moment: kN⋅m (kilonewton-meters)")
    print("   • Stress: MPa (megapascals)")
    print("   • Length: mm, m (millimeters, meters)")
    print("   • Design Standards: ACI 318M-25, AISC (metric)")
    print()
    
    if len(successful) == len(si_examples):
        print("🎉 ALL SI UNIT EXAMPLES COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print(f"⚠️  {len(failed)} examples failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
