#!/usr/bin/env python
#-*-coding:utf-8 -*-
#change_login_sound.py @takamitsu hamada 20200119
#mainsite : http://vsrx.work

import sys,os,os.path,json,shutil
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

class change_login_sound(object):
    def __init__(self):
        gladefile = "change_login_sound.ui"
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
        self.checkbutton1 = treeObj("checkbutton1")
        self.checkbutton2 = treeObj("checkbutton2")
        self.checkbutton3 = treeObj("checkbutton3")
        self.checkbutton4 = treeObj("checkbutton4")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
    def on_button1_clicked(self,widget):
        file_name = os.environ['HOME']+"/.config/openbox/autostart"
        back_file = file_name+".bak"
        shutil.copy(file_name,back_file)
        if self.checkbutton1.get_active() == True:
            #Thread(target=lambda : sp.call("python viper.py jsay ログインサウンドをイオリに変更します。 mei_happy string".strip().split(" "))).start()
            def syssound():
                f=open(file_name,"r")
                string = f.readlines()
                string[2] = "mplayer -ao alsa /usr/share/sounds/Moesound_iori/stereo/desktop-login.ogg &\n"
                string2 = ''.join(string)
                f.close()
                f2 = open(file_name,"w")
                f2.writelines(string2)
                f2.close()
            Thread(target=syssound).start()
            print("It has been changed to the voice of Iori.")
        if self.checkbutton2.get_active() == True:
            #Thread(target=lambda : sp.call("python viper.py jsay ログインサウンドをメイドイオリに変更します。 mei_happy string".strip().split(" "))).start()
            def syssound():
                f=open(file_name,"r")
                string = f.readlines()
                string[2] = "mplayer -ao alsa /usr/share/sounds/Moesound_maid_iori/stereo/desktop-login.ogg &\n"
                string2 = ''.join(string)
                f.close()
                f2 = open(file_name,"w")
                f2.writelines(string2)
                f2.close()
            Thread(target=syssound).start()
            print("It has been changed to the voice of MaidIori.")
        if self.checkbutton3.get_active() == True:
            #sp.call("python viper.py jsay ログインサウンドをSFイオリに変更します。 mei_happy string".strip().split(" "))
            def syssound():
                f=open(file_name,"r")
                string = f.readlines()
                string[2] = "mplayer -ao alsa /usr/share/sounds/Moesound_SF_iori/stereo/desktop-login.ogg &\n"
                string2 = ''.join(string)
                f.close()
                f2 = open(file_name,"w")
                f2.writelines(string2)
                f2.close()
            Thread(target=syssound).start()
            print("It has been changed to the voice of SFIori.")
        if self.checkbutton4.get_active() == True:
            def syssound():
                f=open(file_name,"r")
                string = f.readlines()
                string[2] = "\n"
                string2 = ''.join(string)
                f.close()
                f2 = open(file_name,"w")
                f2.writelines(string2)
                f2.close()
            Thread(target=syssound).start()
            print("No system sound")                 
    def on_button2_clicked(self,widget):
        Gtk.main_quit()

if __name__ == "__main__":
    change_login_sound()
