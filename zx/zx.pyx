# CRISTIAN ECHEVERRÍA RABÍ

from libc.math cimport pow, sqrt

#-----------------------------------------------------------------------------------------
# Constants

cdef int _CF_IEEE   = 0
cdef int _CF_CLASSIC = 1
cdef double _TA_MIN = -90.0
cdef double _TA_MAX =  90.0
cdef double _TC_MIN =  -90.0
cdef double _TC_MAX = 2000.0
cdef double _TENSION_MAX = 50000
#cdef double _ITER_MAX = 20000


CF_IEEE = _CF_IEEE
CF_CLASSIC = _CF_CLASSIC
TA_MIN = _TA_MIN
TA_MAX = _TA_MAX
TC_MIN = _TC_MIN
TC_MAX = _TC_MAX
TENSION_MAX = _TENSION_MAX
#ITER_MAX = _ITER_MAX

#-----------------------------------------------------------------------------------------
# Category 

cdef class Category:
    
    cdef readonly double modelas, coefexp, creep, alpha
    
    def __cinit__(self, double modelas=0.0, double coefexp=0.0, double creep=0.0, 
                  double alpha=0.0):
        self.modelas = modelas
        self.coefexp = coefexp
        self.creep = creep
        self.alpha = alpha

#-----------------------------------------------------------------------------------------
# Conductor

cdef class Conductor:
    
    cdef readonly double diameter, area, weight, strength, r25, hcap
    cdef readonly Category category
    
    def __cinit__(self, Category category, double diameter=0.0, double area=0.0, double weight=0.0, 
                  double strength=0.0, double r25=0.0, double hcap=0.0):
        self.category = category
        self.diameter = diameter
        self.area = area
        self.weight = weight
        self.strength = strength
        self.r25 = r25
        self.hcap = hcap

#-----------------------------------------------------------------------------------------
# CurrentCalc

