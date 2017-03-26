# CRISTIAN ECHEVERRÍA RABÍ

from .constants import (TC_MIN, TC_MAX)

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

    def __init__(self, currentcalc, tempMaxOp=50.0, nsc=1):
        """
        currentcalc : CurrentCalc instance
        tempMaxOp   : Maximum operating temperature for currentcalc.conductor [°C]
        nsc         : Number of subconductor per face
        """
        if tempMaxOp < TC_MIN: raise ValueError("tempMaxOp < TC_MIN")
        if tempMaxOp > TC_MAX: raise ValueError("tempMaxOp > TC_MAX")
        if nsc < 1: raise ValueError("nsc < 1")
        
        self._currentcalc = currentcalc
        self._tempMaxOp = tempMaxOp
        self._nsc = nsc

    #-------------------------------------------------------------------------------------

    def getCurrent(self, ta):
        """Returns current for the OperatingItems [ampere]
        ta : Ambient temperature [°C]
        """
        return self._currentcalc.getCurrent(ta, self._tempMaxOp) * self._nsc
    
    #--------------------------------------------------------------------------
    # Properties
    
    @property
    def currentcalc(self):
        return self._currentcalc
    
    @property
    def tempMaxOp(self):
        return self._tempMaxOp
    
    @property
    def nsc(self):
        return self._nsc


#-----------------------------------------------------------------------------------------

class OperatingTable(list):
    """Object to store OperatingItem instances and calculates current.
    
    Read-only properties
    idx : Optional database key
    items: List of OperatingItem instances
    
    """

    __slots__ = ('_idx', '_items')

    def __init__(self, idx=None):
        """
        idx   : Database key
        """
        self._items = []
        self._idx = idx
    
    #-------------------------------------------------------------------------------------

    def getCurrent(self, ta):
        """Returns lowest current for the OperatingItems contained [ampere]
        ta : Ambient temperature [°C]
        """
        minimo = 100000
        for item in self._items:
            amp = item.getCurrent(ta)
            if amp < minimo: minimo = amp
        return minimo
    
    #--------------------------------------------------------------------------
    # Properties
    
    @property
    def idx(self):
        return self._idx
    
    @property
    def items(self):
        return self._items