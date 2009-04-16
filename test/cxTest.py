# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from cer.conductor import cx

for i,o in cx.Conductor.__dict__.items():
    print i, type(o)
a = cx.Conductor()

print type(a) is cx.Conductor
print cx.Conductor
print cx.version