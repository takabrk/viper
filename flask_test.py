#!/usr/bin/env python
#-*- coding:utf-8 -*-
from flask import Flask,render_template
app=Flask(__name__)

@app.route('/')
def index():
    return render_template("indexold.html",message="カレンさん")

if __name__ == "__main__":
    app.run(port=8000,debug=True)