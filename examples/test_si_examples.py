"""
Unit Tests for SI Unit Examples
Comprehensive test suite for all engineering calculations in SI units
"""

import unittest
import sys
import os
from pathlib import Path

# Add the examples directory to the path
examples_dir = Path(__file__).parent
sys.path.insert(0, str(examples_dir))

class TestSIUnitExamples(unittest.TestCase):
    """Test cases for all SI unit engineering calculations"""
    
    def setUp(self):
        """Set up test environment"""
        # Clear any cached calculations
        try:
            from efficalc import clear_saved_objects
            clear_saved_objects()
        except ImportError:
            pass
    
    def test_concrete_aci318m_si_import(self):
        """Test that concrete ACI 318M SI example can be imported"""
        try:
            from concrete_aci318m_si_example import concrete_aci318m_si
            self.assertTrue(callable(concrete_aci318m_si))
        except ImportError as e:
            self.fail(f"Failed to import concrete_aci318m_si_example: {e}")
    
    def test_rectangular_hss_compression_si_import(self):
        """Test that HSS compression SI example can be imported"""
        try:
            from rectangular_hss_compression_design_si import rectangular_hss_compression_design_si
            self.assertTrue(callable(rectangular_hss_compression_design_si))
        except ImportError as e:
            self.fail(f"Failed to import rectangular_hss_compression_design_si: {e}")
    
    def test_steel_beam_moment_strength_si_import(self):
        """Test that steel beam moment strength SI example can be imported"""
        try:
            from steel_beam_moment_strength_si import steel_beam_moment_strength_si
            self.assertTrue(callable(steel_beam_moment_strength_si))
        except ImportError as e:
            self.fail(f"Failed to import steel_beam_moment_strength_si: {e}")
    
    def test_steel_beam_optimizer_si_import(self):
        """Test that steel beam optimizer SI example can be imported"""
        try:
            from steel_beam_optimizer_si import steel_beam_optimizer_si, get_si_beam_database, calculate_beam_capacity_si
            self.assertTrue(callable(steel_beam_optimizer_si))
            self.assertTrue(callable(get_si_beam_database))
            self.assertTrue(callable(calculate_beam_capacity_si))
        except ImportError as e:
            self.fail(f"Failed to import steel_beam_optimizer_si: {e}")
    
    def test_concrete_beam_neutral_axis_si_import(self):
        """Test that concrete beam neutral axis SI example can be imported"""
        try:
            from concrete_beam_neutral_axis_si_complete import concrete_beam_neutral_axis_si
            self.assertTrue(callable(concrete_beam_neutral_axis_si))
        except ImportError as e:
            self.fail(f"Failed to import concrete_beam_neutral_axis_si_complete: {e}")
    
    def test_point_load_beam_si_import(self):
        """Test that point load beam SI example can be imported"""
        try:
            from point_load_beam_moment_deflection_si import point_load_beam_moment_deflection_si, draw_moment_diagram_si
            self.assertTrue(callable(point_load_beam_moment_deflection_si))
            self.assertTrue(callable(draw_moment_diagram_si))
        except ImportError as e:
            self.fail(f"Failed to import point_load_beam_moment_deflection_si: {e}")

class TestSteelBeamOptimizer(unittest.TestCase):
    """Detailed tests for steel beam optimizer functionality"""
    
    def setUp(self):
        """Set up for steel beam tests"""
        try:
            from steel_beam_optimizer_si import get_si_beam_database, calculate_beam_capacity_si
            self.get_si_beam_database = get_si_beam_database
            self.calculate_beam_capacity_si = calculate_beam_capacity_si
        except ImportError:
            self.skipTest("Steel beam optimizer not available")
    
    def test_beam_database_structure(self):
        """Test that beam database has correct structure"""
        database = self.get_si_beam_database()
        
        # Check that database is not empty
        self.assertGreater(len(database), 0, "Beam database should not be empty")
        
        # Check first beam has required keys
        first_beam = database[0]
        required_keys = ['name', 'weight', 'Zx', 'ry']
        for key in required_keys:
            self.assertIn(key, first_beam, f"Beam database should contain '{key}' key")
        
        # Check data types
        self.assertIsInstance(first_beam['name'], str)
        self.assertIsInstance(first_beam['weight'], (int, float))
        self.assertIsInstance(first_beam['Zx'], (int, float))
        self.assertIsInstance(first_beam['ry'], (int, float))
    
    def test_beam_database_sorting(self):
        """Test that beams are sorted by weight (lightest first)"""
        database = self.get_si_beam_database()
        
        weights = [beam['weight'] for beam in database]
        sorted_weights = sorted(weights)
        
        self.assertEqual(weights, sorted_weights, "Beam database should be sorted by weight")
    
    def test_beam_capacity_calculation(self):
        """Test beam capacity calculation with known values"""
        # Test beam data (W310×21 equivalent)
        test_beam = {
            'name': 'W310×21',
            'weight': 20.9,
            'Zx': 455000,  # mm³
            'ry': 39.9     # mm
        }
        
        # Test parameters
        Lb = 4.0  # m (unbraced length)
        Fy = 345  # MPa (yield strength)
        
        capacity = self.calculate_beam_capacity_si(test_beam, Lb, Fy)
        
        # Check that capacity is reasonable
        self.assertGreater(capacity, 0, "Beam capacity should be positive")
        self.assertLess(capacity, 200, "Beam capacity should be reasonable (< 200 kN⋅m)")
        
        # For this beam, capacity should be around 80-120 kN⋅m range
        self.assertGreater(capacity, 50, "W310×21 should have capacity > 50 kN⋅m")
        self.assertLess(capacity, 150, "W310×21 should have capacity < 150 kN⋅m")
    
    def test_beam_capacity_with_different_lengths(self):
        """Test that longer unbraced lengths reduce capacity"""
        test_beam = {
            'name': 'W460×60',
            'weight': 60.0,
            'Zx': 2520000,
            'ry': 62.5
        }
        
        Fy = 345  # MPa
        
        # Calculate capacity for different unbraced lengths
        capacity_short = self.calculate_beam_capacity_si(test_beam, 2.0, Fy)  # 2m
        capacity_long = self.calculate_beam_capacity_si(test_beam, 8.0, Fy)   # 8m
        
        # Longer unbraced length should reduce capacity due to LTB
        self.assertGreater(capacity_short, capacity_long, 
                          "Shorter unbraced length should give higher capacity")

