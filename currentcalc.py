# CRISTIAN ECHEVERRÍA RABÍ

from cer.value import check
from .constants import (CF_CLASSIC, CF_IEEE, TA_MIN, TA_MAX, TC_MIN, TC_MAX, ITER_MAX)

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
    deltaTemp   : Temperature difference to determine equality [°C] = 0.0001
    
    """

    __slots__ = ('_conductor', '_altitude', '_airVelocity', '_sunEffect', '_emissivity',
                 '_formula', '_deltaTemp')
    
    def __init__(self, conductor):
        """
        conductor : Conductor instance. 
        Valid values are required for r25, diameter and category.alpha
        """
        check.gt(conductor.r25, 0)
        check.gt(conductor.diameter, 0)
        check.gt(conductor.category.alpha, 0)
        check.lt(conductor.category.alpha, 1)
        
        self._conductor = conductor
        
        self._altitude = 300.0
        self._airVelocity = 2.0
        self._sunEffect = 1.0
        self._emissivity = 0.5
        self._formula = CF_IEEE
        self._deltaTemp = 0.0001

    #-------------------------------------------------------------------------------------
    # Public methods
    
    def getResistance(self, tc):
        """Returns resistance [Ohm/km]
        tc : Conductor temperature [°C]
        """
        check.ge(tc, TC_MIN)
        check.le(tc, TC_MAX)
        return self._conductor.r25*(1 + self._conductor.category.alpha*(tc - 25))

    def getCurrent(self, ta, tc):
        """Returns current [ampere]
        ta : Ambient temperature [°C]
        tc : Conductor temperature [°C]
        """
        check.ge(ta, TA_MIN)
        check.le(ta, TA_MAX)
        check.ge(tc, TC_MIN)
        check.le(tc, TC_MAX)
        
        if ta >= tc:
            return 0.0

        D = self._conductor.diameter/25.4              # Diámetro en pulgadas
        Pb = 10**(1.880813592 - self._altitude/18336)  # Presión barométrica en cmHg
        V = self._airVelocity*3600                     # Vel. viento en pies/hora
        Rc = self.getResistance(tc)*0.0003048          # Resistencia en ohm/pies
        Tm = 0.5*(tc + ta)                             # Temperatura media
        Rf = 0.2901577*Pb/(273 + Tm)                   # Densidad rel.aire ¿lb/ft^3?
        Uf = 0.04165 + 0.000111*Tm                     # Viscosidad abs. aire ¿lb/(ft x hora)
        Kf = 0.00739 + 0.0000227*Tm                    # Coef. conductividad term. aire [Watt/(ft x °C)]
        Qc = .283*(Rf**0.5)*(D**0.75)*(tc - ta)**1.25  # watt/ft
        
        if V != 0:
            factor = D*Rf*V/Uf
            Qc1 = 0.1695*Kf*(tc - ta)*factor**0.6
            Qc2 = Kf*(tc - ta)*(1.01 + 0.371*factor**0.52)
            if self._formula == CF_IEEE:    # IEEE criteria
                Qc = max(Qc, Qc1, Qc2)
            else:                           # CLASSIC criteria
                if factor < 12000:
                    Qc = Qc2
                else:
                    Qc = Qc1
        
        LK = ((tc + 273)/100)**4
        MK = ((ta + 273)/100)**4
        Qr = 0.138*D*self._emissivity*(LK - MK)
        Qs = 3.87*D*self._sunEffect
        
        if (Qc + Qr) < Qs: 
            return 0.0
        else: 
            return ((Qc + Qr - Qs)/Rc)**(0.5)

    def getTc(self, ta, ic):
        """Returns conductor temperature [ampere]
        ta : Ambient temperature [°C]
        ic : Current [ampere]
        """
        check.ge(ic, 0)
        check.le(ic, self.getCurrent(ta, TC_MAX))   # Ensure Tc <= TC_MAX
        
        Tmin = ta
        Tmax = TA_MAX
        cuenta = 0
        while (Tmax - Tmin) > self._deltaTemp:
            Tmed = 0.5*(Tmin + Tmax)
            Imed = self.getCurrent(ta, Tmed)
            if Imed > ic:
                Tmax = Tmed
            else:
                Tmin = Tmed
            cuenta = cuenta + 1
            if cuenta > ITER_MAX:
                err_msg = "getTc(): N° iterations > %d" % ITER_MAX
                raise RuntimeError(err_msg)
        return Tmed

    def getTa(self, tc, ic):
        """Returns ambient temperature [ampere]
        tc : Conductor temperature [°C]
        ic : Current [ampere]
        """
        check.ge(ic, 0)
        check.le(ic, self.getCurrent(TA_MIN, tc))   # Ensure Ta >= TA_MIN
        
        Tmin = TC_MIN
        Tmax = tc
        cuenta = 0
        while (Tmax - Tmin) > self._deltaTemp:
            Tmed = 0.5*(Tmin + Tmax)
            Imed = self.getCurrent(Tmed, tc)
            if Imed > ic: 
                Tmin = Tmed
            else: 
                Tmax = Tmed
            cuenta = cuenta+1
            if cuenta > ITER_MAX:
                err_msg = "getTa(): N° iterations > %d" % ITER_MAX
                raise RuntimeError(err_msg)
        return Tmed
    
    #-------------------------------------------------------------------------------------
    # Properties
    
    @property
    def conductor(self):
        return self._conductor
    
    @property
    def altitude(self):
        return self._altitude
    
    @altitude.setter
    def altitude(self, value):
        check.ge(value, 0)
        self._altitude = value
    
    @property
    def airVelocity(self):
        return self._airVelocity
    
    @airVelocity.setter
    def airVelocity(self, value):
        check.ge(value, 0)
        self._airVelocity = value
    
    @property
    def sunEffect(self):
        return self._sunEffect
    
    @sunEffect.setter
    def sunEffect(self, value):
        check.ge(value, 0)
        check.le(value, 1)
        self._sunEffect = value
    
    @property
    def emissivity(self):
        return self._emissivity
    
    @emissivity.setter
    def emissivity(self, value):
        check.ge(value, 0)
        check.le(value, 1)
        self._emissivity = value
    
    @property
    def formula(self):
        return self._formula
    
    @formula.setter
    def formula(self, value):
        check.isIn(value, [CF_CLASSIC, CF_IEEE])
        self._formula = value
    
    @property
    def deltaTemp(self):
        return self._deltaTemp
    
    @deltaTemp.setter
    def deltaTemp(self, value):
        check.gt(value, 0)
        self._deltaTemp = value