#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os,sys

list = [
(4019,3854,3959,4311,4278,4471)
]
try:
#File writing
    f2 = open("kyotei.txt","w")
    f2.write("◇予想\n")
    fw = ""
    for i in list:
        os.system("python kyotei.py %d %d %d %d %d %d" % (i[0],i[1],i[2],i[3],i[4],i[5]))
    f2.write(fw+"\n")
    f2.close()
except:pass
