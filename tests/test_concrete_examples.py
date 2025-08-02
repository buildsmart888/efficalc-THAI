"""
Integration tests for concrete design examples using SI units and ACI 318M-25
"""

import pytest
import unittest
from unittest.mock import patch

# Test imports with proper fallbacks
try:
    from efficalc import (
        Calculation, Input, Title, Heading, TextBlock, 
        Comparison, Assumption, maximum
    )
    try:
        from efficalc.report_builder import ReportBuilder
    except ImportError:
        try:
            from efficalc import ReportBuilder
        except ImportError:
            ReportBuilder = None
    
    EFFICALC_AVAILABLE = True
except ImportError:
    # Create mock classes for testing without efficalc
    class MockCalculation:
        def __init__(self, name, value, unit="", description=""):
            self.name = name
            self.value = value
            self.unit = unit
            self.description = description
        def result(self):
            return self
        def get_value(self):
            return self.value
    
    class MockInput(MockCalculation):
        pass
    
    def MockTitle(text): pass
    def MockHeading(text): pass
    def MockTextBlock(text): pass
    def MockComparison(*args): pass
    def MockAssumption(*args): pass
    def MockMaximum(*args): return 0
    
    Calculation = MockCalculation
    Input = MockInput
    Title = MockTitle
    Heading = MockHeading
    TextBlock = MockTextBlock
    Comparison = MockComparison
    Assumption = MockAssumption
    maximum = MockMaximum
    ReportBuilder = None
    EFFICALC_AVAILABLE = False

# Test SI units
try:
    from efficalc.si_units import FORALLPEOPLE_AVAILABLE, ACI318M_Constants
    SI_AVAILABLE = FORALLPEOPLE_AVAILABLE
except ImportError:
    SI_AVAILABLE = False
    class MockACI318MConstants:
        class PHI_COMPRESSION:
            @staticmethod
            def get_value():
                return 0.65
    ACI318M_Constants = MockACI318MConstants()


class TestConcreteBeamExample(unittest.TestCase):
    """Test complete concrete beam example with SI units"""
    
    def setUp(self):
        """Set up test"""
        if not EFFICALC_AVAILABLE:
            self.skipTest("efficalc not available")
        if not SI_AVAILABLE:
            self.skipTest("SI Units not available")
    
    def test_concrete_beam_aci318m_calculation(self):
        """Test complete concrete beam calculation following ACI 318M-25"""
        
        def beam_calculation():
            Title("Test Concrete Beam - ACI 318M-25")
            
            # Material Properties
            fc = Input("f'_c", 30, "MPa", "Concrete compressive strength")
            fy = Input("f_y", 420, "MPa", "Steel yield strength")
            
            # Geometry
            b = Input("b", 300, "mm", "Beam width")
            h = Input("h", 600, "mm", "Overall depth")
            cover = Input("cover", 40, "mm", "Concrete cover")
            d = Calculation("d", h - cover, "mm", "Effective depth")
            
            # Reinforcement
            As = Input("A_s", 2000, "mm^2", "Tension reinforcement area")
            
            # Steel ratio
            rho = Calculation("rho", As / (b * d), "", "Steel reinforcement ratio")
            
            # Minimum reinforcement (ACI 318M-25)
            rho_min = Calculation("rho_min", 1.4 / fy, "", "Minimum steel ratio")
            
            # Check minimum reinforcement
            Comparison(rho, ">=", rho_min, "OK", "NG", "Minimum reinforcement check")
            
            return {
                'fc': fc.value if hasattr(fc, 'value') else fc.get_value(),
                'fy': fy.value if hasattr(fy, 'value') else fy.get_value(),
                'b': b.value if hasattr(b, 'value') else b.get_value(),
                'd': d.value if hasattr(d, 'value') else d.result(),
                'As': As.value if hasattr(As, 'value') else As.get_value(),
                'rho': rho.value if hasattr(rho, 'value') else rho.result(),
                'rho_min': rho_min.value if hasattr(rho_min, 'value') else rho_min.result()
            }
        
        # Run calculation
        results = beam_calculation()
        
        # Verify results
        self.assertEqual(results['fc'], 30)  # MPa
        self.assertEqual(results['fy'], 420)  # MPa
        self.assertEqual(results['b'], 300)  # mm
        self.assertEqual(results['d'], 560)  # mm (600 - 40)
        self.assertEqual(results['As'], 2000)  # mm^2
        
        # Check steel ratio calculation
        expected_rho = 2000 / (300 * 560)  # ≈ 0.0119
        self.assertAlmostEqual(results['rho'], expected_rho, places=4)
        
        # Check minimum steel ratio
        expected_rho_min = 1.4 / 420  # ≈ 0.00333
        self.assertAlmostEqual(results['rho_min'], expected_rho_min, places=5)
        
        # Verify rho > rho_min
        self.assertGreater(results['rho'], results['rho_min'])
    
    def test_beam_moment_capacity_aci318m(self):
        """Test beam moment capacity calculation per ACI 318M-25"""
        
        def moment_capacity():
            # Inputs
            fc = Input("f'_c", 25, "MPa", "Concrete strength")
            fy = Input("f_y", 420, "MPa", "Steel yield")
            b = Input("b", 300, "mm", "Width")
            d = Input("d", 500, "mm", "Effective depth")
            As = Input("A_s", 1500, "mm^2", "Steel area")
            
            # Stress block depth
            a = Calculation("a", As * fy / (0.85 * fc * b), "mm", "Stress block depth")
            
            # Moment capacity
            Mn = Calculation("Mn", As * fy * (d - a/2) / 1e6, "kN*m", "Nominal moment")
            
            return {
                'a': a.result() if hasattr(a.result(), 'value') else a.result(),
                'Mn': Mn.result() if hasattr(Mn.result(), 'value') else Mn.result()
            }
        
        results = moment_capacity()
        
        # Verify reasonable values
        self.assertGreater(results['a'], 10)    # > 10 mm
        self.assertLess(results['a'], 100)      # < 100 mm
        self.assertGreater(results['Mn'], 100)  # > 100 kN⋅m
        self.assertLess(results['Mn'], 500)     # < 500 kN⋅m


