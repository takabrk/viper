#!/bin/sh

sudo apt update
sudo apt install -y autoconf automake cmake g++ libtool pkg-config libva-dev libdrm-dev libpciaccess-dev libx11-dev vainfo

mkdir -p ~/vaapi
cd ~/vaapi
git clone https://github.com/intel/libva
cd libva
sudo ./autogen.sh --prefix=/usr --libdir=/usr/lib/x86_64-linux-gnu
sudo make clean
sudo make
sudo make uninstall
sudo make install
sudo ldconfig

mkdir -p ~/vaapi/workspace
cd ~/vaapi/workspace
git clone https://github.com/intel/gmmlib
mkdir -p build
cd build
sudo cmake -DCMAKE_BUILD_TYPE= Release -DARCH=64 ../gmmlib
sudo make clean
sudo make
sudo make uninstall
sudo make install

cd ~/vaapi/workspace
git clone https://github.com/intel/media-driver
cd media-driver
git submodule init
git pull
mkdir -p ~/vaapi/workspace/build_media
cd ~/vaapi/workspace/build_media
sudo cmake ../media-driver \
-DMEDIA_VERSION="2.0.0" \
-DBS_DIR_GMMLIB=$PWD/../gmmlib/Source/GmmLib/ \
-DBS_DIR_COMMON=$PWD/../gmmlib/Source/Common/ \
-DBS_DIR_INC=$PWD/../gmmlib/Source/inc/ \
-DBS_DIR_MEDIA=$PWD/../media-driver \
-DCMAKE_INSTALL_PREFIX=/usr \
-DCMAKE_INSTALL_LIBDIR=/usr/lib/x86_64-linux-gnu \
-DINSTALL_DRIVER_SYSCONF=OFF \
-DLIBVA_DRIVERS_PATH=/usr/lib/x86_64-linux-gnu/dri
sudo make clean
sudo make
sudo make uninstall
sudo make install

export LIBVA_DRIVER_NAME=iHD
#sudo echo LIBVA_DRIVER_NAME=iHD >> /etc/environment
vainfo