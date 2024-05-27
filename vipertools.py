#!/usr/bin/env python
#-*-coding:utf-8 -*-
#vipertools.py
#Created by takamitsu hamada
#June 29,2023
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
            "on_kyotei_clicked" : self.on_kyotei_clicked,
            "on_tmpfs_clicked" : self.on_tmpfs_clicked,
            "on_system_tune_clicked" : self.on_system_tune_clicked,
            "on_settings_clicked" : self.on_settings_clicked,
            "on_console_clicked" : self.on_console_clicked,
            "on_synaptic_clicked" : self.on_synaptic_clicked,
            "on_extract_clicked" : self.on_extract_clicked,
            "on_build_clicked" : self.on_build_clicked,
            "on_sound_clicked" : self.on_sound_clicked,
            "on_numbers_clicked" : self.on_numbers_clicked,
            "on_apps_clicked" : self.on_apps_clicked,
            "on_apng_asvg_clicked" : self.on_apng_asvg_clicked,
            "on_cancel_clicked" : self.on_cancel_clicked,
            "on_os_chooser" : self.on_os_chooser,
            "on_ssb_clicked" : self.on_ssb_clicked,
            "on_imagetool_clicked" : self.on_imagetool_clicked,
            "on_ydown_clicked" : self.on_ydown_clicked,
            "on_HLSdown_clicked" : self.on_HLSdown_clicked,
            "on_install_driver_clicked" : self.on_install_driver_clicked,
            "on_button111_clicked" : self.on_button111_clicked,
            "on_talk_text_clicked" : self.on_talk_text_clicked,
            "on_talk_text_file_clicked" : self.on_talk_text_file_clicked,
            "on_vaapi1_clicked" : self.on_vaapi1_clicked
        }
        treeObj = self.tree.get_object
        self.tree.connect_signals(dic)
        self.window = treeObj("console")
        self.window = treeObj("synaptic")
        self.window = treeObj("extract")
        self.window = treeObj("build")
        self.window = treeObj("settings")
        self.window = treeObj("sound")
        self.window = treeObj("numbers")
        self.window = treeObj("apps")
        self.window = treeObj("apng_asvg")
        self.window = treeObj("kyotei")
        self.window = treeObj("imagetool")
        self.window = treeObj("ssb")
        self.name = treeObj("name")
        self.version = treeObj("version")
        self.method = treeObj("method")
        self.level = treeObj("level")
        self.url = treeObj("url")
        self.description = treeObj("description")
        self.os_chooser = treeObj("os_chooser")
        self.kernel_version = treeObj("kernel_version")
        self.codename = treeObj("codename")
        self.window = treeObj("viper_tools")
        #self.vte1 = treeObj("vte1")
        #bigbox = Gtk.Box()
        #self.vte1.add(bigbox)
        #bigbox.add(MyTerm())
        self.downloader = treeObj("downloader")
        self.hls_url = treeObj("hls_url")
        self.output = treeObj("output")
        self.window = treeObj("ydown")
        self.window = treeObj("HLSdown")
        self.window = treeObj("install_driver")
#        self.fcb1 = treeObj("filechooserbutton1")
        self.entry0 = treeObj("entry0")
        self.entry1 = treeObj("entry1")
        self.combo1 = treeObj("comboboxtext1")
        self.combo2 = treeObj("comboboxtext2")
        self.combo3 = treeObj("comboboxtext3")
        self.combo4 = treeObj("comboboxtext4")
        self.combo5 = treeObj("comboboxtext5")
        self.combo6 = treeObj("comboboxtext6")
        self.window = treeObj("button111")
        self.entry_ffmpeg_input = treeObj("entry_ffmpeg_input")
        self.entry_ffmpeg_output = treeObj("entry_ffmpeg_output")
        self.entry_ffmpeg_start = treeObj("entry_ffmpeg_start")
        self.entry_ffmpeg_end = treeObj("entry_ffmpeg_end")
        self.entry_ffmpeg_framerate = treeObj("entry_ffmpeg_framerate")
        self.window = treeObj("talk_text")
        self.window = treeObj("talk_text_file")
        self.input_text = treeObj("input_text")
        self.select_text_file = treeObj("select_text_file")
        self.select_mode = treeObj("select_mode")
        self.window = treeObj("vaapi1")
        self.window = treeObj("viper_tools")
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
        Thread(target=lambda : sp.call("python2 numbers_yosou/numbers.py",shell=True)).start()
        #os.chdir("../")