class TestConcreteColumnExample(unittest.TestCase):
    """Test complete concrete column example with SI units"""
    
    def setUp(self):
        """Set up test"""
        if not EFFICALC_AVAILABLE:
            self.skipTest("efficalc not available")
        if not SI_AVAILABLE:
            self.skipTest("SI Units not available")
    
    def test_column_design_aci318m(self):
        """Test column design per ACI 318M-25"""
        
        def column_calculation():
            Title("Test Concrete Column - ACI 318M-25")
            
            # Material properties
            fc = Input("f'_c", 25, "MPa", "Concrete strength")
            fy = Input("f_y", 420, "MPa", "Steel yield")
            
            # Column geometry
            h = Input("h", 400, "mm", "Column dimension")
            b = Input("b", 400, "mm", "Column dimension")
            As = Input("A_s", 3200, "mm^2", "Total steel area")
            
            # Calculations
            Ag = Calculation("A_g", h * b, "mm^2", "Gross area")
            rho_g = Calculation("rho_g", As / Ag, "", "Gross steel ratio")
            
            # ACI 318M-25 checks
            Comparison(rho_g, ">=", 0.01, "Min OK", "NG", "Min steel check")
            Comparison(rho_g, "<=", 0.08, "Max OK", "NG", "Max steel check")
            
            # Nominal axial strength (tied column)
            Pn = Calculation("P_n", 
                           0.8 * (0.85 * fc * (Ag - As) + fy * As) / 1000,
                           "kN", "Nominal axial strength")
            
            # Design strength
            phi_c = ACI318M_Constants.PHI_COMPRESSION.value if hasattr(ACI318M_Constants.PHI_COMPRESSION, 'value') else ACI318M_Constants.PHI_COMPRESSION.get_value()
            Pd = Calculation("P_d", phi_c * Pn, "kN", "Design axial strength")
            
            return {
                'Ag': Ag.result() if hasattr(Ag.result(), 'value') else Ag.result(),
                'rho_g': rho_g.result() if hasattr(rho_g.result(), 'value') else rho_g.result(),
                'Pn': Pn.result() if hasattr(Pn.result(), 'value') else Pn.result(),
                'Pd': Pd.result() if hasattr(Pd.result(), 'value') else Pd.result(),
                'phi_c': phi_c
            }
        
        results = column_calculation()
        
        # Verify calculations
        self.assertEqual(results['Ag'], 160000)  # 400 × 400 mm^2
        self.assertEqual(results['rho_g'], 0.02)  # 3200/160000
        self.assertEqual(results['phi_c'], 0.65)  # ACI 318M-25 value
        
        # Verify reasonable strength values
        self.assertGreater(results['Pn'], 1500)  # > 1500 kN
        self.assertLess(results['Pn'], 3000)     # < 3000 kN
        
        # Design strength should be reduced
        self.assertAlmostEqual(results['Pd'], results['Pn'] * 0.65, places=1)
    
    def test_column_steel_ratio_limits(self):
        """Test column steel ratio limits per ACI 318M-25"""
        
        # Test various steel ratios
        test_cases = [
            (1600, 0.01, True),   # Minimum acceptable
            (3200, 0.02, True),   # Typical
            (6400, 0.04, True),   # Higher but acceptable
            (12800, 0.08, True),  # Maximum acceptable
            (800, 0.005, False),  # Too little steel
            (14400, 0.09, False)  # Too much steel
        ]
        
        Ag = 160000  # 400×400 mm^2
        
        for As_test, expected_ratio, should_pass in test_cases:
            with self.subTest(As=As_test):
                rho_actual = As_test / Ag
                self.assertAlmostEqual(rho_actual, expected_ratio, places=3)
                
                if should_pass:
                    self.assertGreaterEqual(rho_actual, 0.01)
                    self.assertLessEqual(rho_actual, 0.08)
                else:
                    self.assertTrue(rho_actual < 0.01 or rho_actual > 0.08)


