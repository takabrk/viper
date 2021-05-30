#!/usr/bin/env python
#-*-coding:utf-8 -*-
#apng_asvg.py @takamitsu hamada 20190704
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

class apng_asvg(object):
    def __init__(self):
        gladefile = "apng_asvg.ui"
        self.tree = Gtk.Builder()
        self.tree.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + gladefile)
        dic = {
            "on_button22_clicked" : self.on_button22_clicked,
            "on_button26_clicked" : self.on_button26_clicked,
            "on_button30_clicked" : self.on_button30_clicked,
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.window = treeObj("button22")
        self.window = treeObj("button26")
        self.window = treeObj("button30")
        self.entry8 = treeObj("entry8")
        self.entry10 = treeObj("entry10")
        self.entry11 = treeObj("entry11")
        self.entry12 = treeObj("entry12")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
#APNG button
    def on_button22_clicked(self,widget):
        msg1 = self.entry8.get_text()
        msg3 = self.entry10.get_text()
        msg4 = self.entry11.get_text()
        msg7 = self.entry12.get_text()
        cmdas = "python viper.py apng %s %s %s %s" % (msg1,msg3,msg4,msg7)
        sp.call(cmdas.strip().split(" "))
        print("Finished")        
#animationSVG button
    def on_button26_clicked(self,widget):
        msg1 = self.entry8.get_text()
        msg3 = self.entry10.get_text()
        msg4 = self.entry11.get_text()
        msg7 = self.entry12.get_text()
        cmdp2j = "python viper.py png2jpg %s %s2jpg %s %s 100" % (msg1,msg1,msg3,msg4)
        sp.call(cmdp2j.strip().split(" "))

        cmdas = "python viper.py asvg %s2jpg %s %s %s" % (msg1,msg3,msg4,msg7)
        sp.call(cmdas.strip().split(" "))
        print("Finished")
#Cancel button
    def on_button30_clicked(self,widget):
        Gtk.main_quit()
if __name__ == "__main__":
    apng_asvg()
