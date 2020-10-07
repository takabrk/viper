#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
movie_encoding.py
Copyright@ takamitu hamada
version :  20170121
License      :  BSD License
Web site URL :  http://valkyrieviper.space
"""
import os,sys
import subprocess as sp
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
argv = sys.argv
class movieencoder(object):
    def __init__(self):
        if argv[1] == "import":
            sp.call("cp -a ../valkyrie_desktop/valkyrie_tmp/etc/apt /etc".strip().split(" "))
            sp.call("sudo apt-get update".strip().split(" "))
            sp.call("sudo apt-get install handbrake-cli handbrake-gtk".strip().split(" "))

        if argv[1] == "handbrake":
            self.handbrake()
        if argv[1] == "avc":
            self.convertAVC()
        if argv[1] == "mp3":
            self.convertMP3()
        if argv[1] == "mp4box":
            self.MP4BOX()
        if argv[1] == "moviemarge":
            self.movieMarge()
        if argv[1] == "avi2mp4":
            self.avi2mp4()
        if argv[1] == "mp4mux":
            self.mp4_mux()
        if argv[1] == "mp4demux":
            self.mp4_demux()
        if argv[1] == "avs":
            self.createAVS()
        if argv[1] == "avsffmpeg":
            self.createAVSwithFFMPEG()
    def handbrake(self):
        cmdhb = 'HandBrakeCLI -e x264 -q 20.0 -r 29.97 --cfr --crop 0:0:0:0 -E lame -B 192 -R Auto -f mp4 -i %s -o %s.m4v --width %s --height %s --custom-anamorphic --display-width %s' % (argv[2],argv[3],argv[4],argv[5],argv[6])
        sp.call(cdmdhb.strip().split(" "))
    def convertAVC(self):
        cmdavc = 'x264 --bitrate %s --fps %s --aq-mode 0 --psy-rd 0.5:0 --qpmin 1 --qpstep 16 --scenecut 54 --min-keyint 1 --keyint 300 --8x8dct --partitions "p8x8,b8x8,p4x4,i4x4" --bframes 2 --b-adapt 2 --ref 3 --mixed-refs --direct "auto" --me "hex" --subme 5 --no-chroma-me --threads auto --trellis 2 --cqm "jvt" --no-fast-pskip --no-dct-decimate -o "%s" "%s"' % (argv[2],argv[3],argv[4],argv[5])
        sp.call(cmdavc.strip().split(" "))
    def convertMP3(self):
        cmd = 'lame --vbr-new -V0 -b %d -F -f -m s --notemp --nores --interch 1 -p %s pre.mp3' % (arg[2],arg[3])
        sp.call(cmd.strip().split(" "))
    def MP4BOX(self):
        cmd += 'MP4Box -fps %d -add "%s"#video -add "%s"#audio -new %s' % (arg[2],arg[3],arg[4],arg[5])
        sp.call(cmd.strip().split(" "))
    def movieMarge(self):
        cmd = 'MP4Box -add %s -cat %s -new %s' % (arg[2],arg[3],arg[4])
        sp.call(cmd.strip()ssplit(" "))
    def avi2mp4(self,avi_src,output_new,mp4_fps):
        cmd = 'MP4Box -fps %d -add %s -new %s' % (arg[2],arg[3],arg[4])
        sp.call(cmd.strip().split(" "))
    def mp4_mux(self,input_video,input_audio,output_new,mp4_fps):
        cmd = 'MP4Box -fps %d -add %s#video -add %s#audio -new %s' % (arg[2],arg[3],arg[4],arg[5])
        sp.call(cmd.strip().split(" "))
    def mp4_demux(self):
        cmd = 'MP4Box -raw 1 %s' % (arg[2])
        cmd += 'MP4Box -raw 2 %s' % (arg[2])
        sp.call(cmd.strip().split(" "))
    def createAVS(self):
        f1 = open("infile.avs","w")
        f1.write('avisource("%s")' % (arg[2]))
        #f1.write('AssumeFPS(29.970)')
        f1.write('ConvertToYV12()')
        f1.write('return last')
        f1.close()
    def createAVSwithFFMPEG(self):
        f1 = open("infile.avs","w")
        f1.write('LoadPlugin("FFMpegSource.dll")')
        f1.write('FFmpegSource(%s)' % (arg[2]))
        f1.write('Lanczos4Resize(%s,%s)' % (arg[3],arg[4]))
        f1.write('AssumeFPS(29.970)')
        f1.write('ConvertToYV12()')
        f1.write('return last')
if __name__ == "__main__":
    me = movieencoder()



