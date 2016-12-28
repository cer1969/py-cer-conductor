import time

import cer.conductor as cx
from cer.conductor import ccx

#-----------------------------------------------------------------------------------------

c1 = cx.Conductor(name = 'AAAC 740,8 MCM FLINT',
                  category = cx.CC_AAAC,
                  diameter = 25.17,         # en mm
                  area = 375.4,             # en mm2
                  weight = 1.035,           # en Kg/m
                  strength = 11625.0,       # en Kg
                  r25 = 0.08936,            # Resistencia a 25°C en Ohm/km
                  hcap = 0.05274,           # capacidad calórica
                  )

c2 = ccx.Conductor(name = 'AAAC 740,8 MCM FLINT',
                  category = ccx.CC_AAAC,
                  diameter = 25.17,         # en mm
                  area = 375.4,             # en mm2
                  weight = 1.035,           # en Kg/m
                  strength = 11625.0,       # en Kg
                  r25 = 0.08936,            # Resistencia a 25°C en Ohm/km
                  hcap = 0.05274,           # capacidad calórica
                  )


#VOLTAJE = 220.0     # kV de la línea
#NSC = 1             # N° de subconductores por fase
#FACTOR = 1.968      # Factor de sobrecarga
#SOL = 1.0           # Efecto sol 1:Si, 0:No
#TEMP_MAX_OP = 55.0  # T° maxima de operación línea
#TIEMPO = 15.0       # Tiempo buscado en minutos

#-----------------------------------------------------------------------------------------
time.clock()

ac1 = cx.CurrentCalc(c1)
ac2 = ccx.CurrentCalc(c2)

def benchm(title, ofunc, nfunc, args, n=500):
    print("%s - %d veces" % (title, n))
    print("-------------------------------------------------")
    print ("Old = %f" % ofunc(*args))
    print ("New = %f" % nfunc(*args))

    t1 = time.clock()
    
    for i in range(n):
        ofunc(*args)
    
    t2 = time.clock()
    
    for i in range(n):
        nfunc(*args)
    
    t3 = time.clock()

    print ("Time Old = %f" % (t2 - t1))
    print ("Time New = %f" % (t3 - t2))
    print ("Old/New  = %f" % ((t2-t1)/(t3 - t2)))


benchm("getTc(50, 1000)", ac1.getTc, ac2.getTc, (50, 100))
print(" ")
benchm("getTa(60, 1000)", ac1.getTa, ac2.getTa, (60, 100))
print(" ")
benchm("getResistance(50)", ac1.getResistance, ac2.getResistance, (50,))
print(" ")
benchm("getCurrent(25, 50)", ac1.getCurrent, ac2.getCurrent, (25, 50))

print(" ")

from cer.conductor import _ccx
cc = _ccx.CurrentCalc(25.17, 0.08936, cx.CC_AAAC.alpha, cx.TC_MAX, cx.TA_MIN, cx.TA_MAX)


benchm("getTc(50, 1000)", ac1.getTc, cc.getTc, (50, 100))
print(" ")
benchm("getTa(60, 1000)", ac1.getTa, cc.getTa, (60, 100))
print(" ")
benchm("getResistance(50)", ac1.getResistance, cc.getResistance, (50,))
print(" ")
benchm("getCurrent(25, 50)", ac1.getCurrent, cc.getCurrent, (25, 50))
print(" ")
cc = _ccx.CurrentCalc(25.17, 0.08936, cx.CC_AAAC.alpha, cx.TC_MAX, cx.TA_MIN, cx.TA_MAX)
print(cc.getCurrent(25, 50))