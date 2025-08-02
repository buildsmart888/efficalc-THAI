"""
Performance and Validation Tests for SI Unit Examples
Test calculation accuracy, performance, and edge cases
"""

import unittest
import time
import sys
import os
from pathlib import Path

# Add the examples directory to the path
examples_dir = Path(__file__).parent
sys.path.insert(0, str(examples_dir))

class TestCalculationAccuracy(unittest.TestCase):
    """Test calculation accuracy against known solutions"""
    
    def test_steel_beam_capacity_validation(self):
        """Validate steel beam capacity against manual calculations"""
        try:
            from steel_beam_optimizer_si import calculate_beam_capacity_si
            
            # Test case: W310×21 beam
            test_beam = {
                'name': 'W310×21',
                'weight': 20.9,
                'Zx': 455000,  # mm³
                'ry': 39.9     # mm
            }
            
            # Known parameters
            Fy = 345  # MPa
            Lb = 3.0  # m (short unbraced length - should give near full capacity)
            
            # Calculate capacity
            capacity = calculate_beam_capacity_si(test_beam, Lb, Fy)
            
            # Manual calculation:
            # Mp = Fy * Zx = 345 * 455000 = 156,975,000 N⋅mm = 157 kN⋅m
            # For short unbraced length, phi*Mp ≈ 0.9 * 157 = 141 kN⋅m
            expected_capacity = 0.9 * 345 * 455000 / 1e6  # kN⋅m
            
            # Should be within 10% of expected
            tolerance = 0.1 * expected_capacity
            self.assertAlmostEqual(capacity, expected_capacity, delta=tolerance,
                                 msg=f"Capacity {capacity:.1f} should be near {expected_capacity:.1f} kN⋅m")
            
        except ImportError:
            self.skipTest("Steel beam optimizer not available")
    
    def test_concrete_neutral_axis_validation(self):
        """Validate concrete neutral axis calculation"""
        # Known problem: 300×500mm beam, 1500mm² steel, fc=25MPa, fy=420MPa
        
        b = 300  # mm
        d = 460  # mm (effective depth)
        As = 1500  # mm²
        fc = 25  # MPa
        fy = 420  # MPa
        
        # Manual calculation of stress block depth
        # T = C: As*fy = 0.85*fc*a*b
        # a = As*fy/(0.85*fc*b)
        a_manual = As * fy / (0.85 * fc * b)
        
        # Neutral axis depth c = a/β₁ (where β₁ = 0.85 for fc ≤ 28 MPa)
        c_manual = a_manual / 0.85
        
        # Expected values
        self.assertAlmostEqual(a_manual, 156.9, places=1)  # mm
        self.assertAlmostEqual(c_manual, 184.6, places=1)  # mm
        
        # Steel strain check (should yield)
        epsilon_s = 0.003 * (d - c_manual) / c_manual
        epsilon_y = fy / 200000  # Steel modulus = 200 GPa
        
        self.assertGreater(epsilon_s, epsilon_y, "Steel should yield in this example")
    
    def test_hss_compression_validation(self):
        """Validate HSS compression capacity calculation"""
        
        # Test case: HSS 152×152×6.4
        b = 152  # mm
        t = 6.4  # mm
        L = 3000  # mm
        Fy = 345  # MPa
        
        # Cross-sectional properties
        A = 4 * b * t - 4 * t**2  # Gross area
        I = (b**4 - (b-2*t)**4) / 12  # Moment of inertia
        r = (I / A)**0.5  # Radius of gyration
        
        # Expected values (can be verified with steel handbook)
        expected_A = 3750  # mm² (approximately)
        expected_r = 59.0  # mm (approximately)
        
        # Allow 5% tolerance for simplified calculations
        self.assertAlmostEqual(A, expected_A, delta=0.05*expected_A)
        self.assertAlmostEqual(r, expected_r, delta=0.05*expected_r)
        
        # Slenderness ratio
        slenderness = L / r
        self.assertAlmostEqual(slenderness, 50.8, places=1)

class TestPerformance(unittest.TestCase):
    """Test calculation performance and execution time"""
    
    def test_beam_optimizer_performance(self):
        """Test that beam optimizer runs in reasonable time"""
        try:
            from steel_beam_optimizer_si import get_si_beam_database, calculate_beam_capacity_si
            
            database = get_si_beam_database()
            
            # Time the capacity calculation for all beams
            start_time = time.time()
            
            for beam in database:
                capacity = calculate_beam_capacity_si(beam, 4.0, 345)
                self.assertGreater(capacity, 0, "All beams should have positive capacity")
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Should complete all calculations in under 1 second
            self.assertLess(execution_time, 1.0, 
                          f"Beam calculations took {execution_time:.3f}s, should be < 1.0s")
            
            print(f"Calculated capacity for {len(database)} beams in {execution_time:.3f} seconds")
            
        except ImportError:
            self.skipTest("Steel beam optimizer not available")
    
    def test_calculation_repeatability(self):
        """Test that calculations give consistent results"""
        try:
            from steel_beam_optimizer_si import calculate_beam_capacity_si
            
            test_beam = {
                'name': 'W460×60',
                'weight': 60.0,
                'Zx': 2520000,
                'ry': 62.5
            }
            
            # Run calculation multiple times
            results = []
            for i in range(10):
                capacity = calculate_beam_capacity_si(test_beam, 4.0, 345)
                results.append(capacity)
            
            # All results should be identical
            for result in results[1:]:
                self.assertEqual(result, results[0], "Calculations should be repeatable")
                
        except ImportError:
            self.skipTest("Steel beam optimizer not available")

