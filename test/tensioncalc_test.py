# CRISTIAN ECHEVERRÍA RABÍ 

from cer.conductor import cx
import unittest

#-----------------------------------------------------------------------------------------

class TCConstructor(unittest.TestCase):

    def setUp(self):
        self.catemk = cx.CategoryMaker('AAAC (AASC)', 6450.0, 0.000023, 20.0)
        self.cate = cx.Category('AAAC (AASC)', 6450.0, 0.000023, 20.0)
        self.condmk = cx.ConductorMaker("AAAC 740,8 MCM FLINT", self.cate, 25.17, 375.4, 1.035, 11625.0)
        self.cond = cx.Conductor("AAAC 740,8 MCM FLINT", self.cate, 25.17, 375.4, 1.035, 11625.0)
    
    def test_defaultValues(self):
        # Verifica que se asignen valores por defecto al crear TempleCalc
        tc = cx.TensionCalc(self.cond)
        
        self.assertEqual(tc.conductor, self.cond)
        self.assertEqual(tc.tensionFactorRef, 0.2)
        self.assertEqual(tc.tensionRef, tc.tensionFactorRef*self.cond.strength)
        self.assertEqual(tc.tempRef, 15.0)
        self.assertEqual(tc.creepFactorRef, 1.0)
        self.assertEqual(tc.iceThickRef, 0.0)
        self.assertEqual(tc.windPressureRef, 0.0)
        
        self.assertEqual(tc.creepFactorCal, 1.0)
        self.assertEqual(tc.iceThickCal, 0.0)
        self.assertEqual(tc.windPressureCal, 0.0)
        self.assertEqual(tc.deltaTension, 0.01)
    
    #--------------------------------------------------------------------------
    # Verifica errores en parámetros de conductor y category conductor al crear TempleCalc
    
    def test_errordiameter(self):
        self.condmk.diameter = 0.0
        self.assertRaises(ValueError, cx.TensionCalc, self.condmk.get())
        self.condmk.diameter = -0.1
        self.assertRaises(ValueError, cx.TensionCalc, self.condmk.get())
    
    def test_errorArea(self):
        self.condmk.area = 0.0
        self.assertRaises(ValueError, cx.TensionCalc, self.condmk.get())
        self.condmk.area = -0.1
        self.assertRaises(ValueError, cx.TensionCalc, self.condmk.get())

    def test_errorWeight(self):
        self.condmk.weight = 0.0
        self.assertRaises(ValueError, cx.TensionCalc, self.condmk.get())
        self.condmk.weight = -0.1
        self.assertRaises(ValueError, cx.TensionCalc, self.condmk.get())

    def test_errorStrength(self):
        self.condmk.strength = 0.0
        self.assertRaises(ValueError, cx.TensionCalc, self.condmk.get())
        self.condmk.strength = -0.1
        self.assertRaises(ValueError, cx.TensionCalc, self.condmk.get())
    
    def test_errorModelas(self):
        self.catemk.modelas = 0.0
        cond = cx.Conductor("AAAC 740,8 MCM FLINT", self.catemk.get(), 25.17, 375.4, 1.035, 11625.0)
        self.assertRaises(ValueError, cx.TensionCalc, cond)
        self.catemk.modelas = -0.1
        cond = cx.Conductor("AAAC 740,8 MCM FLINT", self.catemk.get(), 25.17, 375.4, 1.035, 11625.0)
        self.assertRaises(ValueError, cx.TensionCalc, cond)

    def test_errorCoefexp(self):
        self.catemk.coefexp = 0.0
        cond = cx.Conductor("AAAC 740,8 MCM FLINT", self.catemk.get(), 25.17, 375.4, 1.035, 11625.0)
        self.assertRaises(ValueError, cx.TensionCalc, cond)
        self.catemk.coefexp = -0.1
        cond = cx.Conductor("AAAC 740,8 MCM FLINT", self.catemk.get(), 25.17, 375.4, 1.035, 11625.0)
        self.assertRaises(ValueError, cx.TensionCalc, cond)

    def test_errorCreep(self):
        self.catemk.creep = -0.1
        cond = cx.Conductor("AAAC 740,8 MCM FLINT", self.catemk.get(), 25.17, 375.4, 1.035, 11625.0)
        self.assertRaises(ValueError, cx.TensionCalc, cond)


#-----------------------------------------------------------------------------------------

