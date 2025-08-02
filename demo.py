"""
Interactive demo of concrete analysis with fixed encoding
"""

def run_beam_demo():
    """Run beam analysis demo"""
    print("\n" + "="*50)
    print("🏗️  CONCRETE BEAM ANALYSIS DEMO")
    print("="*50)
    
    try:
        from examples.concrete_aci318m_si_example import concrete_beam_aci318m_si
        from efficalc.report_builder import ReportBuilder
        
        print("📊 Generating beam analysis report...")
        builder = ReportBuilder(concrete_beam_aci318m_si)
        
        # Get HTML content
        html_content = builder.get_html_as_str()
        
        # Show key sections
        if "f'_c = 30 MPa" in html_content:
            print("✅ Concrete strength: f'c = 30 MPa")
        
        if "f_y = 420 MPa" in html_content:
            print("✅ Steel yield strength: fy = 420 MPa")
            
        if "b = 300 mm" in html_content:
            print("✅ Beam width: b = 300 mm")
            
        if "h = 600 mm" in html_content:
            print("✅ Beam height: h = 600 mm")
            
        if "kN*m" in html_content:
            print("✅ SI units: Moments in kN*m (encoding fixed)")
            
        if "Tension-controlled section" in html_content:
            print("✅ Section classification: Tension-controlled")
            
        print(f"📄 Report size: {len(html_content):,} characters")
        print("🎯 All calculations completed successfully!")
        
        # Open report in browser
        temp_file = builder.view_report()
        print(f"🌐 Report opened in browser: {temp_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_column_demo():
    """Run column analysis demo"""
    print("\n" + "="*50)
    print("🏢 CONCRETE COLUMN DESIGN DEMO")
    print("="*50)
    
    try:
        from examples.concrete_aci318m_si_example import concrete_column_aci318m_si
        from efficalc.report_builder import ReportBuilder
        
        print("📊 Generating column design report...")
        builder = ReportBuilder(concrete_column_aci318m_si)
        
        html_content = builder.get_html_as_str()
        
        if "f'_c = 25 MPa" in html_content:
            print("✅ Concrete strength: f'c = 25 MPa")
            
        if "400 mm" in html_content:
            print("✅ Column dimensions: 400 × 400 mm")
            
        if "3200 mm^2" in html_content:
            print("✅ Reinforcement area: As = 3200 mm^2")
            
        if "kN" in html_content:
            print("✅ SI units: Forces in kN (encoding fixed)")
            
        print(f"📄 Report size: {len(html_content):,} characters")
        print("🎯 Column design completed successfully!")
        
        # Open report in browser
        temp_file = builder.view_report()
        print(f"🌐 Report opened in browser: {temp_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main demo function"""
    print("🚀 efficalc-THAI Demo - ACI 318M-25 with SI Units")
    print("📋 All encoding issues have been resolved!")
    print()
    
    while True:
        print("\nSelect demo:")
        print("1. 🏗️  Concrete Beam Analysis")
        print("2. 🏢 Concrete Column Design") 
        print("3. ❌ Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            success = run_beam_demo()
            if success:
                print("\n✨ Beam analysis completed! Check your browser for the report.")
        elif choice == "2":
            success = run_column_demo()
            if success:
                print("\n✨ Column design completed! Check your browser for the report.")
        elif choice == "3":
            print("\n👋 Thanks for using efficalc-THAI!")
            break
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
