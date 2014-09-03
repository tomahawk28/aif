'''
Created on Aug 22, 2014

@author: bok61488
'''
from jdprotocol.GpsLogger import GpsLogger

if __name__ == '__main__':
    
    gps = GpsLogger()
    i = 1000
    
    prev = gps.get_compass()
    curr = 0.0
    while i:
        print "i : {0} , compass: {1}".format(i, prev)
        i=i-1
        curr = gps.get_compass()
        diff = prev - curr
        if abs(diff) > 2.0:
            print diff, "\tToo much diff!" 
        prev = curr