#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
PVL Web UI
Copyright@ takamitu hamada
version :  20200430
License      :  BSD License
Web site URL :  http://vsrx.work
"""

import cgi
import subprocess as sp
f=cgi.FieldStorage()
if f.getvalue("printer"):
    sp.call('chromium-browser --disk-cache-dir="/tmp" --app="http://localhost:631/"',shell="True")
if f.getvalue("ssb"):
    sp.call('chromium-browser --disk-cache-dir="/tmp" --app="http://localhost:8000/ssb.html?date=20180822f"',shell="True")