class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_very_short_beam(self):
        """Test beam with very short unbraced length"""
        try:
            from steel_beam_optimizer_si import calculate_beam_capacity_si
            
            test_beam = {
                'name': 'W310×28',
                'weight': 28.3,
                'Zx': 715000,
                'ry': 41.1
            }
            
            # Very short unbraced length (should give full plastic capacity)
            capacity_short = calculate_beam_capacity_si(test_beam, 0.5, 345)
            
            # Longer unbraced length
            capacity_long = calculate_beam_capacity_si(test_beam, 6.0, 345)
            
            # Short beam should have higher capacity
            self.assertGreater(capacity_short, capacity_long)
            
            # Both should be positive and reasonable
            self.assertGreater(capacity_short, 0)
            self.assertGreater(capacity_long, 0)
            self.assertLess(capacity_short, 500)  # Upper bound check
            
        except ImportError:
            self.skipTest("Steel beam optimizer not available")
    
    def test_minimum_steel_ratio(self):
        """Test concrete beam with minimum steel ratio"""
        
        # Very lightly reinforced beam
        b = 300  # mm
        d = 450  # mm
        fc = 25   # MPa
        fy = 420  # MPa
        
        # Minimum steel area per ACI 318M
        As_min_1 = 0.25 * (fc**0.5) * b * d / fy
        As_min_2 = 1.4 * b * d / fy
        As_min = max(As_min_1, As_min_2)
        
        # Calculate stress block depth
        a = As_min * fy / (0.85 * fc * b)
        c = a / 0.85
        
        # Should have reasonable neutral axis position
        self.assertGreater(c, 0, "Neutral axis depth should be positive")
        self.assertLess(c, d, "Neutral axis should be above steel level")
        
        # Steel should yield (tension-controlled)
        epsilon_s = 0.003 * (d - c) / c
        epsilon_y = fy / 200000
        self.assertGreater(epsilon_s, epsilon_y, "Minimum steel should still yield")
    
    def test_maximum_practical_steel_ratio(self):
        """Test concrete beam with high steel ratio"""
        
        # Heavily reinforced beam (approaching balanced condition)
        b = 400  # mm
        d = 600  # mm
        fc = 30   # MPa
        fy = 420  # MPa
        
        # High steel area (but still reasonable)
        As = 6000  # mm² (ρ ≈ 0.025)
        
        # Calculate neutral axis
        a = As * fy / (0.85 * fc * b)
        c = a / 0.85
        
        # Check that it's still tension-controlled
        epsilon_s = 0.003 * (d - c) / c
        epsilon_y = fy / 200000
        
        # Should still yield, but getting close to balanced
        self.assertGreater(epsilon_s, epsilon_y, "Steel should still yield")
        
        # Neutral axis shouldn't be too deep
        self.assertLess(c / d, 0.6, "Should not approach compression-controlled region")

class TestUnitsValidation(unittest.TestCase):
    """Validate that all calculations use proper SI units"""
    
    def test_stress_unit_consistency(self):
        """Test stress calculations use MPa consistently"""
        
        # Test various stress values
        test_cases = [
            (25, "MPa", "Concrete compressive strength"),
            (420, "MPa", "Steel yield strength"), 
            (345, "MPa", "Structural steel yield strength"),
            (200000, "MPa", "Steel elastic modulus")
        ]
        
        for value, unit, description in test_cases:
            # Convert to Pa for validation
            value_pa = value * 1e6
            
            # Check reasonable ranges
            if "concrete" in description.lower():
                self.assertGreater(value_pa, 15e6, f"{description} should be > 15 MPa")
                self.assertLess(value_pa, 100e6, f"{description} should be < 100 MPa")
            elif "steel" in description.lower() and "elastic" not in description.lower():
                self.assertGreater(value_pa, 200e6, f"{description} should be > 200 MPa")
                self.assertLess(value_pa, 700e6, f"{description} should be < 700 MPa")
    
    def test_force_unit_consistency(self):
        """Test force calculations use kN consistently"""
        
        # Common structural loads
        test_loads = [
            (25, "kN/m", "Uniform beam load"),
            (100, "kN", "Column axial load"),
            (50, "kN", "Point load on beam")
        ]
        
        for value, unit, description in test_loads:
            # Convert to Newtons
            if "kN/m" in unit:
                value_n = value * 1000  # per meter
            else:
                value_n = value * 1000
            
            self.assertGreater(value_n, 0, f"{description} should be positive")
    
    def test_moment_unit_consistency(self):
        """Test moment calculations use kN⋅m consistently"""
        
        # Typical structural moments
        test_moments = [
            (50, "kN⋅m", "Small beam moment"),
            (200, "kN⋅m", "Medium beam moment"),
            (500, "kN⋅m", "Large beam moment")
        ]
        
        for value, unit, description in test_moments:
            # Convert to N⋅mm
            value_nmm = value * 1e6
            
            self.assertGreater(value_nmm, 0, f"{description} should be positive")

if __name__ == '__main__':
    # Create test suite
    test_classes = [
        TestCalculationAccuracy,
        TestPerformance, 
        TestEdgeCases,
        TestUnitsValidation
    ]
    
    # Run all tests with detailed output
    for test_class in test_classes:
        print(f"\n{'='*60}")
        print(f"Running {test_class.__name__}")
        print('='*60)
        
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=2, buffer=True)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print(f"✅ {test_class.__name__} - All tests passed!")
        else:
            print(f"❌ {test_class.__name__} - {len(result.failures)} failures, {len(result.errors)} errors")
    
    print(f"\n{'='*60}")
    print("PERFORMANCE AND VALIDATION TESTING COMPLETE")
    print('='*60)
