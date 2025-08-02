# Enhanced unit conversions for efficalc with SI Units support
# Using forallpeople library for comprehensive units handling

try:
    import forallpeople as si
    FORALLPEOPLE_AVAILABLE = True
    
    # Load the default SI environment
    si.environment('default')
    
except ImportError:
    FORALLPEOPLE_AVAILABLE = False
    si = None

# Import Variable from the main package
try:
    from latexexpr_efficalc import Variable
except ImportError:
    # Create a simple fallback Variable class
    class Variable:
        def __init__(self, latex_str, value, unit):
            self.latex_str = latex_str
            self.value = value
            self.unit = unit
            
        def get_value(self):
            return self.value
            
        def __str__(self):
            return f"{self.value} {self.unit}"
        
        def __mul__(self, other):
            if isinstance(other, (int, float)):
                return Variable(f"{self.latex_str} * {other}", self.value * other, self.unit)
            return NotImplemented
            
        def __rmul__(self, other):
            return self.__mul__(other)

# =============================================================================
# SI Base Units and Common Derived Units  
# =============================================================================

# Length units
mm = Variable(r"1 \ \mathrm{mm}", 0.001, "m")
cm = Variable(r"1 \ \mathrm{cm}", 0.01, "m")
m = Variable(r"1 \ \mathrm{m}", 1.0, "m")
km = Variable(r"1 \ \mathrm{km}", 1000.0, "m")

# Force units
N = Variable(r"1 \ \mathrm{N}", 1.0, "N")
kN = Variable(r"1 \ \mathrm{kN}", 1000.0, "N")
MN = Variable(r"1 \ \mathrm{MN}", 1e6, "N")

# Pressure/Stress units
Pa = Variable(r"1 \ \mathrm{Pa}", 1.0, "Pa")
kPa = Variable(r"1 \ \mathrm{kPa}", 1000.0, "Pa")
MPa = Variable(r"1 \ \mathrm{MPa}", 1e6, "Pa")
GPa = Variable(r"1 \ \mathrm{GPa}", 1e9, "Pa")

# Area units
mm2 = Variable(r"1 \ \mathrm{mm^2}", 1e-6, "m^2")
cm2 = Variable(r"1 \ \mathrm{cm^2}", 1e-4, "m^2")
m2 = Variable(r"1 \ \mathrm{m^2}", 1.0, "m^2")

# Volume units
mm3 = Variable(r"1 \ \mathrm{mm^3}", 1e-9, "m^3")
cm3 = Variable(r"1 \ \mathrm{cm^3}", 1e-6, "m^3")
m3 = Variable(r"1 \ \mathrm{m^3}", 1.0, "m^3")

# Moment units (Force * Length)
Nm = Variable(r"1 \ \mathrm{N \cdot m}", 1.0, "N*m")
kNm = Variable(r"1 \ \mathrm{kN \cdot m}", 1000.0, "N*m")
MNm = Variable(r"1 \ \mathrm{MN \cdot m}", 1e6, "N*m")

# =============================================================================
# Imperial to SI Conversions
# =============================================================================

# Length conversions
in_to_mm = Variable(r"25.4 \ \mathrm{mm/in}", 25.4, "mm/in")
ft_to_m = Variable(r"0.3048 \ \mathrm{m/ft}", 0.3048, "m/ft")
in_to_m = Variable(r"0.0254 \ \mathrm{m/in}", 0.0254, "m/in")

# Force conversions
lb_to_N = Variable(r"4.448 \ \mathrm{N/lb}", 4.448, "N/lb")
kip_to_kN = Variable(r"4.448 \ \mathrm{kN/kip}", 4.448, "kN/kip")

# Pressure conversions
psi_to_kPa = Variable(r"6.895 \ \mathrm{kPa/psi}", 6.895, "kPa/psi")
ksi_to_MPa = Variable(r"6.895 \ \mathrm{MPa/ksi}", 6.895, "MPa/ksi")

