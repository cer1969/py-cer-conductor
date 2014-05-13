# CRISTIAN ECHEVERRÍA RABÍ

import cer.conductor as cx
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
        self.assertEqual(cc.altitude, 300.0)
        self.assertEqual(cc.airVelocity, 2.0)
        self.assertEqual(cc.sunEffect, 1.0)
        self.assertEqual(cc.emissivity, 0.5)
        self.assertEqual(cc.formula, cx.CF_IEEE)
        self.assertEqual(cc.deltaTemp, 0.0001)
    
    #--------------------------------------------------------------------------
    # Verifica errores en parámetros de conductor y category conductor al crear CurrentCalc
    
    def test_error_r25(self):
        self.cond.r25 = 0.0
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
        self.cond.r25 = -0.2
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
    
    def test_error_diameter(self):
        self.cond.diameter = 0.0
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
        self.cond.diameter = -0.1
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
    
    def test_error_alpha(self):
        self.cate.alpha = 1.1
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
        self.cate.alpha = -0.1
        self.assertRaises(ValueError, cx.CurrentCalc, self.cond)
        
#-----------------------------------------------------------------------------------------

class TCProperties(unittest.TestCase):
    
    def setUp(self):
        cond = cx.Conductor(category=cx.CC_AAAC, name="AAAC 740,8 MCM FLINT",
                            diameter=25.17, r25=0.089360)
        self.cc = cx.CurrentCalc(cond)
    
    def SetValue(self, prop, value):
        setattr(self.cc, prop, value)
    
    def test_values(self):
        # Varifica asignación de valores correcta
        self.cc.altitude = 150.0
        self.assertEqual(self.cc.altitude, 150.0)
        
        self.cc.airVelocity = 2.0
        self.assertEqual(self.cc.airVelocity, 2.0)
        
        self.cc.sunEffect = 0.5
        self.assertEqual(self.cc.sunEffect, 0.5)
        
        self.cc.emissivity = 0.7
        self.assertEqual(self.cc.emissivity, 0.7)
        
        self.cc.formula = cx.CF_IEEE
        self.assertEqual(self.cc.formula, cx.CF_IEEE)
        
        self.cc.deltaTemp = 0.01
        self.assertEqual(self.cc.deltaTemp, 0.01)
        
    def test_errors(self):
        # Verifica que lanza error con valores fuera de rango
        self.assertRaises(AttributeError, self.SetValue, "conductor", 1)
        
        self.assertRaises(ValueError, self.SetValue, "altitude", -0.1)
        self.assertRaises(ValueError, self.SetValue, "airVelocity", -0.1)
        
        self.assertRaises(ValueError, self.SetValue, "sunEffect", 1.1)
        self.assertRaises(ValueError, self.SetValue, "sunEffect", -0.1)
        
        self.assertRaises(ValueError, self.SetValue, "emissivity", 1.1)
        self.assertRaises(ValueError, self.SetValue, "emissivity", -0.1)
        
        self.assertRaises(ValueError, self.SetValue, "formula", "")
        self.assertRaises(ValueError, self.SetValue, "deltaTemp", -0.1)
        self.assertRaises(ValueError, self.SetValue, "deltaTemp", 0)

#-----------------------------------------------------------------------------------------

class TCMethods(unittest.TestCase):
    
    def setUp(self):
        cond = cx.Conductor(category=cx.CC_AAAC, name="AAAC 740,8 MCM FLINT",
                            diameter=25.17, r25=0.089360)
        self.cc = cx.CurrentCalc(cond)

    def test_getCurrent(self):
        self.assertRaises(ValueError, self.cc.getCurrent, cx.TA_MIN - 1, 50)
        self.assertRaises(ValueError, self.cc.getCurrent, cx.TA_MAX + 1, 50)
        self.assertRaises(ValueError, self.cc.getCurrent, 25, cx.TC_MIN - 1)
        self.assertRaises(ValueError, self.cc.getCurrent, 25, cx.TC_MAX + 1)
        
        # Valores
        self.assertEqual(self.cc.getCurrent(25.0, 25.0), 0.0)
        self.assertEqual(self.cc.getCurrent(30.0, 25.0), 0.0)
        
        self.cc.formula = cx.CF_CLASSIC
        self.assertAlmostEqual(self.cc.getCurrent(25.0, 50.0), 517.7, 1)
        self.assertAlmostEqual(self.cc.getCurrent(30.0, 60.0), 585.4, 1)
        self.assertAlmostEqual(self.cc.getCurrent(10.0, 30.0), 438.4, 1)
        
        amp1 = self.cc.getCurrent(3.0, 30.0)
        self.cc.formula = cx.CF_IEEE
        amp2 = self.cc.getCurrent(3.0, 30.0)
        self.assertNotEqual(amp1, amp2)
        
        self.cc.formula = cx.CF_CLASSIC
        self.cc.sunEffect = 1.0
        amp1 = self.cc.getCurrent(25.0, 50.0)
        self.cc.sunEffect = 0.0
        amp2 = self.cc.getCurrent(25.0, 50.0)
        self.assertNotEqual(amp1, amp2)

    def test_getTc(self):
        # Varifica que los cálculos de getTc sean coherentes con getCurrent
        amp1 = self.cc.getCurrent(25.0, 50.0)
        amp2 = self.cc.getCurrent(35.0, 65.0)
        tc1 = self.cc.getTc(25.0, amp1)
        tc2 = self.cc.getTc(35.0, amp2)
        self.assert_(abs(tc1 - 50) < self.cc.deltaTemp)
        self.assert_(abs(tc2 - 65) < self.cc.deltaTemp)
        
        self.assertRaises(ValueError, self.cc.getTc, cx.TA_MIN - 1, 100)
        self.assertRaises(ValueError, self.cc.getTc, cx.TA_MAX + 1, 100)
        self.assertRaises(ValueError, self.cc.getTc, 30, -1)
        Icmax = self.cc.getCurrent(30, cx.TC_MAX)
        self.assertRaises(ValueError, self.cc.getTc, 30, Icmax + 1)

    def test_getTa(self):
        # Varifica que los cálculos de getTa sean coherentes con getCurrent
        amp1 = self.cc.getCurrent(25.0, 50.0)
        amp2 = self.cc.getCurrent(35.0, 65.0)
        ta1 = self.cc.getTa(50.0, amp1)
        ta2 = self.cc.getTa(65.0, amp2)
        self.assert_(abs(ta1 - 25) < self.cc.deltaTemp)
        self.assert_(abs(ta2 - 35) < self.cc.deltaTemp)
        
        self.assertRaises(ValueError, self.cc.getTa, cx.TC_MIN - 1, 100)
        self.assertRaises(ValueError, self.cc.getTa, cx.TC_MAX + 1, 100)
        self.assertRaises(ValueError, self.cc.getTa, 50, -1)
        Icmax = self.cc.getCurrent(cx.TA_MIN, 50)
        self.assertRaises(ValueError, self.cc.getTa, Icmax + 1, 50)
        
#-----------------------------------------------------------------------------------------

s1 = unittest.TestLoader().loadTestsFromTestCase(TCConstructor)
s2 = unittest.TestLoader().loadTestsFromTestCase(TCProperties)
s3 = unittest.TestLoader().loadTestsFromTestCase(TCMethods)

suite = unittest.TestSuite([s1, s2, s3])

#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)