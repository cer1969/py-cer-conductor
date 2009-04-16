# -*- coding: utf-8 -*-
# CRISTIAN ECHEVERRÍA RABÍ 

from __future__ import division
import unittest

import currentcalc_test, tctimecalc_test, tensioncalc_test, operatingtable_test

#-----------------------------------------------------------------------------------------

slist = [currentcalc_test.suite,
         tctimecalc_test.suite, 
         tensioncalc_test.suite, 
         operatingtable_test.suite,
         ]

suite = unittest.TestSuite(slist)
unittest.TextTestRunner(verbosity=2).run(suite)