#!/usr/bin/env python3
#-*-coding:utf-8 -*-
#downloader.py @takamitsu hamada 20201026
#mainsite : http://vsrx.site

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
            "on_button1_clicked" : self.on_button1_clicked,
            "on_button2_clicked" : self.on_button2_clicked,
            "on_button3_clicked" : self.on_button3_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.entry1 = treeObj("entry1")
        self.entry2 = treeObj("entry2")
        self.entry3 = treeObj("entry3")
        self.window = treeObj("button1")
        self.window = treeObj("button2")
        self.window = treeObj("button3")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
    def on_button1_clicked(self,widget):
        msg1 = self.entry1.get_text()
        cmd = "./downloader.sh %s" % (msg1)
        sp.call(cmd.strip().split(" "))
    def on_button2_clicked(self,widget):
        Gtk.main_quit()
    def on_button3_clicked(self,widget):
        msg1=self.entry2.get_text()
        msg2=self.entry3.get_text()
        cmd = "./download_hls.sh %s %s" % (msg1,msg2)
        sp.call(cmd.strip().split(" "))
if __name__ == "__main__":
    download_youtube()
