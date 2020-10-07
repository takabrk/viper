#!/bin/sh
case $5 in
    h264_vaapi)
        #export LIBVA_DRIVER_NAME=iHD \
        ffmpeg -vaapi_device /dev/dri/$6 \
            -hwaccel vaapi \
            -hwaccel_output_format yuv420p \
            -i $1 \
            -vf "fps=29.97,format=nv12|vaapi,hwupload,scale_vaapi=w=$3:h=$4" \
            -c:v h264_vaapi -profile 100 -level 41 -q 20 -aspect 16:9 \
            -c:a aac -b:a 256k  \
            $2
            ;;\
     hevc_vaapi)
         ffmpeg -vaapi_device /dev/dri/$6 \
             -hwaccel vaapi \
             -hwaccel_output_format vaapi \
             -i $1 \
             -preset slow \
             -vf "fps=29.97,format=p010|vaapi,hwupload,scale_vaapi=w=$3:h=$4" \
             -c:v hevc_vaapi -profile 1 -level 51 -q 20 -aspect 16:9 \
            -c:a aac -b:a 256k  \
             $2
             ;;\
esac