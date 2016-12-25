# CRISTIAN ECHEVERRÍA RABÍ

import cer.conductor.ccx as cx
import unittest

#-----------------------------------------------------------------------------------------

class TCConstructor(unittest.TestCase):

    def setUp(self):
        self.cate = cx.Category(name='AAAC (AASC)', alpha=0.003400)
        self.cond = cx.Conductor(category=self.cate, name="AAAC 740,8 MCM FLINT",
                                 diameter=25.17, r25=0.089360)
    
    def test_defaults(self):
        # Verifica que se asignen valores por defecto al crear CurrentCalc
        cc = cx.CurrentCalc(self.cond)
        
        self.assertEqual(cc.conductor, self.cond)
        self.assertEqual(cc.altitude, 300)
        self.assertEqual(cc.airVelocity, 2)
        self.assertEqual(cc.sunEffect, 1)
        self.assertEqual(cc.emissivity, 0.5)
        self.assertEqual(cc.formula, cx.CF_IEEE)
        self.assertEqual(cc.deltaTemp, 0.01)
    
    #--------------------------------------------------------------------------
    # Verifica errores en parámetros de conductor y category conductor al crear CurrentCalc
    
    def test_error_r25(self):
        self.cond.r25 = 0.001
        self.assertTrue(cx.CurrentCalc(self.cond))
        self.cond.r25 = 0
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
        self.cond.r25 = -0.001
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
    
    def test_error_diameter(self):
        self.cond.diameter = 0.001
        self.assertTrue(cx.CurrentCalc(self.cond))
        self.cond.diameter = 0
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
        self.cond.diameter = -0.001
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
    
    def test_error_alpha(self):
        self.cate.alpha = 0.001
        self.assertTrue(cx.CurrentCalc(self.cond))
        self.cate.alpha = 0.999
        self.assertTrue(cx.CurrentCalc(self.cond))
        self.cate.alpha = 0
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
        self.cate.alpha = -0.001
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
        self.cate.alpha = 1
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
        self.cate.alpha = 1.001
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
        
#-----------------------------------------------------------------------------------------

class TCProperties(unittest.TestCase):
    
    def setUp(self):
        self.cond = cx.Conductor(category=cx.CC_AAAC, name="AAAC 740,8 MCM FLINT",
                            diameter=25.17, r25=0.089360)
        self.cc = cx.CurrentCalc(self.cond)
    
    def SetValue(self, prop, value):
        setattr(self.cc, prop, value)
        return True
    
    def test_conductor(self):
        self.assertEqual(self.cc.conductor, self.cond)
        self.assertRaises(AttributeError, self.SetValue, "conductor", 1)
    
    def test_altitude(self):
        self.cc.altitude = 150.0
        self.assertEqual(self.cc.altitude, 150.0)
        self.assertTrue(self.SetValue("altitude", 0))
        self.assertRaises(ValueError, self.SetValue, "altitude", -0.001)
    
    def test_airVelocity(self):
        self.cc.airVelocity = 2.0
        self.assertEqual(self.cc.airVelocity, 2.0)
        self.assertTrue(self.SetValue("airVelocity", 0))
        self.assertRaises(ValueError, self.SetValue, "airVelocity", -0.001)
    
    def test_sunEffect(self):
        self.cc.sunEffect = 0.5
        self.assertEqual(self.cc.sunEffect, 0.5)
        self.assertTrue(self.SetValue("sunEffect", 0))
        self.assertTrue(self.SetValue("sunEffect", 1))
        self.assertRaises(ValueError, self.SetValue, "sunEffect", -0.001)
        self.assertRaises(ValueError, self.SetValue, "sunEffect", 1.001)
    
    def test_emissivity(self):
        self.cc.emissivity = 0.7
        self.assertEqual(self.cc.emissivity, 0.7)
        self.assertTrue(self.SetValue("emissivity", 0))
        self.assertTrue(self.SetValue("emissivity", 1))
        self.assertRaises(ValueError, self.SetValue, "emissivity", -0.001)
        self.assertRaises(ValueError, self.SetValue, "emissivity", 1.001)
    
    def test_formula(self):
        self.cc.formula = cx.CF_IEEE
        self.assertEqual(self.cc.formula, cx.CF_IEEE)
        self.assertTrue(self.SetValue("formula",cx.CF_IEEE))
        self.assertTrue(self.SetValue("formula",cx.CF_CLASSIC))
        self.assertRaises(ValueError, self.SetValue, "formula", "")
        self.assertRaises(ValueError, self.SetValue, "formula", 1)
        
    def test_deltaTemp(self):
        self.cc.deltaTemp = 0.001
        self.assertEqual(self.cc.deltaTemp, 0.001)
        self.assertTrue(self.SetValue("deltaTemp", 0.0001))
        self.assertRaises(ValueError, self.SetValue, "deltaTemp", -0.0001)
        self.assertRaises(ValueError, self.SetValue, "deltaTemp", 0)

#-----------------------------------------------------------------------------------------

