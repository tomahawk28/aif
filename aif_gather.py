'''
Created on Jul 18, 2014

@author: ji-hyuk.bok@jdsu.com

'''

import threading
import time
from Queue import Queue
from jdprotocol.CellAdvisor import CellAdvisor
from jdprotocol.GpsLogger import GpsLogger

def run_celladvisor_async(cell_advisor, q):
    ret = cell_advisor.get_interference_power()
    q.put(ret)

if __name__ == "__main__":

    s1, s2 = CellAdvisor(ip="10.82.26.231",name="omni") , CellAdvisor(ip="10.82.26.64",name="yagi")
    
    gps = GpsLogger()
    
    cell_advisor_list = [s1,s2]
    
    count=3000
    f = open("sample.csv", "w")
    f.write("compass,omni,yagi\n")
    
    before = time.time()
    q = Queue()
    
    while count>0: 
        count -= 1
        print "count: " , count, '\n'
        
        omni_power, yagi_power = 0.0, 0.0
        
        #process_list = [threading.Thread(target=s.send_cmd, args=()) for s in socket_list ]
        
        thread_list = [threading.Thread(target=run_celladvisor_async, args=(cell_advisor,q)) for cell_advisor in cell_advisor_list ]
        
        compass = gps.get_compass()
        print "compass degree:", compass
        
        for thread in thread_list:
            thread.start()
        
        for s in cell_advisor_list:
            ret =  q.get(timeout=2)
            #print ret
            if ret["name"] == "omni":
                omni_power = ret["power"]
            else:
                yagi_power = ret["power"]
        
        f.write("{},{},{}\n".format(compass,omni_power,yagi_power))
        
     
    for cell_advisor in cell_advisor_list:
        cell_advisor.close()
    
    gps.close()
    end = time.time()
    
    print "elapsed: " , end - before , "seconds"
    f.close() 
        