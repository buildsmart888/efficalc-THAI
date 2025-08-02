#!/usr/bin/env python3
"""
Comprehensive Test Runner for SI Unit Examples
Runs all unit tests, integration tests, and validation tests
"""

import unittest
import sys
import os
import time
from pathlib import Path
from io import StringIO

def run_test_file(test_file_path):
    """Run a specific test file and capture results"""
    try:
        # Import and run the test module
        spec = importlib.util.spec_from_file_location("test_module", test_file_path)
        test_module = importlib.util.module_from_spec(spec)
        
        # Capture output
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_capture = StringIO()
        stderr_capture = StringIO()
        
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        
        try:
            spec.loader.exec_module(test_module)
            
            # Run tests
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(test_module)
            runner = unittest.TextTestRunner(stream=stdout_capture, verbosity=2)
            result = runner.run(suite)
            
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
        return {
            'success': result.wasSuccessful(),
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'stdout': stdout_capture.getvalue(),
            'stderr': stderr_capture.getvalue()
        }
        
    except Exception as e:
        return {
            'success': False,
            'tests_run': 0,
            'failures': 0,
            'errors': 1,
            'stdout': '',
            'stderr': str(e)
        }

def main():
    """Run comprehensive test suite"""
    
    print("=" * 80)
    print("EFFICALC-THAI SI UNITS - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print()
    
    # Test files to run
    test_files = [
        "test_si_examples.py",
        "test_engineering_scenarios.py", 
        "test_performance_validation.py"
    ]
    
    examples_dir = Path(__file__).parent
    results = {}
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    start_time = time.time()
    
    # Run each test file
    for i, test_file in enumerate(test_files, 1):
        test_path = examples_dir / test_file
        
        print(f"[{i}/{len(test_files)}] Running {test_file}...")
        print("-" * 60)
        
        if not test_path.exists():
            print(f"❌ Test file not found: {test_path}")
            results[test_file] = {
                'success': False,
                'tests_run': 0,
                'failures': 0,
                'errors': 1,
                'message': 'File not found'
            }
            continue
        
        # Run tests using subprocess to avoid import conflicts
        import subprocess
        try:
            # Use the virtual environment Python if available
            python_exe = Path("D:/OneDrive - Thaniyagroup/GitHub/efficalc-THAI/.venv/Scripts/python.exe")
            if python_exe.exists():
                cmd = [str(python_exe), str(test_path)]
            else:
                cmd = [sys.executable, str(test_path)]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(examples_dir),
                timeout=60  # 60 second timeout
            )
            
            if result.returncode == 0:
                print("✅ Tests completed successfully")
                results[test_file] = {
                    'success': True,
                    'tests_run': 'N/A',
                    'failures': 0,
                    'errors': 0,
                    'message': 'All tests passed'
                }
            else:
                print("❌ Tests failed")
                print("STDERR:", result.stderr[:500])  # First 500 chars
                results[test_file] = {
                    'success': False,
                    'tests_run': 'N/A',
                    'failures': 1,
                    'errors': 0,
                    'message': result.stderr[:200] if result.stderr else 'Unknown error'
                }
                
        except subprocess.TimeoutExpired:
            print("❌ Tests timed out (> 60 seconds)")
            results[test_file] = {
                'success': False,
                'tests_run': 0,
                'failures': 0,
                'errors': 1,
                'message': 'Timeout'
            }
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            results[test_file] = {
                'success': False,
                'tests_run': 0,
                'failures': 0,
                'errors': 1,
                'message': str(e)
            }
        
        print()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Summary
    print("=" * 80)
    print("TEST EXECUTION SUMMARY")
    print("=" * 80)
    
    successful_files = sum(1 for r in results.values() if r['success'])
    failed_files = len(test_files) - successful_files
    
    print(f"Total test files: {len(test_files)}")
    print(f"Successful: {successful_files}")
    print(f"Failed: {failed_files}")
    print(f"Execution time: {execution_time:.2f} seconds")
    print()
    
    # Detailed results
    for test_file, result in results.items():
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status} {test_file}")
        if not result['success']:
            print(f"    Error: {result['message']}")
    
    print()
    
    # Test categories summary
    print("📊 TEST CATEGORIES COVERED:")
    print("   • Unit Tests: Import verification, function testing")
    print("   • Integration Tests: Real-world engineering scenarios")
    print("   • Performance Tests: Execution speed, repeatability")
    print("   • Validation Tests: Calculation accuracy verification")
    print("   • Edge Cases: Boundary conditions, extreme values")
    print("   • Units Tests: SI unit consistency validation")
    print()
    
    # Engineering scenarios tested
    print("🏗️  ENGINEERING SCENARIOS TESTED:")
    print("   • Office building floor beams")
    print("   • Residential garage beams")
    print("   • Warehouse heavy load beams")
    print("   • Crane runway beams")
    print("   • Equipment platform beams")
    print("   • Light and heavy HSS columns")
    print("   • Residential and commercial concrete beams")
    print()
    
    # Technical validation
    print("🔬 TECHNICAL VALIDATIONS:")
    print("   • Steel beam capacity calculations")
    print("   • Concrete neutral axis analysis")
    print("   • HSS compression member design")
    print("   • Point load beam analysis")
    print("   • Force equilibrium verification")
    print("   • Unit consistency checking")
    print()
    
    if successful_files == len(test_files):
        print("🎉 ALL TEST SUITES COMPLETED SUCCESSFULLY!")
        print("✅ SI Unit calculations validated and ready for production use")
        return 0
    else:
        print(f"⚠️  {failed_files} test suites failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    import importlib.util
    exit_code = main()
    sys.exit(exit_code)
