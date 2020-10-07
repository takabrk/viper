#!/usr/bin/env python
#-*- coding:utf-8 -*-

import http.server as m
http.server.test(HandlerClass=m.CGIHTTPRequestHandler)
