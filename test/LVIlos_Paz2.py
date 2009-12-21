# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ

from __future__ import division
import cer.conductor as cx

#-----------------------------------------------------------------------------------------
# NO MODIFICAR

R3 = 3**(0.5) # Raiz de 3

def nform(n,format="%.2f"):
    txt = format % n
    txt = txt.replace(".",",")
    return txt

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# PARÁMETROS MODIFICABLES

# Línea 220 Los Vilos - Pan de Azúcar 1
c1 = cx.Conductor(name = 'AAAC 740,8 MCM FLINT',
                  category = cx.CC_AAAC,
                  diameter = 25.17,               # en mm
                  area = 375.4,                  # en mm2
                  weight = 1.035,                  # en Kg/m
                  strength = 11625.0,            # en Kg
                  r25 = 0.08936,                 # Resistencia a 25°C en Ohm/km
                  hcap = 0.05274,                  # capacidad calórica
                  )

VOLTAJE = 220.0     # kV de la línea
NSC = 1             # N° de subconductores por fase
FACTOR = 1.968      # Factor de sobrecarga
SOL = 1.0           # Efecto sol 1:Si, 0:No
TEMP_MAX_OP = 55.0  # T° maxima de operación línea
TIEMPO = 15.0       # Tiempo buscado en minutos

#-----------------------------------------------------------------------------------------

ac = cx.CurrentCalc(c1)
ac.sunEffect = SOL

print c1.name
print u"Temp. Diseño\t%s °C" % nform(TEMP_MAX_OP)
print u"Sobrecarga\t%s %%" % nform((FACTOR-1)*100)
print u"N° subconductores por fase\t%d" % NSC

txtsol = "SI" if SOL else "NO"
print u"Efecto Sol\t%s" % txtsol

print
print u"MVA Inicial para alcazar T°conductor %s°C en %s minutos" % (nform(TEMP_MAX_OP), nform(TIEMPO))
print u"Valores por línea. Considera %d subconductores por fase" % NSC
print u"T°Amb\tT° Inicial\tMva Inicial\tMva Falla"

scc = cx.TcTimeCalc(ac, ta=25.0)

for _tamb in range(10, 45, 5):
    scc.ta = float(_tamb)
    Icini = scc.getIcini(TEMP_MAX_OP, FACTOR, TIEMPO*60.0)
    Tcini = scc.getTc(Icini)
    MvaIni = VOLTAJE*Icini*R3/1000.0*NSC
    MvaFin = MvaIni*FACTOR
    txt = "%.1f\t%.1f\t%.1f\t%.1f" % (scc.ta, Tcini, MvaIni, MvaFin)
    txt = txt.replace(".",",")
    print txt