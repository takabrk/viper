#!/usr/bin/env python
#-*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.path as path
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import numpy as np
import scipy.fftpack
from pylab import *
from PIL import Image,ImageColor,ImageDraw,ImageFilter
import pyglet
from pyglet.window import key
from pyglet.window import mouse

class mat(object):
    def __init__(self):
        pass
    def image_viewer(self,image_src):
        window = pyglet.window.Window()
        image = pyglet.resource.image(image_src)
        @window.event
        def on_draw():
            window.clear()
            image.blit(0,0)
        pyglet.app.run()
    def music_player(self,sound_src):
        music = pyglet.resource.media(sound_src,streaming=False)
        music.play()
        pyglet.app.run()

    def histogram_animation(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        data = np.random.randn(1000)
        n,bins = np.histogram(data,100)

        left = np.array(bins[:-1])
        right = np.array(bins[1:])
        bottom = np.zeros(len(left))
        top = bottom + n
        nrects = len(left)
        nverts = nrects*(1+3+1)
        verts = np.zeros((nverts,2))
        codes = np.ones(nverts,int)*path.Path.LINETO
        codes[0::5] = path.Path.MOVETO
        codes[4::5] = path.Path.CLOSEPOLY
        verts[0::5,0] = left
        verts[0::5,1] = bottom
        verts[1::5,0] = left
        verts[1::5,1] = top
        verts[2::5,0] = right
        verts[2::5,1] = top
        verts[3::5,0] = right
        verts[3::5,1] = bottom

        barpath = path.Path(verts,codes)
        patch = patches.PathPatch(barpath,facecolor = "green",edgecolor = "yellow",alpha=0.5)
        ax.add_patch(patch)

        ax.set_xlim(left[0],right[-1])
        ax.set_ylim(bottom.min(),top.max())

        def animate(i):
            data = np.random.randn(1000)
            n,bins = np.histogram(data,100)
            top = bottom +n
            verts[1::5,1] = top
            verts[2::5,1] = top
        ani = animation.FuncAnimation(fig,animate,100,repeat = False)
        plt.show()
    def animate_decay(self):
        xdata,ydata = [],[]
        def data_gen():
            t = data_gen.t
            cnt = 0
            while cnt < 1000:
                cnt += 1
                t += 0.05
                yield t,np.sin(2*np.pi*t)*np.exp(-t/10.)

        def run(data):
            t,y = data
            xdata.append(t)
            ydata.append(y)
            xmini,xmax = ax.get_xlim()

            if t>=max:
                ax.set_xlim(xmin,2*xmax)
                ax.figure.canvas.draw()
            line.set_data(xdata,ydata)
            return line,
        data_gen.t = 0
        fig = plt.figure()
        ax = fig.add_subplot(111)
        line, = ax.plot([],[],lw = 2)
        ax.set_ylim(-1.1,1.1)
        ax.set_xlim(0,5)
        ax.grid()

        ani = animation.FuncAnimation(fig,run,data_gen,blit=True,interval=10,repeat=False)
        plt.show()
    def random_line(self):
        def update_line(num,data,line):
            line.set_data(data[...,:num])
            return line,
        fig1 = plt.figure()
        data = np.random.rand(2,25)
        l, = plt.plot([],[],"r-")
        plt.xlim(0,1)
        plt.ylim(0,1)
        plt.xlabel("x")
        plt.title("test")
        line_ani = animation.FuncAnimation(fig1,update_line,25,fargs=(data,l),interval=50,blit=True)
        plt.show()
    def random_data_animation(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        line, = ax.plot(np.random.rand(10))
        ax.set_ylim(0,1)

        def update(data):
            line.set_ydata(data)
            return line,
        def data_gen():
            while True:
                yield np.random.rand(10)
        ani = animation.FuncAnimation(fig,update,data_gen,interval=100)
        plt.show()
    def gradation_animation(self):
        fig2 = plt.figure()
        x = np.arange(-9,10)
        y = np.arange(-9,10).reshape(-1,1)
        base = np.hypot(x,y)
        ims = []
        for add in np.arange(15):
            ims.append((plt.pcolor(x,y,base+add,norm=plt.Normalize(0,30)),))
        im_ani = animation.ArtistAnimation(fig2,ims,interval=50,repeat_delay = 3000,blit=True)
        plt.show()
    def contour3d(self):
        fig = plt.figure()
        ax = fig.gca(projection = "3d")
        X,Y,Z = axes3d.get_test_data(0.05)
        ax.plot_surface(X,Y,Z,rstride=8,cstride=8,alpha=0.3)
        cset = ax.contour(X,Y,Z,zdir="z",offset=-100,cmap=cm.coolwarm)
        cset = ax.contour(X,Y,Z,zdir="x",offset=-40,camp=cm.coolwarm)
        cset = ax.contour(X,Y,Z,zdir="y",offset=40,cmap=cm.coolwarm)
        plt.show()
    def bars3d(self):
        fig = plt.figure()
        ax = fig.add_subplot(111,projection="3d")
        for c,z in zip(["r","g","b","y"],[30,20,10,0]):
            xs = np.arange(20)
            ys = np.random.rand(20)
            cs = [c]*len(xs)
            ax.bar(xs,ys,zs=z,zdir="y",color=cs,alpha=0.8)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.show()
    def animate_bubble_sort(self):
        N = 60
        y = np.random.rand(N)*100
        def animated_func():
            for rect,h in zip(rects,x):
                rect.set_height(h)
                fig.canvas.draw()
        def animated_bubblesort():
            rects = plt.bar(range(N),y,1)
            for i in range(len(y)-1):
                for j in range(len(y)-1,i,-1):
                    if(y[j-1] > y[j]):
                        t = y[j]
                        y[j] = y[j-1]
                        y[j-1] = t
                        fig.canvas.draw()
                    for rect,h in zip(rects,y):
                        rect.set_height(h)
            fig.canvas.draw()
        fig = plt.figure()
        win = fig.canvas.manager.window
        win.after(50,animated_bubblesort)
        plt.show()
    def insertion(self):
        N = 60
        y = np.random.rand(N)*100

        def animated_func():
            for rect,h in zip(rects,x):
                rect.set_height(h)
            fig.canvas.draw()
        def animated_insertion():
            rects = plt.bar(range(N),y,1)
            for i in range(0,len(y)):
                for j in range(len(y)-1,i,-1):
                    if y[j-1] < y[j]:
                        continue
                    t = y[j]
                    y[j] = y[j-1]
                    y[j-1] = t
                    for rect,h in zip(rects,y):
                        rect.set_height(h)
                    fig.canvas.draw()
            fig.canvas.draw()
        fig = plt.figure()
        win = fig.canvas.manager.window
        win.after(50,animated_insertion)
        plt.show()
    def fft_amplitude_fig(self,wave_file):
        start=0
        N=256
        wf = wave.open(wave_file,"r")
        fs = wf.getframerate()
        x = wf.readframes(wf.getnframes())
        x = frombuffer(x,dtype="int16")/32768.0
        wf.close()
        X = np.fft.fft(x[start:start+N])
        freqList = np.fft.fftfreq(N,d=1.0/fs)
        subplot(111)
        plot(range(start,start+N),x[start:start+N])
        axis([start,start+N,-1.0,1.0])
        xlabel("time[sample]")
        ylabel("amplitude")
        show()
    def fft_amplitudeSpectrum(self,wave_file):
        start = 0
        N = 256
        wf = wave.open(wave_file,"r")
        fs = wf.getframerate()
        x = wf.readframes(wf.getnframes())
        x = frombuffer(x,dtype="int16")/32768.0
        wf.close()
        X = np.fft.fft(x[start:start+N])
        freqList = np.fft.fftfreq(N,d=1.0/fs)
        subplot(111)
        amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
        plot(freqList,amplitudeSpectrum,marker="o",linestyle="-")
        axis([0,fs/2,0,50])
        xlabel("frequenccy [Hz]")
        ylabel("amplitude sepctrum")
        show()
    def fft_phaseSpectrum(self,wave_file):
        start = 0
        N = 256
        wf = wave.open(wave_file,"r")
        fs = wf.getframerate()
        x = wf.readframes(wf.getnframes())
        x = frombuffer(x,dtype="int16")/32768.0
        wf.close()
        X = np.fft.fft(x[start:start+N])
        freqList = np.fft.fftfreq(N,d=1.0/fs)
        subplot(111)
        phaseSpectrum = [np.arctan2(int(c.imag),int(c.real)) for c in X]
        plot(freqList,phaseSpectrum,marker="o",linestyle="-")
        axis([0,fs/2,-np.pi,np.pi])
        xlabel("frequency [Hz]")
        ylabel("phase spectrum")
        show()
    def dynamic_image(self):
        fig = plt.figure()
        global x,y
        def f(x,y):
            return np.sin(x)+np.cos(y)
        x = np.linspace(0,2*np.pi,120)
        y = np.linspace(0,2*np.pi,100).reshape(-1,1)
        im = plt.imshow(f(x,y),cmap=plt.get_cmap("jet"))

        def updatefig(*args):
            global x,y
            x += np.pi/15.
            y += np.pi/20.
            im.set_array(f(x,y))
            return im,
        ani = animation.FuncAnimation(fig,updatefig,interval=50,blit=True)
        plt.show()
    def image_gradation(self,color1,color2,image_width,image_height):
        img2 = Image.new("RGB",(1,0x100))
        color_a = np.array(ImageColor.getrgb(color1))
        color_b = np.array(ImageColor.getrgb(color2))
        for y in xrange(0x100):
            color = (color_a*(0x100-y)+color_b*y)/0x100
            img2.putpixel((0,y),tuple(color.tolist()))
        img2 = img2.resize((image_width,image_height))
        img2.show()
if __name__ == ""__main__":
    pass
