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

c2 = zx.Conductor(#name = 'AAAC 740,8 MCM FLINT',
                  category = zx.CC_AAAC,
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

ac1 = cx.CurrentCalc(c1)
ac2 = zx.CurrentCalc(c2)
#print(ac2.conductor.category)

bench("getTc(50, 1000)", ac1.getTc, ac2.getTc, (50, 100))
print(" ")
bench("getTa(60, 1000)", ac1.getTa, ac2.getTa, (60, 100))
print(" ")
bench("getResistance(50)", ac1.getResistance, ac2.getResistance, (50,))
print(" ")
bench("getCurrent(25, 50)", ac1.getCurrent, ac2.getCurrent, (25, 50))