cdef class CurrentCalc:

    cdef readonly Conductor conductor
    cdef double _r25, _diameter, _alpha
    cdef double _altitude, _airVelocity, _sunEffect, _emissivity, _deltaTemp
    cdef int _formula

    def __cinit__(self, Conductor conductor):
        if conductor.diameter <= 0: raise ValueError("diameter <= 0")
        if conductor.r25 <= 0: raise ValueError("r25 <= 0")
        if conductor.category.alpha <= 0: raise ValueError("category.alpha <= 0")
        if conductor.category.alpha >= 1: raise ValueError("category.alpha >= 1")

        self.conductor = conductor

        # Para acelerar cálculos
        self._diameter = conductor.diameter
        self._r25 = conductor.r25
        self._alpha = conductor.category.alpha

        self._altitude = 300.0
        self._airVelocity = 2.0
        self._sunEffect = 1.0
        self._emissivity = 0.5
        self._formula = _CF_IEEE
        self._deltaTemp = 0.01

    def getResistance(self, double tc):
        return self._getResistance(tc)
    
    cdef double _getResistance(self, double tc) except -1000:
        if tc < _TC_MIN: raise ValueError("tc < TC_MIN")
        if tc > _TC_MAX: raise ValueError("tc > TC_MAX")
        return self._r25*(1 + self._alpha*(tc - 25))
    
    def getCurrent(self, double ta, double tc):
        return self._getCurrent(ta, tc)
    
    cdef double _getCurrent(self, double ta, double tc) except -1000:
        if ta < _TA_MIN: raise ValueError("ta < TA_MIN")
        if ta > _TA_MAX: raise ValueError("ta > TA_MAX")
        if tc < _TC_MIN: raise ValueError("tc < TC_MIN")
        if tc > _TC_MAX: raise ValueError("tc > TC_MAX")

        cdef double D, Pb, V, Rc, Tm, Rf, Uf, Kf, Qc, factor, Qc1, Qc2, LK, MK, Qr, Qs
        
        if ta >= tc:
            return 0.0
        
        D = self._diameter/25.4                                             # Diámetro en pulgadas
        Pb = pow(10, 1.880813592 - self._altitude/18336)                    # Presión barométrica en cmHg
        V = self._airVelocity*3600                                          # Vel. viento en pies/hora
        Rc = self._getResistance(tc)*0.0003048                              # Resistencia en ohm/pies
        Tm = 0.5*(tc + ta)                                                  # Temperatura media
        Rf = 0.2901577*Pb/(273 + Tm)                                        # Densidad rel.aire ¿lb/ft^3?
        Uf = 0.04165 + 0.000111*Tm                                          # Viscosidad abs. aire ¿lb/(ft x hora)
        Kf = 0.00739 + 0.0000227*Tm                                         # Coef. conductividad term. aire [Watt/(ft x °C)]
        Qc = .283*sqrt(Rf)*pow(D, 0.75)*pow(tc - ta, 1.25)                  # watt/ft
        
        if V != 0:
            factor = D*Rf*V/Uf
            Qc1 = 0.1695*Kf*(tc - ta)*pow(factor, 0.6)
            Qc2 = Kf*(tc - ta)*(1.01 + 0.371*pow(factor, 0.52))
            if self._formula == 0:            # IEEE criteria
                Qc = max(Qc, Qc1, Qc2)
            else:                             # CLASSIC criteria
                if factor < 12000:
                    Qc = Qc2
                else:
                    Qc = Qc1
        
        LK = pow((tc + 273)/100, 4)
        MK = pow((ta + 273)/100, 4)
        Qr = 0.138*D*self._emissivity*(LK - MK)
        Qs = 3.87*D*self._sunEffect
        
        if (Qc + Qr) < Qs: 
            return 0.0
        else: 
            return sqrt((Qc + Qr - Qs)/Rc)
    
    def getTc(self, double ta, double ic):
        return self._getTc(ta, ic)
    
    cdef double _getTc(self, double ta, double ic) except -1000:
        if ta < _TA_MIN: raise ValueError("ta < TA_MIN")
        if ta > _TA_MAX: raise ValueError("ta > TA_MAX")
        if ic < 0: raise ValueError("ic < 0")
        if ic > self._getCurrent(ta, _TC_MAX): raise ValueError("ic > Imax (TC_MAX)")

        cdef double Tmin, Tmax, Tmed, Imed
        #cdef int cuenta
        
        Tmin = ta
        Tmax = _TC_MAX
        #cuenta = 0
        while (Tmax - Tmin) > self._deltaTemp:
            Tmed = 0.5*(Tmin + Tmax)
            Imed = self._getCurrent(ta, Tmed)
            if Imed > ic:
                Tmax = Tmed
            else:
                Tmin = Tmed
            #cuenta = cuenta + 1
            #if cuenta > ITER_MAX:
            #    err_msg = "getTc(): N° iterations > %d" % ITER_MAX
            #    raise RuntimeError(err_msg)
        return Tmed
    
    def getTa(self, double tc, double ic):
        return self._getTa(tc, ic)
    
    cdef double _getTa(self, double tc, double ic) except -1000:
        if tc < _TC_MIN: raise ValueError("tc < TC_MIN")
        if tc > _TC_MAX: raise ValueError("tc > TC_MAX")
        if ic < self._getCurrent(_TA_MAX, tc): raise ValueError("ic < Imin (TA_MAX)")
        if ic > self._getCurrent(_TA_MIN, tc): raise ValueError("ic > Imax (TA_MIN)")
        
        cdef double Tmin, Tmax, Tmed, Imed
        #cdef int cuenta
        
        Tmin = _TA_MIN
        Tmax = min([_TA_MAX, tc])
        if Tmin >= Tmax:
            return tc
        
        #cuenta = 0
        while (Tmax - Tmin) > self._deltaTemp:
            Tmed = 0.5*(Tmin + Tmax)
            Imed = self._getCurrent(Tmed, tc)
            if Imed > ic:
                Tmin = Tmed
            else: 
                Tmax = Tmed
            #cuenta = cuenta+1
            #if cuenta > ITER_MAX:
            #    err_msg = "getTa(): N° iterations > %d" % ITER_MAX
            #    raise RuntimeError(err_msg)
        return Tmed

    @property
    def altitude(self):
        return self._altitude
    
    @altitude.setter
    def altitude(self, double v):
        if v < 0: raise ValueError("altitude < 0")
        self._altitude = v
    
    @property
    def airVelocity(self):
        return self._airVelocity
    
    @airVelocity.setter
    def airVelocity(self, double v):
        if v < 0: raise ValueError("airVelocity < 0")
        self._airVelocity = v
    
    @property
    def sunEffect(self):
        return self._sunEffect
    
    @sunEffect.setter
    def sunEffect(self, double v):
        if v < 0: raise ValueError("sunEffect < 0")
        if v > 1: raise ValueError("sunEffect > 1")
        self._sunEffect = v
    
    @property
    def emissivity(self):
        return self._emissivity
    
    @emissivity.setter
    def emissivity(self, double v):
        if v < 0: raise ValueError("emissivity < 0")
        if v > 1: raise ValueError("emissivity > 1")
        self._emissivity = v
    
    @property
    def formula(self):
        return self._formula
    
    @formula.setter
    def formula(self, int v):
        if v not in [_CF_IEEE, _CF_CLASSIC]: raise ValueError("formula <> CF_IEEE, CF_CLASSIC")
        self._formula = v
    
    @property
    def deltaTemp(self):
        return self._deltaTemp
    
    @deltaTemp.setter
    def deltaTemp(self, double v):
        if v <= 0: raise ValueError("deltaTemp <= 0")
        self._deltaTemp = v

