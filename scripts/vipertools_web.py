#!/usr/bin/env python
#-*- coding:utf-8 -*-
from flask import Flask,render_template,request
app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def form():
    if request.method == 'POST':
        osms = request.form.getlist("osms")
        print("osms:",osms)
        return render_template('index.html')
    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(port=8000,debug=True)