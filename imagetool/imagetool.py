#!/usr/bin/env python
#-*- coding:utf-8 -*-
#imagetool.py @takamitu hamada 20231014
import os,os.path,sys
import subprocess as sp
from rembg import remove
from PIL import Image

try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    sys.exit(1)

class imagetool(object):
    def __init__(self):
        gladefile = "imagetool.ui"
        self.tree = Gtk.Builder()
        self.tree.add_from_file(gladefile)
        dic = {
            "on_button1_clicked" : self.on_button1_clicked,
            "on_button2_clicked" : self.on_button2_clicked,
            "on_button3_clicked" : self.on_button3_clicked,
            "on_button4_clicked" : self.on_button4_clicked,
            "on_button5_clicked" : self.on_button5_clicked,
            "on_button6_clicked" : self.on_button6_clicked,
            "on_button7_clicked" : self.on_button7_clicked,
            "on_button8_clicked" : self.on_button8_clicked,
            "on_button9_clicked" : self.on_button9_clicked,
            "on_filechooserbutton1_file_set" : self.on_filechooserbutton1_file_set,
            "on_clipping_clicked" : self.on_clipping_clicked
        }
        treeObj = self.tree.get_object;
        self.tree.connect_signals(dic)
        self.window = treeObj("button1")
        self.window = treeObj("button2")
        self.window = treeObj("button3")
        self.window = treeObj("button4")
        self.window = treeObj("button5")
        self.window = treeObj("button6")
        self.window = treeObj("button7")
        self.window = treeObj("button8")
        self.window = treeObj("button9")
        self.fcb1 = treeObj("filechooserbutton1")
        self.combo1 = treeObj("comboboxtext1")
        self.entry1 = treeObj("entry1")
        self.entry2 = treeObj("entry2")
        self.entry3 = treeObj("entry3")
        self.entry4 = treeObj("entry4")
        self.entry5 = treeObj("entry5")
        self.entry6 = treeObj("entry6")
        self.entry7 = treeObj("entry7")
        self.window = treeObj("clipping")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
#GIF2PNG button
    def on_button1_clicked(self,widget):
        msg1 = self.entry1.get_text()
        msg2 = self.entry2.get_text()
        msg3 = self.entry3.get_text()
        msg4 = self.entry4.get_text()
        msg5 = self.entry5.get_text()
        os.chdir("../")
        cmdg2p = "python viper.py gif2png %s %s %s %s %s" % (msg1,msg2,msg3,msg4,msg5)
        sp.call(cmdg2p.strip().split(""))
        print("Finished")
        os.chdir("imagetool")
#PNG2GIF button
    def on_button2_clicked(self,widget):
        msg1 = self.entry1.get_text()
        msg2 = self.entry2.get_text()
        msg3 = self.entry3.get_text()
        msg4 = self.entry4.get_text()
        msg5 = self.entry5.get_text()
        os.chdir("../")
        cmdp2g = "python viper.py png2gif %s %s %s %s %s" % (msg1,msg2,msg3,msg4,msg5)
        sp.call(cmdp2g.strip().split(" "))
        print("Finished")
        os.chdir("imagetool")
#PNG2JPG button
    def on_button3_clicked(self,widget):
        msg1 = self.entry1.get_text()
        msg2 = self.entry2.get_text()
        msg3 = self.entry3.get_text()
        msg4 = self.entry4.get_text()
        msg5 = self.entry5.get_text()
        os.chdir("../")
        cmdp2j = "python viper.py png2jpg %s %s %s %s %s" % (msg1,msg2,msg3,msg4,msg5)
        sp.call(cmdp2j.strip().split(" "))
        print("Finished")
        os.chdir("imagetool")
#rotateJPG button
    def on_button4_clicked(self,widget):
        msg1 = self.entry1.get_text()
        msg6 = self.entry6.get_text()
        os.chdir("../")
        cmdrj = "python viper.py rotatejpg %s %s" % (msg1,msg6)
        sp.call(cmdrj.strip().split(" "))
        print("Finished")
        os.chdir("imagetool")
#animationSVG button
    def on_button5_clicked(self,widget):
        msg1 = self.entry1.get_text()
        msg3 = self.entry3.get_text()
        msg4 = self.entry4.get_text()
        msg7 = self.entry7.get_text()
        os.chdir("../")
        cmdas = "python2 viper.py asvg %s %s %s %s" % (msg1,msg3,msg4,msg7)
        sp.call(cmdas.strip().split(" "))
        print("Finished")
        os.chdir("imagetool")
#wifu2x button
    def on_button6_clicked(self,widget):
        msg1 = self.on_filechooserbutton1_file_set(widget)
        msg2 = self.entry2.get_text()
        if(self.combo1.get_active_text() == "scale2.0x"):
            modelv = "scale2.0x"
        if(self.combo1.get_active_text() == "noise1"):
            modelv = "noise1"
        if(self.combo1.get_active_text() == "noise2"):
            modelv = "noise2"
        cndmodel = "python waifu2x.py %s %s models/%s_model.json" % (msg1,msg2,modelv)
        print(cndmodel)
        sp.call(cndmodel.strip().split(" "))
        print("Finished")
#movie2jpg button
    def on_button8_clicked(self,widget):
        msg1 = self.on_filechooserbutton1_file_set(widget)
        msg2 = self.entry2.get_text()
        msg5 = self.entry5.get_text()
        cmdimg = 'avconv -i %s -r %s -qscale 1 -f image2 %s/image-%s.jpg' % (msg1,msg5,msg2,"%3d")
        sp.call(cmdimg.strip().split(" "))
        print("Finished")
    def on_filechooserbutton1_file_set(self,widget):
        msg1 = self.fcb1.get_filename()
        return msg1
    def on_button9_clicked(self,widget):
        msg1 = self.on_filechooserbutton2_file_set(widget)
        msg2 = self.entry9.get_text();
        cmdgu = "./guetzli_linux_x86-64 %s %s" % (msg1,msg2)
        sp.call(cmdgu.strip().split(" "))
    def on_clipping_clicked(self,widget):
        msg1 = self.on_filechooserbutton1_file_set(widget)
        msg2 = self.entry2.get_text()
        input_path = msg1
        output_path = msg2
        input = Image.open(input_path)
        output = remove(input)
        output.save(output_path)
        print("Completed Clipping")
#Cancel button
    def on_button7_clicked(self,widget):
        Gtk.main_quit()
if __name__ == "__main__":
    imagetool()
    Gtk.main()
