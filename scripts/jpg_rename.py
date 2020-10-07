#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import glob,os,sys
argvs = sys.argv
os.chdir(argvs[1])
files = glob.glob("*.jpg")
for i,old_name in enumerate(files):
    new_name = argvs[1] + "{0:03d}.jpg".format(i+1)
    os.rename(old_name,new_name)
    print(old_name+"→"+new_name)