class TCMethods(unittest.TestCase):
    
    def setUp(self):
        cond = cx.Conductor(category=cx.CC_AAAC, name="AAAC 740,8 MCM FLINT",
                            diameter=25.17, r25=0.089360)
        self.cc = cx.CurrentCalc(cond)

    def test_getResistance(self):
        self.assertTrue(self.cc.getResistance(cx.TC_MIN))
        self.assertTrue(self.cc.getResistance(cx.TC_MAX))
        self.assertRaises(ValueError, self.cc.getResistance, cx.TC_MIN - 0.001)
        self.assertRaises(ValueError, self.cc.getResistance, cx.TC_MAX + 0.001)
    
    def test_getCurrent(self):
        self.assertEqual(self.cc.getCurrent(25, 25), 0)
        self.assertEqual(self.cc.getCurrent(26, 25), 0)
        
        self.cc.formula = cx.CF_CLASSIC
        self.assertAlmostEqual(self.cc.getCurrent(25, 50), 517.7, 1)
        self.assertAlmostEqual(self.cc.getCurrent(30, 60), 585.4, 1)
        self.assertAlmostEqual(self.cc.getCurrent(10, 30), 438.4, 1)
        
        amp1 = self.cc.getCurrent(3, 30)
        self.cc.formula = cx.CF_IEEE
        amp2 = self.cc.getCurrent(3, 30)
        self.assertNotEqual(amp1, amp2)
        
        self.cc.sunEffect = 1.0
        amp1 = self.cc.getCurrent(25.0, 50.0)
        self.cc.sunEffect = 0.0
        amp2 = self.cc.getCurrent(25.0, 50.0)
        self.assertNotEqual(amp1, amp2)
        
        self.assertTrue(self.cc.getCurrent(cx.TA_MIN, 50))
        self.assertTrue(self.cc.getCurrent(cx.TA_MAX, 50)>=0)
        self.assertTrue(self.cc.getCurrent(25, cx.TC_MIN)>=0)
        self.assertTrue(self.cc.getCurrent(25, cx.TC_MAX))
        self.assertRaises(ValueError, self.cc.getCurrent, cx.TA_MIN - 0.001, 50)
        self.assertRaises(ValueError, self.cc.getCurrent, cx.TA_MAX + 0.001, 50)
        self.assertRaises(ValueError, self.cc.getCurrent, 25, cx.TC_MIN - 0.001)
        self.assertRaises(ValueError, self.cc.getCurrent, 25, cx.TC_MAX + 0.001)
    
    def test_getTc(self):
        # Verifica que los cálculos de getTc sean coherentes con getCurrent
        amp1 = self.cc.getCurrent(25, 50)
        amp2 = self.cc.getCurrent(35, 65)
        tc1 = self.cc.getTc(25, amp1)
        tc2 = self.cc.getTc(35, amp2)
        self.assertTrue(abs(tc1 - 50) < self.cc.deltaTemp)
        self.assertTrue(abs(tc2 - 65) < self.cc.deltaTemp)
        
        # Verifica rangos de entrada para ta
        Icmax = self.cc.getCurrent(cx.TA_MIN, cx.TC_MAX)
        self.assertTrue(self.cc.getTc(cx.TA_MIN, Icmax))
        self.assertRaises(ValueError, self.cc.getTc, cx.TA_MIN - 0.0001, Icmax)
        
        Icmax = self.cc.getCurrent(cx.TA_MAX, cx.TC_MAX)
        self.assertTrue(self.cc.getTc(cx.TA_MAX, Icmax))
        self.assertRaises(ValueError, self.cc.getTc, cx.TA_MAX + 0.0001, Icmax)
        
        # Verifica rangos de entrada para ic
        self.assertRaises(ValueError, self.cc.getTc, 30, -0.001)
        Icmax = self.cc.getCurrent(30, cx.TC_MAX)
        self.assertTrue(self.cc.getTc(30, Icmax))
        self.assertRaises(ValueError, self.cc.getTc, 30, Icmax + 0.001)
    
    def test_getTa(self):
        # Verifica que los cálculos de getTa sean coherentes con getCurrent
        amp1 = self.cc.getCurrent(25, 50)
        amp2 = self.cc.getCurrent(35, 65)
        ta1 = self.cc.getTa(50, amp1)
        ta2 = self.cc.getTa(65, amp2)
        self.assertTrue(abs(ta1 - 25) < self.cc.deltaTemp)
        self.assertTrue(abs(ta2 - 35) < self.cc.deltaTemp)
        
        # Verifica rangos de entrada para tc
        self.assertTrue(self.cc.getTa(cx.TC_MIN, 0))
        self.assertRaises(ValueError, self.cc.getTa, cx.TC_MIN - 0.0001, 0)
        
        Icmax = self.cc.getCurrent(cx.TA_MIN, cx.TC_MAX)
        self.assertTrue(self.cc.getTa(cx.TC_MAX, Icmax))
        self.assertRaises(ValueError, self.cc.getTa, cx.TC_MAX + 0.0001, Icmax)
        
        # Verifica rangos de entrada para ic
        Icmin = self.cc.getCurrent(cx.TA_MAX, 100)
        Icmax = self.cc.getCurrent(cx.TA_MIN, 100)
        
        self.assertTrue(self.cc.getTa(100, Icmin))
        self.assertRaises(ValueError, self.cc.getTa, 100, Icmin - 0.0001)
        self.assertTrue(self.cc.getTa(100, Icmax))
        self.assertRaises(ValueError, self.cc.getTa, 100, Icmax + 0.0001)
        
#-----------------------------------------------------------------------------------------

s1 = unittest.TestLoader().loadTestsFromTestCase(TCConstructor)
s2 = unittest.TestLoader().loadTestsFromTestCase(TCProperties)
s3 = unittest.TestLoader().loadTestsFromTestCase(TCMethods)

suite = unittest.TestSuite([s1, s2, s3])

#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)