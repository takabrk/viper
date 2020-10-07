#!/bin/sh
  
cpu_core=4
enable_h264=1
enable_h265=0
enable_vp8=1
enable_aac=1
enable_mp3=1
enable_ogg=1
enable_opus=1
enable_ass=0
  
src_dir="$HOME/ffmpeg_sources"
prefix_dir="/usr/local/ffmpeg_build"
  
export PATH=$prefix_dir/bin:$PATH
export PKG_CONFIG_PATH="$prefix_dir/lib/pkgconfig"
enable_option=""
  
repo_yasm="git://github.com/yasm/yasm.git"
repo_x264="https://git.videolan.org/git/x264.git"
repo_x265="https://github.com/videolan/x265.git"
repo_aac="git://github.com/mstorsjo/fdk-aac"
repo_opus="git://github.com/xiph/opus.git"
repo_libvpx="https://chromium.googlesource.com/webm/libvpx.git"
repo_libass="https://github.com/libass/libass.git"
repo_ffmpeg="git://github.com/FFmpeg/FFmpeg"
  
url_nasm="https://www.nasm.us/pub/nasm/releasebuilds/2.14.02/nasm-2.14.02.tar.bz2"
url_autoconf="http://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz"
url_lame="https://sourceforge.net/projects/lame/files/lame/3.100/lame-3.100.tar.gz"
url_ogg="https://ftp.osuosl.org/pub/xiph/releases/ogg/libogg-1.3.3.tar.gz"
url_theora="https://ftp.osuosl.org/pub/xiph/releases/theora/libtheora-1.1.1.tar.bz2"
url_vorbis="https://ftp.osuosl.org/pub/xiph/releases/vorbis/libvorbis-1.3.6.tar.gz"
  
gcc_ver=`gcc -dumpversion | awk -F. '{print $1}'`
  
if [ ${gcc_ver} -ge 6 ]; then
    # for x264, libvpx, ffmpeg
    pic_enable="--enable-pic"
    enable_option=${pic_enable}
fi
  
print_error()
{
    echo "error: $1"
}
  
run_git()
{
    repo="$1"
    opt="$2"
  
    dir=${repo##*/}
    dir=${dir%.git}
  
    if [ -d $dir ]; then
        cd $dir && git pull
        if [ $? -ne 0 ]; then
            print_error "git pull $dir" && exit 1
        fi
    else
        git clone $opt $repo
        if [ $? -ne 0 ]; then
            print_error "git clone $dir" && exit 1
        fi
        cd $dir
    fi
}
  
run_wget()
{
    url="$1"
    file=${url##*/}
    dir=${file%.tar.*}
  
    if [ ! -e $file ]; then
        wget $url
        if [ $? -ne 0 ]; then
            print_error "wget $file" && exit 1
        fi
    fi
  
    case $file in
        *.gz)  tar xvzf $file ;;
        *.bz2) tar xvjf $file ;;
    esac
  
    cd $dir
}
  
uid=`id | sed 's/uid=\([0-9]\+\)(.\+/\1/'`
  
if [ $uid -ne 0 ];then
    print_error "not root user"
    exit 1
fi
  
mkdir -p $src_dir
mkdir -p $prefix_dir
  
aconf_ver=`LANG=C autoconf -V | head -n 1 | sed -e "s/autoconf (GNU Autoconf) \([0-9]*\)\.\([0-9]*\)/\1\2/"`
if [ $aconf_ver -lt 269 ]; then
    echo "---------- build autoconf ----------"
    run_wget $url_autoconf
    ./configure --prefix="$prefix_dir" --bindir="$prefix_dir/bin"
    make -j${cpu_core}
    make install
    make distclean
fi
  
  
echo "---------- build Yasm ----------"
cd $src_dir
run_git $repo_yasm "--depth 1"
autoreconf -fiv
./configure --prefix="$prefix_dir" --bindir="$prefix_dir/bin"
make -j${cpu_core}
if [ $? -ne 0 ]; then
    print_error "make yasm" && exit 1
fi
make install
make distclean
  
  
echo "---------- build NASM ----------"
run_wget $url_nasm
./autogen.sh
./configure --prefix="$prefix_dir" --bindir="$prefix_dir/bin"
make -j${cpu_core}
if [ $? -ne 0 ]; then
    print_error "make nasm" && exit 1
fi
make install
make distclean
  
  
if [ $enable_h264 -eq 1 ]; then
    echo "---------- build libx264  ----------"
    cd $src_dir
    run_git $repo_x264 ""
    ./configure --prefix="$prefix_dir" --bindir="$prefix_dir/bin" --enable-static ${pic_enable}
    make -j${cpu_core}
    if [ $? -ne 0 ]; then
        print_error "make libx264" && exit 1
    fi
    make install
    make distclean
    enable_option="${enable_option} --enable-libx264"
