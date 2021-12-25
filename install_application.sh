#!/bin/sh
sudo apt purge libreoffice-*
sudo apt purge thunderbird*
sudo apt purge transmission*
sudo apt install openbox
sudo apt install lxqt-core
sudo apt install obconf-qt lxappearance lxrandr lxinput
sudo apt install dunst tint2 gmrun stalonetray
sudo apt install xfce4-terminal xfce4-taskmanager xfce4-power-manager xfce4-screenshooter
sudo apt install network-manager-gnome
sudo apt install gnumeric abiword
sudo apt install mozc-server mozc-utils-gui
sudo apt install emacs emacs-mozc
sudo apt install fcitx fcitx-mozc
sudo apt install mousepad
sudo apt install firefox
sudo apt install gimp gimp-gap gimp-plugin-registry gimp-gimic
sudo apt install pulseaudio pavucontrol pulseaudio-utils
sudo apt install pulseaudio-module-jack jackd jackd2 qjackctl
sudo apt install alsamixergui gnome-alsamixer
sudo apt install mpv audacious audacity asunder galculator soundconverter
sudo apt install glade 
sudo apt install blueman
sudo apt install imagemagick
sudo apt install lightdm
sudo apt install ffmpeg obs-studio
sudo apt install gparted
sudo apt install radeon-profile
sudo apt install python-tk python3-tk python3-sphinx
sudo apt install libllvm10 libjpeg8 libjpeg8-dev zlib1g-dev
sudo apt install libfreetype6 libfreetype6-dev apache2
sudo apt install libncurses5-dev
sudo apt install build-essential kernel-package fakeroot git
sudo apt purge texlive*
sudo apt purge ruby*
sudo apt install python3-pip python-pip
sudo apt install libapache2-mod-php7.2 mysql-common php7.2-mysql libmysqlclient20 mysql-server-5.2
sudo apt install open-jtalk mecab mecab-utils mecab-naist-jdic mecab-naist-jdic-eucjp mecab-jumandic
sudo apt install ppsspp
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
sudo apt install winehq-staging winetricks steam-installer
sudo apt install nodejs
sudo apt install chromium-browser

#widebine
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
mkdir chrome-dir
dpkg-deb -x google-chrome-stable_current_amd64.deb chrome-dir
sudo cp -a chrome-dir/opt/google/chrome/WidevineCdm /usr/lib/chromium-browser
#sudo cp -a chrome-dir/opt/google/chrome/libwidevinecdmadapter.so /usr/lib/chromium-browser
#sudo unsquashfs /var/lib/snapd/snaps/chromium_343.snap
#sudo mv squashfs-root /var/lib/snapd/snaps
#sudo rm -r /var/lib/snapd/snaps/chromium_343.snapold
#sudo mv /var/lib/snapd/snaps/chromium_343.snap /var/lib/snapd/snaps/chromium_343.snapold
#sudo rm -r /var/lib/snapd/snaps/chromium_343.snap
#sudo cp -a chrome-dir/opt/google/chrome/libwidevinecdm.so /var/lib/snapd/snaps/squashfs-root/#usr/lib/chromium-browser
#sudo cp -a chrome-dir/opt/google/chrome/libwidevinecdmadapter.so /var/lib/snapd/snaps/#squashfs-root/usr/lib/chromium-browser
#sudo mksquashfs /var/lib/snapd/snaps/squashfs-root /var/lib/snapd/snaps/chromium_343.snap -#comp xz
rm -r chrome-dir
rm -r google-chrome-stable_current_amd64.deb
#rm -r squashfs-root
#sudo rm -r /var/lib/snapd/snaps/squashfs-root
echo Finished
