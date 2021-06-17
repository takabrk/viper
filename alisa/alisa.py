#!/usr/bin/env python
#-*-coding:utf-8 -*-
#alisa.py @takamitsu hamada 20210604
#mainsite : http://vsrx.work

import sys,os,os.path,json
from urllib.request import urlopen
import subprocess as sp
from threading import Thread
import codecs
import pathlib
import textwrap

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    sys.exit(1)

class alisa(object):
    def __init__(self):
        gladefile = "alisa.ui"
        self.tree = Gtk.Builder()
        self.tree.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + gladefile)
        dic = {
            "on_talk_text_clicked" : self.on_talk_text_clicked,
            "on_talk_text_file_clicked" : self.on_talk_text_file_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.window = treeObj("talk_text")
        self.window = treeObj("talk_text_file")
        self.input_text = treeObj("input_text")
        self.select_text_file = treeObj("select_text_file")
        self.select_mode = treeObj("select_mode")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
#alisa
    def on_talk_text_clicked(self,widget):
        msg = self.input_text.get_text()
        if(self.select_mode.get_active_text() == "mei_happy"):
            mv = "mei_happy"
        if(self.select_mode.get_active_text() == "mei_angry"):
            mv = "mei_angry"
        if(self.select_mode.get_active_text() == "mei_bashful"):
            mv = "mei_bashful"
        if(self.select_mode.get_active_text() == "mei_normal"):
            mv = "mei_normal"
        if(self.select_mode.get_active_text() == "mei_sad"):
            mv = "mei_sad"
        if(self.select_mode.get_active_text() == "miku_a"):
            mv = "miku_a"
        if(self.select_mode.get_active_text() == "miku_b"):
            mv = "miku_b"
        if(self.select_mode.get_active_text() == "tohoku_happy"):
            mv = "tohoku_happy"
        if(self.select_mode.get_active_text() == "tohoku_angry"):
            mv = "tohoku_angry"
        if(self.select_mode.get_active_text() == "tohoku_neutral"):
            mv = "tohoku_neutral"
        if(self.select_mode.get_active_text() == "tohoku_sad"):
            mv = "tohoku_sad"
        cmd = "python3 viper.py jsay %s %s" % (msg,mv)
        print(cmd)
        sp.call(cmd.strip().split(" "))
    def on_talk_text_file_clicked(self,widget):
        if(self.select_mode.get_active_text() == "mei_happy"):
            mv = "mei_happy"
        if(self.select_mode.get_active_text() == "mei_angry"):
            mv = "mei_angry"
        if(self.select_mode.get_active_text() == "mei_bashful"):
            mv = "mei_bashful"
        if(self.select_mode.get_active_text() == "mei_normal"):
            mv = "mei_normal"
        if(self.select_mode.get_active_text() == "mei_sad"):
            mv = "mei_sad"
        if(self.select_mode.get_active_text() == "miku_a"):
            mv = "miku_a"
        if(self.select_mode.get_active_text() == "miku_b"):
            mv = "miku_b"
        if(self.select_mode.get_active_text() == "tohoku_happy"):
            mv = "tohoku_happy"
        if(self.select_mode.get_active_text() == "tohoku_angry"):
            mv = "tohoku_angry"
        if(self.select_mode.get_active_text() == "tohoku_neutral"):
            mv = "tohoku_neutral"
        if(self.select_mode.get_active_text() == "tohoku_sad"):
            mv = "tohoku_sad"
        fc1 =  self.select_text_file.get_filename()
        Thread(target=self.thread1).start()
        with open(fc1,mode="rt",encoding="utf-8") as f:
            for textline in f.read().splitlines():
                #text = textwrap.fill(textline)
                 cmd = "python viper.py jsay %s %s" % (textline,mv)
                 sp.call(cmd.strip().split(" "))
        f.close()
    def on_select_mode(self,widget):
        msg1 = self.select_mode.get_filename()
        return msg1
    def thread1(self):
        sp.call("./record.sh".strip().split(" "))

if __name__ == "__main__":
    alisa()
