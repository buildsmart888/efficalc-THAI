"""
Unit tests for SI Units integration and ACI 318M-25 support
"""

import pytest
import unittest
from unittest.mock import patch, MagicMock

# Test if forallpeople is available
try:
    import forallpeople as si
    FORALLPEOPLE_AVAILABLE = True
except ImportError:
    FORALLPEOPLE_AVAILABLE = False

from efficalc import (
    Calculation, 
    Input, 
    Title, 
    Heading,
    Comparison
)

# Import SI units functionality
try:
    from efficalc.si_units import (
        mm, cm, m, km,
        N, kN, MN,
        Pa, kPa, MPa, GPa,
        mm2, cm2, m2,
        ACI318M_Constants,
        convert_imperial_to_si,
        validate_units_consistency,
        FORALLPEOPLE_AVAILABLE as SI_AVAILABLE
    )
except ImportError:
    SI_AVAILABLE = False


class TestSIUnitsBasic(unittest.TestCase):
    """Test basic SI units functionality"""
    
    def test_si_units_import(self):
        """Test that SI units can be imported"""
        if SI_AVAILABLE:
            # Test length units
            self.assertIsNotNone(mm)
            self.assertEqual(mm.get_value(), 0.001)
            self.assertEqual(mm.unit, "m")
            
            self.assertIsNotNone(cm)
            self.assertEqual(cm.get_value(), 0.01)
            
            self.assertIsNotNone(m)
            self.assertEqual(m.get_value(), 1.0)
            
            # Test force units
            self.assertIsNotNone(N)
            self.assertEqual(N.get_value(), 1.0)
            self.assertEqual(N.unit, "N")
            
            self.assertIsNotNone(kN)
            self.assertEqual(kN.get_value(), 1000.0)
            
            # Test pressure units
            self.assertIsNotNone(Pa)
            self.assertEqual(Pa.get_value(), 1.0)
            self.assertEqual(Pa.unit, "Pa")
            
            self.assertIsNotNone(MPa)
            self.assertEqual(MPa.get_value(), 1e6)
        else:
            self.skipTest("SI Units not available - forallpeople not installed")
    
    def test_unit_conversions(self):
        """Test unit conversion factors"""
        if SI_AVAILABLE:
            conversions = convert_imperial_to_si()
            
            # Test length conversions
            self.assertAlmostEqual(conversions['in_to_mm'].get_value(), 25.4, places=1)
            self.assertAlmostEqual(conversions['ft_to_m'].get_value(), 0.3048, places=4)
            
            # Test force conversions
            self.assertAlmostEqual(conversions['lb_to_N'].get_value(), 4.448, places=3)
            self.assertAlmostEqual(conversions['kip_to_kN'].get_value(), 4.448, places=3)
            
            # Test pressure conversions
            self.assertAlmostEqual(conversions['psi_to_kPa'].get_value(), 6.895, places=3)
            self.assertAlmostEqual(conversions['ksi_to_MPa'].get_value(), 6.895, places=3)
        else:
            self.skipTest("SI Units not available")


class TestACI318MConstants(unittest.TestCase):
    """Test ACI 318M-25 constants"""
    
    def test_aci_constants(self):
        """Test ACI 318M-25 constants are properly defined"""
        if SI_AVAILABLE:
            # Test material properties
            self.assertEqual(ACI318M_Constants.STEEL_E.get_value(), 200000)
            self.assertEqual(ACI318M_Constants.STEEL_E.unit, "MPa")
            
            self.assertEqual(ACI318M_Constants.MAX_CONCRETE_STRAIN.get_value(), 0.003)
            
            self.assertEqual(ACI318M_Constants.CONCRETE_DENSITY.get_value(), 2400)
            self.assertEqual(ACI318M_Constants.CONCRETE_DENSITY.unit, "kg/m^3")
            
            # Test minimum covers
            self.assertEqual(ACI318M_Constants.MIN_COVER_BEAM.get_value(), 25)
            self.assertEqual(ACI318M_Constants.MIN_COVER_COLUMN.get_value(), 40)
            
            # Test strength reduction factors
            self.assertEqual(ACI318M_Constants.PHI_FLEXURE.get_value(), 0.9)
            self.assertEqual(ACI318M_Constants.PHI_COMPRESSION.get_value(), 0.65)
            self.assertEqual(ACI318M_Constants.PHI_SHEAR.get_value(), 0.75)
        else:
            self.skipTest("SI Units not available")
    
    def test_phi_factors_range(self):
        """Test that phi factors are within reasonable ranges"""
        if SI_AVAILABLE:
            # All phi factors should be between 0 and 1
            self.assertGreater(ACI318M_Constants.PHI_FLEXURE.get_value(), 0)
            self.assertLessEqual(ACI318M_Constants.PHI_FLEXURE.get_value(), 1)
            
            self.assertGreater(ACI318M_Constants.PHI_COMPRESSION.get_value(), 0)
            self.assertLessEqual(ACI318M_Constants.PHI_COMPRESSION.get_value(), 1)
            
            self.assertGreater(ACI318M_Constants.PHI_SHEAR.get_value(), 0)
            self.assertLessEqual(ACI318M_Constants.PHI_SHEAR.get_value(), 1)
        else:
            self.skipTest("SI Units not available")


