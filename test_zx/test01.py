from cer.conductor import zx

catmk = zx.CategoryMaker('COPPER', 12000.0, 0.0000169, 0.0, 0.00374)

cat1 = catmk.get()
catmk.name = "Juan"
cat2 = catmk.get()

print(cat1.name)
print(cat2.name)

print(zx.CC_AAAC.name)

condmk = zx.ConductorMaker("AAAC 740,8 MCM FLINT", zx.CC_AAAC, diameter=25.17, r25=0.089360)
c1 = condmk.get()

print(c1)
