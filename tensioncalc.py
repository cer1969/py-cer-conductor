# CRISTIAN ECHEVERRÍA RABÍ

import math

from cer.value import check, deco
from .constants import (ITER_MAX, TENSION_MAX)

#-----------------------------------------------------------------------------------------

__all__ = ['TensionCalc']

#-----------------------------------------------------------------------------------------

def _annulsEquation(L, P1, P2, T1, T2, t1, t2, S, M, cfd):
    # Annuls equation of state for iterations. Returns tension value [kg].
    # L      : Ruling span [m] (Luz equivalente)
    # P1, P2 : Transverse tension [kg/m]
    # T1, T2 : Longitudinal tension [kg]
    # t1, t2 : Conductor temperatures [°C]
    # S      : conductor.ares
    # M      : conductor.modelas
    # cfd    : conductor.coefexp
    value = (L**2/24)*((P1**2)*(T2**2)-(P2**2)*(T1**2)) + \
            cfd*(T1**2)*(T2**2)*(t2 - t1) + \
            (T1**2)*(T2**2)*((T2 - T1)/(S*M))
    return value


#-----------------------------------------------------------------------------------------

class TensionCalc(object):
    """Objecto to calculate conductor tension and related parameter (sag and time)
    
    Read-only properties
    conductor  : Conductor instance
    iceLoadRef   : Ice load at reference point [kg/m]
    iceLoadCal   : Ice load at calculation point [kg/m]
    windLoadRef  : Wind load at reference point [kg/m]
    windLoadCal  : Wind load at calculation point [kg/m]
    transLoadRef : Transverse load at reference point [kg/m]
    transLoadCal : Transverse load at calculation point [kg/m]
    
    Read-write properties
    tensionFactorRef : Tension factor at reference point (0 to 1) = 0.2
    tensionRef       : Tension at reference point [kg] 
                       tensionRef = TensionFactorRef * conductor.strength 
    tempRef          : Conductor temperature at reference point [°C] = 15.0
    creepFactorRef   : Creep factor at reference point (0 to 1) = 1.0 
    iceThickRef      : Ice thickness at reference point [mm] = 0.0
    windPressureRef  : Wind pressure at reference point [kg/m2] = 0.0
    creepFactorCal   : Creep factor at calculation point (0 to 1) = 1.0
    iceThickCal      : Ice thickness at calculation point [mm] = 0.0
    windPressureCal  : Wind pressure at calculation point [kg/m2] = 0.0
    deltaTension     : Tension difference to determine equality [kg] = 0.001
    """
    
    __slots__ = ('_conductor', 
                 '_tensionFactorRef', '_tempRef',
                 '_creepFactorRef', '_iceThickRef', '_windPressureRef',
                 '_creepFactorCal', '_iceThickCal', '_windPressureCal',
                 '_deltaTension')
    
    def __init__(self, conductor):
        """
        conductor: Conductor instance.
        Valid values are required for diameter, area, weight, strength and
        category (modelas, coefexp, creep)
        """
        check.gt(conductor.diameter, 0)
        check.gt(conductor.area, 0)
        check.gt(conductor.weight, 0)
        check.gt(conductor.strength, 0)
        check.gt(conductor.category.modelas, 0)
        check.gt(conductor.category.coefexp, 0)
        check.ge(conductor.category.creep, 0)
        
        self._conductor = conductor
        
        self._tensionFactorRef = 0.2
        self._tempRef = 15.0
        self._creepFactorRef = 1.0
        self._iceThickRef = 0.0
        self._windPressureRef = 0.0
        
        self._creepFactorCal = 1.0
        self._iceThickCal = 0.0
        self._windPressureCal = 0.0
        self._deltaTension = 0.001

    #-------------------------------------------------------------------------------------
    # Public methods
    
    def getTension(self, rs, tc):
        """Returns conductor tension [kg]
        rs : Ruling span [m] (Luz equivalente)
        tc : Conductor temperature [°C]
             Without current is equal to ambiente temperature. 
        """
        check.gt(rs, 0)
        
        P1 = self.transLoadRef
        P2 = self.transLoadCal
        T1 = self.tensionRef
        t1 = self._tempRef
        S = self._conductor.area
        M = self._conductor.category.modelas
        cfd = self._conductor.category.coefexp

        # calculate creep to apply
        creep = (self._creepFactorCal - self._creepFactorRef)*self._conductor.category.creep
        
        Tmin = 0
        Tmax = TENSION_MAX
        cuenta = 0
        while (Tmax - Tmin) > self._deltaTension:
            Tmed = 0.5*(Tmin + Tmax)
            valor = _annulsEquation(rs, P1, P2, T1, Tmed, t1, tc + creep, S, M, cfd)
            if valor > 0:
                Tmax = Tmed
            else:
                Tmin = Tmed
            cuenta = cuenta + 1
            if cuenta > ITER_MAX:
                err_msg = "getTension: Nº iterations > %d" % ITER_MAX
                raise RuntimeError(err_msg)
        return Tmed
    
