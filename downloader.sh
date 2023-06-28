#!/bin/sh

#if [ -e /usr/local/bin/youtube-dl ]; then
if [ -e /usr/local/bin/yt-dlp ]; then
#    youtube-dl $1 -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "~/Downloads/%(title)s.(ext)s"
#    youtube-dl $1 -f "bestvideo[ext=mp4][height <=? 720]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "~/Downloads/%(title)s.(ext)s"
    yt-dlp $1 -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "~/Downloads/%(title)s.(ext)s"
else
#    sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl
#    sudo chmod a+rx /usr/local/bin/youtube-dl
    sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
    sudo chmod a+rx /usr/local/bin/yt-dlp
fi