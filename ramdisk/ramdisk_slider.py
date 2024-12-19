#!/usr/bin/env python
#-*- coding:utf-8 -*-
#ramdisk_slider.py @takamitu hamada
#December 19,2024

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
            "on_button_rds_settings_clicked" : self.on_button_rds_settings_clicked,
            "on_button_rds_reboot_clicked" : self.on_button_rds_reboot_clicked,
            "on_button_rds_cancel_clicked" : self.on_button_rds_cancel_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.window = treeObj("button_rds_settings")
        self.window = treeObj("button_rds_reboot")
        self.window = treeObj("button_rds_cancel")
        self.combo1 = treeObj("comboboxtext_rds")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
#reboot button
    def on_button_rds_reboot_clicked(self,widget):
        sp.call("sudo reboot".strip().split(" "))
#Cancel button
    def on_button_rds_cancel_clicked(self,widget):
        Gtk.main_quit()
#Settings Button
    def on_button_rds_settings_clicked(self,widget):
        if(self.combo1.get_active_text() == "256MB"):
             msg = "256M"
        if(self.combo1.get_active_text() == "512MB"):
            msg = "512M"
        if(self.combo1.get_active_text() == "1GB"):
            msg = "1GB"
        if(self.combo1.get_active_text() == "2GB"):
            msg = "2GB"
        if(self.combo1.get_active_text() == "4GB"):
            msg = "4GB"
        if(self.combo1.get_active_text() == "8GB"):
            msg = "8GB"
        with open("/etc/rc.local","w") as f0:
            f0.write("""#!/bin/sh -e
mount -t tmpfs -w -o size=%s tmpfs /tmp
exit 0
            """ % (msg))
        print("Finished tmpfs settings")
if __name__ == "__main__":
    ramdisk_slider()
    Gtk.main()
