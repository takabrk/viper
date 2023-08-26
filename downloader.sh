#!/bin/sh

if [ -e /usr/local/bin/yt-dlp ]; then
#    yt-dlp $1 -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "~/Downloads/%(title)s.(ext)s"
    yt-dlp $1 -f "bestvideo[ext=mp4][width <=? 1920][height <=? 1080][fps <=? 30]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "~/Downloads/%(title)s.(ext)s"
else
    sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
    sudo chmod a+rx /usr/local/bin/yt-dlp
fi