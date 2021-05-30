#!/usr/bin/env python
#-*-coding:utf-8 -*-
#install_apps.py @takamitsu hamada 20190704
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

class install_apps(object):
    def __init__(self):
        gladefile = "install_apps.ui"
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
        self.checkbutton4 = treeObj("checkbutton4")
        self.checkbutton5 = treeObj("checkbutton5")
        self.checkbutton8 = treeObj("checkbutton8")
        self.checkbutton9 = treeObj("checkbutton9")
        self.checkbutton10 = treeObj("checkbutton10")
        self.checkbutton11 = treeObj("checkbutton11")
        self.checkbutton12 = treeObj("checkbutton12")
        self.window = treeObj("window1")
        self.window.show_all()
        if(self.window):
            self.window.connect("destroy",Gtk.main_quit)
        Gtk.main()
    def on_button1_clicked(self,widget):
        if self.checkbutton4.get_active() == True:
            #Thread(target=lambda : sp.call("python viper.py jsay アプリケーションとライブラリをインストールします。パスワードを入力してルート権限になってね。 mei_happy string".strip().split(" "))).start()
            Thread(target=lambda : sp.call("python viper.py importapps && python viper.py pymodules",shell=True)).start()
            print("Installed Applications and Libraries.")
        if self.checkbutton5.get_active() == True:
            sp.call("python viper.py importextraapps",shell=True)
        if self.checkbutton8.get_active() == True:
            #Thread(target=lambda : sp.call("python viper.py jsay システムを変身させるよ。 mei_happy string".strip().split(" "))).start()
            Thread(target=lambda : sp.call("python viper.py valkyrie".strip().split(" "))).start()
        if self.checkbutton9.get_active() == True:
            #Thread(target=lambda : sp.call("python viper.py jsay オンラインストレージを使えるようにするよ。 mei_happy string".strip().split(" "))).start()
            def instdrive():
                sp.call("sudo apt-get install -y grive git".strip().split(" "))
                os.chdir(os.environ['HOME'])
                sp.call("git clone https://github.com/xybu92/onedrive-d.git".strip().split(" "))
                os.chdir("onedrive-d")
                sp.call("./install.sh".strip().split(" "))
                print("Finished")
            Thread(target=instdrive).start()
        if self.checkbutton10.get_active() == True:
            #Thread(target=lambda : sp.call("python viper.py jsay スーパーハッカーになるぞ。 mei_happy string").strip().split(" ")).start()
            def insthack():
                hacks = ["wireshark","kismet","ettercap-graphical","nmap","hydra"]
                for i in hacks:
                    cmdhacks = "sudo apt-get -y install %s" % (i)
                    sp.call(cmdhacks.strip().split(" "))
                print("Finished")
            Thread(target=insthack).start()
        if self.checkbutton11.get_active() == True:
            #Thread(target=lambda : sp.call("python viper.py jsay PPAを追加します。 mei_happy string".strip().split(" "))).start()
            Thread(target=lambda : sp.call("python viper.py ppa".strip().split(" "))).start()
        if self.checkbutton12.get_active() == True:
            #Thread(target=lambda : sp.call("python viper.py jsay プラグインを追加します。 mei_happy string".strip().split(" "))).start()
            Thread(target=lambda : sp.call("sh scripts/install_widevine.sh".strip().split(" "))).start()
    def on_button2_clicked(self,widget):
        Gtk.main_quit()
if __name__ == "__main__":
    install_apps()
