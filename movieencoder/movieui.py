#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os,os.path,sys
import subprocess as sp

try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    sys.exit(1)
class movieui(object):
    def __init__(self):
        gladefile = "movieui.ui"
        self.tree = Gtk.Builder()
        #self.wTree.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + gladefile)
        self.tree.add_from_file(gladefile)
        dic = {
            "on_button1_clicked" : self.on_button1_clicked,
            "on_button2_clicked" : self.on_button2_clicked,
            "on_install_driver_clicked" : self.on_install_driver_clicked, 
            "on_filechooserbutton1_file_set" : self.on_filechooserbutton1_file_set
        }
        self.tree.connect_signals(dic)
        treeObj = self.tree.get_object
        self.window = treeObj("button1")
        self.window = treeObj("button2")
        self.window = treeObj("install_driver")
        self.fcb1 = treeObj("filechooserbutton1")
        self.combo1 = treeObj("comboboxtext1")
        self.combo2 = treeObj("comboboxtext2")
        self.combo3 = treeObj("comboboxtext3")
        self.entry2 = treeObj("entry2")
        self.entry3 = treeObj("entry3")
        self.entry4 = treeObj("entry4")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
    def on_button1_clicked(self,widget):
        msg1 = self.on_filechooserbutton1_file_set(widget)
        msg2 = self.entry2.get_text()
        if(self.combo1.get_active_text() == "640x480"):
            msg3 = 640
            msg4 = 480
        if(self.combo1.get_active_text() == "768x432"):
            msg3 = 768
            msg4 = 432
        if(self.combo1.get_active_text() == "1024x720"):
            msg3 = 1024
            msg4 = 720
        if(self.combo1.get_active_text() == "1280x720"):
            msg3 = 1280
            msg4 = 720
        if(self.combo1.get_active_text() == "1920x1080"):
            msg3 = 1920
            msg4 = 1080
        if(self.combo2.get_active_text() == "h264_vaapi"):
            msg5 = "h264_vaapi"
        if(self.combo2.get_active_text() == "hevc_vaapi"):
            msg5 = "hevc_vaapi"
        if(self.combo3.get_active_text() == "card0"):
            msg6 = "card0"
        if(self.combo3.get_active_text() == "card1"):
            msg6 = "card1"
        if(self.combo3.get_active_text() == "renderD128"):
            msg6 = "renderD128"
        if(self.combo3.get_active_text() == "renderD129"):
            msg6 = "renderD129"
        cmd = "./qsv_enc.sh %s %s %s %s %s %s" % (msg1,msg2,msg3,msg4,msg5,msg6)
        print(cmd)
        sp.call(cmd.strip().split(" "))
    def on_button2_clicked(self,widget):
        Gtk.main_quit()
    def on_filechooserbutton1_file_set(self,widget):
        msg1 = self.fcb1.get_filename()
        return msg1
    def on_install_driver_clicked(self,widget):
        cmd = "./build_media_driver.sh"
        sp.call(cmd.strip().split(" "))
        
if __name__ == "__main__":
    movieui()
    Gtk.main()

