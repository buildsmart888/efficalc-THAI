# SI Units และ ACI 318M-25 Integration Guide

## การเพิ่มรองรับ SI Units และ ACI 318M-25 ใน efficalc

### ภาพรวม

โปรเจค efficalc-THAI ได้รับการปรับปรุงให้รองรับ:
- **SI Units (หน่วยเมตริก)** ผ่านไลบรารี `forallpeople`
- **ACI 318M-25** Building Code Requirements for Structural Concrete (Metric)
- **การแปลงหน่วย** ระหว่าง Imperial และ SI Units

### การติดตั้ง

1. ติดตั้ง forallpeople library:
```bash
pip install forallpeople
```

2. หรือใช้ requirements.txt ที่ปรับปรุงแล้ว:
```bash
pip install -r requirements.txt
```

### การใช้งาน SI Units

#### 1. Import หน่วยพื้นฐาน

```python
from efficalc import (
    # SI Units
    mm, cm, m, km,           # Length units
    N, kN, MN,               # Force units  
    Pa, kPa, MPa, GPa,       # Pressure/Stress units
    mm2, cm2, m2,            # Area units
    mm3, cm3, m3,            # Volume units
    Nm, kNm, MNm,            # Moment units
    
    # Conversion factors
    in_to_mm, ft_to_m,      # Length conversions
    lb_to_N, kip_to_kN,     # Force conversions
    psi_to_kPa, ksi_to_MPa, # Pressure conversions
    
    # ACI 318M-25 Constants
    ACI318M_Constants
)
```

#### 2. ตัวอย่างการใช้งานพื้นฐาน

```python
from efficalc import Calculation, Input, Title

def concrete_beam_si():
    Title("Concrete Beam Analysis - SI Units")
    
    # Material properties in SI
    fc = Input("f'_c", 25, "MPa", "Concrete compressive strength")
    fy = Input("f_y", 420, "MPa", "Steel yield strength")
    
    # Geometry in SI  
    b = Input("b", 300, "mm", "Beam width")
    d = Input("d", 500, "mm", "Effective depth")
    As = Input("A_s", 1500, "mm^2", "Steel area")
    
    # Calculations
    rho = Calculation("\\rho", As / (b * d), "", "Steel ratio")
```

### ACI 318M-25 Constants

#### การใช้ค่าคงที่จาก ACI 318M-25

```python
from efficalc import ACI318M_Constants

# Material properties
Es = ACI318M_Constants.STEEL_E              # 200,000 MPa
max_strain = ACI318M_Constants.MAX_CONCRETE_STRAIN  # 0.003

# Minimum covers
cover_beam = ACI318M_Constants.MIN_COVER_BEAM      # 25 mm
cover_column = ACI318M_Constants.MIN_COVER_COLUMN  # 40 mm

# Strength reduction factors
phi_flexure = ACI318M_Constants.PHI_FLEXURE        # 0.9
phi_compression = ACI318M_Constants.PHI_COMPRESSION # 0.65
```

### การแปลงหน่วย

#### จาก Imperial เป็น SI

```python
from efficalc import Calculation, in_to_mm, ksi_to_MPa

# แปลงขนาดจาก inches เป็น mm
width_in = Input("width", 12, "in", "Beam width in inches") 
width_mm = Calculation("width_mm", width_in * in_to_mm, "mm", "Beam width in mm")

# แปลงความแรงจาก ksi เป็น MPa
fy_ksi = Input("f_y", 60, "ksi", "Steel yield in Imperial")
fy_mpa = Calculation("f_y_mpa", fy_ksi * ksi_to_MPa, "MPa", "Steel yield in SI")
```

#### ตัวอย่างครบวงจร - เสาคอนกรีต

