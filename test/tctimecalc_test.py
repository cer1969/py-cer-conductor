# CRISTIAN ECHEVERRÍA RABÍ 

from cer.conductor import cx
import unittest

#-----------------------------------------------------------------------------------------

class TCConstructor(unittest.TestCase):

    def setUp(self):
        self.cab = cx.Conductor(category=cx.CC_AAAC, name="AAAC 740,8 MCM FLINT",
                                diameter=25.17, r25=0.089360, hcap=0.052744)
    
    def test_defaultValues(self):
        # Verifica que se asignen valores por defecto
        cc = cx.CurrentCalc(self.cab)
        Imax = cc.getCurrent(25.0, cx.TC_MAX)
        scc = cx.TcTimeCalc(cc, 25.0)
        
        self.assertEqual(scc.currentcalc, cc)
        self.assertEqual(scc.currentcalc.conductor, self.cab)
        self.assertEqual(scc.ta, 25.0)
        self.assertEqual(scc.timeStep, 1.0)
        self.assertEqual(scc.deltaIc, 0.01)
        self.assertEqual(scc.icmax, Imax)
    
    #--------------------------------------------------------------------------
    # Verifica errores en parámetros de conductor
    
    def test_errorParameters(self):
        cc = cx.CurrentCalc(self.cab)
        
        self.assertRaises(ValueError, cx.TcTimeCalc, cc, cx.TA_MIN - 1)
        self.assertRaises(ValueError, cx.TcTimeCalc, cc, cx.TA_MAX + 1)
        
        cc.conductor.hcap = 0.0        
        self.assertRaises(ValueError, cx.TcTimeCalc, cc, 25.0)

    
#-----------------------------------------------------------------------------------------

class TCProperties(unittest.TestCase):
    
    def setUp(self):
        cab = cx.Conductor(category=cx.CC_AAAC, name="AAAC 740,8 MCM FLINT",
                           diameter=25.17, r25=0.089360, hcap=0.052744)
        cc = cx.CurrentCalc(cab)
        self.scc = cx.TcTimeCalc(cc, 25.0)
    
    def SetValue(self, prop, value):
        setattr(self.scc, prop, value)
    
    def test_values(self):
        # Varifica asignación de valores correcta
        self.scc.ta = 34.0
        self.assertEqual(self.scc.ta, 34.0)
        
        self.scc.timeStep = 0.5
        self.assertEqual(self.scc.timeStep, 0.5)
        
        self.scc.deltaIc = 0.02
        self.assertEqual(self.scc.deltaIc, 0.02)
        
    def test_errors(self):
        # Verifica que lanza error con valores fuera de rango
        self.assertRaises(AttributeError, self.SetValue, "currentcalc", 1)
        
        self.assertRaises(ValueError, self.SetValue, "ta", cx.TA_MIN-1)
        self.assertRaises(ValueError, self.SetValue, "ta", cx.TA_MAX+1)
        
        self.assertRaises(ValueError, self.SetValue, "timeStep", -0.1)
        self.assertRaises(ValueError, self.SetValue, "timeStep",  0.0)
        self.assertRaises(ValueError, self.SetValue, "timeStep",  61.0)
        
        self.assertRaises(ValueError, self.SetValue, "deltaIc", -0.1)
        self.assertRaises(ValueError, self.SetValue, "deltaIc",  0.0)

#-----------------------------------------------------------------------------------------