fi
  
  
if [ $enable_h265 -eq 1 ]; then
    echo "---------- build libx265  ----------"
    cd $src_dir
    if [ -e "/etc/centos-release" ]; then
    if [ -d "x265" ]; then
        cd x265 && hg update
            if [ $? -ne 0 ]; then
        print_error "hg clone x265" && exit 1
            fi
    else
        hg clone https://bitbucket.org/multicoreware/x265
            if [ $? -ne 0 ]; then
        print_error "hg update x265" && exit 1
            fi
        cd x265
    fi
    else
    run_git $repo_x265 "-b 2.8"
    fi
  
    cd build/linux
    cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$prefix_dir" -DENABLE_SHARED:bool=off ../../source
    make -j${cpu_core}
    if [ $? -ne 0 ]; then
        print_error "make libx265" && exit 1
    fi
    make install
    make clean
    enable_option="${enable_option} --enable-libx265"
fi
  
  
if [ $enable_aac -eq 1 ]; then
    echo "---------- build libfdk_aac ----------"
    cd $src_dir
    run_git $repo_aac "--depth 1"
    autoreconf -fiv
    ./configure --prefix="$prefix_dir" --disable-shared
    make -j${cpu_core}
    if [ $? -ne 0 ]; then
        print_error "make libfdk_aac" && exit 1
    fi
    make install
    make distclean
    enable_option="${enable_option} --enable-libfdk-aac"
fi
  
  
if [ $enable_mp3 -eq 1 ]; then
    echo "---------- build libmp3lame ----------"
    cd $src_dir
    run_wget $url_lame
    ./configure --prefix="$prefix_dir" --bindir="$prefix_dir/bin" --disable-shared --enable-nasm
    make -j${cpu_core}
    if [ $? -ne 0 ]; then
        print_error "make libmp3lame" && exit 1
    fi
    make install
    make distclean
    enable_option="${enable_option} --enable-libmp3lame"
fi
  
  
if [ $enable_opus -eq 1 ]; then
    echo "---------- build libopus ----------"
    cd $src_dir
    run_git $repo_opus ""
    ./autogen.sh
    ./configure --prefix="$prefix_dir" --disable-shared
    make -j${cpu_core}
    if [ $? -ne 0 ]; then
        print_error "make libopus" && exit 1
    fi
    make install
    make distclean
    enable_option="${enable_option} --enable-libopus"
fi
  
  
if [ $enable_ogg -eq 1 ]; then
    echo "---------- build libogg  ----------"
    cd $src_dir
    run_wget $url_ogg
    ./configure --prefix="$prefix_dir" --disable-shared
    make -j${cpu_core}
    if [ $? -ne 0 ]; then
        print_error "make libogg" && exit 1
    fi
    make install
    make distclean
  
    echo "---------- build libvorbis ----------"
    cd $src_dir
    run_wget $url_vorbis
    LDFLAGS="-L$prefix_dir/lib" CPPFLAGS="-I$prefix_dir/include" ./configure --prefix="$prefix_dir" --with-ogg="$prefix_dir" --disable-shared
    make -j${cpu_core}
    if [ $? -ne 0 ]; then
        print_error "make libvorbis" && exit 1
    fi
    make install
    make distclean
    enable_option="${enable_option} --enable-libvorbis"
  
    echo "---------- build libtheora ----------"
    cd $src_dir
    run_wget $url_theora
    ./configure --prefix="$prefix_dir" --disable-shared --disable-examples
    make -j${cpu_core}
    if [ $? -ne 0 ]; then
    print_error "make libtheora" && exit 1
    fi
    make install
    make clean
    enable_option="${enable_option} --enable-libtheora"
fi
  
  
if [ $enable_vp8 -eq 1 ]; then
    echo "---------- build libvpx ----------"
    cd $src_dir
    run_git $repo_libvpx "--depth 1"
    ./configure --prefix="$prefix_dir" --disable-examples ${pic_enable}
    make -j${cpu_core}
    if [ $? -ne 0 ]; then
        print_error "make libvpx" && exit 1
    fi
    make install
    make clean
    enable_option="${enable_option} --enable-libvpx"
fi
  
  
if [ $enable_ass -eq 1 ]; then
    echo "---------- build libass ----------"
    cd $src_dir
    run_git $repo_libass "--depth 1"
    autoreconf -fiv
    ./configure --prefix="$prefix_dir" --disable-shared
    make -j${cpu_core}
    if [ $? -ne 0 ]; then
        print_error "make libass" && exit 1
    fi
    make install
    make clean
    enable_option="${enable_option} --enable-libass"
fi
  
  
echo "---------- build FFmpeg ----------"
cd $src_dir
run_git $repo_ffmpeg "--depth 1"
  
./configure \
  --prefix="$prefix_dir" --extra-cflags="-I$prefix_dir/include" \
  --extra-ldflags="-L$prefix_dir/lib" \
  --extra-libs="-lm -lpthread" \
  --bindir="$prefix_dir/bin" \
  --pkg-config-flags="--static" \
  --enable-gpl \
  --enable-nonfree \
  --enable-libfreetype \
  $enable_option
make -j${cpu_core}
if [ $? -ne 0 ]; then
    print_error "make ffmpeg" && exit 1
fi
make install
make distclean
hash -r