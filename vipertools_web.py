#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys,os,os.path,json
import subprocess as sp
from threading import Thread
import codecs
from flask import Flask,render_template,request
app=Flask(__name__)
runner=app.test_cli_runner()
@app.route('/',methods=['GET','POST'])
def form():
    if request.method == 'POST':
        if request.form.get("submit"):
            osms = request.form.getlist("osms")
            print("osms:",osms)
            msg1 = osms[0]
            msg2 = osms[1]
            msg3 = osms[2]
            msg4 = osms[3]
            msg5 = osms[4]
            msg6 = osms[5]
            #msg7 = osms[6]
            f1 = open("vsrx_builder/configs/DIST","w")
            f1.write(msg1)
            f1.close()
            f2 = open("vsrx_builder/configs/VERSION","w")
            f2.write(msg2)
            f2.close()
            f3 = open("vsrx_builder/configs/CODENAME","w")
            f3.write(msg3)
            f3.close()
            f4 = open("vsrx_builder/configs/DESCRIPTION","w")
            f4.write(msg4)
            f4.close()
            f5 = open("vsrx_builder/configs/RELEASENOTES","w")
            f5.write(msg5)
            f5.close()
            f6 = open("vsrx_builder/configs/EXTENDED","w")
            f6.write(msg6)
            f6.close()
            #f7 = open("vsrx_builder/configs/ISOFILE","w")
            #f7.write(msg7)
            #f7.close()
            sp.run("""sudo mkdir /home/ubuntu-builder
            sudo cp -a vsrx_builder/configs /home/ubuntu-builder
        """,shell=True)
        if request.form.get("console"):
            #Thread(target=lambda : sp.run("sudo vsrx_builder/extras/Console",shell=True))
            runner.invoke(sp.run("sudo vsrx_builder/extras/Console",shell=True))
        if request.form.get("synaptic"):
            runner.invoke(sp.run("sudo vsrx_builder/extras/Synaptic",shell=True))
        if request.form.get("extract"):
            runner.invoke(os.chdir("vsrx_builder"))
            runner.invoke(sp.run("sudo extras/Extract",shell=True))
            runner.invoke(os.chdir("../"))
        if request.form.get("build"):
            runner.invoke(sp.run("sudo vsrx_builder/extras/Build",shell=True))        
        return render_template('index.html')
    else:
        return render_template('index.html')
if __name__ == "__main__":
    Thread(target=lambda : app.run(port=8000,debug=False)).start()