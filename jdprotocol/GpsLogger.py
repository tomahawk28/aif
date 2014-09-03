'''
Created on Aug 18, 2014

@author: bok61488
'''

import serial
from math import cos, sin, atan2, atan, pi, sqrt

class coordinate:
    def __init__(self,x,y,z):
        self.x, self.y, self.z = x, y, z
    
    def normalize(self):
        return map(lambda x: -x/sqrt(self.x**2+self.y**2+self.z**2),(self.x,self.y,self.z))
        
class GpsLogger:
    def __init__(self,port=13):
        
        self.ser = serial.Serial(port=port,baudrate=625000,stopbits=2,timeout=1)
        if not self.ser.isOpen():
            print "try Opening GPS Logger..."
            self.ser.open()
    
    def wrap(self,angle):
        if angle > pi:
            angle -= (2*pi)
        if angle < -pi:
            angle += (2*pi)
        if angle < 0:
            angle += (2*pi)
        return angle
    
    def get_compass(self):
        tilt, comp = None, None
        cmd = "$PAAG,MODE,READONE\r\n"
        self.ser.write(bytearray(cmd))
        
        while(tilt is None or comp is None):
            i = 2 if [tilt,comp].count(None) == 1 else 4
            while i:
                i=i-1 
                sample = self.ser.readline().split(',')
                
                if len(sample)<5 or 'A' not in sample[-1]:
                    break
                
                if 'T' in sample:
                    #print sample
                    tilt = coordinate(**dict(zip(('x','y','z'),map(float,sample[4:-1]))))
                elif 'C' in sample:
                    comp = coordinate(**dict(zip(('x','y','z'),map(float,sample[4:-1]))))
                elif '' in sample:
                    self.ser.write(bytearray(cmd))
                    
        #tilt-compensated
        
        phi = -atan( tilt.x / sqrt(tilt.y**2+tilt.z**2))
        theta = -atan( tilt.y / sqrt(tilt.x**2+tilt.z**2))
        
        comp.x, comp.y, comp.z = -comp.x, -comp.y, -comp.z
        
        variation = 16.528986*(pi/180) 
        
        Xh = comp.x*cos(theta) + comp.z*(theta)
        Yh = comp.x*sin(phi)*sin(theta) + comp.y * cos(phi) - comp.z * sin(phi) * sin(theta)
        
        return self.wrap((atan2(Yh, Xh))+variation)*180/pi 
        
    
        
    
    def close(self):
        self.ser.close()   
    
    
