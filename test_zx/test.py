# CRISTIAN ECHEVERRÍA RABÍ 

import unittest

import currentcalc_test, operatingtable_test #tctimecalc_test, tensioncalc_test

#-----------------------------------------------------------------------------------------

slist = [currentcalc_test.suite,
         operatingtable_test.suite,
         #tctimecalc_test.suite, 
         #tensioncalc_test.suite, 
         ]

suite = unittest.TestSuite(slist)
unittest.TextTestRunner(verbosity=2).run(suite)