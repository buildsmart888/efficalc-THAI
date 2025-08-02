"""
Working concrete design tests with proper API usage
"""

import pytest
import unittest
import sys
import os

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test imports with proper fallbacks
try:
    from efficalc import (
        Calculation, Input, Title, Heading, TextBlock, 
        Comparison, Assumption, maximum
    )
    EFFICALC_AVAILABLE = True
except ImportError:
    EFFICALC_AVAILABLE = False

# Test SI units
try:
    from efficalc.si_units import FORALLPEOPLE_AVAILABLE, ACI318M_Constants
    SI_AVAILABLE = FORALLPEOPLE_AVAILABLE
except ImportError:
    SI_AVAILABLE = False


class TestConcreteDesignSI(unittest.TestCase):
    """Test concrete design with SI units - working version"""
    
    def setUp(self):
        """Set up test"""
        if not EFFICALC_AVAILABLE:
            self.skipTest("efficalc not available")
        if not SI_AVAILABLE:
            self.skipTest("SI Units not available")
    
    def test_beam_geometry_calculation(self):
        """Test basic beam geometry calculation"""
        
        # Input values
        b = Input("b", 300, "mm", "Beam width")
        h = Input("h", 600, "mm", "Overall depth")
        cover = Input("cover", 40, "mm", "Concrete cover")
        
        # Calculate effective depth
        d = Calculation("d", h - cover, "mm", "Effective depth")
        
        # Get values
        b_val = float(b)
        h_val = float(h)
        cover_val = float(cover)
        d_val = float(d)
        
        # Verify calculations
        self.assertEqual(b_val, 300.0)
        self.assertEqual(h_val, 600.0)
        self.assertEqual(cover_val, 40.0)
        self.assertEqual(d_val, 560.0)  # 600 - 40
    
    def test_material_properties_si(self):
        """Test material properties in SI units"""
        
        # Material properties
        fc = Input("f'_c", 30, "MPa", "Concrete compressive strength")
        fy = Input("f_y", 420, "MPa", "Steel yield strength")
        
        # Get values
        fc_val = float(fc)
        fy_val = float(fy)
        
        # Verify values
        self.assertEqual(fc_val, 30.0)
        self.assertEqual(fy_val, 420.0)
        
        # Check reasonable ranges for SI units
        self.assertGreaterEqual(fc_val, 15.0)  # Minimum concrete strength
        self.assertLessEqual(fc_val, 80.0)     # Maximum practical strength
        self.assertGreaterEqual(fy_val, 250.0) # Minimum steel yield
        self.assertLessEqual(fy_val, 550.0)    # Maximum practical yield
    
    def test_steel_ratio_calculation(self):
        """Test steel reinforcement ratio calculation"""
        
        # Inputs
        As = Input("A_s", 2000, "mm^2", "Steel area")
        b = Input("b", 300, "mm", "Width")
        d = Input("d", 560, "mm", "Effective depth")
        fy = Input("f_y", 420, "MPa", "Steel yield")
        
        # Calculate steel ratio
        rho = Calculation("rho", As / (b * d), "", "Steel ratio")
        rho_min = Calculation("rho_min", 1.4 / fy, "", "Minimum steel ratio")
        
        # Get values
        rho_val = float(rho)
        rho_min_val = float(rho_min)
        
        # Verify calculations
        expected_rho = 2000.0 / (300.0 * 560.0)  # ≈ 0.0119
        expected_rho_min = 1.4 / 420.0           # ≈ 0.00333
        
        self.assertAlmostEqual(rho_val, expected_rho, places=4)
        self.assertAlmostEqual(rho_min_val, expected_rho_min, places=5)
        self.assertGreater(rho_val, rho_min_val)  # Should satisfy minimum
    
    def test_unit_conversions(self):
        """Test unit conversions between Imperial and SI"""
        
        # Imperial to SI conversions
        fc_psi = Input("f'_c", 4000, "psi", "Concrete strength (Imperial)")
        fy_ksi = Input("f_y", 60, "ksi", "Steel yield (Imperial)")
        b_in = Input("b", 12, "in", "Width (Imperial)")
        
        # Convert to SI
        fc_mpa = Calculation("f'_c_SI", fc_psi * 6.895 / 1000, "MPa", "Concrete (SI)")
        fy_mpa = Calculation("f_y_SI", fy_ksi * 6.895, "MPa", "Steel (SI)")
        b_mm = Calculation("b_SI", b_in * 25.4, "mm", "Width (SI)")
        
        # Get converted values
        fc_mpa_val = float(fc_mpa)
        fy_mpa_val = float(fy_mpa)
        b_mm_val = float(b_mm)
        
        # Verify conversions
        self.assertAlmostEqual(fc_mpa_val, 27.58, places=1)  # 4000 psi → MPa
        self.assertAlmostEqual(fy_mpa_val, 413.7, places=1)  # 60 ksi → MPa
        self.assertAlmostEqual(b_mm_val, 304.8, places=1)    # 12 in → mm
    
    def test_aci318m_constants(self):
        """Test ACI 318M-25 constants availability"""
        
        # Test phi factors
        phi_compression = ACI318M_Constants.PHI_COMPRESSION
        phi_flexure = ACI318M_Constants.PHI_FLEXURE
        phi_shear = ACI318M_Constants.PHI_SHEAR
        
        # Get values
        phi_c_val = float(phi_compression)
        phi_f_val = float(phi_flexure)
        phi_s_val = float(phi_shear)
        
        # Verify ACI 318M-25 values
        self.assertEqual(phi_c_val, 0.65)  # Compression-controlled
        self.assertEqual(phi_f_val, 0.90)  # Flexure
        self.assertEqual(phi_s_val, 0.75)  # Shear
    
    def test_concrete_strength_design(self):
        """Test concrete strength design calculations"""
        
        # Material properties
        fc = Input("f'_c", 25, "MPa", "Concrete strength")
        fy = Input("f_y", 420, "MPa", "Steel yield")
        
        # Section properties
        b = Input("b", 300, "mm", "Width")
        d = Input("d", 500, "mm", "Effective depth")
        As = Input("A_s", 1500, "mm^2", "Steel area")
        
        # Calculate stress block depth
        a = Calculation("a", As * fy / (0.85 * fc * b), "mm", "Stress block depth")
        
        # Calculate moment capacity
        Mn = Calculation("Mn", As * fy * (d - a/2) / 1e6, "kN*m", "Nominal moment")
        
        # Get values
        a_val = float(a)
        Mn_val = float(Mn)
        
        # Verify reasonable values
        self.assertGreater(a_val, 10.0)    # > 10 mm
        self.assertLess(a_val, 100.0)      # < 100 mm
        self.assertGreater(Mn_val, 100.0)  # > 100 kN⋅m
        self.assertLess(Mn_val, 500.0)     # < 500 kN⋅m
    
    def test_column_design_si(self):
        """Test column design with SI units"""
        
        # Material properties
        fc = Input("f'_c", 25, "MPa", "Concrete strength")
        fy = Input("f_y", 420, "MPa", "Steel yield")
        
        # Column geometry
        h = Input("h", 400, "mm", "Column dimension")
        b = Input("b", 400, "mm", "Column dimension")
        As = Input("A_s", 3200, "mm^2", "Total steel area")
        
        # Calculate areas and ratios
        Ag = Calculation("A_g", h * b, "mm^2", "Gross area")
        rho_g = Calculation("rho_g", As / Ag, "", "Gross steel ratio")
        
        # Get values
        Ag_val = float(Ag)
        rho_g_val = float(rho_g)
        
        # Verify calculations
        self.assertEqual(Ag_val, 160000.0)  # 400 × 400 mm^2
        self.assertEqual(rho_g_val, 0.02)   # 3200/160000
        
        # Check ACI 318M-25 limits
        self.assertGreaterEqual(rho_g_val, 0.01)  # Minimum steel ratio
        self.assertLessEqual(rho_g_val, 0.08)     # Maximum steel ratio
    
    def test_calculation_with_comparison(self):
        """Test calculations with comparison checks"""
        
        # Setup beam calculation
        fc = Input("f'_c", 30, "MPa", "Concrete strength")
        fy = Input("f_y", 420, "MPa", "Steel yield")
        As = Input("A_s", 2000, "mm^2", "Steel area")
        b = Input("b", 300, "mm", "Width")
        d = Input("d", 560, "mm", "Effective depth")
        
        # Calculate steel ratio
        rho = Calculation("rho", As / (b * d), "", "Steel ratio")
        rho_min = Calculation("rho_min", 1.4 / fy, "", "Minimum steel ratio")
        
        # Create comparison (this tests the Comparison functionality)
        comparison = Comparison(rho, ">=", rho_min, "OK", "NG", "Steel ratio check")
        
        # Get values for verification
        rho_val = float(rho)
        rho_min_val = float(rho_min)
        
        # Verify the comparison would pass
        self.assertGreaterEqual(rho_val, rho_min_val)


