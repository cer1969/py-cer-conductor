# CRISTIAN ECHEVERRÍA RABÍ

import math

from cer.value import check, deco
from .constants import (TA_MIN, TA_MAX, TC_MAX, ITER_MAX)

#-----------------------------------------------------------------------------------------

__all__ = ['TcTimeCalc', 'TcTimeData']

#-----------------------------------------------------------------------------------------

class TcTimeCalc(object):
    """Object to produce TcTimeData instance and calculate the parameters involved.
    
    Read-only properties
    currentcalc : CurrentCalc instance
    icmax       : Maximum current (varies with the value of ta)
    
    Read-write properties
    ta        : Ambient temperature [°C]
    timeStep  : Time step for iterations (o to 60) [seconds]
    deltaIc   : Current difference to determine equality [ampere] = 0.01
    
    """

    __slots__ = ('_currentcalc', '_ta', '_icmax', '_timeStep', '_deltaIc')
    
    def __init__(self, currentcalc, ta):
        """
        currentcalc : CurrentCalc instance
        ta          : Ambient temperature [°C]
        Valid values are required for currentcalc.conductor.hcap and Ta
        """
        check.gt(currentcalc.conductor.hcap, 0)
        
        self._currentcalc = currentcalc
        self._setTa(ta)
        self._timeStep  = 1.0
        self._deltaIc   = 0.01
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def getResistance(self, tc):
        """Shortcut for currentcalc.getResistance"""
        return self._currentcalc.getResistance(tc)
    
    def getCurrent(self, tc):
        """Shortcut for currentcalc.getCurrent(ta, tc)"""
        return self._currentcalc.getCurrent(self._ta, tc)

    def getTc(self, ic):
        """Shortcut for currentcalc.getTc(ta, ic)"""
        return self._currentcalc.getTc(self._ta, ic)

    def getData(self, tcx, icfin, lapse, timex=0):
        """Returns TcTimeData instance
        tcx   : Conductor temperature to start calculus [°C]
        icfin : Final current (after change) that stay constant during lapse [ampere]
        lapse : Time interval to calculate Tc values [seconds]
        timex : Optional. To start on time different than zero [seconds]
                Time is relative so timex can be negative.
        Is not necessary to start the sequence with the balance temperature prior
        to the change in current.
        """
        check.ge(icfin, 0)
        check.le(icfin, self._icmax)
        check.gt(lapse, 0)
        
        npasos = int(math.ceil(lapse/self._timeStep)) + 1
        times = [(timex + x*self._timeStep) for x in range(npasos)]
        
        K = 0.86/3600*self._timeStep/self._currentcalc.conductor.hcap
        temp = tcx
        sal = []
        for tiempo in times:
            sal.append((tiempo, temp))
            Rtemp = self.getResistance(temp)*.0003048  # Resistencia Ohm/pie
            Itemp = self.getCurrent(temp)
            deltatemp = K*Rtemp*(icfin**2 - Itemp**2)
            temp = temp + deltatemp
        return TcTimeData(sal)

    def getIcini(self, tcx, factor, lapse):
        """Iterates and returns the initial current Icini [ampere] (before change)
        tcx     : Conductor temperature to rich after lapse [°C]
        factor  : Ifin/Iini
        lapse   : Time interval to rich tcx [seconds]
        """
        check.gt(tcx, self._ta)
        check.le(tcx, TC_MAX)
        check.gt(factor, 0)
        check.ge(lapse, 0)
        
        ibmin = 0
        ibmax = self._icmax/factor
        cuenta = 0
        while (ibmax - ibmin) > self._deltaIc:
            ibmed = 0.5*(ibmin + ibmax)
            tmed = self.getTc(ibmed)
            perfil = self.getData(tmed, ibmed*factor, lapse+self._timeStep, timex=0)
            tc = perfil.getTc(lapse)
            
            if tc > tcx:
                ibmax = ibmed
            else:
                ibmin = ibmed
            
            cuenta = cuenta + 1
            if cuenta > ITER_MAX:
                err_msg = "getIfin: Nº iterations > %d" % ITER_MAX
                raise RuntimeError(err_msg)
        return ibmed

    def getIcfin(self, tcx, icini, lapse, tcxini=None):
        """Iterates and returns the final current Ifin [ampere] (after change)
        tcx    : Conductor temperature to rich after lapse [°C]
        Icini  : Initial current (before change) [ampere]
        lapse  : Time interval to rich Tcx [seconds]
        tcxini : Optional. If None it will be calculated using Iini.
        """
        check.gt(tcx, self._ta)
        check.le(tcx, TC_MAX)
        check.gt(icini, 0)
        check.le(icini, self._icmax)
        check.ge(lapse, 0)
        
        Tini = self.getTc(icini)
        if tcxini is None:
            tcxini = Tini
        
        # Test if it growing or not
        if tcx > Tini:
            check.ge(tcxini, Tini)
            check.lt(tcxini,  tcx)
            ibmin = icini
            ibmax = self._icmax
        else:
            check.le(tcxini, Tini)
            check.gt(tcxini,  tcx)
            ibmin = 0.0
            ibmax = icini
        
        cuenta = 0
        while (ibmax - ibmin) > self._deltaIc:
            ibmed = 0.5*(ibmin + ibmax)
            perfil = self.getData(tcxini, ibmed, lapse + self._timeStep, timex=0)
            tc = perfil.getTc(lapse)
            
            if tc > tcx:
                ibmax = ibmed
            else:
                ibmin = ibmed
            
            cuenta = cuenta + 1
            if cuenta > ITER_MAX:
                err_msg = "getIfin: Nº iterations > %d" % ITER_MAX
                raise RuntimeError(err_msg)
        return ibmed
    
    #-------------------------------------------------------------------------------------
    # Properties methods
    
    def _getCurrentCalc(self):
        return self._currentcalc
    
    def _getIcmax(self):
        return self._icmax
    
    def _getTa(self):
        return self._ta
    
    @deco.ge(TA_MIN)
    @deco.le(TA_MAX)
    def _setTa(self, value):
        self._ta = value
        self._icmax = self.getCurrent(TC_MAX)
    
    def _getTimeStep(self):
        return self._timeStep
    
    @deco.gt(0)
    @deco.le(60)
    def _setTimeStep(self, value):
        self._timeStep = value
    
    def _getDeltaIc(self):
        return self._deltaIc
    
    @deco.gt(0)
    def _setDeltaIc(self, value):
        self._deltaIc = value
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    currentcalc  = property(_getCurrentCalc)
    icmax        = property(_getIcmax)
    ta           = property(_getTa,       _setTa)
    timeStep     = property(_getTimeStep, _setTimeStep)
    deltaIc      = property(_getDeltaIc,  _setDeltaIc)


