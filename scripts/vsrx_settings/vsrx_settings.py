#!/usr/bin/env python
#-*-coding:utf-8 -*-
#vipertools.py @takamitu hamada 20200430
import sys,os,os.path,json
import subprocess as sp
from threading import Thread
import codecs

try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    sys.exit(1)

class valkyrie_setting(object):
    def __init__(self):
        gladefile = "vsrx_settings.ui"
        self.tree = Gtk.Builder()
        self.tree.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + gladefile)
        dic = {
            "on_button11_clicked" : self.on_button11_clicked,
            "on_button12_clicked" : self.on_button12_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.window = treeObj("button11")
        self.window = treeObj("button12")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
    def on_button11_clicked(self,widget):
        Thread(target=lambda : sp.call('chromium-browser --disk-cache-dir="/tmp" --app="http://localhost:8000/ssb.html?date=20180822f"',shell="True")).start()
#Cancel button
    def on_button12_clicked(self,widget):
        Gtk.main_quit()

if __name__ == "__main__":
    Thread(target=lambda : sp.call(valkyrie_setting(),shell="True")).start()
    Thread(target=lambda : sp.call("./start_server &",shell="True")).start()