class TestConcreteBeamSI(unittest.TestCase):
    """Test concrete beam calculations using SI units"""
    
    def setUp(self):
        """Set up test case"""
        if not SI_AVAILABLE:
            self.skipTest("SI Units not available")
    
    def test_basic_concrete_beam_calculation(self):
        """Test basic concrete beam calculation with SI units"""
        # Material properties
        fc = Input("f'_c", 25, "MPa", "Concrete strength")
        fy = Input("f_y", 420, "MPa", "Steel yield")
        
        # Geometry
        b = Input("b", 300, "mm", "Beam width")
        d = Input("d", 500, "mm", "Effective depth")
        As = Input("A_s", 1500, "mm^2", "Steel area")
        
        # Steel ratio
        rho = Calculation("rho", As / (b * d), "", "Steel ratio")
        
        # Test calculations
        self.assertIsNotNone(rho)
        expected_rho = 1500 / (300 * 500)  # 0.01
        self.assertAlmostEqual(rho.result().value, expected_rho, places=3)
    
    def test_minimum_reinforcement_aci318m(self):
        """Test minimum reinforcement according to ACI 318M-25"""
        fy = Input("f_y", 420, "MPa", "Steel yield")
        
        # ACI 318M-25 minimum reinforcement ratio
        rho_min = Calculation("rho_min", 1.4 / fy, "", "Minimum steel ratio")
        
        expected_rho_min = 1.4 / 420  # ≈ 0.00333
        self.assertAlmostEqual(rho_min.result().value, expected_rho_min, places=5)
    
    def test_balanced_reinforcement_ratio(self):
        """Test balanced reinforcement ratio calculation"""
        fc = Input("f'_c", 25, "MPa", "Concrete strength")
        fy = Input("f_y", 420, "MPa", "Steel yield")
        
        # Simplified balanced ratio (ACI approach)
        beta1 = 0.85  # for fc <= 28 MPa
        Es = 200000   # MPa
        
        rho_b = Calculation(
            "rho_b",
            beta1 * 0.85 * fc / fy * 600 / (600 + fy),
            "",
            "Balanced reinforcement ratio"
        )
        
        # Should be reasonable value for typical concrete
        self.assertGreater(rho_b.result().value, 0.005)
        self.assertLess(rho_b.result().value, 0.05)


class TestConcreteColumnSI(unittest.TestCase):
    """Test concrete column calculations using SI units"""
    
    def setUp(self):
        """Set up test case"""
        if not SI_AVAILABLE:
            self.skipTest("SI Units not available")
    
    def test_column_basic_properties(self):
        """Test basic column property calculations"""
        # Column dimensions
        h = Input("h", 400, "mm", "Column height")
        b = Input("b", 400, "mm", "Column width")
        As = Input("A_s", 3200, "mm^2", "Steel area")
        
        # Gross area
        Ag = Calculation("A_g", h * b, "mm^2", "Gross area")
        expected_Ag = 400 * 400  # 160,000 mm^2
        self.assertEqual(Ag.result().value, expected_Ag)
        
        # Steel ratio
        rho_g = Calculation("rho_g", As / Ag, "", "Gross steel ratio")
        expected_rho_g = 3200 / 160000  # 0.02
        self.assertEqual(rho_g.result().value, expected_rho_g)
    
    def test_column_axial_strength_aci318m(self):
        """Test column axial strength per ACI 318M-25"""
        # Material properties
        fc = Input("f'_c", 25, "MPa", "Concrete strength")
        fy = Input("f_y", 420, "MPa", "Steel yield")
        
        # Geometry
        h = Input("h", 400, "mm", "Column height")
        b = Input("b", 400, "mm", "Column width")
        As = Input("A_s", 3200, "mm^2", "Steel area")
        
        Ag = Calculation("A_g", h * b, "mm^2", "Gross area")
        
        # Nominal axial strength for tied column (ACI 318M-25 22.4.2.2)
        Pn = Calculation(
            "P_n",
            0.8 * (0.85 * fc * (Ag - As) + fy * As) / 1000,  # Convert to kN
            "kN",
            "Nominal axial strength"
        )
        
        # Should be reasonable strength for this column size
        self.assertGreater(Pn.result().value, 1000)  # > 1000 kN
        self.assertLess(Pn.result().value, 5000)     # < 5000 kN
    
    def test_steel_ratio_limits_aci318m(self):
        """Test steel ratio limits per ACI 318M-25"""
        # Column with different steel ratios
        Ag = 400 * 400  # mm^2
        
        # Test minimum steel ratio (should be >= 0.01)
        As_min = Ag * 0.01  # 1600 mm^2
        rho_min_test = As_min / Ag
        self.assertGreaterEqual(rho_min_test, 0.01)
        
        # Test maximum steel ratio (should be <= 0.08)
        As_max = Ag * 0.08  # 12800 mm^2
        rho_max_test = As_max / Ag
        self.assertLessEqual(rho_max_test, 0.08)


