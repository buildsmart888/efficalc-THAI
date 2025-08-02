"""
Integration Test Cases for SI Unit Examples
Test real-world engineering scenarios with expected results
"""

import unittest
import sys
import os
from pathlib import Path

# Add the examples directory to the path
examples_dir = Path(__file__).parent
sys.path.insert(0, str(examples_dir))

class TestEngineeringScenarios(unittest.TestCase):
    """Test cases based on real engineering scenarios"""
    
    def test_scenario_1_office_building_beam(self):
        """
        Scenario: Office building floor beam design
        Requirements: 6m span, 25 kN/m uniform load
        Expected: Beam selection around W310×28 to W360×33
        """
        try:
            from steel_beam_optimizer_si import get_si_beam_database, calculate_beam_capacity_si
            
            # Scenario parameters
            span = 6.0  # m
            uniform_load = 25  # kN/m
            moment_demand = uniform_load * span**2 / 8  # Simple span formula
            
            # Expected moment ≈ 112.5 kN⋅m
            self.assertAlmostEqual(moment_demand, 112.5, places=1)
            
            # Find suitable beam
            database = get_si_beam_database()
            suitable_beams = []
            
            for beam in database:
                capacity = calculate_beam_capacity_si(beam, 4.0, 345)  # 4m unbraced length
                if capacity >= moment_demand:
                    suitable_beams.append((beam['name'], beam['weight'], capacity))
            
            self.assertGreater(len(suitable_beams), 0, "Should find suitable beams")
            
            # First suitable beam should be reasonably sized
            lightest_beam = suitable_beams[0]
            self.assertLess(lightest_beam[1], 80, "Lightest suitable beam should be < 80 kg/m")
            
        except ImportError:
            self.skipTest("Steel beam optimizer not available")
    
    def test_scenario_2_residential_beam(self):
        """
        Scenario: Residential beam over garage opening
        Requirements: 4m span, 40 kN point load at center
        Expected: Smaller beam, around W250×28 to W310×28
        """
        try:
            from steel_beam_optimizer_si import get_si_beam_database, calculate_beam_capacity_si
            
            # Scenario parameters
            span = 4.0  # m
            point_load = 40  # kN
            moment_demand = point_load * span / 4  # Point load at center
            
            # Expected moment = 40 kN⋅m
            self.assertEqual(moment_demand, 40)
            
            # Find suitable beam
            database = get_si_beam_database()
            suitable_beams = []
            
            for beam in database:
                capacity = calculate_beam_capacity_si(beam, 2.0, 345)  # 2m unbraced length
                if capacity >= moment_demand:
                    suitable_beams.append((beam['name'], beam['weight'], capacity))
            
            self.assertGreater(len(suitable_beams), 0, "Should find suitable beams")
            
            # Should be able to use a light beam
            lightest_beam = suitable_beams[0]
            self.assertLess(lightest_beam[1], 50, "Should be able to use beam < 50 kg/m")
            
        except ImportError:
            self.skipTest("Steel beam optimizer not available")
    
    def test_scenario_3_warehouse_heavy_load(self):
        """
        Scenario: Warehouse beam with heavy equipment load
        Requirements: 8m span, 80 kN/m uniform load
        Expected: Heavy beam, around W610×125 or larger
        """
        try:
            from steel_beam_optimizer_si import get_si_beam_database, calculate_beam_capacity_si
            
            # Scenario parameters
            span = 8.0  # m
            uniform_load = 80  # kN/m (heavy industrial load)
            moment_demand = uniform_load * span**2 / 8
            
            # Expected moment = 640 kN⋅m
            self.assertEqual(moment_demand, 640)
            
            # Find suitable beam
            database = get_si_beam_database()
            suitable_beams = []
            
            for beam in database:
                capacity = calculate_beam_capacity_si(beam, 6.0, 345)  # 6m unbraced length
                if capacity >= moment_demand:
                    suitable_beams.append((beam['name'], beam['weight'], capacity))
            
            self.assertGreater(len(suitable_beams), 0, "Should find suitable heavy beams")
            
            # Should require a heavy beam
            lightest_beam = suitable_beams[0]
            self.assertGreater(lightest_beam[1], 100, "Should require beam > 100 kg/m for heavy load")
            
        except ImportError:
            self.skipTest("Steel beam optimizer not available")

