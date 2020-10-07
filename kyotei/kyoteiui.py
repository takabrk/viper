#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys,os,os.path
try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    sys.exit(1)
class kyoteiui(object):
    def __init__(self):
        gladefile = "kyotei.ui"
        self.wTree = Gtk.Builder()
        #self.wTree.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + gladefile)
        self.wTree.add_from_file(gladefile)
        dic = {
            "on_button1_clicked" : self.on_button1_clicked,
            "on_button2_clicked" : self.on_button2_clicked
        }
        self.wTree.connect_signals(dic)
        self.window = self.wTree.get_object("button1")
        self.window = self.wTree.get_object("button2")
        self.window = self.wTree.get_object("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
    def on_button1_clicked(self,widget):
        self.entry1 = self.wTree.get_object("entry1")
        self.entry2 = self.wTree.get_object("entry2")
        self.entry3 = self.wTree.get_object("entry3")
        self.entry4 = self.wTree.get_object("entry4")
        self.entry5 = self.wTree.get_object("entry5")
        self.entry6 = self.wTree.get_object("entry6")
        self.msg1 = self.entry1.get_text()
        self.msg2 = self.entry2.get_text()
        self.msg3 = self.entry3.get_text()
        self.msg4 = self.entry4.get_text()
        self.msg5 = self.entry5.get_text()
        self.msg6 = self.entry6.get_text()
        self.msg = self.msg1+" "+self.msg2+" "+self.msg3+" "+self.msg4+" "+self.msg5+" "+self.msg6
        print(self.msg)
        os.system("python2 kyotei.py "+self.msg)
        print("Finished")
    def on_button2_clicked(self,widget):
         Gtk.main_quit()
if __name__ == "__main__":
    kyoteiui()
    Gtk.main()