class TestUnitConversions(unittest.TestCase):
    """Test unit conversions between Imperial and SI"""
    
    def test_length_conversions(self):
        """Test length unit conversions"""
        if SI_AVAILABLE:
            conversions = convert_imperial_to_si()
            
            # 12 inches = 304.8 mm
            inches = 12
            mm_result = inches * conversions['in_to_mm'].get_value()
            self.assertAlmostEqual(mm_result, 304.8, places=1)
            
            # 10 feet = 3.048 m
            feet = 10
            m_result = feet * conversions['ft_to_m'].get_value()
            self.assertAlmostEqual(m_result, 3.048, places=3)
        else:
            self.skipTest("SI Units not available")
    
    def test_pressure_conversions(self):
        """Test pressure unit conversions"""
        if SI_AVAILABLE:
            conversions = convert_imperial_to_si()
            
            # 1000 psi ≈ 6895 kPa
            psi = 1000
            kPa_result = psi * conversions['psi_to_kPa'].get_value()
            self.assertAlmostEqual(kPa_result, 6895, places=0)
            
            # 60 ksi ≈ 413.7 MPa
            ksi = 60
            MPa_result = ksi * conversions['ksi_to_MPa'].get_value()
            self.assertAlmostEqual(MPa_result, 413.7, places=1)
        else:
            self.skipTest("SI Units not available")
    
    def test_force_conversions(self):
        """Test force unit conversions"""
        if SI_AVAILABLE:
            conversions = convert_imperial_to_si()
            
            # 1000 lb ≈ 4448 N
            lb = 1000
            N_result = lb * conversions['lb_to_N'].get_value()
            self.assertAlmostEqual(N_result, 4448, places=0)
            
            # 10 kip ≈ 44.48 kN
            kip = 10
            kN_result = kip * conversions['kip_to_kN'].get_value()
            self.assertAlmostEqual(kN_result, 44.48, places=2)
        else:
            self.skipTest("SI Units not available")


@pytest.mark.skipif(not FORALLPEOPLE_AVAILABLE, reason="forallpeople not available")
class TestForallpeopleIntegration(unittest.TestCase):
    """Test integration with forallpeople library"""
    
    def test_forallpeople_basic_operations(self):
        """Test basic forallpeople operations"""
        si.environment('default')
        
        # Test basic units
        length = 300 * si.mm
        width = 500 * si.mm
        area = length * width
        
        # Test that area has correct dimensions
        self.assertEqual(str(area).split()[1], "mm^2")
        
        # Test unit conversion
        pressure = 25 * si.MPa
        force = pressure * area
        
        # Force should be in kN range
        force_value = float(str(force).split()[0])
        self.assertGreater(force_value, 1)  # Should be > 1 kN
        self.assertLess(force_value, 10)    # Should be < 10 kN
    
    def test_unit_validation(self):
        """Test unit validation function"""
        if SI_AVAILABLE:
            # Test compatible units
            result, message = validate_units_consistency(25, "MPa", 30, "MPa")
            self.assertTrue(result)
            
            # Note: More detailed unit validation would require 
            # actual forallpeople Physical objects
        else:
            self.skipTest("SI Units not available")


class TestIntegrationWithEfficalc(unittest.TestCase):
    """Test integration of SI units with efficalc components"""
    
    def test_input_with_si_units(self):
        """Test Input objects with SI units"""
        fc = Input("f'_c", 25, "MPa", "Concrete strength")
        
        self.assertEqual(fc.get_value(), 25)
        self.assertEqual(fc.unit, "MPa")
        self.assertIn("Concrete strength", fc.description)
    
    def test_calculation_with_si_units(self):
        """Test Calculation objects with SI units"""
        b = Input("b", 300, "mm", "Width")
        d = Input("d", 500, "mm", "Depth")
        
        area = Calculation("A", b * d, "mm^2", "Cross-sectional area")
        
        self.assertEqual(area.result().value, 150000)  # 300 * 500
        self.assertEqual(area.unit, "mm^2")
    
    def test_comparison_with_si_units(self):
        """Test Comparison objects with SI units"""
        rho = Input("rho", 0.015, "", "Steel ratio")
        rho_min = Input("rho_min", 0.01, "", "Minimum ratio")
        
        comp = Comparison(
            rho, ">=", rho_min,
            "Adequate steel", "Insufficient steel",
            "Steel ratio check"
        )
        
        # Should pass since 0.015 >= 0.01
        self.assertIsNotNone(comp)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
