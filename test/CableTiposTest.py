# CRISTIAN ECHEVERRÍA RABÍ 

import cer.conductor as cx

#-----------------------------------------------------------------------------------------

myTipo = cx.CC_CU
print(myTipo.name)
print(myTipo.modelas)
print(myTipo.coefexp)
print(myTipo.creep)
print(myTipo.idx)

cab = cx.Conductor()
cab.name = "CU 300 MCM"
cab.category = myTipo
cab.diameter = 15.95
cab.area = 152.00
cab.weight = 1.378
cab.strength = 6123.0
cab.r25 = 0.12270

print()
print(cab.name)    
print(cab.strength)
print(cab.hcap)
print(cab.idx)
