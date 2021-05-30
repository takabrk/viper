#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import print_function
import time
from flask import Flask,request
app = Flask(__name__)
@app.route("/",methods=['POST'])

def post():
    #msg1 = request.form.get('name_distro_input')
    #f1 = open('vsrx_builder/configs/DIST','w')
    #f1.write(msg1)
    #f1.close()
    pass

if __name__ == "__main__":
    app.run(host="localhost",port=5000)