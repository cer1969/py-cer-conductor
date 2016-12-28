# CRISTIAN ECHEVERRÍA RABÍ

from cer.value.checker import Check
from .constants import (CF_CLASSIC, CF_IEEE, TA_MIN, TA_MAX, TC_MIN, TC_MAX, ITER_MAX)

from . import _ccx

#-----------------------------------------------------------------------------------------

__all__ = ['CurrentCalc']

#-----------------------------------------------------------------------------------------

class CurrentCalc(object):
    """Object to calculate conductor current and temperatures.
    
    Read-only properties
    conductor  : Conductor instance
    
    Read-write properties
    altitude    : Altitude [m] = 300.0
    airVelocity : Velocity of air stream [ft/seg] =   2.0
    sunEffect   : Sun effect factor (0 to 1) = 1.0
    emissivity  : Emissivity (0 to 1) = 0.5  
    formula     : Define formula for current calculation = CF_IEEE
    deltaTemp   : Temperature difference to determine equality [°C] = 0.01
    
    """
    __slots__ = ('_conductor', '_cc')
    
    def __init__(self, conductor):
        """
        conductor : Conductor instance. 
        Valid values are required for r25, diameter and category.alpha
        """
        Check(conductor._diameter).gt(0)
        Check(conductor._r25).gt(0)
        Check(conductor._category._alpha).gt(0).lt(1)
        
        self._conductor = conductor

        self._cc = _ccx.CurrentCalc(conductor._diameter, conductor._r25, conductor._category._alpha,
                                    TC_MAX, TA_MIN, TA_MAX)
        
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def getResistance(self, tc):
        """Returns resistance [Ohm/km]
        tc : Conductor temperature [°C]
        """
        Check(tc).ge(TC_MIN).le(TC_MAX)
        return self._cc.getResistance(tc)

    def getCurrent(self, ta, tc):
        """Returns current [ampere]
        ta : Ambient temperature [°C]
        tc : Conductor temperature [°C]
        """
        Check(ta).ge(TA_MIN).le(TA_MAX)
        Check(tc).ge(TC_MIN).le(TC_MAX)
        return self._cc.getCurrent(ta, tc)
    
    def getTc(self, ta, ic):
        """Returns conductor temperature [ampere]
        ta : Ambient temperature [°C]
        ic : Current [ampere]
        """
        Check(ta).ge(TA_MIN).le(TA_MAX)
        _Imin = 0
        _Imax = self.getCurrent(ta, TC_MAX)
        Check(ic).ge(_Imin).le(_Imax) # Ensure ta <= Tc <= TC_MAX
        return self._cc.getTc(ta, ic)
    
    def getTa(self, tc, ic):
        """Returns ambient temperature [ampere]
        tc : Conductor temperature [°C]
        ic : Current [ampere]
        """
        Check(tc).ge(TC_MIN).le(TC_MAX)
        
        _Imin = self.getCurrent(TA_MAX, tc)
        _Imax = self.getCurrent(TA_MIN, tc)
        Check(ic).ge(_Imin).le(_Imax) # Ensure TA_MIN =< Ta =< TA_MAX
        return self._cc.getTa(tc, ic)
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    @property
    def conductor(self):
        return self._conductor
    
    @property
    def altitude(self):
        return self._cc.altitude
    
    @altitude.setter
    def altitude(self, value):
        Check(value).ge(0)
        self._cc.altitude = value
    
    @property
    def airVelocity(self):
        return self._cc.airVelocity
    
    @airVelocity.setter
    def airVelocity(self, value):
        Check(value).ge(0)
        self._cc.airVelocity = value
    
    @property
    def sunEffect(self):
        return self._cc.sunEffect
    
    @sunEffect.setter
    def sunEffect(self, value):
        Check(value).ge(0).le(1)
        self._cc.sunEffect = value
    
    @property
    def emissivity(self):
        return self._cc.emissivity
    
    @emissivity.setter
    def emissivity(self, value):
        Check(value).ge(0).le(1)
        self._cc.emissivity = value
    
    @property
    def formula(self):
        formula = CF_IEEE if self._cc.formula == 0 else CF_CLASSIC
        return formula
    
    @formula.setter
    def formula(self, value):
        Check(value).isIn([CF_CLASSIC, CF_IEEE])
        formula = 0 if value == CF_IEEE else 1
        self._cc.formula = formula
    
    @property
    def deltaTemp(self):
        return self._cc.deltaTemp
    
    @deltaTemp.setter
    def deltaTemp(self, value):
        Check(value).gt(0)
        self._cc.deltaTemp = value