#=========================================================================================
#    def GetTensionTable(self, rs, span, tcList, nper=1):
#        """Retorna tabla con valores de Tc, tensión de templado en kg, flecha máxima 
#        en metros y tiempo de percusiones en segundos.
#        rs     : Ruling span [m] (Luz equivalente)
#        span   : Test span [m] (Luz de temple)
#        tcList : Lista con temperatura del conductor en °C. Si no hay transferencia es igual a T° ambiente.
#        nper   :   N° de percusiones para calcular tiempo 
#        """
#        data = []
#        for tc in tcList:
#            tension = self.getTension(rs, tc)
#            sag = self.getSag(tension, span)
#            stime = nper * self.getSagTime(sag)
#            data.append((tc, tension, sag, stime))
#        return sal
#=========================================================================================
    
    def getSag(self, tension, span):
        """Returns maximum sag at calculation point [m]
        tension : Conductor tension [kg]
        span    : Test span [m] (Luz de temple)
        """
        P = self.iceLoadCal
        a = tension/P
        x = span / 2
        return a*(math.cosh(x/a)-1)

    @staticmethod
    def getSagTime(sag):
        """staticmethod: Returns sag time [sec] for one cicle
        sag : maximum sag [m]
        """
        return math.sqrt(sag/0.306)
    
    def getIceLoad(self, it):
        """Returns weight load of ice per unit length [kg/m]
        Water weights 1 kg per litre ( 1 m3 weights 1000 kg)
        it : Ice thickness [mm]
        """
        D = self._conductor.diameter
        P = self._conductor.weight
        return (it**2 + it*D) * math.pi * 0.001 + P
    
    def getWindLoad(self, it, wp):
        """Returns wind load per unit length [kg/m]
        it : Ice thickness [mm]
        wp : wind pressure [kg/m2]
        """ 
        D = self._conductor.diameter
        return (2*it + D)*wp*0.001
    
    def getTransLoad(self, it, wp):
        """Returns transverse load per unit length [kg/m]
        it : Ice thickness [mm]
        wp : wind pressure [kg/m2]
        """ 
        FH = self.getIceLoad(it)
        FV = self.getWindLoad(it, wp)
        return math.sqrt(FH**2 + FV**2)
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    @property
    def conductor(self):
        return self._conductor
    
    @property
    def iceLoadRef(self):
        return self.getIceLoad(self._iceThickRef)
    
    @property
    def iceLoadCal(self):
        return self.getIceLoad(self._iceThickCal)
    
    @property
    def windLoadRef(self):
        return self.getWindLoad(self._iceThickRef, self._windPressureRef)
    
    @property
    def windLoadCal(self):
        return self.getWindLoad(self._iceThickCal, self._windPressureCal)
    
    @property
    def transLoadRef(self):
        return self.getTransLoad(self._iceThickRef, self._windPressureRef)
    
    @property
    def transLoadCal(self):
        return self.getTransLoad(self._iceThickCal, self._windPressureCal)
    
    @property
    def tensionFactorRef(self):
        return self._tensionFactorRef
    
    @tensionFactorRef.setter
    def tensionFactorRef(self, value):
        check.ge(value, 0)
        check.le(value, 1)
        self._tensionFactorRef = value
    
    @property
    def tensionRef(self):
        return self._tensionFactorRef*self._conductor.strength
    
    @tensionRef.setter
    def tensionRef(self, value):
        check.ge(value, 0)
        self._tensionFactorRef = value/self._conductor.strength
    
    @property
    def tempRef(self):
        return self._tempRef
    
    @tempRef.setter
    def tempRef(self, value):
        self._tempRef = value
    
    @property
    def creepFactorRef(self):
        return self._creepFactorRef
    
    @creepFactorRef.setter
    def creepFactorRef(self, value):
        check.ge(value, 0)
        check.le(value, 1)
        self._creepFactorRef = value
    
    @property
    def iceThickRef(self):
        return self._iceThickRef
    
    @iceThickRef.setter
    def iceThickRef(self, value):
        check.ge(value, 0)
        self._iceThickRef = value
    
    @property
    def windPressureRef(self):
        return self._windPressureRef
    
    @windPressureRef.setter
    def windPressureRef(self, value):
        check.ge(value, 0)
        self._windPressureRef = value
    
    @property
    def creepFactorCal(self):
        return self._creepFactorCal
    
    @creepFactorCal.setter
    def creepFactorCal(self, value):
        check.ge(value, 0)
        check.le(value, 1)
        self._creepFactorCal = value
    
    @property
    def iceThickCal(self):
        return self._iceThickCal
    
    @iceThickCal.setter
    def iceThickCal(self, value):
        check.ge(value, 0)
        self._iceThickCal = value
    
    @property
    def windPressureCal(self):
        return self._windPressureCal
    
    @windPressureCal.setter
    def windPressureCal(self, value):
        check.ge(value, 0)
        self._windPressureCal = value

    @property
    def deltaTension(self):
        return self._deltaTension
    
    @deltaTension.setter
    def deltaTension(self, value):
        check.gt(value, 0)
        self._deltaTension = value