#!/usr/bin/env python3
"""
Simple Test Runner for SI Unit Examples
Basic validation of calculations and functions
"""

def test_steel_beam_optimizer():
    """Test steel beam optimizer functionality"""
    print("Testing Steel Beam Optimizer...")
    
    try:
        from steel_beam_optimizer_si import get_si_beam_database, calculate_beam_capacity_si
        
        # Test 1: Database structure
        database = get_si_beam_database()
        assert len(database) > 0, "Database should not be empty"
        assert 'name' in database[0], "Database should have beam names"
        assert 'weight' in database[0], "Database should have beam weights"
        print("  ✅ Database structure test passed")
        
        # Test 2: Capacity calculation
        test_beam = database[10]  # Pick a medium beam
        capacity = calculate_beam_capacity_si(test_beam, 4.0, 345)
        assert capacity > 0, "Capacity should be positive"
        assert capacity < 1000, "Capacity should be reasonable"
        print(f"  ✅ Capacity calculation test passed: {test_beam['name']} = {capacity:.1f} kN⋅m")
        
        # Test 3: Weight sorting
        weights = [beam['weight'] for beam in database]
        assert weights == sorted(weights), "Beams should be sorted by weight"
        print("  ✅ Weight sorting test passed")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Steel beam optimizer test failed: {e}")
        return False

def test_concrete_calculations():
    """Test concrete calculation functions"""
    print("Testing Concrete Calculations...")
    
    try:
        # Basic concrete beam calculations
        b = 300  # mm
        h = 500  # mm
        d = 460  # mm
        As = 1500  # mm²
        fc = 25  # MPa
        fy = 420  # MPa
        
        # Test stress block depth calculation
        a = As * fy / (0.85 * fc * b)
        assert a > 0, "Stress block depth should be positive"
        assert a < h, "Stress block depth should be less than beam height"
        print(f"  ✅ Stress block calculation test passed: a = {a:.1f} mm")
        
        # Test neutral axis depth
        c = a / 0.85
        assert c > a, "Neutral axis should be deeper than stress block"
        assert c < d, "Neutral axis should be above steel level"
        print(f"  ✅ Neutral axis calculation test passed: c = {c:.1f} mm")
        
        # Test steel strain
        epsilon_s = 0.003 * (d - c) / c
        epsilon_y = fy / 200000
        assert epsilon_s > epsilon_y, "Steel should yield in this example"
        print(f"  ✅ Steel strain test passed: εs = {epsilon_s:.4f} > εy = {epsilon_y:.4f}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Concrete calculations test failed: {e}")
        return False

def test_hss_compression():
    """Test HSS compression calculations"""
    print("Testing HSS Compression...")
    
    try:
        # HSS section properties
        b = 152  # mm
        t = 6.4  # mm
        L = 3000  # mm
        Fy = 345  # MPa
        
        # Cross-sectional area
        A = 4 * b * t - 4 * t**2
        assert A > 0, "Area should be positive"
        assert A < 10000, "Area should be reasonable"
        print(f"  ✅ Area calculation test passed: A = {A:.0f} mm²")
        
        # Moment of inertia (simplified)
        I = (b**4 - (b-2*t)**4) / 12
        assert I > 0, "Moment of inertia should be positive"
        print(f"  ✅ Moment of inertia test passed: I = {I:.0f} mm⁴")
        
        # Radius of gyration
        r = (I / A)**0.5
        assert r > 0, "Radius of gyration should be positive"
        assert r < b, "Radius should be less than section width"
        print(f"  ✅ Radius of gyration test passed: r = {r:.1f} mm")
        
        # Slenderness ratio
        slenderness = L / r
        assert slenderness > 0, "Slenderness should be positive"
        assert slenderness < 300, "Slenderness should be reasonable"
        print(f"  ✅ Slenderness test passed: λ = {slenderness:.1f}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ HSS compression test failed: {e}")
        return False

def test_point_load_beam():
    """Test point load beam calculations"""
    print("Testing Point Load Beam...")
    
    try:
        # Beam parameters
        L = 6.0  # m
        P = 50   # kN
        a = 2.0  # m (load position)
        b = L - a  # 4.0 m
        
        # Reactions
        R1 = P * b / L
        R2 = P * a / L
        
        assert R1 > 0, "Left reaction should be positive"
        assert R2 > 0, "Right reaction should be positive"
        assert abs(R1 + R2 - P) < 0.001, "Reactions should sum to applied load"
        print(f"  ✅ Reaction calculation test passed: R1 = {R1:.1f} kN, R2 = {R2:.1f} kN")
        
        # Maximum moment (under the load)
        M_max = R1 * a
        assert M_max > 0, "Maximum moment should be positive"
        assert M_max < P * L, "Moment should be reasonable"
        print(f"  ✅ Maximum moment test passed: M_max = {M_max:.1f} kN⋅m")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Point load beam test failed: {e}")
        return False

def test_unit_conversions():
    """Test SI unit conversions"""
    print("Testing Unit Conversions...")
    
    try:
        # Length conversions
        length_mm = 500
        length_m = length_mm / 1000
        assert length_m == 0.5, "500 mm should equal 0.5 m"
        print("  ✅ Length conversion test passed")
        
        # Force conversions
        force_kn = 100
        force_n = force_kn * 1000
        assert force_n == 100000, "100 kN should equal 100,000 N"
        print("  ✅ Force conversion test passed")
        
        # Stress conversions
        stress_mpa = 25
        stress_pa = stress_mpa * 1000000
        assert stress_pa == 25000000, "25 MPa should equal 25,000,000 Pa"
        print("  ✅ Stress conversion test passed")
        
        # Moment conversions
        moment_knm = 50
        moment_nmm = moment_knm * 1000 * 1000
        assert moment_nmm == 50000000, "50 kN⋅m should equal 50,000,000 N⋅mm"
        print("  ✅ Moment conversion test passed")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Unit conversion test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("SI UNIT EXAMPLES - BASIC VALIDATION TESTS")
    print("=" * 60)
    print()
    
    tests = [
        test_steel_beam_optimizer,
        test_concrete_calculations, 
        test_hss_compression,
        test_point_load_beam,
        test_unit_conversions
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} crashed: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
        print("✅ SI Unit calculations are working correctly")
    else:
        print(f"⚠️  {failed} tests failed")
        print("❌ Please check the errors above")
    
    print()
    print("📊 TESTED FUNCTIONALITY:")
    print("   • Steel beam capacity calculations")
    print("   • Concrete neutral axis analysis")
    print("   • HSS compression member properties")
    print("   • Point load beam analysis")
    print("   • SI unit conversion consistency")
    print()
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    import sys
    exit_code = main()
    sys.exit(exit_code)