class TCProperties(unittest.TestCase):
    
    def setUp(self):
        cab = cx.Conductor(category=cx.CC_AAAC, name="AAAC 740,8 MCM FLINT",
                           diameter=25.17, area=375.4, weight=1.035, strength=11625.0)
        self.tc = cx.TensionCalc(cab)
    
    def SetValue(self, prop, value):
        setattr(self.tc, prop, value)
    
    def testValues(self):
        # Varifica asignación de valores correcta
        self.tc.tensionFactorRef = 0.3
        self.assertEqual(self.tc.tensionFactorRef, 0.3)
        self.tc.tensionRef = 2000.0
        self.assertAlmostEqual(self.tc.tensionRef, 2000.0, 2)
        self.tc.tempRef = 17.0
        self.assertAlmostEqual(self.tc.tempRef, 17.0, 2)
        self.tc.creepFactorRef = 0.5
        self.assertEqual(self.tc.creepFactorRef, 0.5)
        self.tc.iceThickRef = 15.0
        self.assertAlmostEqual(self.tc.iceThickRef, 15.0, 2)
        self.tc.windPressureRef = 40.0
        self.assertAlmostEqual(self.tc.windPressureRef, 40.0, 2)
        
        self.tc.creepFactorCal = 0.5
        self.assertEqual(self.tc.creepFactorCal, 0.5)
        self.tc.iceThickCal = 15.0
        self.assertAlmostEqual(self.tc.iceThickCal, 15.0, 2)
        self.tc.windPressureCal = 40.0
        self.assertAlmostEqual(self.tc.windPressureCal, 40.0, 2)
        self.tc.deltaTension = 0.2
        self.assertAlmostEqual(self.tc.deltaTension, 0.2, 2)
        
    def testErrors(self):
        # Verifica que lanza error con valores fuera de rango
        self.assertRaises(ValueError, self.SetValue, "tensionFactorRef", -0.1)
        self.assertRaises(ValueError, self.SetValue, "tensionFactorRef", 1.1)
        self.assertRaises(ValueError, self.SetValue, "tensionRef", -0.1)
        self.assertRaises(ValueError, self.SetValue, "creepFactorRef", -0.1)
        self.assertRaises(ValueError, self.SetValue, "creepFactorRef", 1.1)
        self.assertRaises(ValueError, self.SetValue, "iceThickRef", -0.1)
        self.assertRaises(ValueError, self.SetValue, "windPressureRef", -0.1)
        
        self.assertRaises(ValueError, self.SetValue, "creepFactorCal", -0.1)
        self.assertRaises(ValueError, self.SetValue, "creepFactorCal", 1.1)
        self.assertRaises(ValueError, self.SetValue, "iceThickCal", -0.1)
        self.assertRaises(ValueError, self.SetValue, "windPressureCal", -0.1)
        self.assertRaises(ValueError, self.SetValue, "deltaTension", -0.1)
        self.assertRaises(ValueError, self.SetValue, "deltaTension",  0.0)
        
        # Propiedades de solo lectura
        self.assertRaises(AttributeError, self.SetValue, "iceLoadRef", 1)
        self.assertRaises(AttributeError, self.SetValue, "iceLoadCal", 1)
        self.assertRaises(AttributeError, self.SetValue, "windLoadRef", 1)
        self.assertRaises(AttributeError, self.SetValue, "windLoadCal", 1)
        self.assertRaises(AttributeError, self.SetValue, "transLoadRef", 1)
        self.assertRaises(AttributeError, self.SetValue, "transLoadCal", 1)

#-----------------------------------------------------------------------------------------

class TCMethods(unittest.TestCase):
    
    def setUp(self):
        cab = cx.Conductor(category=cx.CC_AAAC, name="AAAC 740,8 MCM FLINT",
                           diameter=25.17, area=375.4, weight=1.035, strength=11625.0)
        self.tc = cx.TensionCalc(cab)

    def test_getTension(self):
        # Errores de argumentos
        self.assertRaises(ValueError, self.tc.getTension, -0.1, 30.0)
        
        # Valores
        f1 = 2000.0
        t1 = 15.0
        self.tc.tensionRef = f1
        self.tc.tempRef = t1
        t2 = 50.0
        f2 = self.tc.getTension(100, t2)
        
        self.tc.tensionRef = f2
        self.tc.tempRef = t2
        self.assertAlmostEqual(self.tc.getTension(100, t1), f1, 1)

        
#-----------------------------------------------------------------------------------------

s1 = unittest.TestLoader().loadTestsFromTestCase(TCConstructor)
s2 = unittest.TestLoader().loadTestsFromTestCase(TCProperties)
s3 = unittest.TestLoader().loadTestsFromTestCase(TCMethods)

suite = unittest.TestSuite([s1, s2, s3])

#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)