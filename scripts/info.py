#!/usr/bin/env python
#-*- coding:utf-8 -*-
#info.py
#This script created by takamitsu hamada

import subprocess as sp
import tkinter.messagebox as msb

def information():
    cmd1 = "cat /etc/lsb-release | grep 'DISTRIB_DESCRIPTION'"
    cmd2 = "cat /proc/version"
    cmd3 = "dmesg | grep scheduler"
    #cmd4 = "cat /proc/cpuinfo | grep 'model name' | tail -n 1"
    #cmd5 = "cat /proc/meminfo | grep MemTotal"
    #cmd6 = "dmesg | grep -i PDS"
    #cmd7 = "dmesg | grep -i MuQSS"
    #cmd8 = 'dmesg | grep -i "cacule cpu"'

    ret1 = sp.check_output(cmd1,shell=True)
    ret2 = sp.check_output(cmd2.split(" "))
    ret3 = sp.check_output(cmd3,shell=True)
    #ret4 = sp.check_output(cmd4,shell=True)
    #ret5 = sp.check_output(cmd5,shell=True)
    #ret6 = sp.check_output(cmd6,shell=True)
    msb.showinfo("About UBOLD-OP",ret1+ ret2 + ret3)
if __name__ == "__main__":
    information()
