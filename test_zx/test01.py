from cer.conductor import _zx

catmk = _zx.CategoryMaker('COPPER', 12000.0, 0.0000169, 0.0, 0.00374)

cat1 = catmk.get()
catmk.name = "Juan"
cat2 = catmk.get()

print(cat1.name)
print(cat2.name)

print(_zx.CC_AAAC.name)
