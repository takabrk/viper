#!/usr/bin/env python2
#-*- coding:utf-8 -*-
#jsay Created by takamitu hamada 20170323

import sys,os,os.path
import subprocess as sp
import codecs
sys.path.append("..")
from viper import PrepareChain
from viper import GenerateText

try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    sys.exit(1)
class jsay(object):
    def __init__(self):
        gladefile="jsay.ui"
        self.tree = Gtk.Builder()
        #self.wTree.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + gladefile)
        self.tree.add_from_file(gladefile)
        dic = {
            "on_button1_clicked" : self.on_button1_clicked,
            "on_button2_clicked" : self.on_button2_clicked,
            "on_button3_clicked" : self.on_button3_clicked,
            "on_button4_clicked" : self.on_button4_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.window = treeObj("button1")
        self.window = treeObj("button2")
        self.window = treeObj("button3")
        self.window = treeObj("button4")
        self.combo1 = treeObj("comboboxtext1")
        self.combo2 = treeObj("comboboxtext2")
        self.entry1 = treeObj("entry1")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
    def on_button1_clicked(self,widget):
        msg = self.entry1.get_text()
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
        os.chdir("../")
        cmd = "python viper.py jsay %s %s %s" % (msg,mv,"string")
        sp.call(cmd.strip().split(" "))
        os.chdir("alice")
    def on_button2_clicked(self,widget):
        Gtk.main_quit()
    def on_button3_clicked(self,widget):
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
        if(self.combo2.get_active_text() == "関西弁"):
            f = open("kansai.txt")
            text = f.read()
            f.close()
            #chain = PrepareChain(text)
            #triplet_freqs = chain.make_triplet_freqs()
            #chain.save(triplet_freqs,True)
            #generator = GenerateText()
            #gg = generator.generate()
            #print(gg)
            #print(type(gg))
            f2 = codecs.open("test111.txt","w","utf-8")
            #f2.write(gg)
            f2.write(text)
            f2.close()
        if(self.combo2.get_active_text() == "文学"):
            f = open("bungaku.txt")
            text = f.read()
            f.close()
            #chain = PrepareChain(text)
            #triplet_freqs = chain.make_triplet_freqs()
            #chain.save(triplet_freqs,True)
            #generator = GenerateText()
            #gg = generator.generate()
            #print(gg)
            #print(type(gg))
            f2 = codecs.open("test111.txt","w","utf-8")
            #f2.write(gg)
            f2.write(text)
            f2.close()
        if(self.combo2.get_active_text() == "エロ"):
            f = open("./ero.txt")
            text = f.read()
            f.close()
            #chain = PrepareChain(text)
            #triplet_freqs = chain.make_triplet_freqs()
            #chain.save(triplet_freqs,True)
            #generator = GenerateText()
            #gg = generator.generate()
            #print(gg)
            #print(type(gg))
            f2 = codecs.open("test111.txt","w","utf-8")
            #f2.write(gg)
            f2.write(text)
            f2.close()
        os.chdir("../")
        #cmd = "python viper.py jsay %s %s %s" % ("alice/test111.txt",mv,"data")
        cmd = "python viper.py jsay %s %s %s" % ("alice/test111.txt",mv,"data")
        sp.call(cmd.strip().split(" "))
        os.chdir("alice")
    def on_button4_clicked(self,widget):
        os.chdir("../")
        #sp.call("python viper.py jsay すうどくを解いちゃうぞ。 mei_happy string".strip().split(" "))
        sp.call("python viper.py sudoku".strip().split(" "))
        os.chdir("alice")
    def on_filechooserbutton1_file_set(self,widget):
        msg2 = self.fcb1.get_filename()
        return msg2
if __name__ == "__main__":
    jsay()
    Gtk.main()
