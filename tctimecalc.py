# CRISTIAN ECHEVERRÍA RABÍ

import math

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
        if currentcalc.conductor.hcap <= 0: raise ValueError("hcap <= 0")
        
        self._currentcalc = currentcalc
        self.ta = ta
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
        if icfin < 0: raise ValueError("icfin < 0")
        if icfin > self._icmax: raise ValueError("icfin > icmax (ta)")
        if lapse <= 0: raise ValueError("lapse <= 0")
        
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
        if tcx <= self._ta: raise ValueError("tcx <= ta")
        if tcx > TC_MAX: raise ValueError("tcx > TC_MAX")
        if factor <= 0: raise ValueError("factor <= 0")
        if lapse <= 0: raise ValueError("lapse <= 0")
        
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
        if tcx <= self._ta: raise ValueError("tcx <= ta")
        if tcx > TC_MAX: raise ValueError("tcx > TC_MAX")
        if icini <= 0: raise ValueError("icini <= 0")
        if icini > self._icmax: raise ValueError("icini > icmax (ta)")
        if lapse <= 0: raise ValueError("lapse <= 0")
        
        Tini = self.getTc(icini)
        if tcxini is None:
            tcxini = Tini
        
        # Test if it growing or not
        if tcx > Tini:
            if tcxini < Tini: raise ValueError("tcxini < Tini growing")
            if tcxini >= tcx: raise ValueError("tcxini >= tcx growing")
            ibmin = icini
            ibmax = self._icmax
        else:
            if tcxini > Tini: raise ValueError("tcxini > Tini not growing")
            if tcxini <= tcx: raise ValueError("tcxini <= tcx not growing")
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
    # Properties
    
    @property
    def currentcalc(self):
        return self._currentcalc
    
    @property
    def icmax(self):
        return self._icmax
    
    @property
    def ta(self):
        return self._ta
    
    @ta.setter
    def ta(self, value):
        if value < TA_MIN: raise ValueError("value < TA_MIN")
        if value > TA_MAX: raise ValueError("valueta > TA_MAX")
        self._ta = value
        self._icmax = self.getCurrent(TC_MAX)
    
    @property
    def timeStep(self):
        return self._timeStep
    
    @timeStep.setter
    def timeStep(self, value):
        if value <= 0: raise ValueError("value <= 0")
        if value > 60: raise ValueError("value > 60")
        self._timeStep = value
    
    @property
    def deltaIc(self):
        return self._deltaIc
    
    @deltaIc.setter
    def deltaIc(self, value):
        if value <= 0: raise ValueError("value <= 0")
        self._deltaIc = value


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
        if len(data) <= 1: raise ValueError("len(data) <= 1")
        
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
        tcs = [x[1] for x in self]
        grow = self._growing
        ilo = 0
        ihi = len(tcs) - 1
        
        while ihi - ilo > 1:
            mid = (ilo + ihi) // 2
            if tc > tcs[mid]:
                ilo = mid if grow else ilo
                ihi = ihi if grow else mid
            else:
                ihi = mid if grow else ihi
                ilo = ilo if grow else mid
        
        t0, v0 = self[ilo]
        t1, v1 = self[ihi]
        
        tx = (tc - v0)*(t1 - t0)/(v1 - v0) + t0
        if tx < 0:
            tx = 0
        return tx
    
    def getTc(self, t):
        """Returns conductor temperature Tc [°C] riched al t seconds 
        with intepolations of values.
        t : Time [seconds] 
        """
        times = [x[0] for x in self]
        ilo = 0
        ihi = len(times) - 1
        
        while ihi - ilo > 1:
            mid = (ilo + ihi) // 2
            if t > times[mid]:
                ilo = mid
            else:
                ihi = mid
        
        t0, v0 = self[ilo]
        t1, v1 = self[ihi]

        return (t - t0)*(v1 - v0)/(t1 - t0) + v0
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    @property
    def growing(self):
        return self._growing
    
    @property
    def tempMin(self):
        return self._tempMin
    
    @property
    def tempMax(self):
        return self._tempMax
    
    @property
    def timeMin(self):
        return self[0][0]
    
    @property
    def timeMax(self):
        return self[-1][0]