class TestConcreteBeamScenarios(unittest.TestCase):
    """Test cases for concrete beam calculations"""
    
    def test_concrete_beam_residential(self):
        """
        Scenario: Residential concrete beam
        Typical dimensions: 300×500mm with 3×20M bars
        """
        # Test parameters for residential beam
        b = 300  # mm width
        h = 500  # mm height  
        cover = 40  # mm
        d = h - cover  # 460 mm effective depth
        
        # Steel area for 3×20M bars (≈ 3×300 = 900 mm²)
        As = 942  # mm² (actual area of 3×20M)
        
        # Material properties
        fc = 25  # MPa
        fy = 420  # MPa
        
        # Calculate steel ratio
        rho = As / (b * d)
        
        # Steel ratio should be reasonable (0.005 to 0.02 typical)
        self.assertGreater(rho, 0.005, "Steel ratio should be > 0.005")
        self.assertLess(rho, 0.02, "Steel ratio should be < 0.02")
        
        # Calculate approximate capacity using simplified method
        # a = As*fy/(0.85*fc*b)
        a = As * fy / (0.85 * fc * b)
        moment_arm = d - a/2
        Mn = As * fy * moment_arm / 1e6  # Convert to kN⋅m
        
        # Residential beam should have reasonable capacity (50-150 kN⋅m)
        self.assertGreater(Mn, 50, "Residential beam should have > 50 kN⋅m capacity")
        self.assertLess(Mn, 150, "Residential beam should have < 150 kN⋅m capacity")
    
    def test_concrete_beam_commercial(self):
        """
        Scenario: Commercial building beam
        Larger dimensions: 400×700mm with 6×25M bars
        """
        # Test parameters for commercial beam
        b = 400  # mm width
        h = 700  # mm height
        cover = 50  # mm (larger cover for fire rating)
        d = h - cover  # 650 mm effective depth
        
        # Steel area for 6×25M bars (≈ 6×500 = 3000 mm²)
        As = 2945  # mm² (actual area of 6×25M)
        
        # Material properties
        fc = 30  # MPa (higher strength)
        fy = 420  # MPa
        
        # Calculate steel ratio
        rho = As / (b * d)
        
        # Steel ratio should be reasonable
        self.assertGreater(rho, 0.005, "Steel ratio should be > 0.005")
        self.assertLess(rho, 0.025, "Steel ratio should be < 0.025")
        
        # Calculate approximate capacity
        a = As * fy / (0.85 * fc * b)
        moment_arm = d - a/2
        Mn = As * fy * moment_arm / 1e6  # Convert to kN⋅m
        
        # Commercial beam should have higher capacity (200-500 kN⋅m)
        self.assertGreater(Mn, 200, "Commercial beam should have > 200 kN⋅m capacity")
        self.assertLess(Mn, 500, "Commercial beam should have < 500 kN⋅m capacity")

