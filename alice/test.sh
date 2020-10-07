#!/bin/sh
TMP=/tmp/jsay.wav
echo "静波まつりちゃんを紹介します。" | open_jtalk \
-x "/var/lib/mecab/dic/open-jtalk/naist-jdic" \
-m "/home/valkyrie/viper/alice/file/mei/mei_happy.htsvoice" \
-ow $TMP && \
aplay --quiet $TMP
rm -f $TMP