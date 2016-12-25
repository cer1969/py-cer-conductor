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

#print (ac1.getTc(50, 1000))
#print (ac2.getTc(50, 1000))
print(ac1.getResistance(50))
print(ac2.getResistance(50))

t1 = time.clock()
for i in range(1000):
    #ac1.getTc(50, 1000)
    ac1.getResistance(50)

t2 = time.clock()

for i in range(1000):
    #ac2.getTc(50, 1000)
    ac2.getResistance(50)

t3 = time.clock()

print ((t2 - t1)/(t3 - t2))