class TestHSSCompressionScenarios(unittest.TestCase):
    """Test cases for HSS compression members"""
    
    def test_hss_column_light_load(self):
        """
        Scenario: Light load column in residential construction
        HSS 102×102×6.4, 3m height, light axial load
        """
        # Column parameters
        b = 102  # mm
        t = 6.4  # mm wall thickness
        L = 3000  # mm length
        Fy = 345  # MPa
        
        # Calculate cross-sectional area (approximate)
        A = 4 * b * t - 4 * t**2  # Hollow section area
        
        # Calculate radius of gyration (approximate)
        I = (b**4 - (b-2*t)**4) / 12  # Moment of inertia
        r = (I / A)**0.5  # Radius of gyration
        
        # Slenderness ratio
        slenderness = L / r
        
        # Should be a reasonable slenderness for a column
        self.assertLess(slenderness, 200, "Slenderness should be < 200")
        self.assertGreater(slenderness, 20, "Slenderness should be > 20")
        
        # Approximate buckling capacity (simplified)
        if slenderness < 100:
            # Short column - yielding controls
            Pn = A * Fy / 1000  # Convert to kN
        else:
            # Long column - buckling controls (simplified)
            Fe = 200000 * 3.14159**2 / slenderness**2  # Euler buckling stress
            Pn = A * min(Fy, Fe) / 1000
        
        # Light load column should have reasonable capacity (100-500 kN)
        self.assertGreater(Pn, 100, "Light column should support > 100 kN")
        self.assertLess(Pn, 500, "Light column should be < 500 kN capacity")
    
    def test_hss_column_heavy_load(self):
        """
        Scenario: Heavy load column in commercial construction
        HSS 203×203×12.7, 4m height, heavy axial load
        """
        # Column parameters
        b = 203  # mm
        t = 12.7  # mm wall thickness
        L = 4000  # mm length
        Fy = 345  # MPa
        
        # Calculate cross-sectional area (approximate)
        A = 4 * b * t - 4 * t**2
        
        # Calculate radius of gyration (approximate)
        I = (b**4 - (b-2*t)**4) / 12
        r = (I / A)**0.5
        
        # Slenderness ratio
        slenderness = L / r
        
        # Should be reasonable for heavy column
        self.assertLess(slenderness, 150, "Heavy column slenderness should be < 150")
        
        # Approximate capacity
        if slenderness < 100:
            Pn = A * Fy / 1000
        else:
            Fe = 200000 * 3.14159**2 / slenderness**2
            Pn = A * min(Fy, Fe) / 1000
        
        # Heavy column should have high capacity (800-2000 kN)
        self.assertGreater(Pn, 800, "Heavy column should support > 800 kN")
        self.assertLess(Pn, 2000, "Heavy column should be < 2000 kN capacity")

class TestPointLoadBeamScenarios(unittest.TestCase):
    """Test cases for point load beam analysis"""
    
    def test_crane_beam_scenario(self):
        """
        Scenario: Overhead crane runway beam
        10m span, 200 kN wheel load at 3m from left support
        """
        # Beam parameters
        L = 10.0  # m span
        P = 200  # kN point load
        a = 3.0  # m distance from left support
        b = L - a  # 7.0 m distance from right support
        
        # Calculate reactions
        R1 = P * b / L  # Left reaction
        R2 = P * a / L  # Right reaction
        
        # Check equilibrium
        self.assertAlmostEqual(R1 + R2, P, places=1, msg="Reactions should sum to applied load")
        
        # Calculate maximum moment (occurs under the load)
        M_max = R1 * a
        
        # Expected values
        self.assertAlmostEqual(R1, 140, places=1)  # 200 * 7/10
        self.assertAlmostEqual(R2, 60, places=1)   # 200 * 3/10
        self.assertAlmostEqual(M_max, 420, places=1)  # 140 * 3
        
        # Crane beam moment should be substantial
        self.assertGreater(M_max, 300, "Crane beam should have > 300 kN⋅m moment")
    
    def test_equipment_platform_beam(self):
        """
        Scenario: Equipment platform beam
        6m span, 50 kN equipment load at center
        """
        # Beam parameters
        L = 6.0  # m span
        P = 50  # kN point load
        a = L / 2  # Load at center
        
        # For center load, reactions are equal
        R1 = R2 = P / 2
        
        # Maximum moment at center
        M_max = P * L / 4
        
        # Expected values
        self.assertEqual(R1, 25)  # kN
        self.assertEqual(R2, 25)  # kN
        self.assertEqual(M_max, 75)  # kN⋅m
        
        # Platform beam should be manageable size
        self.assertLess(M_max, 100, "Platform beam should be < 100 kN⋅m")

if __name__ == '__main__':
    # Run all test cases
    unittest.main(
        verbosity=2,
        buffer=True,
        catchbreak=True,
        exit=False
    )