class TCMethods(unittest.TestCase):
    
    def setUp(self):
        cab = cx.Conductor(category=cx.CC_AAAC, name="AAAC 740,8 MCM FLINT",
                           diameter=25.17, r25=0.089360, hcap=0.052744)
        cc = cx.CurrentCalc(cab)
        self.scc = cx.TcTimeCalc(cc, 25.0)
        self.scc.timeStep = 7

    def test_getData(self):
        #def getTcTime(self, tcx, icfin, lapse, timex=0):
        # tcx
        self.assertRaises(ValueError, self.scc.getData, cx.TC_MIN-1, 500, 15*60)
        self.assertRaises(ValueError, self.scc.getData, cx.TC_MAX+1, 500, 15*60)
        # icfin
        self.assertRaises(ValueError, self.scc.getData, 50, -0.1, 15*60)
        self.assertRaises(ValueError, self.scc.getData, 50, self.scc.icmax + 1, 15*60)
        # lapse
        self.assertRaises(ValueError, self.scc.getData, 50, 500,  0.0)
        self.assertRaises(ValueError, self.scc.getData, 50, 500, -0.1) 

    def test_getIcini(self):
        # tcx
        self.assertRaises(ValueError, self.scc.getIcini, self.scc.ta, 2, 500)
        self.assertRaises(ValueError, self.scc.getIcini, cx.TC_MAX+1, 2, 500)
        # factor
        self.assertRaises(ValueError, self.scc.getIcini, 50,  0.0, 500)
        self.assertRaises(ValueError, self.scc.getIcini, 50, -0.1, 500)
        # lapse
        self.assertRaises(ValueError, self.scc.getIcini, 50, 2, -0.1)

    def test_getIcfin(self):
        # def getIcfin(self, tcx, icini, lapse, tcxini=None):
        # tcx
        self.assertRaises(ValueError, self.scc.getIcfin, self.scc.ta, 250, 500)
        self.assertRaises(ValueError, self.scc.getIcfin, cx.TC_MAX+1, 250, 500)
        # icini
        self.assertRaises(ValueError, self.scc.getIcfin, 50,  0.0, 500)
        self.assertRaises(ValueError, self.scc.getIcfin, 50, -0.1, 500)
        self.assertRaises(ValueError, self.scc.getIcfin, 50, self.scc.icmax + 1, 500)
        # lapse
        self.assertRaises(ValueError, self.scc.getIcfin, 50, 250, -0.1)
        # tcxini
        Tini = self.scc.getTc(250)
        # tcx > Tini creciente
        Tcx = Tini + 10
        self.assertRaises(ValueError, self.scc.getIcfin, Tcx, 250, 500, Tini - 1)
        self.assertRaises(ValueError, self.scc.getIcfin, Tcx, 250, 500, Tcx)
        # tcx > Tini creciente
        Tcx = Tini - 10
        self.assertRaises(ValueError, self.scc.getIcfin, Tcx, 250, 500, Tini + 1)
        self.assertRaises(ValueError, self.scc.getIcfin, Tcx, 250, 500, Tcx)
        
    def test_growing(self):
        Iini = 0.7*self.scc.getCurrent(50)
        Ifin = 2*Iini
        Tcini = self.scc.getTc(Iini)
        #Tcfin = self.scc.getTc(Ifin)
        lapse = 5*60
        
        curva1 = self.scc.getData(Tcini, Ifin, lapse, timex=0)
        Tcx = curva1.getTc(60*1)  # Tc luego de 1 minuto
        curva2 = self.scc.getData(Tcx, Ifin, lapse - 1*60, timex=1*60)
        
        self.assertEqual(curva1.growing, True)
        self.assertEqual(curva2.growing, True)
        
        # Verificamos que se puede partir en cualquier punto de la curva
        self.assertAlmostEqual(curva1.getTc(1.0*60), curva2.getTc(1.0*60), 1)
        self.assertAlmostEqual(curva1.getTc(1.5*60), curva2.getTc(1.5*60), 1)
        self.assertAlmostEqual(curva1.getTc(3.0*60), curva2.getTc(3.0*60), 1)
        
        # Verifica corriente inicial
        I = self.scc.getIcini(48, Ifin/Iini, curva1.getTime(48))
        self.assertAlmostEqual(I, Iini, 1)
        I = self.scc.getIcini(50, Ifin/Iini, curva1.getTime(50))
        self.assertAlmostEqual(I, Iini, 1)
        
        # Verifica corriente final
        I = self.scc.getIcfin(48, Iini, curva1.getTime(48), tcxini=None)
        self.assertAlmostEqual(I, Ifin, 1)
        lap = curva1.getTime(50) - curva1.getTime(45)
        I = self.scc.getIcfin(50, Iini, lap, tcxini=45)
        self.assertAlmostEqual(I, Ifin, 1)

    def test_notgrowing(self):
        Iini = self.scc.getCurrent(50)
        Ifin = 0.5*Iini
        Tcini = self.scc.getTc(Iini)
        #Tcfin = self.scc.getTc(Ifin)
        lapse = 5*60
        
        curva1 = self.scc.getData(Tcini, Ifin, lapse, timex=0)
        
        Tcx = curva1.getTc(60*1)  # Tc luego de 1 minuto
        curva2 = self.scc.getData(Tcx, Ifin, lapse - 1*60, timex=1*60)
        
        self.assertEqual(curva1.growing, False)
        self.assertEqual(curva2.growing, False)
        
        # Verificamos que se puede partir en cualquier punto de la curva
        self.assertAlmostEqual(curva1.getTc(1.0*60), curva2.getTc(1.0*60), 1)
        self.assertAlmostEqual(curva1.getTc(1.5*60), curva2.getTc(1.5*60), 1)
        self.assertAlmostEqual(curva1.getTc(3.0*60), curva2.getTc(3.0*60), 1)
        
        # Verifica corriente inicial
        I = self.scc.getIcini(48, Ifin/Iini, curva1.getTime(48)+0.0001)
        self.assertAlmostEqual(I, Iini, 0)
        I = self.scc.getIcini(50, Ifin/Iini, curva1.getTime(50)+0.0001)
        self.assertAlmostEqual(I, Iini, 0)
        
        # Verifica corriente final
        I = self.scc.getIcfin(48, Iini, curva1.getTime(48), tcxini=None)
        self.assertAlmostEqual(I, Ifin, 1)
        lap = curva1.getTime(45) - curva1.getTime(49)
        I = self.scc.getIcfin(45, Iini, lap, tcxini=49)
        self.assertAlmostEqual(I, Ifin, 1)

    def test_TcTimeData(self):
        data = [(0,0)]
        # Verifica que lanza error con len(data) < 2 
        self.assertRaises(ValueError, cx.TcTimeData, data)

#-----------------------------------------------------------------------------------------

s1 = unittest.TestLoader().loadTestsFromTestCase(TCConstructor)
s2 = unittest.TestLoader().loadTestsFromTestCase(TCProperties)
s3 = unittest.TestLoader().loadTestsFromTestCase(TCMethods)

suite = unittest.TestSuite([s1, s2, s3])

#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)