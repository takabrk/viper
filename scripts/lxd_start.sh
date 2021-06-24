#!/bin/sh
lxc launch ubuntu:20.04 steam
lxc exec steam -- sh -c \
  "apt update && apt full-upgrade -y && apt autoremove -y"
lxc config set steam raw.idmap 'both 1000 1000'
lxc exec steam -- dpkg --add-architecture i386
lxc exec steam -- sh -c 'apt update && apt install -y \
  x11-apps mesa-utils libgl1-mesa-glx:i386 \
  libcanberra-gtk-module:i386 pulseaudio dbus-x11 \
  language-pack-ja fonts-noto-cjk-extra \
  fonts-noto-color-emoji'
lxc exec steam -- update-locale LANG=ja_JP.UTF-8
lxc exec steam -- timedatectl set-timezone Asia/Tokyo
 lxc exec steam -- sed -i "s/; enable-shm = yes/enable-shm = no/g" /etc/pulse/client.conf
lxc exec steam -- sh -c "echo export PULSE_SERVER=unix:/tmp/.pulse-native | tee --append /home/ubuntu/.profile"
lxc config device add steam pa disk source=/run/user/1000/pulse/native path=/tmp/.pulse-native
lxc exec steam -- usermod -aG video ubuntu
lxc config set steam environment.DISPLAY :0
lxc config device add steam xorg disk \
  source=/tmp/.X11-unix/X0 path=/tmp/.X11-unix/X0
lxc config device add steam mygpu gpu \
  gid=`getent group video | cut -d: -f3`
lxc config set steam boot.autostart false

#lxc exec steam -- \
  wget https://steamcdn-a.akamaihd.net/client/installer/steam.deb
#lxc exec steam -- apt install -y ./steam.deb

#lxc restart steam

#lxc exec steam -- sudo --user=ubuntu --login steam