# Area conversions
in2_to_mm2 = Variable(r"645.16 \ \mathrm{mm^2/in^2}", 645.16, "mm^2/in^2")
in2_to_cm2 = Variable(r"6.4516 \ \mathrm{cm^2/in^2}", 6.4516, "cm^2/in^2")

# Volume conversions
in3_to_cm3 = Variable(r"16.387 \ \mathrm{cm^3/in^3}", 16.387, "cm^3/in^3")

# Moment conversions
kip_ft_to_kNm = Variable(r"1.356 \ \mathrm{kN \cdot m/(kip \cdot ft)}", 1.356, "kN*m/(kip*ft)")
lb_ft_to_Nm = Variable(r"1.356 \ \mathrm{N \cdot m/(lb \cdot ft)}", 1.356, "N*m/(lb*ft)")

# =============================================================================
# ACI 318M-25 Specific Constants
# =============================================================================

class ACI318M_Constants:
    """
    Constants from ACI 318M-25 (Metric version)
    """
    
    # Material Properties (typical values)
    CONCRETE_DENSITY = Variable(r"2400 \ \mathrm{kg/m^3}", 2400, "kg/m^3")  # Normal weight concrete
    STEEL_DENSITY = Variable(r"7850 \ \mathrm{kg/m^3}", 7850, "kg/m^3")    # Steel reinforcement
    
    # Modulus of Elasticity for Steel (ACI 318M-25 20.2.2.2)
    STEEL_E = Variable(r"200000 \ \mathrm{MPa}", 200000, "MPa")
    
    # Maximum concrete strain (ACI 318M-25 22.2.2.1)
    MAX_CONCRETE_STRAIN = Variable(r"0.003", 0.003, "")
    
    # Minimum concrete cover (typical values from ACI 318M-25 Table 20.5.1.3.1)
    MIN_COVER_SLAB = Variable(r"20 \ \mathrm{mm}", 20, "mm")      # Interior exposure
    MIN_COVER_BEAM = Variable(r"25 \ \mathrm{mm}", 25, "mm")     # Interior exposure
    MIN_COVER_COLUMN = Variable(r"40 \ \mathrm{mm}", 40, "mm")   # Interior exposure
    
    # Strength reduction factors (ACI 318M-25 Chapter 21)
    PHI_FLEXURE = Variable(r"0.9", 0.9, "")                     # Flexure
    PHI_COMPRESSION = Variable(r"0.65", 0.65, "")               # Compression (tied)
    PHI_COMPRESSION_SPIRAL = Variable(r"0.75", 0.75, "")        # Compression (spiral)
    PHI_SHEAR = Variable(r"0.75", 0.75, "")                     # Shear

# =============================================================================
# Helper Functions for Unit Conversion
# =============================================================================

def convert_imperial_to_si():
    """
    Helper function to convert common Imperial units to SI
    Returns a dictionary of conversion factors
    """
    conversions = {
        # Length
        'in_to_mm': in_to_mm,
        'ft_to_m': ft_to_m,
        'in_to_m': in_to_m,
        
        # Force
        'lb_to_N': lb_to_N,
        'kip_to_kN': kip_to_kN,
        
        # Pressure/Stress
        'psi_to_kPa': psi_to_kPa,
        'ksi_to_MPa': ksi_to_MPa,
        
        # Area
        'in2_to_mm2': in2_to_mm2,
        'in2_to_cm2': in2_to_cm2,
        
        # Volume
        'in3_to_cm3': in3_to_cm3,
        
        # Moment
        'kip_ft_to_kNm': kip_ft_to_kNm,
        'lb_ft_to_Nm': lb_ft_to_Nm,
    }
    return conversions