#install apps
    def on_apps_clicked(self,widget):
        sp.run("python3 install_apps.py".strip().split(" "))
#create apng and asvg
    def on_apng_asvg_clicked(self,widget):
        sp.run("python3 apng_asvg/apng_asvg.py".strip().split(" "))
#kyotei
    def on_kyotei_clicked(self,widget):
        def kyotei():
            os.chdir("kyotei")
            sp.run("./kyotei.sh".strip().split(" "))
            os.chdir("../")
        Thread(target=kyotei).start()
#change the settings of tmpfs 
    def on_tmpfs_clicked(self,widget):
        def ramdisk():
            os.chdir("ramdisk")
            sp.run("sudo python3 ramdisk_slider.py".strip().split(" "))
            os.chdir("../")
        Thread(target=ramdisk).start()
    def on_button6_clicked(self,widget):
        sp.run("python3 viper.py deldpkginfo".strip().split(" "))
        sp.run("sudo apt-get upgrade".strip().split(" "))
#compression file
#    def on_button10_clicked(self,widget):
#        Thread(target=lambda : sp.run("python3 #file_compression.py".strip().split(" "))).start()

#setting faststart
    def on_system_tune_clicked(self,widget):
        sp.run("sudo python3 viper.py faststart".strip().split(" "))
        sp.run("sudo python3 viper.py valkyrie".strip().split(" "))
        print("Finish Settings")
#SSB
    def on_ssb_clicked(self,widget):
        Thread(target=lambda : sp.call("./start_server &",shell="True")).start()
        Thread(target=lambda : sp.call('google-chrome --disk-cache-dir="/tmp" --app="http://localhost:8000/ssb.html?date=20180822f"',shell="True")).start()
#Image Tool
    def on_imagetool_clicked(self,widget):
        os.chdir("imagetool")
        sp.run("python3 imagetool.py".strip().split(" "))
        os.chdir("../")
#UBOLD-OP builder
#settings
    def on_settings_clicked(self,widget):
        msg1 = self.name.get_text()
        msg2 = self.version.get_text()
        msg3 = self.method.get_text()
        msg4 = self.level.get_text()
        msg5 = self.url.get_text()
        msg6 = self.description.get_text()
        msg7 = self.on_os_chooser(widget)
        msg8 = self.kernel_version.get_text()
        msg9 = self.codename.get_text()
        f1 = open("valkyrie_builder/configs/OSNAME","w")
        f1.write(msg1)
        f1.close()
        f2 = open("valkyrie_builder/configs/OSVERSION","w")
        f2.write(msg2)
        f2.close()
        f3 = open("valkyrie_builder/configs/COMPRESSIONMETHOD","w")
        f3.write(msg3)
        f3.close()
        f4 = open("valkyrie_builder/configs/COMPRESSIONLEVEL","w")
        f4.write(msg4)
        f4.close()
        f5 = open("valkyrie_builder/configs/RELEASENOTES","w")
        f5.write(msg5)
        f5.close()
        f6 = open("valkyrie_builder/configs/DESCRIPTION","w")
        f6.write(msg6)
        f6.close()
        f7 = open("valkyrie_builder/configs/ISOFILE","w")
        f7.write(msg7)
        f7.close()
        f8 = open("valkyrie_builder/extras/config","w")
        f8.write("""#/usr/bin/bash

# Define common variables
WORKPATH=/home/valkyrie-builder
ISOPATH=/home/valkyrie-builder/ISO
FSPATH=/home/valkyrie-builder/FileSystem

# Define Extract variables
MOUNTPATH=/media/ISO
YOURARCH=$(uname -m)

# Define Wizard variables
APPS=/home/valkyrie-builder/configs/PACKAGES

#Kernel Version

VERSIONPOINT=""" +msg8)
        f8.close()
        f9 = open("valkyrie_builder/configs/CODENAME","w")
        f9.write(msg9)
        f9.close()
        if os.path.isfile("/home/valkyrie-builder"):
            os.mkdir("/home/valkyrie-builder")
        sp.run("sudo cp -a valkyrie_builder/configs /home/valkyrie-builder",shell=True)
