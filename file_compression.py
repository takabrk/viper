#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os,sys,os.path
import subprocess as sp
try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    sys.exit(1)
class file_compression(object):
    def __init__(self):
        gladefile = "file_compression.ui"
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
        self.combo1 = treeObj("comboboxtext1")
        self.entry1 = treeObj("entry1")
        self.entry2 = treeObj("entry2")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
    def on_button1_clicked(self,widget):
        msg1 = self.entry1.get_text()
        msg2 = self.entry2.get_text()
        if(self.combo1.get_active_text() == "zip"):
            sp.call("zip -r %s %s" % (msg2,msg1),shell=True)
        if(self.combo1.get_active_text() == "7zip"):
            sp.call("7z a %s %s" % (msg2,msg1))
        if(self.combo1.get_active_text() == "tar.gz"):
            sp.call("tar czvf %s %s" % (msg2,msg1))
    def on_button2_clicked(self,widget):
        Gtk.main_quit()
if __name__ == "__main__":
    file_compression()
    Gtk.main()