def validate_units_consistency(value1, unit1, value2, unit2):
    """
    Validate that two quantities have consistent dimensions
    using forallpeople Physical instances if available
    """
    if not FORALLPEOPLE_AVAILABLE:
        return True, "forallpeople not available - skipping unit validation"
    
    try:
        # Create Physical instances
        phys1 = value1 * getattr(si, unit1.replace('^', ''), si.m)  # Default to meter if unit not found
        phys2 = value2 * getattr(si, unit2.replace('^', ''), si.m)
        
        # Check if dimensions are compatible for addition
        try:
            result = phys1 + phys2
            return True, f"Units are compatible: {phys1} + {phys2} = {result}"
        except:
            return False, f"Units are incompatible: {phys1.dimensions} vs {phys2.dimensions}"
            
    except Exception as e:
        return False, f"Error validating units: {str(e)}"

# =============================================================================
# Export commonly used units for easy import
# =============================================================================

__all__ = [
    # SI Base units
    'mm', 'cm', 'm', 'km',
    'N', 'kN', 'MN',
    'Pa', 'kPa', 'MPa', 'GPa',
    'mm2', 'cm2', 'm2',
    'mm3', 'cm3', 'm3',
    'Nm', 'kNm', 'MNm',
    
    # Conversion factors
    'in_to_mm', 'ft_to_m', 'in_to_m',
    'lb_to_N', 'kip_to_kN',
    'psi_to_kPa', 'ksi_to_MPa',
    'in2_to_mm2', 'in2_to_cm2',
    'in3_to_cm3',
    'kip_ft_to_kNm', 'lb_ft_to_Nm',
    
    # Constants class
    'ACI318M_Constants',
    
    # Helper functions
    'convert_imperial_to_si',
    'validate_units_consistency',
    
    # Availability flag
    'FORALLPEOPLE_AVAILABLE',
]

# =============================================================================
# Imperial to SI Conversions
# =============================================================================

# Length conversions
in_to_mm = Variable(r"25.4 \ \mathrm{mm/in}", 25.4, "mm/in")
ft_to_m = Variable(r"0.3048 \ \mathrm{m/ft}", 0.3048, "m/ft")
in_to_m = Variable(r"0.0254 \ \mathrm{m/in}", 0.0254, "m/in")

# Force conversions
lb_to_N = Variable(r"4.448 \ \mathrm{N/lb}", 4.448, "N/lb")
kip_to_kN = Variable(r"4.448 \ \mathrm{kN/kip}", 4.448, "kN/kip")

# Pressure conversions
psi_to_kPa = Variable(r"6.895 \ \mathrm{kPa/psi}", 6.895, "kPa/psi")
ksi_to_MPa = Variable(r"6.895 \ \mathrm{MPa/ksi}", 6.895, "MPa/ksi")

# Area conversions
in2_to_mm2 = Variable(r"645.16 \ \mathrm{mm^2/in^2}", 645.16, "mm^2/in^2")
in2_to_cm2 = Variable(r"6.4516 \ \mathrm{cm^2/in^2}", 6.4516, "cm^2/in^2")

# Volume conversions
in3_to_cm3 = Variable(r"16.387 \ \mathrm{cm^3/in^3}", 16.387, "cm^3/in^3")

# Moment conversions
kip_ft_to_kNm = Variable(r"1.356 \ \mathrm{kN \cdot m/(kip \cdot ft)}", 1.356, "kN*m/(kip*ft)")
lb_ft_to_Nm = Variable(r"1.356 \ \mathrm{N \cdot m/(lb \cdot ft)}", 1.356, "N*m/(lb*ft)")

# =============================================================================
# ACI 318M-25 Specific Constants
# =============================================================================

