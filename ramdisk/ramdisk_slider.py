#!/usr/bin/env python
#-*- coding:utf-8 -*-
#ramdisk_slider.py @takamitu hamada 20170107
import os,os.path,sys
import subprocess as sp
try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    sys.exit(1)

class ramdisk_slider(object):
    def __init__(self):
        gladefile = "ramdisk_slider.ui"
        self.tree = Gtk.Builder()
        self.tree.add_from_file(gladefile)
        dic = {
            "on_button1_clicked" : self.on_button1_clicked,
            "on_button2_clicked" : self.on_button2_clicked,
            "on_button3_clicked" : self.on_button3_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.window = treeObj("button1")
        self.window = treeObj("button2")
        self.window = treeObj("button3")
        self.combo1 = treeObj("comboboxtext1")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
#strage button
    def on_button1_clicked(self,widget):
        sp.call("sudo reboot".strip().split(" "))
#Cancel button
    def on_button2_clicked(self,widget):
        Gtk.main_quit()
#Settings Button
    def on_button3_clicked(self,widget):
        if(self.combo1.get_active_text() == "200MB"):
             msg = "200M"
        if(self.combo1.get_active_text() == "500MB"):
            msg = "500M"
        if(self.combo1.get_active_text() == "1GB"):
            msg = "1GB"
        if(self.combo1.get_active_text() == "1.5GB"):
            msg = "1.5GB"
        if(self.combo1.get_active_text() == "2GB"):
            msg = "2GB"
        if(self.combo1.get_active_text()  == "3GB"):
            msg = "3GB"
        if(self.combo1.get_active_text() == "4GB"):
            msg = "4GB"
        if(self.combo1.get_active_text() == "8GB"):
            msg = "8GB"
        f0 = open("/etc/rc.local","w")
        f0.write("""#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

mount -t tmpfs -w -o size=%s tmpfs /tmp
exit 0
            """ % (msg))
        f0.close()
        print("Finished")
if __name__ == "__main__":
    ramdisk_slider()
    Gtk.main()
