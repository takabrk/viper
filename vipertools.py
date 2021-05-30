#!/usr/bin/env python
#-*-coding:utf-8 -*-
#vipertools.py @takamitsu hamada 20201026
#mainsite : http://vsrx.work

import sys,os,os.path,json
import subprocess as sp
from threading import Thread
import codecs
#from MyTerm import MyTerm
try:
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk
except:
    try:
        import pgi
        pgi.install_as_gi()
        gi.require_version("Gtk","3.0")
        from gi.repository import Gtk
    except:
        print("GTK not available",file=sys.stderr)
        sys.exit(1)
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass

class valkyrie_setting(object):
    def __init__(self):
        gladefile = "viperTools.ui"
        self.tree = Gtk.Builder()
        self.tree.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/" + gladefile)
        dic = {
            "on_button4_clicked" : self.on_buttonkyotei_clicked,
            "on_buttontmpfs_clicked" : self.on_buttontmpfs_clicked,
            "on_button13_clicked" : self.on_button13_clicked,
            "on_button17_clicked" : self.on_button17_clicked,
            "on_button18_clicked" : self.on_button18_clicked,
            "on_button19_clicked" : self.on_button19_clicked,
            "on_button20_clicked" : self.on_button20_clicked,
            "on_button21_clicked" : self.on_button21_clicked,
            "on_sound_clicked" : self.on_sound_clicked,
            "on_numbers_clicked" : self.on_numbers_clicked,
            "on_apps_clicked" : self.on_apps_clicked,
            "on_m2p_clicked" :  self.on_m2p_clicked,
            "on_reading_clicked" : self.on_reading_clicked,
            "on_apng_asvg_clicked" : self.on_apng_asvg_clicked,
            "on_cancel_clicked" : self.on_cancel_clicked,
            "on_download_youtube_clicked" : self.on_download_youtube_clicked,
            "on_movie_enc_clicked" : self.on_movie_enc_clicked,
            "on_filechooserbutton1_file_set" : self.on_filechooserbutton1_file_set,
            "on_ssb_clicked" : self.on_ssb_clicked,
            "on_imagetool_clicked" : self.on_imagetool_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.window = treeObj("button3")
        self.window = treeObj("button4")
        self.window = treeObj("button5")
        self.window = treeObj("button6")
        self.window = treeObj("button13")
        self.window = treeObj("sound")
        self.window = treeObj("numbers")
        self.window = treeObj("apps")
        self.window = treeObj("m2p")
        self.window = treeObj("reading")
        self.window = treeObj("apng_asvg")
        self.window = treeObj("download_youtube")
        self.window = treeObj("movie_enc")
        self.window = treeObj("on_buttonkyotei_clicked")
        self.window = treeObj("on_imagetool_clicked")
        self.window = treeObj("on_ssb_clicked")
        self.entry1 = treeObj("entry1")
        self.entry2 = treeObj("entry2")
        self.entry3 = treeObj("entry3")
        self.entry4 = treeObj("entry4")
        self.entry5 = treeObj("entry5")
        self.entry6 = treeObj("entry6")
        self.fcb1 = treeObj("filechooserbutton1")
        self.window = treeObj("window1")
        #self.vte1 = treeObj("vte1")
        #bigbox = Gtk.Box()
        #self.vte1.add(bigbox)
        #bigbox.add(MyTerm())
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
#change login sound
    def on_sound_clicked(self,widget):
        sp.run("python3 change_login_sound/change_login_sound.py".strip().split(" "))
#numbers
    def on_numbers_clicked(self,widget):
        #os.chdir("numbers") 
        #Thread(target=lambda : sp.call("python viper.py jsay ナンバーズの予想を行います。   mei_happy string".strip().split(" "))).start()
        Thread(target=lambda : sp.call("python2 numbers/numbers.py",shell=True)).start()
        #os.chdir("../")
#install apps
    def on_apps_clicked(self,widget):
        sp.run("python3 install_apps/install_apps.py".strip().split(" "))
#movie2pics
    def on_m2p_clicked(self,widget):
        sp.run("python3 movie2pics/movie2pics.py".strip().split(" "))
#alisa
    def on_reading_clicked(self,widget):
        os.chdir("alisa")
        sp.run("python3 alisa.py".strip().split(" "))
        os.chdir("../")
#create apng and asvg
    def on_apng_asvg_clicked(self,widget):
        sp.run("python3 alisa/apng_asvg.py".strip().split(" "))
#downloader
    def on_download_youtube_clicked(self,widget):
        os.chdir("downloader")
        sp.run("python3 downloader.py".strip().split(" "))
        os.chdir("../")
#encode movie with QSV
    def on_movie_enc_clicked(self,widget):
        os.chdir("movieencoder")
        sp.run("python3 movieui.py".strip().split(" "))
        os.chdir("../")
#kyotei
    def on_buttonkyotei_clicked(self,widget):
        def kyotei():
            os.chdir("kyotei")
            sp.run("./kyotei.sh".strip().split(" "))
            os.chdir("../")
        Thread(target=kyotei).start()
#change the settings of tmpfs 
    def on_buttontmpfs_clicked(self,widget):
        def ramdisk():
            os.chdir("ramdisk")
            sp.run("sudo python3 ramdisk_slider.py".strip().split(" "))
            os.chdir("../")
        Thread(target=ramdisk).start()
    def on_button6_clicked(self,widget):
        sp.run("python3 viper.py deldpkginfo".strip().split(" "))
        sp.run("sudo apt-get upgrade".strip().split(" "))
#compression file
    def on_button10_clicked(self,widget):
        Thread(target=lambda : sp.run("python3 file_compression.py".strip().split(" "))).start()
#setting faststart
    def on_button13_clicked(self,widget):
        sp.run("sudo python3 viper.py faststart".strip().split(" "))
        sp.run("sudo python3 viper.py valkyrie".strip().split(" "))
        print("Finish Settings")
#SSB
    def on_ssb_clicked(self,widget):
        Thread(target=lambda : sp.call("./start_server &",shell="True")).start()
        Thread(target=lambda : sp.call('chromium-browser --disk-cache-dir="/tmp" --app="http://localhost:8000/ssb.html?date=20180822f"',shell="True")).start()
#Image Tool
    def on_imagetool_clicked(self,widget):
        os.chdir("imagetool")
        sp.run("python3 imagetool.py".strip().split(" "))
        os.chdir("../")
#Valkyrie Linux builder
#settings
    def on_button17_clicked(self,widget):
        msg1 = self.entry1.get_text()
        msg2 = self.entry2.get_text()
        msg3 = self.entry3.get_text()
        msg4 = self.entry4.get_text()
        msg5 = self.entry5.get_text()
        msg6 = self.entry6.get_text()
        msg7 = self.on_filechooserbutton1_file_set(widget)
        f1 = open("vsrx_builder/configs/DIST","w")
        f1.write(msg1)
        f1.close()
        f2 = open("vsrx_builder/configs/VERSION","w")
        f2.write(msg2)
        f2.close()
        f3 = open("vsrx_builder/configs/CODENAME","w")
        f3.write(msg3)
        f3.close()
        f4 = open("vsrx_builder/configs/DESCRIPTION","w")
        f4.write(msg4)
        f4.close()
        f5 = open("vsrx_builder/configs/RELEASENOTES","w")
        f5.write(msg5)
        f5.close()
        f6 = open("vsrx_builder/configs/EXTENDED","w")
        f6.write(msg6)
        f6.close()
        f7 = open("vsrx_builder/configs/ISOFILE","w")
        f7.write(msg7)
        f7.close()
        sp.run("""sudo mkdir /home/ubuntu-builder
        sudo cp -a vsrx_builder/configs /home/ubuntu-builder
        """,shell=True)
#Console
    def on_button18_clicked(self,widget):
        sp.run("sudo vsrx_builder/extras/Console",shell=True)
#Synaptic
    def on_button19_clicked(self,widget):
        sp.run("sudo vsrx_builder/extras/Synaptic",shell=True)
#Extract
    def on_button20_clicked(self,widget):
        os.chdir("vsrx_builder")
        sp.run("sudo extras/Extract",shell=True)
        os.chdir("../")
#on_filechooserbutton1_file_set
    def on_filechooserbutton1_file_set(self,widget):
        msg_ss = self.fcb1.get_filename()
        return msg_ss
#Build
    def on_button21_clicked(self,widget):
        sp.run("sudo vsrx_builder/extras/Build",shell=True)

#Cancel
    def on_cancel_clicked(self,widget):
        Gtk.main_quit()

if __name__ == "__main__":
    #sp.run("python3 viper.py jsay お帰りなさいませ、マスター。私はブリュンヒルデと申します。ご注文はお決まりですか？ mei_happy string".strip().split(" "))
    valkyrie_setting()