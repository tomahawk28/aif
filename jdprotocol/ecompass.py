'''
Created on Aug 18, 2014

@author: bok61488
'''

import serial
from math import cos, sin, atan2, atan, pi, sqrt
        
class ecompass:
    def __init__(self,port=3):
        
        self.ser = serial.Serial(port=port,baudrate=115200,stopbits=2,timeout=3)
        if not self.ser.isOpen():
            print "try Opening eCompass..."
            self.ser.open()
    
    def wrap(self,angle):
        if angle > pi:
            angle -= (2*pi)
        if angle < -pi:
            angle += (2*pi)
        if angle < 0:
            angle += (2*pi)
        return angle
    
    def _get_compass(self):
        
        while True:
            self.ser.write([0x7f,0x46,0x02,0x00,0x00,0x7e])
        
            ret = list(self.ser.read(12))
        
            if(len(ret)!=12):
                #print 'Error: response length is ', len(ret)
                continue
            
            ret = map(lambda x: hex(ord(x))[2:], ret[4:-2])
            ret = [ret[i]+ret[i+1] for i in range(0,len(ret),2)]
            ret = map(lambda x: self.twos_comp(int(x,16), 16), ret)
            
            return self.wrap(-atan2(ret[1], ret[0]))*180/pi
            
    
    def get_compass(self):
        l=[]
        i=0
        while i<10: 
            i=i+1
            l+=[self._get_compass()]
        return sum(l)/len(l)
    
    def switch_antenna(self, antenna_num):
        self.ser.write([0x7f,0x46,0x01,antenna_num,0x7e])
        
    def twos_comp(self, val, bits):
        """compute the 2's compliment of int value val"""
        if( (val&(1<<(bits-1))) != 0 ):
            val = val - (1<<bits)
        return val

    
    def close(self):
        self.ser.close()   
    
    