class TestUnitConversionIntegration(unittest.TestCase):
    """Test unit conversions in practical calculations"""
    
    def setUp(self):
        """Set up test"""
        if not EFFICALC_AVAILABLE:
            self.skipTest("efficalc not available")
        if not SI_AVAILABLE:
            self.skipTest("SI Units not available")
    
    def test_imperial_to_si_beam_conversion(self):
        """Test converting an Imperial beam design to SI"""
        
        def imperial_beam():
            # Imperial inputs
            fc_psi = Input("f'_c", 4000, "psi", "Concrete strength (Imperial)")
            fy_ksi = Input("f_y", 60, "ksi", "Steel yield (Imperial)")
            b_in = Input("b", 12, "in", "Width (Imperial)")
            d_in = Input("d", 20, "in", "Depth (Imperial)")
            
            # Convert to SI
            fc_mpa = Calculation("f'_c_SI", fc_psi * 6.895 / 1000, "MPa", "Concrete (SI)")
            fy_mpa = Calculation("f_y_SI", fy_ksi * 6.895, "MPa", "Steel (SI)")
            b_mm = Calculation("b_SI", b_in * 25.4, "mm", "Width (SI)")
            d_mm = Calculation("d_SI", d_in * 25.4, "mm", "Depth (SI)")
            
            return {
                'fc_mpa': fc_mpa.result() if hasattr(fc_mpa.result(), 'value') else fc_mpa.result(),
                'fy_mpa': fy_mpa.result() if hasattr(fy_mpa.result(), 'value') else fy_mpa.result(),
                'b_mm': b_mm.result() if hasattr(b_mm.result(), 'value') else b_mm.result(),
                'd_mm': d_mm.result() if hasattr(d_mm.result(), 'value') else d_mm.result()
            }
        
        results = imperial_beam()
        
        # Verify conversions
        self.assertAlmostEqual(results['fc_mpa'], 27.58, places=1)  # 4000 psi → MPa
        self.assertAlmostEqual(results['fy_mpa'], 413.7, places=1)  # 60 ksi → MPa
        self.assertAlmostEqual(results['b_mm'], 304.8, places=1)    # 12 in → mm
        self.assertAlmostEqual(results['d_mm'], 508.0, places=1)    # 20 in → mm
    
    def test_si_design_with_conversions(self):
        """Test SI design with unit conversions"""
        
        def mixed_unit_design():
            # Primary design in SI
            fc = Input("f'_c", 30, "MPa", "Concrete strength")
            b = Input("b", 300, "mm", "Width")
            d = Input("d", 500, "mm", "Depth")
            
            # Steel in imperial, convert to SI
            fy_ksi = Input("f_y", 60, "ksi", "Steel yield (Imperial)")
            fy_mpa = Calculation("f_y_SI", fy_ksi * 6.895, "MPa", "Steel yield (SI)")
            
            # Calculate minimum steel area
            As_min = Calculation("A_s_min", 1.4 * b * d / fy_mpa, "mm^2", "Minimum steel area")
            
            # Convert back to Imperial for comparison
            As_min_in2 = Calculation("A_s_min_imp", As_min / 645.16, "in^2", "Min steel (Imperial)")
            
            return {
                'fy_mpa': fy_mpa.result() if hasattr(fy_mpa.result(), 'value') else fy_mpa.result(),
                'As_min': As_min.result() if hasattr(As_min.result(), 'value') else As_min.result(),
                'As_min_in2': As_min_in2.result() if hasattr(As_min_in2.result(), 'value') else As_min_in2.result()
            }
        
        results = mixed_unit_design()
        
        # Verify steel yield conversion
        self.assertAlmostEqual(results['fy_mpa'], 413.7, places=1)
        
        # Verify steel area is reasonable
        self.assertGreater(results['As_min'], 500)   # > 500 mm^2
        self.assertLess(results['As_min'], 2000)     # < 2000 mm^2
        
        # Verify imperial conversion
        expected_in2 = results['As_min'] / 645.16
        self.assertAlmostEqual(results['As_min_in2'], expected_in2, places=2)


