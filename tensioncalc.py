# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division
import math

from cer.value import check, deco
from constants import (ITER_MAX, TENSION_MAX)

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
    # Properties methods
    
    def _getConductor(self):
        return self._conductor
    
    def _getIceLoadRef(self):
        return self.getIceLoad(self._iceThickRef)
    
    def _getIceLoadCal(self):
        return self.getIceLoad(self._iceThickCal)
    
    def _getWindLoadRef(self):
        return self.getWindLoad(self._iceThickRef, self._windPressureRef)
    
    def _getWindLoadCal(self):
        return self.getWindLoad(self._iceThickCal, self._windPressureCal)
    
    def _getTransLoadRef(self):
        return self.getTransLoad(self._iceThickRef, self._windPressureRef)
    
    def _getTransLoadCal(self):
        return self.getTransLoad(self._iceThickCal, self._windPressureCal)
    
    def _getTensionFactorRef(self):
        return self._tensionFactorRef
    
    @deco.ge(0)
    @deco.le(1)
    def _setTensionFactorRef(self, value):
        self._tensionFactorRef = value
    
    def _getTensionRef(self):
        return self._tensionFactorRef*self._conductor.strength
    
    @deco.ge(0)
    def _setTensionRef(self, value):
        self._tensionFactorRef = value/self._conductor.strength
    
    def _getTempRef(self):
        return self._tempRef
    
    def _setTempRef(self, value):
        self._tempRef = value
    
    def _getCreepFactorRef(self):
        return self._creepFactorRef
    
    @deco.ge(0)
    @deco.le(1)
    def _setCreepFactorRef(self, value):
        self._creepFactorRef = value
    
    def _getIceThickRef(self):
        return self._iceThickRef
    
    @deco.ge(0)
    def _setIceThickRef(self, value):
        self._iceThickRef = value
    
    def _getWindPressureRef(self):
        return self._windPressureRef
    
    @deco.ge(0)
    def _setWindPressureRef(self, value):
        self._windPressureRef = value
    
    def _getCreepFactorCal(self):
        return self._creepFactorCal
    
    @deco.ge(0)
    @deco.le(1)
    def _setCreepFactorCal(self, value):
        self._creepFactorCal = value
    
    def _getIceThickCal(self):
        return self._iceThickCal
    
    @deco.ge(0)
    def _setIceThickCal(self, value):
        self._iceThickCal = value
    
    def _getWindPressureCal(self):
        return self._windPressureCal
    
    @deco.ge(0)
    def _setWindPressureCal(self, value):
        self._windPressureCal = value
    
    def _getDeltaTension(self):
        return self._deltaTension
    
    @deco.gt(0)
    def _setDeltaTension(self, value):
        self._deltaTension = value
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    conductor    = property(_getConductor)
    iceLoadRef   = property(_getIceLoadRef)
    iceLoadCal   = property(_getIceLoadCal)
    windLoadRef  = property(_getWindLoadRef)
    windLoadCal  = property(_getWindLoadCal)
    transLoadRef = property(_getTransLoadRef)
    transLoadCal = property(_getTransLoadCal)
    
    tensionFactorRef = property(_getTensionFactorRef, _setTensionFactorRef)
    tensionRef       = property(_getTensionRef,       _setTensionRef)
    tempRef          = property(_getTempRef,          _setTempRef)
    creepFactorRef   = property(_getCreepFactorRef,   _setCreepFactorRef)
    iceThickRef      = property(_getIceThickRef,      _setIceThickRef)
    windPressureRef  = property(_getWindPressureRef,  _setWindPressureRef)
    creepFactorCal   = property(_getCreepFactorCal,   _setCreepFactorCal)
    iceThickCal      = property(_getIceThickCal,      _setIceThickCal)
    windPressureCal  = property(_getWindPressureCal,  _setWindPressureCal)
    deltaTension     = property(_getDeltaTension,     _setDeltaTension)
    