# efficalc-THAI: ACI 318M-25 และ SI Units Support

## 🎯 วัตถุประสงค์

โปรเจค efficalc-THAI เป็นการปรับปรุง [efficalc](https://github.com/youandvern/efficalc) เพื่อรองรับ:

- **ACI 318M-25** - Building Code Requirements for Structural Concrete (Metric)
- **SI Units** - ระบบหน่วยสากล (International System of Units)
- **การแปลงหน่วย** ระหว่าง Imperial และ Metric systems

## 🚀 คุณสมบัติใหม่

### ✅ สิ่งที่เพิ่มขึ้น

- 🌍 **SI Units Support**: ใช้ [forallpeople](https://github.com/connorferster/forallpeople) สำหรับจัดการหน่วย SI
- 📊 **ACI 318M-25 Constants**: ค่าคงที่และสูตรตามมาตรฐาน ACI 318M-25
- 🔄 **Unit Conversions**: แปลงหน่วยระหว่าง Imperial ↔ SI อัตโนมัติ
- 📋 **Ready-to-use Examples**: ตัวอย่างการออกแบบคอนกรีตด้วย SI units

### 📦 หน่วยที่รองรับ

#### ความยาว (Length)
- `mm`, `cm`, `m`, `km`

#### แรง (Force)  
- `N`, `kN`, `MN`

#### ความเค้น (Stress/Pressure)
- `Pa`, `kPa`, `MPa`, `GPa`

#### พื้นที่ (Area)
- `mm^2`, `cm^2`, `m^2`

#### ปริมาตร (Volume)
- `mm^3`, `cm^3`, `m^3`

#### โมเมนต์ (Moment)
- `N⋅m`, `kN⋅m`, `MN⋅m`

## 📥 การติดตั้ง

### 1. Clone Repository

```bash
git clone https://github.com/buildsmart888/efficalc-THAI.git
cd efficalc-THAI
```

### 2. สร้าง Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

หรือติดตั้งแยก:
```bash
pip install forallpeople>=1.0.0
```

## 🔧 การใช้งาน

### ตัวอย่างพื้นฐาน - คานคอนกรีต

```python
from efficalc import *

def concrete_beam_si():
    Title("Concrete Beam Analysis - ACI 318M-25")
    
    # Material Properties (SI Units)
    fc = Input("f'_c", 25, "MPa", "Concrete compressive strength")
    fy = Input("f_y", 420, "MPa", "Steel yield strength")
    
    # Geometry (SI Units)
    b = Input("b", 300, "mm", "Beam width")
    d = Input("d", 500, "mm", "Effective depth")
    As = Input("A_s", 1500, "mm^2", "Steel area")
    
    # Steel ratio calculation
    rho = Calculation("\\rho", As / (b * d), "", "Steel ratio")
    
    # ACI 318M-25 minimum reinforcement check
    rho_min = Calculation("\\rho_{min}", 1.4 / fy, "", "Minimum steel ratio", 
                         "ACI 318M-25 9.6.1.2")
    
    Comparison(rho, ">=", rho_min, "OK", "NG", "Minimum steel check")

if __name__ == "__main__":
    from efficalc.report_builder import ReportBuilder
    builder = ReportBuilder(concrete_beam_si)
    builder.view_report()
```

### ตัวอย่างเสาคอนกรีต

```python
from efficalc import *

def concrete_column_si():
    Title("Concrete Column Design - ACI 318M-25")
    
    # Material properties
    fc = Input("f'_c", 25, "MPa", "Concrete strength")
    fy = Input("f_y", 420, "MPa", "Steel yield")
    
    # Column geometry
    h = Input("h", 400, "mm", "Column dimension")
    b = Input("b", 400, "mm", "Column dimension")
    As = Input("A_s", 3200, "mm^2", "Total steel area")
    
    # Calculations
    Ag = Calculation("A_g", h * b, "mm^2", "Gross area")
    rho_g = Calculation("\\rho_g", As / Ag, "", "Gross steel ratio")
    
    # ACI 318M-25 checks
    Comparison(rho_g, ">=", 0.01, "Min OK", "NG", "Min steel", "ACI 318M-25 10.6.1.1")
    Comparison(rho_g, "<=", 0.08, "Max OK", "NG", "Max steel", "ACI 318M-25 10.6.1.1")
    
    # Nominal strength (tied column)
    Pn = Calculation("P_n", 
                     0.8 * (0.85 * fc * (Ag - As) + fy * As) / 1000,
                     "kN", "Nominal strength", "ACI 318M-25 22.4.2.2")
    
    # Design strength
    phi_c = ACI318M_Constants.PHI_COMPRESSION
    Pd = Calculation("P_d", phi_c * Pn, "kN", "Design strength")
```

### การแปลงหน่วย

```python
from efficalc import *

def unit_conversion_example():
    Title("Unit Conversion: Imperial ↔ SI")
    
    # Imperial inputs
    fc_psi = Input("f'_c", 3000, "psi", "Concrete strength (Imperial)")
    width_in = Input("b", 12, "in", "Width (Imperial)")
    
    # Convert to SI
    fc_mpa = Calculation("f'_c_SI", fc_psi * psi_to_kPa / 1000, "MPa", 
                        "Concrete strength (SI)")
    width_mm = Calculation("b_SI", width_in * in_to_mm, "mm", 
                          "Width (SI)")
    
    # Convert back to Imperial
    fc_psi_back = Calculation("f'_c_back", fc_mpa * 1000 / psi_to_kPa, "psi", 
                             "Converted back to Imperial")
```

## 🧪 การทดสอบ

### รันตัวอย่าง

```bash
# ตัวอย่าง SI Units พื้นฐาน
python examples/si_units_demo.py

# ตัวอย่าง ACI 318M-25
python examples/concrete_aci318m_si_example.py

# Main demo ที่ปรับปรุง
python main.py
```

### ตรวจสอบ SI Units

```python
# ตรวจสอบว่า forallpeople ติดตั้งถูกต้อง
import forallpeople as si
si.environment('default')

pressure = 25 * si.MPa
area = 300 * si.mm * 500 * si.mm
force = pressure * area

print(f"Pressure: {pressure}")  # 25.000 MPa
print(f"Area: {area}")          # 150000.000 mm^2  
print(f"Force: {force}")        # 3.750 kN
```

## 📚 ค่าคงที่ ACI 318M-25

### Material Properties
```python
ACI318M_Constants.STEEL_E              # 200,000 MPa
ACI318M_Constants.MAX_CONCRETE_STRAIN  # 0.003
ACI318M_Constants.CONCRETE_DENSITY     # 2400 kg/m^3
```

### Minimum Covers
```python
ACI318M_Constants.MIN_COVER_SLAB    # 20 mm
ACI318M_Constants.MIN_COVER_BEAM    # 25 mm  
ACI318M_Constants.MIN_COVER_COLUMN  # 40 mm
```

### Strength Reduction Factors
```python
ACI318M_Constants.PHI_FLEXURE      # 0.9
ACI318M_Constants.PHI_COMPRESSION  # 0.65 (tied)
ACI318M_Constants.PHI_SHEAR        # 0.75
```

## 📁 โครงสร้างโปรเจค

```
efficalc-THAI/
├── efficalc/
│   ├── si_units.py              # SI units และ ACI constants
│   ├── __init__.py              # Export SI units
│   └── unit_conversions.py      # Imperial units (เดิม)
├── examples/
│   ├── si_units_demo.py         # Demo SI units
│   ├── concrete_aci318m_si_example.py  # ACI 318M-25 examples
│   └── concrete_beam_neutral_axis.py   # Original Imperial
├── SI_UNITS_GUIDE.md            # คู่มือการใช้งาน SI
├── requirements.txt             # Dependencies รวม forallpeople
└── main.py                      # Demo ที่ปรับปรุง
```

## 🔄 Backward Compatibility

โปรเจคนี้ยังคงรองรับการใช้งานแบบเดิม:
- Imperial units ยังใช้ได้ปกติ
- AISC steel sections ทำงานเหมือนเดิม  
- API เดิมไม่เปลี่ยนแปลง

หาก forallpeople ไม่ติดตั้ง โปรแกรมจะทำงานแบบเดิมโดยไม่มี SI units support

## 🎯 Use Cases

### สำหรับวิศวกรไทย
- ใช้ SI units ตามมาตรฐานสากล
- รองรับ ACI 318M-25 ที่เป็น metric version
- แปลงหน่วยระหว่างระบบต่างๆ ได้

### สำหรับโปรเจคนานาชาติ  
- ส่งมอบเอกสารเป็น SI units
- ใช้มาตรฐาน ACI 318M-25 
- ความเข้ากันได้กับซอฟต์แวร์ metric อื่นๆ

### สำหรับการศึกษา
- เรียนรู้ concrete design ด้วย SI units
- เปรียบเทียบ Imperial vs Metric
- ทำความเข้าใจ ACI 318M-25

## 🤝 Contributing

1. Fork โปรเจค
2. สร้าง feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit การเปลี่ยนแปลง (`git commit -m 'Add some AmazingFeature'`)
4. Push ไป branch (`git push origin feature/AmazingFeature`)
5. เปิด Pull Request

## 📄 License

MIT License - ดู [LICENSE](LICENSE) สำหรับรายละเอียด

## 🙏 Acknowledgments

- [efficalc](https://github.com/youandvern/efficalc) - Original library
- [forallpeople](https://github.com/connorferster/forallpeople) - SI units support
- [ACI 318M-25](https://www.concrete.org) - Concrete design standard

---

**หมายเหตุ**: โปรเจคนี้เป็นการปรับปรุงเพื่อรองรับ ACI 318M-25 และ SI Units โดยไม่กระทบต่อ functionality เดิม