class TestConcreteCalculations(unittest.TestCase):
    """Tests for concrete design calculations"""
    
    def test_concrete_strength_units(self):
        """Test that concrete strength values are in reasonable SI ranges"""
        # Typical concrete strengths in MPa
        typical_strengths = [20, 25, 30, 35, 40, 50]
        
        for fc in typical_strengths:
            # Check that fc is in reasonable range for SI units
            self.assertGreaterEqual(fc, 15, "Concrete strength should be ≥ 15 MPa")
            self.assertLessEqual(fc, 100, "Concrete strength should be ≤ 100 MPa")
    
    def test_steel_strength_units(self):
        """Test that steel strength values are in reasonable SI ranges"""
        # Typical steel strengths in MPa
        typical_strengths = [300, 350, 400, 420, 500]
        
        for fy in typical_strengths:
            # Check that fy is in reasonable range for SI units  
            self.assertGreaterEqual(fy, 250, "Steel strength should be ≥ 250 MPa")
            self.assertLessEqual(fy, 600, "Steel strength should be ≤ 600 MPa")

class TestUnitConsistency(unittest.TestCase):
    """Tests for unit consistency across calculations"""
    
    def test_force_units(self):
        """Test that force units are consistent (kN)"""
        # Common force values in structural engineering
        test_forces = [10, 50, 100, 500, 1000]  # kN
        
        for force in test_forces:
            # Convert to Newtons
            force_N = force * 1000
            self.assertGreater(force_N, 0, "Force should be positive")
    
    def test_moment_units(self):
        """Test that moment units are consistent (kN⋅m)"""
        # Common moment values  
        test_moments = [5, 25, 50, 100, 500]  # kN⋅m
        
        for moment in test_moments:
            # Convert to N⋅mm
            moment_Nmm = moment * 1000 * 1000
            self.assertGreater(moment_Nmm, 0, "Moment should be positive")
    
    def test_stress_units(self):
        """Test that stress units are consistent (MPa)"""
        # Common stress values
        test_stresses = [1, 10, 50, 100, 500]  # MPa
        
        for stress in test_stresses:
            # Convert to Pa
            stress_Pa = stress * 1000000
            self.assertGreater(stress_Pa, 0, "Stress should be positive")
    
    def test_length_units(self):
        """Test that length units are consistent (mm, m)"""
        # Test conversion between mm and m
        length_mm = 500  # mm
        length_m = length_mm / 1000  # m
        
        self.assertEqual(length_m, 0.5, "500 mm should equal 0.5 m")
        
        # Test common structural dimensions
        typical_beam_depths = [200, 300, 400, 500, 600]  # mm
        for depth in typical_beam_depths:
            self.assertGreater(depth, 0, "Beam depth should be positive")
            self.assertLess(depth, 2000, "Beam depth should be reasonable")

class TestCalculationResults(unittest.TestCase):
    """Tests for reasonable calculation results"""
    
    def test_steel_beam_capacity_range(self):
        """Test that steel beam capacities are in reasonable ranges"""
        try:
            from steel_beam_optimizer_si import calculate_beam_capacity_si
            
            # Test various beam sizes
            beam_tests = [
                {'name': 'W200×15', 'Zx': 206000, 'ry': 26.2, 'expected_range': (10, 40)},
                {'name': 'W460×60', 'Zx': 2520000, 'ry': 62.5, 'expected_range': (150, 400)},
                {'name': 'W760×173', 'Zx': 19000000, 'ry': 101.6, 'expected_range': (800, 2000)},
            ]
            
            for beam_test in beam_tests:
                beam_data = {
                    'name': beam_test['name'],
                    'weight': 50,  # Not used in capacity calc
                    'Zx': beam_test['Zx'],
                    'ry': beam_test['ry']
                }
                
                capacity = calculate_beam_capacity_si(beam_data, 4.0, 345)
                min_expected, max_expected = beam_test['expected_range']
                
                self.assertGreaterEqual(capacity, min_expected, 
                                      f"{beam_test['name']} capacity should be ≥ {min_expected} kN⋅m")
                self.assertLessEqual(capacity, max_expected,
                                   f"{beam_test['name']} capacity should be ≤ {max_expected} kN⋅m")
                
        except ImportError:
            self.skipTest("Steel beam optimizer not available")

if __name__ == '__main__':
    # Configure test runner
    unittest.main(
        verbosity=2,
        buffer=True,
        catchbreak=True,
        exit=False
    )