class TestSIUnitsIntegration(unittest.TestCase):
    """Test SI units integration with efficalc"""
    
    def test_si_units_availability(self):
        """Test that SI units are available"""
        self.assertTrue(SI_AVAILABLE, "SI units should be available")
    
    def test_aci318m_constants_complete(self):
        """Test that all required ACI 318M-25 constants are available"""
        
        if not SI_AVAILABLE:
            self.skipTest("SI Units not available")
        
        # Test all major phi factors
        constants_to_test = [
            'PHI_COMPRESSION',
            'PHI_FLEXURE', 
            'PHI_SHEAR',
            'PHI_COMPRESSION_SPIRAL'
        ]
        
        for const_name in constants_to_test:
            with self.subTest(constant=const_name):
                self.assertTrue(hasattr(ACI318M_Constants, const_name),
                               f"Missing constant: {const_name}")
                
                const_val = getattr(ACI318M_Constants, const_name)
                const_float = float(const_val)
                
                # Phi factors should be between 0.5 and 1.0
                self.assertGreaterEqual(const_float, 0.5)
                self.assertLessEqual(const_float, 1.0)
    
    def test_mixed_calculations(self):
        """Test calculations mixing efficalc and SI units"""
        
        if not EFFICALC_AVAILABLE or not SI_AVAILABLE:
            self.skipTest("Required libraries not available")
        
        # Create a mixed calculation
        fc_si = Input("f'_c", 25, "MPa", "Concrete strength")
        phi_c = ACI318M_Constants.PHI_COMPRESSION
        
        # Calculate design strength
        design_strength = Calculation("f'_c_design", fc_si * phi_c, "MPa", "Design strength")
        
        # Get result
        result = float(design_strength)
        expected = 25.0 * 0.65  # 16.25 MPa
        
        self.assertAlmostEqual(result, expected, places=2)