#-----------------------------------------------------------------------------------------

class TcTimeData(tuple):
    """Inmutable secuence with tuples (time, Tc) 
    
    Read-only properties
    growing : True if the secuence grows in Tc values
    tempMin : Maximun conductor temperature into the secuence [°C]
    tempMax : Minimun conductor temperature into the secuence [°C]
    timeMin : Maximun time value into the secuence [seg]
    timeMax : Minimun time value into the secuence [seg]
    
    """
    
    def __new__(cls, data):
        """
        data : Secuence with tuples (time, Tc)
        len(data) must be greater than 1
        """
        check.gt(len(data), 1)
        
        t = tuple.__new__(cls, data)
                
        tlist = [x[1] for x in t]
        t._tempMin = min(tlist)
        t._tempMax = max(tlist)
        t._growing = t[-1][1] > t[0][1]
        
        return t
    
    #-------------------------------------------------------------------------------------
    # Public methods
    
    def getTime(self, tc):
        """Returns time [seconds] to rich Tc with intepolations of values.
        tc : Conductor temperature [°C] 
        If tc is out of range it returns POS_INDEF or NEG_INDEF
        """
        i = 0
        if tc < self._tempMin:
            i = 1 if self._growing else (len(self) - 1)
        elif tc > self._tempMax:
            i = (len(self) - 1) if self._growing else 1
        else:
            if self._growing:
                while self[i][1] < tc:
                    i = i + 1
            else:
                while self[i][1] > tc:
                    i = i + 1
        t0, v0 = self[i-1]
        t1, v1 = self[i]
        tx = (tc - v0)*(t1 - t0)/(v1 - v0) + t0
        return tx
    
    def getTc(self, t):
        """Returns conductor temperature Tc [°C] riched al t seconds 
        with intepolations of values.
        t : Time [seconds] 
        """
        i = 0
        if t < self.timeMin:
            i = 1
        elif t > self.timeMax:
            i = len(self) - 1
        else:
            while self[i][0] < t:
                i = i + 1
        t0, v0 = self[i-1]
        t1, v1 = self[i]
        return (t - t0)*(v1 - v0)/(t1 - t0) + v0
    
    #-------------------------------------------------------------------------------------
    # Properties methods
    
    def _isGrowing(self):
        return self._growing
    
    def _getTempMin(self):
        return self._tempMin
    
    def _getTempMax(self):
        return self._tempMax
    
    def _getTimeMin(self):
        return self[0][0]

    def _getTimeMax(self):
        return self[-1][0]
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    growing = property(_isGrowing)
    tempMin = property(_getTempMin)
    tempMax = property(_getTempMax)
    timeMin = property(_getTimeMin)
    timeMax = property(_getTimeMax)
    