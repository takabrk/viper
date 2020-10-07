#!/usr/bin/env python
#-*-coding:utf-8 -*-
#alice.py @takamitsu hamada 20200805
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

#from viper import PrepareChain
#from viper import GenerateText
try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    sys.exit(1)

class alice(object):
    def __init__(self):
        gladefile = "alice.ui"
        self.tree = Gtk.Builder()
        self.tree.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + gladefile)
        dic = {
            "on_button7_clicked" : self.on_button7_clicked,
            "on_button23_clicked" : self.on_button23_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.window = treeObj("button7")
        self.window = treeObj("button23")
        self.entry7 = treeObj("entry7")
        self.combo1 = treeObj("comboboxtext1")
        self.combo2 = treeObj("comboboxtext2")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
#Alice
    def on_button7_clicked(self,widget):
        msg = self.entry7.get_text()
        if(self.combo1.get_active_text() == "mei_happy"):
            mv = "mei_happy"
        if(self.combo1.get_active_text() == "mei_angry"):
            mv = "mei_angry"
        if(self.combo1.get_active_text() == "mei_bashful"):
            mv = "mei_bashful"
        if(self.combo1.get_active_text() == "mei_normal"):
            mv = "mei_normal"
        if(self.combo1.get_active_text() == "mei_sad"):
            mv = "mei_sad"
        if(self.combo1.get_active_text() == "miku_a"):
            mv = "miku_a"
        if(self.combo1.get_active_text() == "miku_b"):
            mv = "miku_b"
        if(self.combo1.get_active_text() == "tohoku_happy"):
            mv = "tohoku_happy"
        if(self.combo1.get_active_text() == "tohoku_angry"):
            mv = "tohoku_angry"
        if(self.combo1.get_active_text() == "tohoku_neutral"):
            mv = "tohoku_neutral"
        if(self.combo1.get_active_text() == "tohoku_sad"):
            mv = "tohoku_sad"
        cmd = "python3 viper.py jsay %s %s" % (msg,mv)
        print(cmd)
        sp.call(cmd.strip().split(" "))
    def on_button23_clicked(self,widget):
        if(self.combo1.get_active_text() == "mei_happy"):
            mv = "mei_happy"
        if(self.combo1.get_active_text() == "mei_angry"):
            mv = "mei_angry"
        if(self.combo1.get_active_text() == "mei_bashful"):
            mv = "mei_bashful"
        if(self.combo1.get_active_text() == "mei_normal"):
            mv = "mei_normal"
        if(self.combo1.get_active_text() == "mei_sad"):
            mv = "mei_sad"
        if(self.combo1.get_active_text() == "miku_a"):
            mv = "miku_a"
        if(self.combo1.get_active_text() == "miku_b"):
            mv = "miku_b"
        if(self.combo1.get_active_text() == "tohoku_happy"):
            mv = "tohoku_happy"
        if(self.combo1.get_active_text() == "tohoku_angry"):
            mv = "tohoku_angry"
        if(self.combo1.get_active_text() == "tohoku_neutral"):
            mv = "tohoku_neutral"
        if(self.combo1.get_active_text() == "tohoku_sad"):
            mv = "tohoku_sad"
        if(self.combo2.get_active_text() == "関西弁"):
            with open("kansai.txt",mode="rt",encoding="utf-8") as f:
                for textline in f.read().splitlines():
                    #text = textwrap.fill(textline)
                    cmd = "python viper.py jsay %s %s" % (textline,mv)
                    sp.call(cmd.strip().split(" "))
            f.close()
            #f = open("kansai.txt")
            #text = f.read()
            #f.close()
            #chain = PrepareChain(text)
            #triplet_freqs = chain.make_triplet_freqs()
            #chain.save(triplet_freqs,True)
            #generator = GenerateText()
            #gg = generator.generate()
            #print(gg)
            #print(type(gg))
            #f2 = codecs.open("test111.txt","w","utf-8")
            #f2.write(gg)
            #f2.write(text)
            #f2.close()
        if(self.combo2.get_active_text() == "文学"):
            with open("bungaku.txt",mode="rt",encoding="utf-8") as f:
                for textline in f.read().splitlines():
                    #text = textwrap.fill(textline)
                    cmd = "python viper.py jsay %s %s" % (textline,mv)
                    sp.call(cmd.strip().split(" "))
            f.close()
            #f = open("bungaku.txt")
            #text = f.read()
            #f.close()
            #chain = PrepareChain(text)
            #triplet_freqs = chain.make_triplet_freqs()
            #chain.save(triplet_freqs,True)
            #generator = GenerateText()
            #gg = generator.generate()
            #print(gg)
            #print(type(gg))
            #f2 = codecs.open("test111.txt","w","utf-8")
            #f2.write(gg)
            #f2.write(text)
            #f2.close()
        if(self.combo2.get_active_text() == "エロ"):
            with open("ero.txt",mode="rt",encoding="utf-8") as f:
                for textline in f.read().splitlines():
                    #text = textwrap.fill(textline)
                    cmd = "python viper.py jsay %s %s" % (textline,mv)
                    sp.call(cmd.strip().split(" "))
            f.close()
            #f = open("ero.txt")
            #text = f.read()
            #f.close()
            #print(text)
            #chain = PrepareChain(text)
            #triplet_freqs = chain.make_triplet_freqs()
            #chain.save(triplet_freqs,True)
            #generator = GenerateText()
            #gg = generator.generate()
            #print(gg)
            #print(type(gg))
            #f2 = codecs.open("test111.txt","w","utf-8")
            #f2.write(gg)
            #f2.write(text)
            #f2.close()
        #cmd = "python viper.py jsay %s %s %s" % ("test111.txt",mv,"data")
        #sp.call(cmd.strip().split(" "))
    def on_filechooserbutton1_file_set(self,widget):
        msg2 = self.fcb1.get_filename()
        return msg2

if __name__ == "__main__":
    alice()