#Console
    def on_console_clicked(self,widget):
        sp.run("xfce4-terminal --hide-menubar -x sh -c 'sudo valkyrie_builder/extras/Console; read'",shell=True)
#Synaptic
    def on_synaptic_clicked(self,widget):
        sp.run("sudo valkyrie_builder/extras/Synaptic",shell=True)
#Extract
    def on_extract_clicked(self,widget):
        os.chdir("valkyrie_builder")
        sp.run("sudo extras/Extract",shell=True)
        os.chdir("../")
#on_os_chooser
    def on_os_chooser(self,widget):
        msg_ss = self.os_chooser.get_filename()
        return msg_ss
#Build
    def on_build_clicked(self,widget):
        sp.run("sudo valkyrie_builder/extras/Build",shell=True)
#Movie Changer
    def on_ydown_clicked(self,widget):
        msg1 = self.downloader.get_text()
        cmd = "./downloader.sh %s" % (msg1)
        sp.call(cmd.strip().split(" "))
    def on_HLSdown_clicked(self,widget):
        msg1=self.hls_url.get_text()
        msg2=self.output.get_text()
        cmd = "./download_hls.sh %s %s" % (msg1,msg2)
        sp.call(cmd.strip().split(" "))
    def on_vaapi1_clicked(self,widget):
        msg1 = self.entry0.get_text()
        msg2 = self.entry1.get_text()
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
        if(self.combo4.get_active_text() == "4M"):
            msg7 = "4M"
        if(self.combo4.get_active_text() == "8M"):
            msg7 = "8M"
        if(self.combo4.get_active_text() == "10M"):
            msg7 = "10M"
        if(self.combo4.get_active_text() == "12M"):
            msg7 = "12M"
        if(self.combo4.get_active_text() == "16M"):
            msg7 = "16M"
        if(self.combo4.get_active_text() == "18M"):
            msg7 = "18M"
        if(self.combo4.get_active_text() == "20M"):
            msg7 = "20M"
        if(self.combo5.get_active_text() == "128k"):
            msg8 = "128k"
        if(self.combo5.get_active_text() == "192k"):
            msg8 = "192k"
        if(self.combo5.get_active_text() == "256k"):
            msg8 = "256k"
        if(self.combo5.get_active_text() == "386k"):
            msg8 = "386k"
        if(self.combo5.get_active_text() == "512k"):
            msg8 = "512k"
        if(self.combo6.get_active_text() == "29.97"):
            msg9 = "29.97"
        if(self.combo6.get_active_text() == "60"):
            msg9 = "60"
        cmd = "./qsv_enc.sh %s %s %s %s %s %s %s %s %s" % (msg1,msg2,msg3,msg4,msg5,msg6,msg7,msg8,msg9)
        print(cmd)
        sp.call(cmd.strip().split(" "))
#    def on_filechooserbutton1_file_set(self,widget):
#        msg1 = self.fcb1.get_filename()
#        return msg1
    def on_install_driver_clicked(self,widget):
        cmd = "./build_media_driver.sh"
        sp.call(cmd.strip().split(" "))
#ffmpeg
    def on_button111_clicked(self,widget):
        msg1 = self.entry_ffmpeg_input.get_text()
        msg2 = self.entry_ffmpeg_output.get_text()
        msg3 = self.entry_ffmpeg_start.get_text()
        msg4 = self.entry_ffmpeg_end.get_text()
        msg5 = self.entry_ffmpeg_framerate.get_text()
        cmd = "./movie2pics.sh %s %s %s %s %s" % (msg3,msg4,msg5,msg1,msg2)
        sp.call(cmd.strip().split(" "))
#viper_text_reading
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
        cmd = "python3 viper_for_jsay.py jsay %s %s" % (msg,mv)
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
                 cmd = "python viper_for_jsay.py jsay %s %s" % (textline,mv)
                 sp.call(cmd.strip().split(" "))
        f.close()
    def on_select_mode(self,widget):
        msg1 = self.select_mode.get_filename()
        return msg1
    def thread1(self):
        sp.call("./record.sh".strip().split(" "))
#Cancel
    def on_cancel_clicked(self,widget):
        Gtk.main_quit()

if __name__ == "__main__":
    #sp.run("python3 viper.py jsay お帰りなさいませ、マスター。私はブリュンヒルデと申します。ご注文はお決まりですか？ mei_happy string".strip().split(" "))
    valkyrie_setting()
