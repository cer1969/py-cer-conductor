# CRISTIAN ECHEVERRÍA RABÍ 

import cer.conductor as cx

for i,o in cx.Conductor.__dict__.items():
    print(i, type(o))
a = cx.Conductor()

print(type(a) is cx.Conductor)
print(cx.Conductor)
print(cx.version)


cu300 = cx.Conductor("CU 300 MCM", cx.CC_CU, 15.95, 152.00, 1.378, 6123.0, 0.12270, 0, "")
cc = cx.CurrentCalc(cu300)

#cc.deltaTemp = 0

for i, va in enumerate([10, 15, 20, 25, 30]):
    for j, vc in enumerate([30, 35, 40, 45, 50]):
        current = cc.getCurrent(va, vc)
        txt = "i=%d, i=%d, Ta=%.2f, Tc=%.2f, I=%.2f" % (i, j, va, vc, current)
        print(txt)
        
#print (cc.deltaTemp)