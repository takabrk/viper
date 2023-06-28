#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
viper_for jsay.py
Copyright@ takamitsu hamada
version :  20200805
License      :  BSD License
Web site URL :  http://vsrx.work
"""
import math,re,glob,string,os,time,sys
import subprocess as sp

argvs = sys.argv
argvcount = len(argvs)
homedir = os.environ['HOME']+"/viper_text_reading/file/"
#viper Class
class viper_for_jsay(object):
    def __init__(self):
        pass
    def installExtraApplications(self):
        ba = ["open-jtalk","mecab","mecab-utils","mecab-naist-jdic","mecab-naist-jdic-eucjp","mecab-jumandic","python-mecab"]
        for i in ba:
            sp.call("sudo apt-get install -y %s" % (i),shell=True)

#jsay
    def talk(self,text,voice):
        if(voice == "mei_happy"):
            modelv = homedir+"mei/mei_happy.htsvoice"
        if(voice == "mei_angry"):
            modelv = homedir+"mei/mei_angry.htsvoice"
        if(voice == "mei_bashful"):
            modelv = homedir+"mei/mei_bashful.htsvoice"
        if(voice == "mei_normal"):
            modelv = homedir+"mei/mei_normal.htsvoice"
        if(voice == "mei_sad"):
            modelv = homedir+"mei/mei_sad.htsvoice"
        if(voice == "miku_a"):
            modelv = homedir+"miku/TYPE-α.htsvoice"
        if(voice == "miku_b"):
            modelv = homedir+"miku/TYPE-β.htsvoice"
        if(voice == "tohoku_angry"):
            modelv = homedir+"tohoku/tohoku-f01-angry.htsvoice"
        if(voice == "tohoku_happy"):
            modelv = homedir+"tohoku/tohoku-f01-happy.htsvoice"
        if(voice == "tohoku_neutral"):
            modelv = homedir+"tohoku/tohoku-f01-neutral.htsvoice"
        if(voice == "tohoku_sad"):
            modelv = homedir+"tohoku/tohoku-f01-sad.htsvoice"
        sp.call("""TMP=/tmp/jsay.wav
echo %s | open_jtalk \
-x "/var/lib/mecab/dic/open-jtalk/naist-jdic" \
-m %s \
-ow $TMP && \
aplay --quiet $TMP
rm -f $TMP""" % (text,modelv),shell=True)

if __name__ == "__main__":
    v = viper_for_jsay()
    try:
        if argvs[1] == "jsay":
            v.talk(argvs[2],argvs[3])
    except:pass
