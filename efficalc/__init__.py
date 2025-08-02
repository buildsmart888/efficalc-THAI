from latexexpr_efficalc import (
    a_brackets,
    absolute,
    add,
    brackets,
    c_brackets,
    cos,
    cosh,
    div,
    div2,
    exp,
    ln,
    log,
    log10,
    maximum,
    minimum,
    minus,
    mul,
    neg,
    plus,
    pos,
    power,
    r_brackets,
    root,
    s_brackets,
    sin,
    sinh,
    sqr,
    sqrt,
    sub,
    tan,
    tanh,
    times,
)

from .base_definitions.assumption import Assumption
from .base_definitions.calculation import Calculation, CalculationLength
from .base_definitions.comparison import Comparison
from .base_definitions.comparison_statement import ComparisonStatement
from .base_definitions.figure import (
    FigureBase,
    FigureFromBytes,
    FigureFromFile,
    FigureFromMatplotlib,
)
from .base_definitions.heading import Heading
from .base_definitions.input import Input
from .base_definitions.shared import (
    CalculationItem,
    clear_all_input_default_overrides,
    clear_saved_objects,
    get_all_calc_objects,
    get_override_or_default_value,
    save_calculation_item,
    set_input_default_overrides,
)
from .base_definitions.symbolic import Symbolic
from .base_definitions.table import InputTable, Table
from .base_definitions.text_block import TextBlock
from .base_definitions.title import Title
from .constants import ONE, PI, TWO, ZERO, E
from .unit_conversions import deg_to_rad, ft_to_in, k_to_lb

# Import SI units and conversions (optional import to handle missing forallpeople)
try:
    from .si_units import (
        # SI Base units
        mm, cm, m, km,
        N, kN, MN,
        Pa, kPa, MPa, GPa,
        mm2, cm2, m2,
        mm3, cm3, m3,
        Nm, kNm, MNm,
        
        # Conversion factors
        in_to_mm, ft_to_m, in_to_m,
        lb_to_N, kip_to_kN,
        psi_to_kPa, ksi_to_MPa,
        in2_to_mm2, in2_to_cm2,
        in3_to_cm3,
        kip_ft_to_kNm, lb_ft_to_Nm,
        
        # Constants and utilities
        ACI318M_Constants,
        convert_imperial_to_si,
        validate_units_consistency,
    )
    
    # Set a flag to indicate SI units are available
    SI_UNITS_AVAILABLE = True
    
except ImportError:
    # If forallpeople is not installed, set flag to False
    SI_UNITS_AVAILABLE = False
    
    # Create placeholder variables to prevent import errors
    class SIUnitsNotAvailable:
        def __getattr__(self, name):
            raise ImportError(
                f"SI Units feature requires 'forallpeople' library. "
                f"Install it with: pip install forallpeople"
            )
    
    _si_placeholder = SIUnitsNotAvailable()
    
    # Assign placeholders for SI units
    mm = cm = m = km = _si_placeholder
    N = kN = MN = _si_placeholder  
    Pa = kPa = MPa = GPa = _si_placeholder
    mm2 = cm2 = m2 = _si_placeholder
    mm3 = cm3 = m3 = _si_placeholder
    Nm = kNm = MNm = _si_placeholder
    
    # Conversion factors placeholders
    in_to_mm = ft_to_m = in_to_m = _si_placeholder
    lb_to_N = kip_to_kN = _si_placeholder
    psi_to_kPa = ksi_to_MPa = _si_placeholder
    in2_to_mm2 = in2_to_cm2 = _si_placeholder
    in3_to_cm3 = _si_placeholder
    kip_ft_to_kNm = lb_ft_to_Nm = _si_placeholder
    
    # Constants and utilities placeholders
    ACI318M_Constants = _si_placeholder
    convert_imperial_to_si = _si_placeholder
    validate_units_consistency = _si_placeholder