```python
from efficalc import *

def concrete_column_aci318m():
    Title("Concrete Column Design - ACI 318M-25")
    
    Heading("Material Properties")
    fc = Input("f'_c", 25, "MPa", "Concrete strength")
    fy = Input("f_y", 420, "MPa", "Steel yield strength")
    
    Heading("Geometry")  
    h = Input("h", 400, "mm", "Column height")
    b = Input("b", 400, "mm", "Column width")
    As = Input("A_s", 3200, "mm^2", "Total steel area")
    
    # Gross area
    Ag = Calculation("A_g", h * b, "mm^2", "Gross area")
    
    # Steel ratio
    rho_g = Calculation("\\rho_g", As / Ag, "", "Gross steel ratio")
    
    # ACI 318M-25 limits
    Comparison(rho_g, ">=", 0.01, "Min steel OK", "Insufficient steel", 
               "Minimum steel check", "ACI 318M-25 10.6.1.1")
    
    Comparison(rho_g, "<=", 0.08, "Max steel OK", "Excessive steel",
               "Maximum steel check", "ACI 318M-25 10.6.1.1")
    
    # Nominal axial strength (tied column)
    Pn = Calculation("P_n", 
                     0.8 * (0.85 * fc * (Ag - As) + fy * As) / 1000,
                     "kN", "Nominal axial strength", 
                     "ACI 318M-25 22.4.2.2")
    
    # Design strength
    phi_c = ACI318M_Constants.PHI_COMPRESSION
    Pd = Calculation("P_d", phi_c * Pn, "kN", "Design axial strength")
```

### Integration กับ forallpeople

#### การตรวจสอบหน่วย

```python
import forallpeople as si

# สร้าง Physical quantities ด้วย forallpeople
pressure = 25 * si.MPa
length = 300 * si.mm
area = length**2

print(f"Pressure: {pressure}")  # 25.000 MPa
print(f"Area: {area}")          # 90000.000 mm^2

# Automatic unit conversion
force = pressure * area
print(f"Force: {force}")        # 2.250 kN
```

### โครงสร้างไฟล์ที่เพิ่มขึ้น

```
efficalc/
├── si_units.py              # SI units และ conversion factors
├── __init__.py              # Updated สำหรับ SI units export
└── unit_conversions.py      # Imperial units (เดิม)

examples/
├── si_units_demo.py         # ตัวอย่างการใช้ SI units
├── concrete_aci318m_si_example.py  # ตัวอย่าง ACI 318M-25
└── concrete_beam_neutral_axis.py   # ตัวอย่างเดิม (Imperial)

requirements.txt             # เพิ่ม forallpeople>=1.0.0
pyproject.toml              # เพิ่ม forallpeople dependency
```

### ข้อดีของการ Integration

1. **หน่วยสากล**: ใช้ SI units ตาม International System of Units
2. **มาตรฐานสมัยใหม่**: รองรับ ACI 318M-25 (metric version)
3. **ความยืดหยุ่น**: แปลงหน่วยระหว่าง Imperial และ SI ได้
4. **ตรวจสอบหน่วย**: ใช้ forallpeople ตรวจสอบความถูกต้องของหน่วย
5. **เข้ากันได้**: ยังใช้ระบบเดิมกับ Imperial units ได้

### การทดสอบ

รันตัวอย่างเพื่อทดสอบ:

```bash
python examples/si_units_demo.py
python examples/concrete_aci318m_si_example.py
```

### หมายเหตุ

- forallpeople เป็น optional dependency - ถ้าไม่ติดตั้งก็ยังใช้งานระบบเดิมได้
- SI units constants ตาม ACI 318M-25 official values
- รองรับทั้ง metric และ Imperial units ในโปรเจคเดียวกัน

### อ้างอิง

- [ACI 318M-25](https://www.concrete.org/store/productdetail.aspx?ItemID=318M25) - Building Code Requirements for Structural Concrete (Metric)
- [forallpeople](https://github.com/connorferster/forallpeople) - Python SI units library
- [efficalc Documentation](https://youandvern.github.io/efficalc) - Original documentation
