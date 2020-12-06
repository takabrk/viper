#!/bin/sh
case $5 in
    h264_vaapi)
        #export LIBVA_DRIVER_NAME=iHD \
        cd $1
        ls *.mp4 | sed 's/\.mp4$//' | xargs -I@ ffmpeg -y -vaapi_device /dev/dri/$6 \
            -i @.mp4 \
            -vf "fps=$9,format=nv12,hwupload,scale_vaapi=w=$3:h=$4" \
            -c:v h264_vaapi -profile:v 100 -level 41 -b:v $7 -aspect 16:9 \
            -c:a aac -b:a $8  \
            $2/@-ext.mp4
            ;;\
     hevc_vaapi)
         ffmpeg -y -vaapi_device /dev/dri/$6 \
             -i $1 \
             -vf "fps=$9,format=p010,hwupload,scale_vaapi=w=$3:h=$4" \
             -c:v hevc_vaapi -profile:v 2 -level 51 -b:v $7  -aspect 16:9 \
            -c:a aac -b:a $8  \
             $2
             ;;\
esac