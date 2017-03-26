# CRISTIAN ECHEVERRÍA RABÍ

from cer.conductor import zx
import unittest

#-----------------------------------------------------------------------------------------

class TCTablaOperacion(unittest.TestCase):

    def setUp(self):
        self.cab0 = zx.Conductor(name="CU 2/0 AWG", category=zx.CC_CU,
                                 diameter=10.5, r25=0.2767)
        self.cab1 = zx.Conductor(name="COPPERWELD 3/8", category=zx.CC_CUWELD,
                                 diameter=9.78, r25=1.030581)
        self.cc0 = zx.CurrentCalc(self.cab0)
        self.cc1 = zx.CurrentCalc(self.cab1)
        self.item0 = zx.OperatingItem(self.cc0,  50.0, 1)
        self.item1 = zx.OperatingItem(self.cc1, 125.0, 1)

    def test_itemsDefaults(self):
        self.assertEqual(self.item0.currentcalc.conductor, self.cab0)
        self.assertEqual(self.item0.tempMaxOp, 50.0)
        self.assertEqual(self.item0.nsc, 1)

    def test_itemError(self):
        # tempMaxOp
        self.assertRaises(ValueError, zx.OperatingItem, self.cc0, zx.TC_MIN - 1, 1)
        self.assertRaises(ValueError, zx.OperatingItem, self.cc1, zx.TC_MAX + 1, 1)
        # nsc
        self.assertRaises(ValueError, zx.OperatingItem, self.cc0, 50.0, 0)
        self.assertRaises(ValueError, zx.OperatingItem, self.cc1, 50.0, -1)

    def test_itemReadOnly(self):
        def setValue(prop, value):
            setattr(self.item0, prop, value)
        self.assertRaises(AttributeError, setValue, "currentcalc", 3)
        self.assertRaises(AttributeError, setValue, "tempMaxOp", 3)
        self.assertRaises(AttributeError, setValue, "nsc", 3)

    def test_tableDefaults(self):
        opt = zx.OperatingTable()
        self.assertEqual(opt.items, [])
        self.assertEqual(opt.idx, None)
        opt = zx.OperatingTable(23)
        self.assertEqual(opt.items, [])
        self.assertEqual(opt.idx, 23)
        opt = zx.OperatingTable("hola")
        self.assertEqual(opt.items, [])
        self.assertEqual(opt.idx, "hola")
    
    def test_tableReadOnly(self):
        opt = zx.OperatingTable()
        def setValue(prop, value):
            setattr(opt, prop, value)
        self.assertRaises(AttributeError, setValue, "items", 3)
        self.assertRaises(AttributeError, setValue, "idx", 100)
    
    def test_tableAppend(self):
        opt = zx.OperatingTable()
        opt.items.append(self.item0)
        opt.items.append(self.item1)
        self.assertEqual(opt.items[0].currentcalc.conductor, self.cab0)
        self.assertEqual(opt.items[1].currentcalc.conductor, self.cab1)

    def test_tableGetCurrent(self):
        opt = zx.OperatingTable()
        opt.items.extend([self.item0, self.item1])
        
        ta = 25.0
        ic = opt.getCurrent(ta)
        ic0 = self.item0.currentcalc.getCurrent(ta, self.item0.tempMaxOp)
        ic1 = self.item1.currentcalc.getCurrent(ta, self.item1.tempMaxOp)
        self.assertEqual(ic, min([ic0, ic1]))

        ta = 80.0
        ic = opt.getCurrent(ta)
        ic0 = self.item0.currentcalc.getCurrent(ta, self.item0.tempMaxOp)
        ic1 = self.item1.currentcalc.getCurrent(ta, self.item1.tempMaxOp)
        self.assertEqual(ic, min([ic0, ic1]))

#-----------------------------------------------------------------------------------------

s1 = unittest.TestLoader().loadTestsFromTestCase(TCTablaOperacion)

suite = unittest.TestSuite([s1])

#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
