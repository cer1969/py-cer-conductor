# CRISTIAN ECHEVERRÍA RABÍ

#from libc.math cimport pow

#-----------------------------------------------------------------------------------------
# CurrentCalc 

cdef double _getResistance(double tc, double conductor_r25, double category_alpha):
    """Returns resistance [Ohm/km]
    tc : Conductor temperature [°C]
    """
    return conductor_r25*(1 + category_alpha*(tc - 25))

cpdef double getResistance(double tc, double conductor_r25, double category_alpha):
    return _getResistance(tc, conductor_r25, category_alpha)


cdef double _getCurrent(double ta, double tc, double conductor_r25, double category_alpha,
        double conductor_diameter, double altitude, double airVelocity, int formula, 
        double emissivity, double sunEffect):
    """Returns current [ampere]
    ta : Ambient temperature [°C]
    tc : Conductor temperature [°C]
    """
    cdef double D, Pb, V, Rc, Tm, Rf, Uf, Kf, Qc, factor, Qc1, Qc2, LK, MK, Qr, Qs
    
    if ta >= tc:
        return 0.0
    
    D = conductor_diameter/25.4                                         # Diámetro en pulgadas
    Pb = 10**(1.880813592 - altitude/18336)                             # Presión barométrica en cmHg
    V = airVelocity*3600                                                # Vel. viento en pies/hora
    Rc = _getResistance(tc, conductor_r25, category_alpha)*0.0003048    # Resistencia en ohm/pies
    Tm = 0.5*(tc + ta)                                                  # Temperatura media
    Rf = 0.2901577*Pb/(273 + Tm)                                        # Densidad rel.aire ¿lb/ft^3?
    Uf = 0.04165 + 0.000111*Tm                                          # Viscosidad abs. aire ¿lb/(ft x hora)
    Kf = 0.00739 + 0.0000227*Tm                                         # Coef. conductividad term. aire [Watt/(ft x °C)]
    Qc = .283*(Rf**0.5)*(D**0.75)*(tc - ta)**1.25                       # watt/ft
    
    if V != 0:
        factor = D*Rf*V/Uf
        Qc1 = 0.1695*Kf*(tc - ta)*factor**0.6
        Qc2 = Kf*(tc - ta)*(1.01 + 0.371*factor**0.52)
        if formula == 0:            # IEEE criteria
            Qc = max(Qc, Qc1, Qc2)
        else:                       # CLASSIC criteria
            if factor < 12000:
                Qc = Qc2
            else:
                Qc = Qc1
    
    LK = ((tc + 273)/100)**4
    MK = ((ta + 273)/100)**4
    Qr = 0.138*D*emissivity*(LK - MK)
    Qs = 3.87*D*sunEffect
    
    if (Qc + Qr) < Qs: 
        return 0.0
    else: 
        return ((Qc + Qr - Qs)/Rc)**(0.5)

cpdef double getCurrent(double ta, double tc, double conductor_r25, double category_alpha,
        double conductor_diameter, double altitude, double airVelocity, int formula, 
        double emissivity, double sunEffect):
    return _getCurrent(ta, tc, conductor_r25, category_alpha, conductor_diameter, altitude,
        airVelocity, formula, emissivity, sunEffect)


cdef double _getTc(double ta, double ic, double TC_MAX, double deltaTemp, double conductor_r25,
        double category_alpha, double conductor_diameter, double altitude, double airVelocity,
        int formula, double emissivity, double sunEffect):
    """Returns conductor temperature [ampere]
    ta : Ambient temperature [°C]
    ic : Current [ampere]
    """
    cdef double Tmin, Tmax, Tmed, Imed
    cdef int cuenta
    
    Tmin = ta
    Tmax = TC_MAX
    cuenta = 0
    while (Tmax - Tmin) > deltaTemp:
        Tmed = 0.5*(Tmin + Tmax)
        Imed = _getCurrent(ta, Tmed, conductor_r25, category_alpha, conductor_diameter,
            altitude, airVelocity, formula, emissivity, sunEffect)
        if Imed > ic:
            Tmax = Tmed
        else:
            Tmin = Tmed
        cuenta = cuenta + 1
        #if cuenta > ITER_MAX:
        #    err_msg = "getTc(): N° iterations > %d" % ITER_MAX
        #    raise RuntimeError(err_msg)
    return Tmed
    
cpdef double getTc(double ta, double ic, double TC_MAX, double deltaTemp, double conductor_r25,
        double category_alpha, double conductor_diameter, double altitude, double airVelocity,
        int formula, double emissivity, double sunEffect):
    return _getTc(ta, ic, TC_MAX, deltaTemp, conductor_r25, category_alpha, conductor_diameter,
        altitude, airVelocity, formula, emissivity, sunEffect)