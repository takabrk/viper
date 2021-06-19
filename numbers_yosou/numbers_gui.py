#!/usr/bin/env python
#-*-coding:utf-8 -*-
#numbers_gui.py @takamitsu hamada 20190801
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

class numbers_gui(object):
    def __init__(self):
        gladefile = "numbers.ui"
        self.tree = Gtk.Builder()
        self.tree.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + gladefile)
        dic = {
            "on_button1_clicked" : self.on_button1_clicked,
            "on_button2_clicked" : self.on_button2_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.window = treeObj("button1")
        self.window = treeObj("button2")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
    def on_button1_clicked(self,widget):
        #Thread(target=lambda : sp.call("python viper.py jsay ナンバーズの予想を行います。 mei_happy string".strip().split(" "))).start()
        Thread(target=lambda : sp.call("python2 numbers.py",shell=True)).start()
    def on_button2_clicked(self,widget):
        Gtk.main_quit()
if __name__ == "__main__":
    numbers_gui()
