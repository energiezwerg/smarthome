#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016 Christian Strassburg  c.strassburg@gmx.de
#########################################################################
# Personal and non-commercial use only, redistribution is prohibited.
#########################################################################

import unittest
import lib.test_utils
class SmartHomeTestSuite(unittest.TestCase):

    def test_all(self):           
        testSuite = unittest.TestSuite()
        testResult = unittest.TestResult()
        confTest = LibUtilsTest()
        testSuite.addTest(configtest.suite())
        test = testSuite.run(testResult)
        print (testResult.testsRun) # prints 1 if run "normally"






if __name__ == '__main__':
    unittest.main(verbosity=2)


