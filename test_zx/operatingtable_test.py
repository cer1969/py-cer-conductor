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

    def test_itemsDefaults(self):
        cc0 = zx.CurrentCalc(self.cab0)
        item = zx.OperatingItem(cc0)

        self.assertEqual(item.currentcalc.conductor, self.cab0)
        self.assertEqual(item.tempMaxOp, 50.0)
        self.assertEqual(item.nsc, 1)

    def test_itemError(self):
        cc0 = zx.CurrentCalc(self.cab0)
        cc1 = zx.CurrentCalc(self.cab1)
        # tempMaxOp
        self.assertRaises(ValueError, zx.OperatingItem, cc0, zx.TC_MIN - 1, 1)
        self.assertRaises(ValueError, zx.OperatingItem, cc1, zx.TC_MAX + 1, 1)
        # nsc
        self.assertRaises(ValueError, zx.OperatingItem, cc0, 50.0, 0)
        self.assertRaises(ValueError, zx.OperatingItem, cc1, 50.0, -1)

    def test_itemReadOnly(self):
        cc0 = zx.CurrentCalc(self.cab0)
        item = zx.OperatingItem(cc0)

        def setValue(prop, value):
            setattr(item, prop, value)

        self.assertRaises(AttributeError, setValue, "currentcalc", 3)
        self.assertRaises(AttributeError, setValue, "tempMaxOp", 3)
        self.assertRaises(AttributeError, setValue, "nsc", 3)

    # def test_tableNoArguments(self):
    #     cc0 = cx.CurrentCalc(self.cab0)
    #     cc1 = cx.CurrentCalc(self.cab1)
    #     to = cx.OperatingTable()
    #     to.append(cx.OperatingItem(cc0,  50.0, 1))
    #     to.append(cx.OperatingItem(cc1, 125.0, 1))
    #     self.assertEqual(to[0].currentcalc.conductor, self.cab0)
    #     self.assertEqual(to[1].currentcalc.conductor, self.cab1)

    # def test_tableWithArguments(self):
    #     cc0 = cx.CurrentCalc(self.cab0)
    #     cc1 = cx.CurrentCalc(self.cab1)
    #     to = cx.OperatingTable([cx.OperatingItem(cc0,  50.0, 1),
    #                             cx.OperatingItem(cc1, 125.0, 1)])
    #     self.assertEqual(to[0].currentcalc.conductor, self.cab0)
    #     self.assertEqual(to[1].currentcalc.conductor, self.cab1)


    # def test_tableGetCurrent(self):
    #     cc0 = cx.CurrentCalc(self.cab0)
    #     cc1 = cx.CurrentCalc(self.cab1)
    #     item0 = cx.OperatingItem(cc0,  50.0, 1)
    #     item1 = cx.OperatingItem(cc1, 125.0, 1)
    #     to = cx.OperatingTable([item0, item1])

    #     ta = 25.0
    #     ic = to.getCurrent(ta)
    #     ic0 = item0.currentcalc.getCurrent(ta, item0.tempMaxOp)
    #     ic1 = item1.currentcalc.getCurrent(ta, item1.tempMaxOp)
    #     self.assertEqual(ic, min([ic0, ic1]))

#-----------------------------------------------------------------------------------------

s1 = unittest.TestLoader().loadTestsFromTestCase(TCTablaOperacion)

suite = unittest.TestSuite([s1])

#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
