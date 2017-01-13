# CRISTIAN ECHEVERRÍA RABÍ

from cer.conductor import cx
from cer.conductor import zx
from bench import bench

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

c2 = zx.Conductor(name = 'AAAC 740,8 MCM FLINT',
                  category = zx.CC_AAAC,
                  diameter = 25.17,         # en mm
                  area = 375.4,             # en mm2
                  weight = 1.035,           # en Kg/m
                  strength = 11625.0,       # en Kg
                  r25 = 0.08936,            # Resistencia a 25°C en Ohm/km
                  hcap = 0.05274,           # capacidad calórica
                  )

#-----------------------------------------------------------------------------------------

ac1 = cx.CurrentCalc(c1)
ac2 = zx.CurrentCalc(c2)
opi1 = cx.OperatingItem(ac1, 50, 1)
opi2 = zx.OperatingItem(ac2, 50, 1)

#bench("getTc(50, 1000)", ac1.getTc, ac2.getTc, (50, 100))
#print(" ")
#bench("getTa(60, 1000)", ac1.getTa, ac2.getTa, (60, 100))
#print(" ")
#bench("getCurrent(30)", opi2.getCurrent, opi2.getCurrent2, (30,))
#print(" ")
bench("getCurrent(30)", opi1.getCurrent, opi2.getCurrent, (30,))

