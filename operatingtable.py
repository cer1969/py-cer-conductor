# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division

from cer.utils.value import check
from cer.utils.value import deco
from constants import (CF_ENDESA, CF_IEEE, TC_MIN, TC_MAX)

#-----------------------------------------------------------------------------------------

__all__ = ['OperatingItem', 'OperatingTable']

#-----------------------------------------------------------------------------------------

class OperatingItem(object):
    """Container for conductor and operating conditions
    
    Read-only properties
    currentcalc : CurrentCalc instance
    tempMaxOp   : Maximux operating temperature for currentcalc.conductor [°C]
    nsc         : Number of subconductor per fase
    
    """
    
    __slots__ = ('_currentcalc', '_tempMaxOp','_nsc')

    def __init__(self, currentcalc, tempMaxOp=50.0, nsc=1, altitude=300.0,
                 emissivity=0.5):
        """
        currentcalc : CurrentCalc instance
        tempMaxOp   : Maximum operating temperature for currentcalc.conductor [°C]
        nsc         : Number of subconductor per face
        altitude    : Altitude [m] = 300.0
        emissivity  : Emissivity (0 to 1) = 0.5
        """
        currentcalc.altitude = altitude
        currentcalc.emissivity = emissivity
        check.ge(tempMaxOp, TC_MIN)
        check.le(tempMaxOp, TC_MAX)
        check.ge(nsc, 1)
        
        self._currentcalc = currentcalc
        self._tempMaxOp = tempMaxOp
        self._nsc = nsc

    #-------------------------------------------------------------------------------------

    def getCurrent(self, ta):
        """Returns current for the OperatingItems [ampere]
        ta : Ambient temperature [°C]
        """
        return self.currentcalc.getCurrent(ta, self.tempMaxOp) * self.nsc

    #-------------------------------------------------------------------------------------
    
    def getCurrentList(self, taList):
        """Returns list with current [ampere]
        taList: Secuence with ambient temperatures [°C]
        """
        sal = [self.getCurrent(ta) for ta in taList]
        return sal
    
    #--------------------------------------------------------------------------
    # Properties methods
    
    def _getCurrentCalc(self):
        return self._currentcalc
    
    def _getTempMaxOp(self):
        return self._tempMaxOp
    
    def _getNsc(self):
        return self._nsc
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    currentcalc  = property(_getCurrentCalc)
    tempMaxOp    = property(_getTempMaxOp)
    nsc          = property(_getNsc)

#-----------------------------------------------------------------------------------------

class OperatingTable(list):
    """Mutable secuence to store OperatingItem instances and calculates current.
    
    Read-only properties
    idx : Optional database key
    
    """

    __slots__ = ('idx',)

    def __init__(self, items=None, idx=None):
        """
        items : Secuence with OperatingItem instance
        idx   : Database key
        """
        its = [] if items is None else items
        
        list.__init__(self, its)
        self.idx = idx
    
    #-------------------------------------------------------------------------------------

    def getCurrent(self, ta):
        """Returns lowest current for the OperatingItems contained [ampere]
        ta : Ambient temperature [°C]
        """
        minimo = 100000
        for item in self:
            amp = item.getCurrent(ta)
            if amp < minimo: minimo = amp
        return minimo
    
    def getCurrentList(self, taList):
        """Returns list with current [ampere]
        taList: Secuence with ambient temperatures [°C]
        """
        sal = [self.getCurrent(ta) for ta in taList]
        return sal

    #-------------------------------------------------------------------------------------
    # Properties methods 
    
    def _getAirVelocity(self):
        return self[0].currentcalc.airVelocity

    @deco.ge(0)
    def _setAirVelocity(self, value):
        for i in self:
            i.currentcalc.airVelocity = value 
    
    def _getSunEffect(self):
        return self[0].currentcalc.sunEffect
    
    @deco.ge(0)
    @deco.le(1)
    def _setSunEffect(self, value):
        for i in self:
            i.currentcalc.sunEffect = value
    
    def _getEmissivity(self):
        return self[0].currentcalc.emissivity

    @deco.ge(0)
    @deco.le(1)
    def _setEmissivity(self, value):
        for i in self:
            i.currentcalc.emissivity = value
    
    def _getFormula(self):
        return self[0].currentcalc.formula
    
    @deco.isIn([CF_ENDESA, CF_IEEE])
    def _setFormula(self, value):
        for i in self:
            i.currentcalc.formula = value

    #-------------------------------------------------------------------------------------
    # Properties
    
    airVelocity = property(_getAirVelocity, _setAirVelocity)
    sunEffect   = property(_getSunEffect,   _setSunEffect)
    emissivity  = property(_getEmissivity,  _setEmissivity)
    formula     = property(_getFormula,     _setFormula)