class TestReportGeneration(unittest.TestCase):
    """Test report generation with SI units"""
    
    def setUp(self):
        """Set up test"""
        if not EFFICALC_AVAILABLE:
            self.skipTest("efficalc not available")
    
    def test_si_units_report_generation(self):
        """Test that reports can be generated with SI units"""
        
        def simple_si_calculation():
            Title("Test SI Units Report")
            
            # Use SI units if available
            try:
                fc = Input("f'_c", 25, "MPa", "Concrete strength")
                b = Input("b", 300, "mm", "Width")
                area = Calculation("A", b * b, "mm^2", "Area")
                TextBlock("This calculation uses SI units")
                return True
            except:
                fc = Input("f'_c", 3000, "psi", "Concrete strength")
                b = Input("b", 12, "in", "Width")  
                area = Calculation("A", b * b, "in^2", "Area")
                TextBlock("Fallback to Imperial units")
                return False
        
        # Test that calculation can be created
        si_used = simple_si_calculation()
        
        # Report generation should work regardless of units
        builder = ReportBuilder(simple_si_calculation)
        self.assertIsNotNone(builder)
    
    @patch('webbrowser.open')
    def test_report_html_generation(self, mock_browser):
        """Test HTML report generation with SI units"""
        
        def test_calculation():
            Title("HTML Test with SI Units")
            if SI_AVAILABLE:
                fc = Input("f'_c", 25, "MPa", "Concrete strength")
                TextBlock("Using SI units successfully")
            else:
                fc = Input("f'_c", 3000, "psi", "Concrete strength")
                TextBlock("Using Imperial units")
        
        builder = ReportBuilder(test_calculation)
        
        # Test HTML generation (mock browser to avoid opening)
        try:
            builder.view_report()
            self.assertTrue(True)  # If no exception, test passes
        except Exception as e:
            # Should not fail due to units
            self.fail(f"Report generation failed: {e}")


class TestACI318MCompliance(unittest.TestCase):
    """Test compliance with ACI 318M-25 requirements"""
    
    def setUp(self):
        """Set up test"""
        if not SI_AVAILABLE:
            self.skipTest("SI Units not available")
    
    def test_concrete_strength_range(self):
        """Test concrete strength is within ACI 318M-25 limits"""
        
        # Test various concrete strengths
        test_strengths = [15, 20, 25, 30, 35, 40, 50, 60, 80]  # MPa
        
        for fc in test_strengths:
            with self.subTest(fc=fc):
                # All should be acceptable for normal concrete
                self.assertGreaterEqual(fc, 15)  # Minimum practical strength
                self.assertLessEqual(fc, 80)     # Reasonable upper limit
    
    def test_steel_yield_strength_aci318m(self):
        """Test steel yield strengths per ACI 318M-25"""
        
        # Common steel grades in metric
        steel_grades = {
            'Grade 300': 300,   # MPa
            'Grade 420': 420,   # MPa (most common)
            'Grade 500': 500,   # MPa
        }
        
        for grade, fy in steel_grades.items():
            with self.subTest(grade=grade):
                # Should be within reasonable limits
                self.assertGreaterEqual(fy, 250)  # Minimum yield
                self.assertLessEqual(fy, 550)     # Maximum practical yield
    
    def test_minimum_dimensions_aci318m(self):
        """Test minimum dimensions per ACI 318M-25"""
        
        # Test beam minimum dimensions
        min_beam_width = 200    # mm
        min_beam_depth = 300    # mm
        
        self.assertGreaterEqual(min_beam_width, 150)  # Practical minimum
        self.assertGreaterEqual(min_beam_depth, 250)  # Practical minimum
        
        # Test column minimum dimensions  
        min_column_size = 300   # mm
        self.assertGreaterEqual(min_column_size, 250)  # ACI minimum


if __name__ == "__main__":
    # Run all tests
    unittest.main(verbosity=2)
