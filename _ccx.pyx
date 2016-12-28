# CRISTIAN ECHEVERRÍA RABÍ

from libc.math cimport pow, sqrt

#-----------------------------------------------------------------------------------------
# CurrentCalc 

cdef class CurrentCalc:

    cdef double _r25, _diameter, _alpha
    cdef double _altitude, _airVelocity, _sunEffect, _emissivity, _deltaTemp
    cdef double _TC_MAX, _TA_MIN, _TA_MAX
    cdef int _formula

    def __cinit__(self, double diameter, double r25, double alpha, 
                  double TC_MAX, double TA_MIN, double TA_MAX):
        
        self._diameter = diameter
        self._r25 = r25
        self._alpha = alpha

        self._TC_MAX = TC_MAX
        self._TA_MIN = TA_MIN
        self._TA_MAX = TA_MAX

        self._altitude = 300.0
        self._airVelocity = 2.0
        self._sunEffect = 1.0
        self._emissivity = 0.5
        self._formula = 0
        self._deltaTemp = 0.01
    
    #-------------------------------------------------------------------------------------
    # Public methods

    def getResistance(self, double tc):
        return self._getResistance(tc)
    
    def getCurrent(self, double ta, double tc):
        return self._getCurrent(ta, tc)
    
    def getTc(self, double ta, double ic):
        return self._getTc(ta, ic)
    
    def getTa(self, double tc, double ic):
        return self._getTa(tc, ic)
    
    #-------------------------------------------------------------------------------------
    # Private methods

    cdef double _getResistance(self, double tc):
        return self._r25*(1 + self._alpha*(tc - 25))
    
    cdef double _getCurrent(self, double ta, double tc):
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
    
    cdef double _getTc(self, double ta, double ic):
        cdef double Tmin, Tmax, Tmed, Imed
        cdef int cuenta
        
        Tmin = ta
        Tmax = self._TC_MAX
        cuenta = 0
        while (Tmax - Tmin) > self._deltaTemp:
            Tmed = 0.5*(Tmin + Tmax)
            Imed = self._getCurrent(ta, Tmed)
            if Imed > ic:
                Tmax = Tmed
            else:
                Tmin = Tmed
            cuenta = cuenta + 1
            #if cuenta > ITER_MAX:
            #    err_msg = "getTc(): N° iterations > %d" % ITER_MAX
            #    raise RuntimeError(err_msg)
        return Tmed
    
    cdef double _getTa(self, double tc, double ic):
        cdef double Tmin, Tmax, Tmed, Imed
        cdef int cuenta
        
        Tmin = self._TA_MIN
        Tmax = min([self._TA_MAX, tc])
        if Tmin >= Tmax:
            return tc
        
        cuenta = 0
        while (Tmax - Tmin) > self._deltaTemp:
            Tmed = 0.5*(Tmin + Tmax)
            Imed = self._getCurrent(Tmed, tc)
            if Imed > ic:
                Tmin = Tmed
            else: 
                Tmax = Tmed
            cuenta = cuenta+1
            #if cuenta > ITER_MAX:
            #    err_msg = "getTa(): N° iterations > %d" % ITER_MAX
            #    raise RuntimeError(err_msg)
        return Tmed

    #-------------------------------------------------------------------------------------
    # Read-only properties

    @property
    def diameter(self):
        return self._diameter
    
    @property
    def r25(self):
        return self._r25
    
    @property
    def alpha(self):
        return self._alpha
    
    #-------------------------------------------------------------------------------------
    # Read-write properties

    @property
    def altitude(self):
        return self._altitude
    
    @altitude.setter
    def altitude(self, double v):
        self._altitude = v
    
    @property
    def airVelocity(self):
        return self._airVelocity
    
    @airVelocity.setter
    def airVelocity(self, double v):
        self._airVelocity = v
    
    @property
    def sunEffect(self):
        return self._sunEffect
    
    @sunEffect.setter
    def sunEffect(self, double v):
        self._sunEffect = v
    
    @property
    def emissivity(self):
        return self._emissivity
    
    @emissivity.setter
    def emissivity(self, double v):
        self._emissivity = v
    
    @property
    def formula(self):
        return self._formula
    
    @formula.setter
    def formula(self, int v):
        self._formula = v
    
    @property
    def deltaTemp(self):
        return self._deltaTemp
    
    @deltaTemp.setter
    def deltaTemp(self, double v):
        self._deltaTemp = v