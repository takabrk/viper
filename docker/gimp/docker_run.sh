#!/bin/sh

#docker run \
#    -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
#   -v /run/user/$UID/pulse/native:/tmp/pulse/native \
#    -v $HOME/.config/pulse/cookie:/tmp/pulse/cookie \
#   -it --rm takabrk/gimp -e DISPLAY=192.168.100.175:1

#docker run --rm -v /tmp/.X11-unix:/tmp/.X11-unix takabrk/gimp
#docker run -i --rm takabrk/ubuntu &

#docker run --rm --privileged --shm-size=1gb \
#    -v /run/udev:/run/udev \
#    -v /run/dbus:/run/dbus \
#    -v /run/systemd:/run/systemd \
#    takabrk/ubuntu

#docker run -it -d --name vsrx takabrk/ubuntu
#docker exec -it vsrx /bin/bash
docker run -ti --rm \
       -e DISPLAY=$DISPLAY \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       --name vsrx \
       takabrk/ubuntu