class TestReportGeneration(unittest.TestCase):
    """Test report generation with SI units"""
    
    def setUp(self):
        """Set up test"""
        if not EFFICALC_AVAILABLE:
            self.skipTest("efficalc not available")
    
    def test_title_and_text_creation(self):
        """Test that title and text blocks can be created"""
        
        # These should not raise exceptions
        title = Title("Test Concrete Design - ACI 318M-25")
        heading = Heading("Material Properties")
        text = TextBlock("This calculation follows ACI 318M-25 requirements.")
        
        # Test passes if no exceptions raised
        self.assertTrue(True)
    
    def test_si_calculation_elements(self):
        """Test creating calculation elements with SI units"""
        
        # Material properties in SI
        fc = Input("f'_c", 30, "MPa", "Concrete compressive strength")
        fy = Input("f_y", 420, "MPa", "Steel yield strength")
        
        # Geometry in SI
        b = Input("b", 300, "mm", "Beam width")
        h = Input("h", 600, "mm", "Overall depth")
        
        # Calculations
        area = Calculation("A", b * h, "mm^2", "Cross-sectional area")
        
        # Verify values
        self.assertEqual(float(fc), 30.0)
        self.assertEqual(float(fy), 420.0)
        self.assertEqual(float(b), 300.0)
        self.assertEqual(float(h), 600.0)
        self.assertEqual(float(area), 180000.0)  # 300 × 600


def run_concrete_tests():
    """Run all concrete design tests"""
    
    print("=" * 60)
    print("CONCRETE DESIGN TESTS WITH SI UNITS")
    print("=" * 60)
    
    # Check prerequisites
    print(f"efficalc available: {EFFICALC_AVAILABLE}")
    print(f"SI units available: {SI_AVAILABLE}")
    print()
    
    if not EFFICALC_AVAILABLE:
        print("❌ efficalc not available - skipping tests")
        return False
    
    if not SI_AVAILABLE:
        print("❌ SI units not available - skipping SI tests")
        return False
    
    # Run test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConcreteDesignSI))
    suite.addTests(loader.loadTestsFromTestCase(TestSIUnitsIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestReportGeneration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('Exception:')[-1].strip()}")
    
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == "__main__":
    success = run_concrete_tests()
    sys.exit(0 if success else 1)
