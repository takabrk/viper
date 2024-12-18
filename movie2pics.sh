#!/bin/sh
ffmpeg -ss $1 -t $2 -r $3 -i $4 $5/%04d.png
echo "Complete process"
