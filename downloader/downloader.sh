#!/bin/sh

if [ -e /usr/local/bin/youtube-dl ]; then
    youtube-dl $1 -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "~/Downloads/%(title)s.(ext)s"
else
    sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl
    sudo chmod a+rx /usr/local/bin/youtube-dl
fi