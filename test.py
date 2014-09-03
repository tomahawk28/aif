'''
Created on Aug 25, 2014

@author: bok61488
'''
#import Image

from jdprotocol.CellAdvisor import CellAdvisor
from ctypes import *

""" filename: 50 char
    date: 30 char
    size: unsigned int
"""
class FileList(Structure):
    _fields_ = [('filename', c_char*50),
                ('date', c_char*20),
                ('size', c_uint)]


s = CellAdvisor(ip="10.82.26.64",name="omni")

ret = s.send_cmd(0x02, "1")

#print type(ret) , ret

#print ret
print list(ret[79:84])

f = FileList(filename=ret[:50],date=ret[50:71],size=ret[70:74])

#print f.filename, f.date, f.size
#print ret[50]

#print ret.count("\xff\xdb")

#db_index = [i for i, v in enumerate(ret) if v=="\xdb"]

#for index in db_index:
#    if ret[index-5] == "\xff":
#        print "got it", ret[index-6:index+25]
#        ret.count("\xff\x00\xfcE1f")
#print len(ret)

#ret = re.sub("\xff.+\xdb","\xff\xdb",ret)



#print len(ret)




