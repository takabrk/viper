#!/usr/bin/env python
#-*-coding:utf-8 -*-
#start_jack_pulse.py @takamitsu hamada 20190710
#mainsite : http://vsrx.site

import sys,os,os.path,json
from urllib.request import urlopen
import subprocess as sp
import codecs
try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    sys.exit(1)

class start_jack_pulse(object):
    def __init__(self):
        gladefile = "start_jack_pulse.ui"
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
        self.checkbutton1 = treeObj("checkbutton1")
        self.checkbutton2 = treeObj("checkbutton2")
        self.checkbutton3 = treeObj("checkbutton3")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
    def on_button1_clicked(self,widget):
        if self.checkbutton1.get_active() == True:
            sp.call("./start_jack_pulse.sh on".strip().split(" "))
            print("Start PulseAudio+Jack Connection Kit.")
        if self.checkbutton2.get_active() == True:
            sp.call("./start_jack_pulse.sh off".strip().split(" "))
            print(" PulseAudio Mode.")
    def on_button2_clicked(self,widget):
        Gtk.main_quit()

if __name__ == "__main__":
    start_jack_pulse()
