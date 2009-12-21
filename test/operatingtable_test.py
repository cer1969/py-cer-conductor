# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from __future__ import division
import cer.conductor as cx
import unittest

#-----------------------------------------------------------------------------------------

class TCTablaOperacion(unittest.TestCase):

    def setUp(self):
        self.cab0 = cx.Conductor(name="CU 2/0 AWG", category=cx.CC_CU,
                                 diameter=10.5, r25=0.2767)
        self.cab1 = cx.Conductor(name="COPPERWELD 3/8", category=cx.CC_CUWELD, 
                                 diameter=9.78, r25=1.030581)
        
    def test_itemsDefaults(self):
        cc0 = cx.CurrentCalc(self.cab0)
        item = cx.OperatingItem(cc0)
        
        self.assertEqual(item.currentcalc.conductor, self.cab0)
        self.assertEqual(item.tempMaxOp, 50.0)
        self.assertEqual(item.nsc, 1)
        self.assertEqual(item.currentcalc.altitude, 300.0)
        self.assertEqual(item.currentcalc.emissivity, 0.5)
    
    def test_itemError(self):
        cc0 = cx.CurrentCalc(self.cab0)
        cc1 = cx.CurrentCalc(self.cab1)
        # tempMaxOp
        self.assertRaises(ValueError, cx.OperatingItem, cc0, cx.TC_MIN - 1, 1)
        self.assertRaises(ValueError, cx.OperatingItem, cc1, cx.TC_MAX + 1, 1)
        # nsc
        self.assertRaises(ValueError, cx.OperatingItem, cc0, 50.0, 0)
        self.assertRaises(ValueError, cx.OperatingItem, cc1, 50.0, -1)
        # altitude
        self.assertRaises(ValueError, cx.OperatingItem, cc1, 50.0, 1, altitude=-0.1)
        # emissivity
        self.assertRaises(ValueError, cx.OperatingItem, cc1, 50.0, 1, emissivity=-0.1)
        self.assertRaises(ValueError, cx.OperatingItem, cc1, 50.0, 1, emissivity= 1.1)

    def test_itemReadOnly(self):
        cc0 = cx.CurrentCalc(self.cab0)
        item = cx.OperatingItem(cc0)
        
        def setValue(prop, value):
            setattr(item, prop, value)
        
        self.assertRaises(AttributeError, setValue, "currentcalc", 3)
        self.assertRaises(AttributeError, setValue, "tempMaxOp", 3)
        self.assertRaises(AttributeError, setValue, "nsc", 3)
        
    
    def test_tableNoArguments(self):
        cc0 = cx.CurrentCalc(self.cab0)
        cc1 = cx.CurrentCalc(self.cab1)
        to = cx.OperatingTable()
        to.append(cx.OperatingItem(cc0,  50.0, 1))
        to.append(cx.OperatingItem(cc1, 125.0, 1))
        self.assertEqual(to[0].currentcalc.conductor, self.cab0)
        self.assertEqual(to[1].currentcalc.conductor, self.cab1)
    
    def test_tableWithArguments(self):
        cc0 = cx.CurrentCalc(self.cab0)
        cc1 = cx.CurrentCalc(self.cab1)
        to = cx.OperatingTable([cx.OperatingItem(cc0,  50.0, 1),
                                cx.OperatingItem(cc1, 125.0, 1)])
        self.assertEqual(to[0].currentcalc.conductor, self.cab0)
        self.assertEqual(to[1].currentcalc.conductor, self.cab1)


    def test_tableGetCurrent(self):
        cc0 = cx.CurrentCalc(self.cab0)
        cc1 = cx.CurrentCalc(self.cab1)
        item0 = cx.OperatingItem(cc0,  50.0, 1)
        item1 = cx.OperatingItem(cc1, 125.0, 1)
        to = cx.OperatingTable([item0, item1])
        
        ta = 25.0
        ic = to.getCurrent(ta)
        ic0 = item0.currentcalc.getCurrent(ta, item0.tempMaxOp)
        ic1 = item1.currentcalc.getCurrent(ta, item1.tempMaxOp)
        self.assertEqual(ic, min([ic0, ic1]))
        
#-----------------------------------------------------------------------------------------

s1 = unittest.TestLoader().loadTestsFromTestCase(TCTablaOperacion)

suite = unittest.TestSuite([s1])

#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)