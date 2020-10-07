#!/bin/sh
dir = "~/Downloads/"
ffmpeg -i $1 -c copy -bsf:a aac_adtstoasc ${dir}$2