#!/usr/bin/env python3
"""
Runner script for point load beam calculation with SI units
ใช้ระบบ SI units และ forallpeople library
"""

import sys
import os

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the calculation function
from examples.point_load_beam_si_units import calculation, si_units_demo

try:
    from efficalc.report_builder import ReportBuilder
except ImportError:
    try:
        from efficalc import ReportBuilder
    except ImportError:
        print("ReportBuilder not found, running calculation only...")
        ReportBuilder = None

def main():
    """Run the SI units beam calculation and generate report"""
    
    print("=" * 70)
    print("POINT LOAD BEAM CALCULATION - SI UNITS VERSION")
    print("การคำนวณคานด้วยระบบเมตริก (SI Units)")
    print("=" * 70)
    
    try:
        # Run SI units demonstration first
        si_units_demo()
        
        print("\n" + "="*50)
        print("GENERATING CALCULATION REPORT")
        print("="*50)
        
        if ReportBuilder:
            # Generate and view report
            print("สร้าง HTML report ด้วย SI units...")
            builder = ReportBuilder(calculation)
            builder.view_report()
            print("✅ Report สร้างเสร็จและเปิดใน browser แล้ว")
        else:
            # Just run the calculation
            print("รันการคำนวณ...")
            calculation()
            print("✅ การคำนวณเสร็จสมบูรณ์")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*50)
    print("สรุปการคำนวณ SI UNITS")
    print("="*50)
    print("✅ ระบบหน่วย: SI Units (Metric)")
    print("✅ ความยาวคาน: 6.0 m")
    print("✅ แรงกระทำ: 50 kN")
    print("✅ ตำแหน่งแรง: 2.0 m จากจุดรองรับซ้าย")
    print("✅ วัสดุ: เหล็ก (E = 200,000 MPa)")
    print("✅ หน่วยผลลัพธ์: kN*m สำหรับ moment, mm สำหรับ deflection")
    print("✅ การตรวจสอบ: deflection limit L/250")
    
    print("\n🎯 ระบบ efficalc-THAI รองรับ SI units เต็มรูปแบบแล้ว!")
    print("📊 สามารถสร้าง professional engineering reports ด้วยระบบเมตริก")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
