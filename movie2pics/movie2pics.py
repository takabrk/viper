#!/usr/bin/env python
#-*-coding:utf-8 -*-
#movie2pics.py @takamitsu hamada 20190707
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

class movie2pics(object):
    def __init__(self):
        gladefile = "movie2pics.ui"
        self.tree = Gtk.Builder()
        self.tree.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + gladefile)
        dic = {
            "on_button111_clicked" : self.on_button111_clicked,
            "on_button116_clicked" : self.on_button116_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.window = treeObj("button111")
        self.window = treeObj("button116")
        self.entry_ffmpeg_input = treeObj("entry_ffmpeg_input")
        self.entry_ffmpeg_output = treeObj("entry_ffmpeg_output")
        self.entry_ffmpeg_start = treeObj("entry_ffmpeg_start")
        self.entry_ffmpeg_end = treeObj("entry_ffmpeg_end")
        self.entry_ffmpeg_framerate = treeObj("entry_ffmpeg_framerate")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
    def on_button2_clicked(self,widget):
        Gtk.main_quit()
#ffmpeg
    def on_button111_clicked(self,widget):
        msg1 = self.entry_ffmpeg_input.get_text()
        msg2 = self.entry_ffmpeg_output.get_text()
        msg3 = self.entry_ffmpeg_start.get_text()
        msg4 = self.entry_ffmpeg_end.get_text()
        msg5 = self.entry_ffmpeg_framerate.get_text()
        cmd = "ffmpeg -ss %s -t %s -r %s -i %s %s.png" % (msg3,msg4,msg5,msg1,msg2)
        sp.call(cmd.strip().split(" "))
#ffmpeg cancel
    def on_button116_clicked(self,widget):
        Gtk.main_quit()

if __name__ == "__main__":
    movie2pics()
