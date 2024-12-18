#!/bin/sh
#HLS Downloader
ffmpeg -i $1 -c copy -bsf:a aac_adtstoasc $2
echo "Download movie"
