#!/bin/sh

#sudo dpkg -i *.deb
#sudo cp -a ./linux_modules/lib /
sudo cp -a ./90-override.conf /etc/sysctl.d/
sudo cp -a ./daemon.conf /etc/pulse/
cp -a  ./.asoundrc ~/
cp -a ./autostart ~/.config/openbox/
sudo apt-get -y install pulseaudio  pavucontrol pulseaudio-utils pulseaudio-module-jack jackd jackd2 qjackctl alsamixergui gnome-alsamixer audacious audacious-plugins mpv gnome-mpv
sudo apt-get -y install openbox obconf-qt obmenu pcmanfm-qt lxappearance lxrandr lxinput lxsession-logout plank nitrogen xfce4-terminal xfce4-taskmanager xfce4-settings xfce4-power-manager network-manager-gnome chromium-browser
