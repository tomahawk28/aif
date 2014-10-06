'''
Created on Aug 25, 2014

@author: bok61488
'''

import sys
from time import sleep

from jdprotocol.CellAdvisor import CellAdvisor
from jdprotocol.ecompass import ecompass


ecompass = ecompass(port=3)

#omni = CellAdvisor(ip="192.168.0.102",name="omni")
yagi = CellAdvisor(ip="192.168.0.102",name="yagi")

"""
Testing log
"""
f = open("yagi_roof_highangle.csv", "w")
f.write("compass,yagi_1,yagi_2,yagi_3,yagi_4,yagi_5,yagi_6\n")

"""
Initialize members
"""
compass = 0.0
yagi_power_table = [0.0]*6


"""
Process 
"""
while compass < 360.0:
    
    print "\nCurrent compass: {}".format(compass)
    print "Keep going?:"
    sys.stdin.readline()
    
    #omni_power = omni.get_interference_power()["power"]
    for i in range(6):
        ecompass.switch_antenna(i)
        sleep(0.3)
        yagi_power_table[i]= yagi.get_interference_power()["power"]
    
    
    #print ecompass._get_compass()
    #print omni_power
    print yagi_power_table
    csv_format = ",".join(["{}"]*7) + "\n"
    f.write( csv_format.format(compass,*yagi_power_table))
    
    #-- Add 5.0 degree to compass for rotation
    compass += 5.0
    
    
    
print "All Done!"
f.close()







