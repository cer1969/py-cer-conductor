# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from __future__ import division
import cer.conductor as cx
import time

#-----------------------------------------------------------------------------------------

t0 = time.clock()

cab = cx.Conductor(category=cx.CC_AAAC, name="AAAC 740,8 MCM FLINT", diameter=25.17,
                   r25=0.089360, hcap=0.052744)
ac = cx.CurrentCalc(cab)
ac.sunEffect = 1.0

# Supongamos 2 líneas en paralelo con 70% de su transferencia nominal con sol
# Cada línea tendra una corriente Ic0 y temperatura de conductor Tc0
scc = cx.TcTimeCalc(ac, 25.0)
scc.timeStep = 1

# Usamos scc que ya tiene asociada la T° ambiente
Icnom = scc.getCurrent(50.0)
Ic0 = 0.7*Icnom
Tc0 = scc.getTc(Ic0)

# Se produce una falla en una de las líneas y la otra se sobrecarga al doble
# La línea en servicio queda con corriente Ic1 = 2*Ic0
Ic1 = 2*Ic0
print Ic0, Ic1

# Si esta condición se mantiene por 5 minutos el conductor alcanzará temperatura Tc1

curva1 = scc.getData(tcx=Tc0, icfin=Ic1, lapse=60*5, timex=0)
Tc1 = curva1.getTc(60*5)
print Tc0, Tc1
print scc.getIcini(tcx=48, factor=2, lapse=curva1.getTime(48))
print scc.getIcini(tcx=50, factor=2, lapse=curva1.getTime(50))

print scc.getIcfin(tcx=48, icini=Ic0, lapse=curva1.getTime(48), tcxini=None)
lap = curva1.getTime(50) - curva1.getTime(45)
print scc.getIcfin(tcx=50, icini=Ic0, lapse=lap, tcxini=45)


"""
for i in curva1:
    txt = "%.2f\t%.3f" % i
    txt = txt.replace(".",",")
    print txt
"""

# Para demostrar que la progresión se mantiene iniciando en otro punto
Tcx = curva1.getTc(60*1)
curvax = scc.getData(tcx=Tcx, icfin=Ic1, lapse=60*4, timex=60*1)
Tc1x = curvax.getTc(60*5)
print curva1.getTc(60*1.0) - curvax.getTc(60*1.0) 
print curva1.getTc(60*1.5) - curvax.getTc(60*1.5)
print curva1.getTc(60*3.0) - curvax.getTc(60*3.0)

# Entonces se bota carga para obtener una corriente Ic3 igual a 90% de la nominal
# Vemos como evoluciona en 10 minutos alcanzando temperatura Tc2
Ic2 = 0.9*Icnom
curva2 = scc.getData(tcx=Tc1, icfin=Ic2, lapse=60*10, timex=60*5)
Tc2 = curva2.getTc(60*15)

# Concatenamos los resultados
# De esta forma la lista incluirá valores para t=600 seg y t=900 seg
sal1 = [x for x in curva1 if x[1] < Tc1]
sal2 = [x for x in curva2 if x[1] > Tc2]
sal = sal1 + sal2 + [(60*15, Tc2)]


# Ahora veamos el período en que se supero Tcmax 50°C
timeOver = curva2.getTime(50) - curva1.getTime(50)
print "Minutos sobre 50 C = %.2f" % (timeOver/60)


print Icnom
curva3 = scc.getData(tcx=50, icfin=300, lapse=60*10, timex=0)
print curva3[0], curva3[-1]
print curva3.getTime(48)

print "****", scc.getIcini(tcx=48, factor=300/Icnom, lapse=curva3.getTime(48))
print "****", scc.getIcini(tcx=43, factor=300/Icnom, lapse=curva3.getTime(43))

print scc.getIcfin(tcx=48, icini=Icnom, lapse=curva3.getTime(48), tcxini=None)
lap = curva3.getTime(43) - curva3.getTime(48)
print scc.getIcfin(tcx=43, icini=Icnom, lapse=lap, tcxini=48)