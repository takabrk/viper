#!/usr/bin/env python
#-*-coding:utf-8 -*-
#vipertools.py @takamitsu hamada 20221118
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
            "on_imagetool_clicked" : self.on_imagetool_clicked
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
        self.codename = treeObj("codename")
        self.os_name = treeObj("os_name")
        self.url = treeObj("url")
        self.description = treeObj("description")
        self.os_chooser = treeObj("os_chooser")
        self.window = treeObj("viper_tools")
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
        Thread(target=lambda : sp.call("python2 numbers_yosou/numbers.py",shell=True)).start()
        #os.chdir("../")
#install apps
    def on_apps_clicked(self,widget):
        sp.run("python3 install_apps/install_apps.py".strip().split(" "))
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
#Valkyrie Linux builder
#settings
    def on_settings_clicked(self,widget):
        msg1 = self.name.get_text()
        msg2 = self.version.get_text()
        msg3 = self.codename.get_text()
        msg4 = self.os_name.get_text()
        msg5 = self.url.get_text()
        msg6 = self.description.get_text()
        msg7 = self.on_os_chooser(widget)
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
    def on_console_clicked(self,widget):
        sp.run("xfce4-terminal --hide-menubar -x sh -c 'sudo vsrx_builder/extras/Console; read'",shell=True)
#Synaptic
    def on_synaptic_clicked(self,widget):
        sp.run("sudo vsrx_builder/extras/Synaptic",shell=True)
#Extract
    def on_extract_clicked(self,widget):
        os.chdir("vsrx_builder")
        sp.run("sudo extras/Extract",shell=True)
        os.chdir("../")
#on_os_chooser
    def on_os_chooser(self,widget):
        msg_ss = self.os_chooser.get_filename()
        return msg_ss
#Build
    def on_build_clicked(self,widget):
        sp.run("sudo vsrx_builder/extras/Build",shell=True)

#Cancel
    def on_cancel_clicked(self,widget):
        Gtk.main_quit()

if __name__ == "__main__":
    #sp.run("python3 viper.py jsay お帰りなさいませ、マスター。私はブリュンヒルデと申します。ご注文はお決まりですか？ mei_happy string".strip().split(" "))
    valkyrie_setting()