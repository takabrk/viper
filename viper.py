#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
viper.py
This script created by takamitsu hamada
version :  20231014
License      :  BSD License
Web site URL :  http://vsrx.work
"""
import math,re,glob,string,os,time
import random,shutil,codecs
import operator,sys,wave,base64
import subprocess as sp
from datetime import *
import unittest,sqlite3,os.path
from collections import defaultdict
from gi.repository import GLib

argvs = sys.argv
argvcount = len(argvs)
homedir = os.environ['HOME']+"/viper/"
#viper Class
class viper(object):
    def __init__(self):
        pass
#VSRX Desktop
    def setupValkyrie(self):
        sp.call("""
            sudo cp -a valkyrie_desktop/etc/skel /etc
            sudo chown -R root /etc/skel
            sudo chgrp -R root /etc/skel
            sudo chmod -R 755 /etc/skel
            sudo cp -a valkyrie_desktop/usr/share /usr
            sudo chown -R root /usr/share/backgrounds
            sudo chgrp -R root /usr/share/backgrounds
            sudo chmod -R 755 /usr/share/backgrounds
            sudo chown -R root /usr/share/icons
            sudo chgrp -R root /usr/share/icons
            sudo chmod -R 755 /usr/share/icons
            sudo chown -R root /usr/share/xsessions
            sudo chgrp -R root /usr/share/xsessions
            sudo chmod -R 755 /usr/share/xsessions
            sudo cp -a valkyrie_desktop/etc/xdg /etc
            sudo chown -R root /etc/xdg
            sudo chgrp -R root /etc/xdg
            sudo chmod 755 /etc/xdg
            sudo cp -a ~/viper /etc/skel
            sudo apt-get install synaptic
            sudo apt-get update
        """,shell=True)
        self.set_sources_list()
    def suckout(self):
        sp.call("""
            rm -r valkyrie_desktop/etc/skel
            mkdir valkyrie_desktop/etc/skel
            cp -a ~/.config/openbox valkyrie_desktop/etc/skel/.config
            cp -a ~/.config/tint2 valkyrie_desktop/etc/skel/.config
            cp -a ~/.config/conky valkyrie_desktop/etc/skel/.config
            cp -a ~/.config/gtk-2.0 valkyrie_desktop/etc/skel/.config
            cp -a ~/.config/gtk-3.0 valkyrie_desktop/etc/skel/.config
            cp -a ~/.config/fcitx valkyrie_desktop/etc/skel/.config
            cp -a ~/.config/fontconfig valkyrie_desktop/etc/skel/.config
            cp -a ~/.config/jack valkyrie_desktop/etc/skel/.config
            cp -a ~/.config/xfce4 valkyrie_desktop/etc/skel/.config
            cp -a ~/.config/lxqt valkyrie_desktop/etc/skel/.config
            cp -a ~/.gtkrc-2.0 valkyrie_desktop/etc/skel
            cp -a ~/.Xdefaults valkyrie_desktop/etc/skel
            cp -a ~/.emacs.d valkyrie_desktop/etc/skel
            cp -a ~/.gconf valkyrie_desktop/etc/skel
            cp -a ~/.themes valkyrie_desktop/etc/skel
            cp -a ~/.config/blender valkyrie_desktop/etc/skel/.config
            cp -a ~/.config/GIMP valkyrie_desktop/etc/skel/.config
            rm -r valkyrie_desktop/usr/share/backgrounds
            cp -a /usr/share/backgrounds valkyrie_desktop/usr/share
            rm -r valkyrie_desktop/etc/apt/sources.list.d
            cp -a /etc/apt valkyrie_desktop/etc
            rm -r valkyrie_desktop/etc/xdg
            cp -a /etc/xdg valkyrie_desktop/etc
            cp -a /etc/lsb-release valkyrie_desktop/etc/lsb-release
            cp -a /etc/rc.local valkyrie_desktop/etc
        """,shell=True)
        print("Finished")
    def set_plymouth(self):
        sp.call("""
            sudo apt-get install plymouth
            sudo apt-get install plymouth-theme-solar
            sudo cp -a valkyrie_desktop/lib/plymouth /lib
            sudo chown -R root /lib/plymouth
            sudo chgrp -R root /lib/plymouth
            sudo chmod -R 755 /lib/plymouth
            sudo update-alternatives --config default.plymouth
        """,shell=True)
    def set_sources_list(self):
        sp.call("""
            sudo cp -a valkyrie_desktop/etc/apt/* /etc/apt
            sudo apt-get update
            #sudo dpkg --set-selections < synaptic_list.txt
            #sudo apt-get dselect-upgrade
            sudo apt-get upgrade
        """,shell=True)
    def set_wireless_poweroff(self):
        sp.call("""
            sudo cp -a valkyrie_desktop/etc/pm/power.d/wireless /etc/pm/power.d
            sudo chown -R root /etc/pm/power.d/wireless
            sudo chgrp -R root /etc/pm/power.d/wireless
            sudo chmod -R 755 /etc/pm/power.d/wireless
        """,shell=True)
    def set_blacklist(self):
        sp.call("""
            sudo cp -a valkyrie_desktop/etc/modprobe.d/blacklist.conf /etc/modprobe.d
            sudo chown -R root /etc/modprobe.d/blacklist.conf
            sudo chgrp -R root /etc/modprobe.d/blacklist.conf
            sudo chmod -R root /etc/modprobe.d/blacklist.conf
        """,shell=True)
    def del_dpkg_info(self):
        sp.call("""
            sudo rm -r /var/lib/dpkg/info/*.postinst
            sudo rm -r /var/lib/dpkg/info/*.postrm
            sudo rm -r /var/lib/dpkg/info/*.preinst
            sudo rm -r /var/lib/dpkg/info/*.prerm
        """,shell=True)
    def update_rc(self,script_name):
        sp.call("update-rc.d %s defaults" % (script_name),shell=True)
    def off_service(self):
        sp.call("""
            sysv-rc-conf avahi-daemon off
            sysv-rc-conf bluetooth off
            sysv-rc-conf cups off
            sysv-rc-conf dns-clean off
            sysv-rc-conf pppd-dns off
            sysv-rc-conf speech-dispatcher off
            sysv-rc-conf plymouth off
            sysv-rc-conf rsync off
        """,shell=True)
    def addPPA(self):
        sp.call("""sudo add-apt-repository ppa:xorg-edgers/ppa
sudo add-apt-repository ppa:canonical-kernel-team/ppa
sudo add-apt-repository ppa:otto-kesselgulasch/gimp
sudo add-apt-repository ppa:alexlarsson/flatpak
sudo apt-add-repository ppa:ppsspp/stable
sudo add-apt-repository ppa:ubuntuhandbook1/avidemux
sudo add-apt-repository ppa:alexlarsson/flatpak
sudo add-apt-repository ppa.launchpad.net/haraldhv/shotcut/ubuntu
sudo add-apt-repository ppa.launchpad.net/lucioc/sayonara/ubuntu
sudo add-apt-repository ppa.launchpad.net/ubuntu-x-swat/updates/ubuntu
sudo add-apt-repository [arch=amd64,i386] http://repo.steampowered.com/steam/
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable test edge"
sudo apt-get update""",shell=True)
    def installApplications(self):
        base = ["lxqt-core","obconf-qt","lxappearance","lxrandr","lxinput",
"dunst","tint2","gmrun",
"xfce4-terminal","xfce4-taskmanager","xfce4-power-manager",
"network-manager-gnome",
"emacs25-nox","leafpad",
"pulseaudio","pavucontrol","pulseaudio-utils",
"pulseaudio-module-jack","jackd","jackd2","qjackctl",
"alsamixergui","gnome-alsamixer",
"mpv","imagemagick","firefox",
"ffmpeg","obs-studio",
"python-tk","python3-tk","python3-sphinx",
"libllvm9","libjpeg8","libjpeg8-dev","zlib1g-dev",
"libfreetype6","libfreetype6-dev","apache2",
"libncurses5-dev",
"fakeroot","build-essential","git",
"python3-pip","python-pip"]
    def installExtraApplications(self):
        ba = ["google-chrome-stable","unity-hub","scribus","obs-studio",
"python-tk","python3-tk","python3-sphinx",
"libllvm9","libjpeg8","libjpeg8-dev","zlib1g-dev",
"libfreetype6","libfreetype6-dev","apache2",
"libncurses5-dev",
"fakeroot","build-essential","git",
"python3-pip","open-jtalk","mecab","mecab-utils","mecab-naist-jdic","mecab-naist-jdic-eucjp","mecab-jumandic"]
        for i in ba:
            sp.call("sudo apt-get install -y %s" % (i),shell=True)
    def installPythonModules(self):
        list2 = ["scipy","numpy","pandas","seaborn","mecab-python3","mecab-python","scikit-learn","statsmodels","beautifulsoup4","matplotlib","rembg"]
        for i in list2:
            sp.call("sudo pip2 install --no-cache-dir -I %s" % (i),shell=True)
            sp.call("sudo pip3 install --no-cache-dir -I %s" % (i),shell=True)
    def faststart(self):
        sp.call("apt-get install preload ccache sysv-rc-conf",shell=True)
        fs = open("/etc/default/preload")
        lines = fs.readlines()
        fs.close()
        fss = open("/etc/default/preload","w")
        for line in lines:
            fss.write("%s" % (re.sub("# OPTIONS=","OPTIONS=",line)))
            print(line[:-1])
        fss.close()
        sp.call("sudo service preload restart",shell=True)

        f2=open("/etc/rc.local","w")
        f2.write("""#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

mount -t tmpfs -w -o size=%sm tmpfs /tmp
exit 0
        """ % (1000))
        f2.close()

        f3=open("/etc/sysctl.conf","w")
        f3.write("""#
# /etc/sysctl.conf - Configuration file for setting system variables
# See /etc/sysctl.d/ for additional system variables
# See sysctl.conf (5) for information.
#

#kernel.domainname = example.com

# Uncomment the following to stop low-level messages on console
#kernel.printk = 3 4 1 3

##############################################################3
# Functions previously found in netbase
#

# Uncomment the next two lines to enable Spoof protection (reverse-path filter)
# Turn on Source Address Verification in all interfaces to
# prevent some spoofing attacks
net.ipv4.conf.default.rp_filter=1
net.ipv4.conf.all.rp_filter=1

# Uncomment the next line to enable TCP/IP SYN cookies
# See http://lwn.net/Articles/277146/
# Note: This may impact IPv6 TCP sessions too
net.ipv4.tcp_syncookies=1

# Uncomment the next line to enable packet forwarding for IPv4
#net.ipv4.ip_forward=1

# Uncomment the next line to enable packet forwarding for IPv6
#  Enabling this option disables Stateless Address Autoconfiguration
#  based on Router Advertisements for this host
#net.ipv6.conf.all.forwarding=1


###################################################################
# Additional settings - these settings can improve the network
# security of the host and prevent against some network attacks
# including spoofing attacks and man in the middle attacks through
# redirection. Some network environments, however, require that these
# settings are disabled so review and enable them as needed.
#
# Do not accept ICMP redirects (prevent MITM attacks)
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
# _or_
# Accept ICMP redirects only for gateways listed in our default
# gateway list (enabled by default)
# net.ipv4.conf.all.secure_redirects = 1
#
# Do not send ICMP redirects (we are not a router)
net.ipv4.conf.all.send_redirects = 0
#
# Do not accept IP source route packets (we are not a router)
#net.ipv4.conf.all.accept_source_route = 0
#net.ipv6.conf.all.accept_source_route = 0
#
# Log Martian Packets
net.ipv4.conf.all.log_martians = 1
#
vm.swappiness = 0
vm.dirty_ratio = 3
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_wmem = 4096 87380 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_no_metrics_save = 1
net.ipv4.tcp_moderate_rcvbuf = 1
net.core.netdev_max_backlog = 5000
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv4.tcp_syncookies = 1
net.ipv4.icmp_echo_ignore_all = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.default.secure_redirects = 0
net.ipv4.icmp_ignore_bogus_error_responses = 1
net.ipv4.tcp_timestamps = 0
net.ipv4.ip_local_port_range = 1024 65000
fs.file-max = 204708
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.eth0.rp_filter = 1
net.ipv4.tcp_rfc1337 = 1
kernel.threads-max = 131072
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_window_scaling = 1
net.ipv4.tcp_keepalive_time = 10
net.ipv4.tcp_keepalive_probes = 2
net.ipv4.tcp_keepalive_intvl = 3
kernel.panic = 60

#kernel.yield_type = 2
#kernel.interactive = 0
#kernel.rr_interval = 1

#kernel.nr_requests = 128
#kernel.read_ahead_kb = 16384
#kernel.rq_affinity = 2
#kernel.add_random = 0
#kernel.sched_nr_migrate = 128
#kernel.sched_rt_period_us = 1000000
#kernel.sched_rt_runtime_us = 980000
#net.ipv4.tcp_congestion_control=westwood
        """)
        f3.close()

        f4=open("/etc/init.d/rc")
        lines2 = f4.readlines()
        f4.close()
        f4s=open("/etc/init.d/rc","w")
        for line2 in lines2:
            f4s.write("%s" % (re.sub("CONCURRENCY=makefile","CONCURRENCY=shell",line2)))
            print(line2[:-1])
        f4s.close()
#jsay
    def talk(self,text,voice):
        if(voice == "mei_happy"):
            modelv = homedir+"alisa/file/mei/mei_happy.htsvoice"
        if(voice == "mei_angry"):
            modelv = homedir+"alisa/file/mei/mei_angry.htsvoice"
        if(voice == "mei_bashful"):
            modelv = homedir+"alisa/file/mei/mei_bashful.htsvoice"
        if(voice == "mei_normal"):
            modelv = homedir+"alisa/file/mei/mei_normal.htsvoice"
        if(voice == "mei_sad"):
            modelv = homedir+"alisa/file/mei/mei_sad.htsvoice"
        if(voice == "miku_a"):
            modelv = homedir+"alisa/file/miku/TYPE-α.htsvoice"
        if(voice == "miku_b"):
            modelv = homedir+"alisa/file/miku/TYPE-β.htsvoice"
        if(voice == "tohoku_angry"):
            modelv = homedir+"alisa/file/tohoku/tohoku-f01-angry.htsvoice"
        if(voice == "tohoku_happy"):
            modelv = homedir+"alisa/file/tohoku/tohoku-f01-happy.htsvoice"
        if(voice == "tohoku_neutral"):
            modelv = homedir+"alisa/file/tohoku/tohoku-f01-neutral.htsvoice"
        if(voice == "tohoku_sad"):
            modelv = homedir+"alisa/file/tohoku/tohoku-f01-sad.htsvoice"
        sp.call("""TMP=/tmp/jsay.wav
echo %s | open_jtalk \
-x "/var/lib/mecab/dic/open-jtalk/naist-jdic" \
-m %s \
-ow $TMP && \
aplay --quiet $TMP
rm -f $TMP""" % (text,modelv),shell=True)
#Changed PNG to JPEG
    def png2jpg(self):
        inputdir = sys.argv[2]
        outputdir = sys.argv[3]
        dirbase = sorted(set(os.listdir(inputdir)))
        try:
            os.mkdir(outputdir)
        except:pass
        for i in range(len(dirbase)):
            if i<10:
                sp.call("convert "+inputdir+"/"+dirbase[i] + " "+outputdir+"/000"+str(i)+".jpg",shell=True)
            elif i>=10 and i<100:
                sp.call("convert "+inputdir+"/"+dirbase[i] + " "+outputdir+"/00"+str(i)+".jpg",shell=True)
            elif i>=100 and i<1000:
                sp.call("convert "+inputdir+"/"+dirbase[i] + " "+outputdir+"/0"+str(i)+".jpg",shell=True)
            elif i>=1000 and i<10000:
                sp.call("convert "+inputdir+"/"+dirbase[i] + " "+outputdir+"/"+str(i)+".jpg",shell=True)
        os.chdir(outputdir)
        sp.call("mogrify -geometry %sx%s -quality %s *.jpg" % (argvs[4],argvs[5],argvs[6]),shell=True)

#Changed PNG to GIF
    def png2gif(self):
        inputdir = sys.argv[2]
        outputdir = sys.argv[3]
        dirbase = sorted(set(os.listdir(inputdir)))
        try:
            os.mkdir(outputdir)
        except:pass
        for i in range(len(dirbase)):
            if i<10:
                sp.call("convert "+inputdir+"/"+dirbase[i]+" "+outputdir+"/000"+str(i)+".gif",shell=True)
            elif i>=10 and i<100:
                sp.call("convert "+inputdir+"/"+dirbase[i]+" "+outputdir+"/00"+str(i)+".gif",shell=True)
            elif i>=100 and i<1000:
                sp.call("convert "+inputdir+"/"+dirbase[i]+" "+outputdir+"/0"+str(i)+".gif",shell=True)
            elif i>=1000 and i<10000:
                sp.call("convert "+inputdir+"/"+dirbase[i]+" "+outputdir+str(i)+".gif",shell=True)
        os.chdir(outputdir)
        sp.call("mogrify -geometry %sx%s -quality %s *.gif" % (argvs[4],argvs[5],argvs[6]),shell=True)
#Changed GIF to PNG
    def gif2png(self):
        inputdir = sys.argv[2]
        outputdir = sys.argv[3]
        dirbase = sorted(set(os.listdir(inputdir)))
        try:
            os.mkdir(outputdir)
        except:pass
        for i in range(len(dirbase)):
            if i<10:
                sp.call("convert "+inputdir+"/"+dirbase[i]+" "+outputdir+"/000"+str(i)+".png",shell=True)
            elif i>=10 and i<100:
                sp.call("convert "+inputdir+"/"+dirbase[i]+" "+outputdir+"/00"+str(i)+".png",shell=True)
            elif i>=100 and i<1000:
                sp.call("convert "+inputdir+"/"+dirname[i]+" "+outdir+"/0"+str(i)+".png",shell=True)
            elif i>=1000 and i<10000:
                sp.call("convert "+inputdir+"/"+dirname[i]+" "+outdir+"/"+str(i)+".png",shell=True)
        os.chdir(outputdir)
        sp.call("mogrify -geometry %sx%s -quality %s *.png" % (argvs[4],argvs[5],argvs[6]),shell=True)
#rotate JPEG
    def rotateJPEG(self):
        dir = sys.argv[2]
        os.chdir(dir)
        sp.call("mogrify -rotate %s *.jpg" % (argvs[3]),shell=True)
#movie2jpg
    def movie2jpg(self):
        dir = argvs[2]
        try:
            os.mkdir(dir)
        except:
            print("It is already.")
        os.chdir(dir)
        sp.call('avconv -i %s -r 24 -qscale 1 -vf "scale=%s:%s" -f image2 image-%03d.jpg' % (argvs[3],argvs[4],argvs[5]),shell=True)
#apng
    def apng(self):
        dir = argvs[2]
        outputpng = argvs[2] + ".png"
        os.chdir(dir)
        fps = argvs[5]
        sp.call('apngasm %s %s/*.png 1 %s' % (outputpng,dir,fps),shell=True)
#asvg
    def animationSVG(self):
        dir = argvs[2]+"/"
        dirbase = os.listdir(argvs[2])
        imagearr = sorted(set([dirbase[i] for i in range(len(dirbase))]))
        outputsvg = argvs[2]+".svg"
        objwidth = argvs[3]
        objheight = argvs[4]
        fps = argvs[5]
        datau = "data:image/jpeg;base64,"
        animrange = len(imagearr)
        base64arr = []
        for i in imagearr:
            file = open(dir+i,"rb")
            fr = base64.encodestring(file.read())
            decfile = fr.decode("utf-8")
            base64arr.append(decfile)
            file.close()
        svgfile = open(outputsvg,"w")
        svgfile.write("""<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg[
 <!ATTLIST image width CDATA "100%"
     height CDATA "100%"
     preserveAspectRatio CDATA "none">
 <!ENTITY fname "bath001/ss">
]>
        """)
        svgfile.write("""<svg width="%spx" height="%spx" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="main">
 <defs>
        """ % (objwidth,objheight))
        for i in range(animrange):
            svgfile.write("<image xlink:href='"+datau+base64arr[i]+"' id='f"+str(i+1)+"' />\n")
        svgfile.write("""
 </defs>
 <use>
  <animate attributeName="xlink:href" begin="0s" dur="%ss" repeatCount="indefinite" values="
        """ %(fps))
        for i in range(1,animrange):
            svgfile.write("#f"+str(i)+";")
        svgfile.write("""#f3" />
 </use>
</svg>
        """)
        print(svgfile)
        svgfile.close()

#ahtml.py
    def ahtml(self):
        dir = str(argvs[2])+"/"
        dirbase = os.listdir(argvs[2])
        imagearr = sorted(set([dirbase[i] for i in range(len(dirbase))]))
        outputhtml = str(argvs[2])+".html"
        objwidth = argvs[3]
        objheight = argvs[4]
        intervalTime = 50;
        datau = "data:image/jpeg;base64,"
        animrange = len(imagearr)
        base64arr = []
        for i in imagearr:
            file = open(dir+i,"rb")
            fr = base64.encodestring(file.read())
            decfile = fr.decode("utf-8")
            base64arr.append(decfile)
            file.close()
        htmlfile = open(outputhtml,"w")
        htmlfile.write("""<!DOCTYPE html>
<html lang="ja">
<head>
    <style type="text/css">
        #imgobj{
            width:%spx;
            height:%spx;
        }
    </style>
</head>
<body>
<img src="" alt="" id="imgobj"/>
<script type="text/javascript">
jsarr = [
        """ % (objwidth,objheight))
        for i in range(animrange):
            htmlfile.write("'"+dir+imagearr[i]+"',")
        htmlfile.write("""'%s'];
imgobj = document.getElementById("imgobj");
var i = 0;
var si = setInterval(function(){
    imgobj.src = jsarr[i];
    i++;
    if(i>jsarr.length-1){clearInterval(si);}
},%s);
</script>
</body>
</html>
        """ % (dir+imagearr[-1],intervalTime))
        htmlfile.close()

#soundconverter
    def mp3ogg(self):
        sp.call("ffmpeg -i " + arg[2] + ".mp3 -ab " + arg[3] + "k " + arg[2] + ".ogg",shell=True)
    def oggmp3(self):
        sp.call("ffmpeg -i " + arg[2] + ".ogg -ab " + arg[3] + "k " + arg[2] + ".mp3",shell=True)
    def aacogg(self):
        sp.call("ffmpeg -i " + arg[2] + ".aac -ab " + arg[3] + "k " + arg[2] + ".ogg",shell=True)
    def aacmp3(self):
        sp.call("ffmpeg -i " + arg[2] + ".aac -ab " + arg[3] + "k " + arg[2] + ".mp3",shell=True)
    def mp3aac(self):
        sp.call("ffmpeg -i " + arg[2] + ".mp3 -ab " + arg[3] + "k " + arg[2] + ".aac",shell=True)
#image info
    def image_info(self,image_src):
        from PIL import Image
        img = Image.open(image_src)
        print("format：%s,size： %s,colormode： %s" % (img.format,img.size,img.mode))
#image flip
    def image_flip(self,image_src,image_mode):
        from PIL import Image
        img = Image.open(image_src)
        if image_mode == "left_right":
            its = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif image_mode == "top_bottom":
            its = img.transpose(Image.FLIP_TOP_BOTTOM)
        its.show()
#image filter edges
    def image_filter_edges(self,image_src,ang):
        from PIL import Image,ImageFilter
        img7 = Image.open(image_src)
        rimg = img7.filter(ImageFilter.FIND_EDGES).rotate(ang)
        rimg.show()
#sudoku
    def sudoku(self):
        import sys;L=[];S=lambda D:(0in D)and[L.append(D.index(0)),[(D.__setitem__(L[-1],i),S(D),D.__setitem__(L.pop(),0))for i in set(range(1,10))-set(D[L[-1]/9*9:L[-1]/9*9+9]+D[L[-1]%9:81:9]+[d for n in(0,1,2)for d in D[L[-1]/27*27+L[-1]%9/3*3+n*9:L[-1]/27*27+L[-1]%9/3*3+n*9+3]])]]or([sys.stdout.write('%d'%d+('\n'if i%9==8 else' '))for i,d in enumerate(D)],sys.exit());S([int(c)if c!='.'else 0for c in'..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..'])

#自動文章作成
class PrepareChain(object):
    BEGIN = u"__BEGIN_SENTENCE__"
    END = u"__END_SENTENCE__"

    DB_PATH = "alisa/chain.db"
    DB_SCHEMA_PATH = "alisa/schema.sql"

    def __init__(self, text):
        # if isinstance(text, str):
            # text = text.decode("utf-8")
        self.text = text
        self.tagger = MeCab.Tagger('-Ochasen')

    def make_triplet_freqs(self):
        sentences = self._divide(self.text)
        triplet_freqs = defaultdict(int)
        for sentence in sentences:
            morphemes = self._morphological_analysis(sentence)
            triplets = self._make_triplet(morphemes)
            for (triplet, n) in triplets.items():
                triplet_freqs[triplet] += n

        return triplet_freqs

    def _divide(self, text):
        delimiter = u"。|．|\."
        text = re.sub(r"({0})".format(delimiter), r"\1\n", text)
        sentences = text.splitlines()
        sentences = [sentence.strip() for sentence in sentences]

        return sentences

    def _morphological_analysis(self, sentence):
        morphemes = []
        # sentence = sentence.encode("utf-8")
        node = self.tagger.parseToNode(sentence)
        while node:
            if node.posid != 0:
                try:
                    #morpheme = node.surface.decode("utf-8")
                    morpheme = node.surface
                except UnicodeDecodeError:
                    morpheme = node.surface.decode("latin-1")
                #morpheme = node.surface
                morphemes.append(morpheme)
            node = node.next
        return morphemes

    def _make_triplet(self, morphemes):
        if len(morphemes) < 3:
            return {}

        triplet_freqs = defaultdict(int)

        # for i in xrange(len(morphemes)-2):
        for i in range(len(morphemes)-2):
            triplet = tuple(morphemes[i:i+3])
            triplet_freqs[triplet] += 1

        triplet = (PrepareChain.BEGIN, morphemes[0], morphemes[1])
        triplet_freqs[triplet] = 1

        triplet = (morphemes[-2], morphemes[-1], PrepareChain.END)
        triplet_freqs[triplet] = 1

        return triplet_freqs

    def save(self, triplet_freqs, init=False):

        con = sqlite3.connect(PrepareChain.DB_PATH)

        if init:
            with open(PrepareChain.DB_SCHEMA_PATH, "r") as f:
                schema = f.read()
                con.executescript(schema)

            datas = [(triplet[0], triplet[1], triplet[2], freq) for (triplet, freq) in triplet_freqs.items()]

            p_statement = u"insert into chain_freqs (prefix1, prefix2, suffix, freq) values (?, ?, ?, ?)"
            con.executemany(p_statement, datas)

        con.commit()
        con.close()

    def show(self, triplet_freqs):
        for triplet in triplet_freqs:
            print("|".join(triplet), "\t", triplet_freqs[triplet])

class GenerateText(object):
    def __init__(self, n=5):
        self.n = n

    def generate(self):
        if not os.path.exists(PrepareChain.DB_PATH):
            raise IOError(u"DBファイルが存在しません")

        con = sqlite3.connect(PrepareChain.DB_PATH)
        con.row_factory = sqlite3.Row

        generated_text = u""

        for i in range(self.n):
            text = self._generate_sentence(con)
            generated_text += text

        con.close()

        return generated_text

    def _generate_sentence(self, con):

        morphemes = []

        first_triplet = self._get_first_triplet(con)
        morphemes.append(first_triplet[1])
        morphemes.append(first_triplet[2])

        while morphemes[-1] != PrepareChain.END:
            prefix1 = morphemes[-2]
            prefix2 = morphemes[-1]
            triplet = self._get_triplet(con, prefix1, prefix2)
            morphemes.append(triplet[2])

        result = "".join(morphemes[:-1])

        return result

    def _get_chain_from_DB(self, con, prefixes):
        sql = u"select prefix1, prefix2, suffix, freq from chain_freqs where prefix1 = ?"

        if len(prefixes) == 2:
            sql += u" and prefix2 = ?"

        result = []

        cursor = con.execute(sql, prefixes)
        for row in cursor:
            result.append(dict(row))

        return result

    def _get_first_triplet(self, con):
        prefixes = (PrepareChain.BEGIN,)

        chains = self._get_chain_from_DB(con, prefixes)

        triplet = self._get_probable_triplet(chains)

        return (triplet["prefix1"], triplet["prefix2"], triplet["suffix"])

    def _get_triplet(self, con, prefix1, prefix2):
        prefixes = (prefix1, prefix2)

        chains = self._get_chain_from_DB(con, prefixes)

        triplet = self._get_probable_triplet(chains)

        return (triplet["prefix1"], triplet["prefix2"], triplet["suffix"])

    def _get_probable_triplet(self, chains):
        probability = []

        for (index, chain) in enumerate(chains):
            # for j in xrange(chain["freq"]):
            for j in range(chain["freq"]):
                probability.append(index)

        chain_index = random.choice(probability)

        return chains[chain_index]

if __name__ == "__main__":
    v = viper()
    try:
        if argvs[1] == "importapps":
            v.installApplications()
        if argvs[1] == "importextraapps":
            v.installExtraApplications()
        if argvs[1] == "pymodules":
            v.installPythonModules()
        if argvs[1] == "ppa":
            v.addPPA()
        if argvs[1] == "jsay":
            v.talk(argvs[2],argvs[3])
        if(argvs[1] == "png2jpg"):
            v.png2jpg()
        if(argvs[1] == "png2gif"):
            v.png2gif()
        if(argvs[1] == "gif2png"):
            v.gif2png()
        if(argvs[1] == "rotatejpg"):
            v.rotateJPEG()
        if(argvs[1] == "movie2jpg"):
            v.movie2jpg()
        if(argvs[1] == "asvg"):
            v.animationSVG()
        if(argvs[1] == "apng"):
            v.apng()
        if(argvs[1] == "ahtml"):
            v.ahtml()
        if argvs[1] == "mp3ogg":
            v.mp3ogg()
        if argvs[1] == "oggmp3":
            v.oggmp3()
        if argvs[1] == "aacogg":
            v.aacogg()
        if argvs[1] == "aacmp3":
            v.aacmp3()
        if argvs[1] == "mp3aac":
            v.mp3aac()
        if argvs[1] == "uninstall":
            sp.call("""pip freeze > piplist.txt
sudo pip uninstall -r piplist.txt
            """,shell=True)
        if argvs[1] == "findmodule":
            v.findModule()
        if argvs[1] == "httpclient":
            v.http_client(argvs[2])
        if argvs[1] == "imageinfo":
            v.image_info(argvs[2])
        if argvs[1] == "imageflip":
            v.image_flip(argvs[2],argvs[3])
        if argvs[1] == "imagefilteredges":
            v.image_filter_edges(argvs[2],argvs[3])
        if argvs[1] == "sudoku":
            v.sudoku()
        if argvs[1] == "valkyrie":
            v.setupValkyrie()
            v.installApplications()
            #self.set_sources_list()
            #self.set_plymouth()
            sp.call("sudo apt-get clean",shell=True)
            #os.system("sudo apt-get autoremove")
            #self.del_dpkg_info()
            #os.system("fc-cache -f -v")
            #os.system("umount valkyrie_tmp")
            print("Finish")
        if argvs[1] == "deldpkginfo":
            v.del_dpkg_info()
        if argvs[1] == "suckout":
            v.suckout()
        if argvs[1] == "faststart":
            v.faststart()
        if argvs[1] == "deldpkginfo":
            v.del_dpkg_info()
    except:pass
