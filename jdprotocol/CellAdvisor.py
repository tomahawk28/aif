'''
Created on Aug 18, 2014

@author: bok61488
'''

import socket
import xml.etree.ElementTree as ET

class CellAdvisor:
    def __init__(self, ip,name):
        self.ip = ip
        self.name = name
        self.socket= \
            socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(3)    
        self.socket.connect((ip,66))
        
    def close(self):
        self.socket.close()

        
    def send_cmd(self, cmd, data=None):
        
        carry=""
        over=False
    
        # Send Trace data request
        if not data:
            self.socket.send(bytearray([0x7F, 'C', cmd, 0x1, 0x1 , 0x70 , 0x7E]))
        else:
            self.socket.send(bytearray([0x7F, 'C', cmd, 0x1, 0x1] + list(data) + [0x70 , 0x7E]))
            
        while not over:
            data = ''
            while len(data)==0:
                data = self.socket.recv(4000)
                
            carry += data
                
            if carry[-1] == '~':
                # get index of last packet starting point
                i=-carry[::-1].index(chr(0x7f))-1
                t=map(ord, list(carry[i+3:i+5]))
                if t[0] <= t[1]+1:
                    over=True
                    break
        
        carry = ''.join([x[5:-1] if x[-2] != '}' else x[5:-2] for x in carry.split('~') if len(x)>0])
        
        #print carry
        
        ret=""
        xor_need=False
        for i in carry:
            if i == '}':
                xor_need = True
            else:
                if not xor_need:
                    ret += i 
                else: 
                    ret += chr(ord(i)^0x20)
                xor_need = False
            #ret+=i
                
        return ret
    
    def get_interference_power(self):
        ret = self.send_cmd(0x83)
        trace_data = ET.fromstring(ret).find('TraceData')
        power_list = [float(trace_data.get('P'+str(x))) for x in range(200,300)]
        max_power = max(power_list)
        #power =  float(ET.fromstring(ret).find('TraceData').get('P251'))
        if max_power not in power_list:
            max_power *= -1.0 
        return {'power': max_power, 'name':self.name}

    def get_sample(self):
        ret = self.send_cmd(0x01)
        return {'power': ret, 'name':self.name}