class ACI318M_Constants:
    """
    Constants from ACI 318M-25 (Metric version)
    """
    
    # Material Properties (typical values)
    CONCRETE_DENSITY = Variable(r"2400 \ \mathrm{kg/m^3}", 2400, "kg/m^3")  # Normal weight concrete
    STEEL_DENSITY = Variable(r"7850 \ \mathrm{kg/m^3}", 7850, "kg/m^3")    # Steel reinforcement
    
    # Modulus of Elasticity for Steel (ACI 318M-25 20.2.2.2)
    STEEL_E = Variable(r"200000 \ \mathrm{MPa}", 200000, "MPa")
    
    # Maximum concrete strain (ACI 318M-25 22.2.2.1)
    MAX_CONCRETE_STRAIN = Variable(r"0.003", 0.003, "")
    
    # Minimum concrete cover (typical values from ACI 318M-25 Table 20.5.1.3.1)
    MIN_COVER_SLAB = Variable(r"20 \ \mathrm{mm}", 20, "mm")      # Interior exposure
    MIN_COVER_BEAM = Variable(r"25 \ \mathrm{mm}", 25, "mm")     # Interior exposure
    MIN_COVER_COLUMN = Variable(r"40 \ \mathrm{mm}", 40, "mm")   # Interior exposure
    
    # Strength reduction factors (ACI 318M-25 Chapter 21)
    PHI_FLEXURE = Variable(r"0.9", 0.9, "")                     # Flexure
    PHI_COMPRESSION = Variable(r"0.65", 0.65, "")               # Compression (tied)
    PHI_COMPRESSION_SPIRAL = Variable(r"0.75", 0.75, "")        # Compression (spiral)
    PHI_SHEAR = Variable(r"0.75", 0.75, "")                     # Shear

# =============================================================================
# Helper Functions for Unit Conversion
# =============================================================================

def convert_imperial_to_si():
    """
    Helper function to convert common Imperial units to SI
    Returns a dictionary of conversion factors
    """
    conversions = {
        # Length
        'in_to_mm': in_to_mm,
        'ft_to_m': ft_to_m,
        'in_to_m': in_to_m,
        
        # Force
        'lb_to_N': lb_to_N,
        'kip_to_kN': kip_to_kN,
        
        # Pressure/Stress
        'psi_to_kPa': psi_to_kPa,
        'ksi_to_MPa': ksi_to_MPa,
        
        # Area
        'in2_to_mm2': in2_to_mm2,
        'in2_to_cm2': in2_to_cm2,
        
        # Volume
        'in3_to_cm3': in3_to_cm3,
        
        # Moment
        'kip_ft_to_kNm': kip_ft_to_kNm,
        'lb_ft_to_Nm': lb_ft_to_Nm,
    }
    return conversions

def validate_units_consistency(value1, unit1, value2, unit2):
    """
    Validate that two quantities have consistent dimensions
    using forallpeople Physical instances
    """
    try:
        # Create Physical instances
        phys1 = value1 * getattr(si, unit1, si.m)  # Default to meter if unit not found
        phys2 = value2 * getattr(si, unit2, si.m)
        
        # Check if dimensions are compatible for addition
        try:
            result = phys1 + phys2
            return True, f"Units are compatible: {phys1} + {phys2} = {result}"
        except:
            return False, f"Units are incompatible: {phys1.dimensions} vs {phys2.dimensions}"
            
    except Exception as e:
        return False, f"Error validating units: {str(e)}"

# =============================================================================
# Export commonly used units for easy import
# =============================================================================

__all__ = [
    # SI Base units
    'mm', 'cm', 'm', 'km',
    'N', 'kN', 'MN',
    'Pa', 'kPa', 'MPa', 'GPa',
    'mm2', 'cm2', 'm2',
    'mm3', 'cm3', 'm3',
    'Nm', 'kNm', 'MNm',
    
    # Conversion factors
    'in_to_mm', 'ft_to_m', 'in_to_m',
    'lb_to_N', 'kip_to_kN',
    'psi_to_kPa', 'ksi_to_MPa',
    'in2_to_mm2', 'in2_to_cm2',
    'in3_to_cm3',
    'kip_ft_to_kNm', 'lb_ft_to_Nm',
    
    # Constants class
    'ACI318M_Constants',
    
    # Helper functions
    'convert_imperial_to_si',
    'validate_units_consistency',
]
