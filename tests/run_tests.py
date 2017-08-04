import unittest
import glob
import  os
import sys
BASE = '/'.join(os.path.realpath(__file__).split('/')[:-2])
sys.path.insert(0, BASE)

def create_testsuite(searchname):
    testfiles = glob.glob(searchname, recursive=True)
    tests = [stri[:-3] for stri in testfiles]
    #print(tests)
    suites = [unittest.defaultTestLoader.loadTestsFromName(name) for name in tests]
    testSuite = unittest.TestSuite(suites)
    return testSuite

print(os.getcwd())
#os.chdir(BASE)
#print(os.getcwd())

#testSuite = create_testsuite("test_*.py")
testSuite = create_testsuite("**/test_*.py")
#text_runner = unittest.TextTestRunner().run(testSuite)
testSuite = unittest.defaultTestLoader.discover("plugins/","test_*.py")

text_runner = unittest.TextTestRunner().run(testSuite)
