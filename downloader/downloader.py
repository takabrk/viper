#!/usr/bin/env python3
#-*-coding:utf-8 -*-
#downloader.py @takamitsu hamada 20210604
#mainsite : http://vsrx.work

import sys,os,os.path,json
from urllib.request import urlopen
import subprocess as sp
from threading import Thread
import codecs
try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    sys.exit(1)

class download_youtube(object):
    def __init__(self):
        gladefile = "downloader.ui"
        self.tree = Gtk.Builder()
        self.tree.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + gladefile)
        dic = {
            "on_ok1_clicked" : self.on_ok1_clicked,
            "on_ok2_clicked" : self.on_ok2_clicked,
            "on_close_clicked" : self.on_close_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.downloader = treeObj("downloader")
        self.hls_url = treeObj("hls_url")
        self.output = treeObj("output")
        self.window = treeObj("ok1")
        self.window = treeObj("ok2")
        self.window = treeObj("close")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
    def on_ok1_clicked(self,widget):
        msg1 = self.downloader.get_text()
        cmd = "./downloader.sh %s" % (msg1)
        sp.call(cmd.strip().split(" "))
    def on_ok2_clicked(self,widget):
        msg1=self.hls_url.get_text()
        msg2=self.output.get_text()
        cmd = "./download_hls.sh %s %s" % (msg1,msg2)
        sp.call(cmd.strip().split(" "))
    def on_close_clicked(self,widget):
        Gtk.main_quit()
if __name__ == "__main__":
    download_youtube()
