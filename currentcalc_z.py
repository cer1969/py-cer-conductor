# CRISTIAN ECHEVERRÍA RABÍ

from . import _zx

#-----------------------------------------------------------------------------------------

__all__ = ['CurrentCalc']

#-----------------------------------------------------------------------------------------

class CurrentCalc(_zx.CurrentCalc):

    __slots__ = ('_conductor',)
    
    def __init__(self, conductor):
        self._conductor = conductor
        super().__init__(conductor._diameter, conductor._r25, conductor._category._alpha)
    
    @property
    def conductor(self):
        return self._conductor