#!/bin/sh
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