#-----------------------------------------------------------------------------------------
# OperatingItem

cdef class OperatingItem:

    cdef readonly CurrentCalc currentcalc
    cdef readonly double tempMaxOp
    cdef readonly int nsc

    def __cinit__(self, CurrentCalc currentcalc, double tempMaxOp=50.0, int nsc=1):
        if tempMaxOp < _TC_MIN: raise ValueError("tempMaxOp < TC_MIN")
        if tempMaxOp > _TC_MAX: raise ValueError("tempMaxOp > TC_MAX")
        if nsc < 1: raise ValueError("nsc < 1")

        self.currentcalc = currentcalc
        self.tempMaxOp = tempMaxOp
        self.nsc = nsc

    def getCurrent(self, double ta):
        return self._getCurrent(ta)

    cdef double _getCurrent(self, double ta) except -1000:
        return self.currentcalc._getCurrent(ta, self.tempMaxOp) * self.nsc

#-----------------------------------------------------------------------------------------
# OperatingTable

cdef class OperatingTable:

    cdef readonly list items
    cdef readonly object idx

    def __cinit__(self, object idx=None):
        self.items = []
        self.idx = idx

    def getCurrent(self, double ta):
        return self._getCurrent(ta)
    
    cdef double _getCurrent(self, double ta) except -1000:
        cdef double minimo, amp
        cdef OperatingItem item

        minimo = 100000
        for item in self.items:
            amp = item._getCurrent(ta)
            if amp < minimo: minimo = amp
        return minimo

#-----------------------------------------------------------------------------------------
# TcTimeData

cdef class TcTimeData:

    cdef readonly tuple data, temps, times
    cdef readonly double growing, tempMin, tempMax, timeMin, timeMax
    
    def __cinit__(self, object data):
        if len(data) <= 1: raise ValueError("len(data) <= 1")
        
        self.data = tuple(data)
        self.growing = self.data[-1][1] > self.data[0][1]
        self.times = tuple([x[0] for x in self.data])
        self.temps = tuple([x[1] for x in self.data])
        self.tempMin = min(self.temps)
        self.tempMax = max(self.temps)
        self.timeMin = self.times[0]
        self.timeMax = self.times[-1]
    
    def getTime(self, double tc):
        return self._getTime(tc)

    cdef double _getTime(self, double tc) except -1000:        
        cdef double t0, t1, v0, v1, tx
        cdef int ilo, ihi, mid

        ilo = 0
        ihi = len(self.temps) - 1
        
        while ihi - ilo > 1:
            mid = int((ilo + ihi) // 2)
            if tc > self.temps[mid]:
                ilo = mid if self.growing else ilo
                ihi = ihi if self.growing else mid
            else:
                ihi = mid if self.growing else ihi
                ilo = ilo if self.growing else mid
        
        t0, v0 = self.data[ilo]
        t1, v1 = self.data[ihi]
        
        tx = (tc - v0)*(t1 - t0)/(v1 - v0) + t0
        if tx < 0:
            tx = 0
        return tx
    
    def getTc(self, double t):
        return self._getTc(t)
    
    cdef double _getTc(self, double t) except -1000:
        cdef double t0, t1, v0, v1
        cdef int ilo, ihi, mid
        
        ilo = 0
        ihi = len(self.times) - 1
        
        while ihi - ilo > 1:
            mid = int((ilo + ihi) // 2)
            if t > self.times[mid]:
                ilo = mid
            else:
                ihi = mid
        
        t0, v0 = self.data[ilo]
        t1, v1 = self.data[ihi]

        return (t - t0)*(v1 - v0)/(t1 - t0) + v0