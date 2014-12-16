'''
Created on Aug 21, 2014

@author: bok61488
'''
import logging
import sys
import unittest

from jdprotocol.CellAdvisor import CellAdvisor


class Test(unittest.TestCase):

    
    def setUp(self):
        self.s = CellAdvisor(ip="10.82.26.12",name="omni")


    def tearDown(self):
        self.s.close()


    def test_get_interference_power(self):
        ret = self.s.get_interference_power()
        self.assertTrue("name" in ret)
        self.assertEqual(ret["name"], "omni", "the given name to advisor should be same exist in a result packet")
        self.assertTrue("power" in ret)
        self.assertTrue(type(ret["power"])  is float)
    
    def test_send_cmd(self):
        with open("screen2.jpg", "wb") as f:
            ret = self.s.send_cmd(0x60)
            f.write(ret)
            
        
        self.assertIs(list(ret), "")
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "celladvisor_test" ).setLevel( logging.DEBUG )
    unittest.main()