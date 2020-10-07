FROM ubuntu:18.04

#ENV DISPLAY=:0

RUN sed -i 's@archive.ubuntu.com@ftp.jaist.ac.jp/pub/Linux@' /etc/apt/sources.list

RUN export DEBIAN_FRONTEND=noninteractive \
    && wget -qO - http://repo.radeon.com/rocm/apt/debian/rocm.gpg.key | sudo apt-key add -
 \
    && sudo sh -c 'echo deb [arch=amd64] http://repo.radeon.com/rocm/apt/debian/ xenial main > /etc/apt/sources.list.d/rocm.list'
 \
    && sudo apt-get update \
           sudo apt install -y build-essential python3 python3-dev python3-pip pkg-config check cmake libhdf5-dev python3-pip \
           sudo apt install -y build-essential \
           sudo apt install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev \
           sudo apt install -y libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev \
           sudo apt install python3-wheel python3-mock python3-future python3-yaml \
           sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
           sudo apt install -y libxvidcore-dev libx264-dev \
           sudo apt install -y libgtk-3-dev \
           sudo apt install -y libatlas-base-dev gfortran pylint \
           sudo apt install -y --allow-unauthenticated \
           rocm-dkms rocm-dev rocm-libs \
           rocm-device-libs \
           hsa-ext-rocr-dev hsakmt-roct-dev hsa-rocr-dev \
           rocm-opencl rocm-opencl-dev \
           rocm-utils \
           rocm-profiler cxlactivitylogger \
           miopen-hip miopengemm \
           sudo pip3 install -y setuptools scipy numpy six pillow h5py keras\
           sudo pip3 install tensorflow-rocm \
           sudo usermod -a -G video $LOGNAME \
           echo 'export HIP_VISIBLE_DEVICES=0' >> ~/.profile \
           echo 'export HCC_HOME=/opt/rocm/hcc' >> ~/.profile \
           echo 'export ROCM_HOME=/opt/rocm/bin' >> ~/.profile \
           echo 'export HIP_PATH=/opt/rocm/hip' >> ~/.profile \
           echo 'export PATH=/usr/local/bin:$HCC_HOME/bin:$HIP_PATH/bin:$ROCM_HOME:$PATH:/opt/rocm/opencl/bin/x86_64' >> ~/.profile \
           echo 'export LD_LIBRARY=$LD_LIBRARY:/opt/rocm/opencl/lib/x86_64' >> ~/.profile \
           echo 'export LC_ALL="en_US.UTF-8"' >> ~/.profile \
           echo 'export LC_CTYPE="en_US.UTF-8"' >> ~/.profile \
           source ~/.profile \
           export PIP=pip3 \
           export PYTHON=python3 \
           export HIP_PLATFORM=hcc \
           export PLATFORM=hcc \

RUN locale-gen ja_JP.UTF-8
ENV LANG=ja_JP.UTF-8

ENV TZ=Asia/Tokyo

ENV GTK_IM_MODULE=fcitx \
    QT_IM_MODULE=fcitx \
    XMODIFIERS=@im=fcitx \
    DefalutIMModule=fcitx

#ARG DOCKER_UID=1000
#ARG DOCKER_USER=docker
#ARG DOCKER_PASSWORD=docker
#RUN useradd -m --uid ${DOCKER_UID} --groups sudo --shell /bin/bash ${DOCKER_USER} && echo ${DOCKER_USER}:${DOCKER_PASSWORD} | chpasswd

#WORKDIR /home/${DOCKER_USER}

#RUN chown -R ${DOCKER_USER} ./

#USER ${DOCKER_USER}

RUN export uid=1000 gid=1000 && \
    mkdir -p /home/valkyrie && \
    echo "valkyrie:x:${uid}:${gid}:valkyrie,,,:/home/valkyrie:/bin/bash" >> /etc/passwd && \
    echo "valk,yrie:x:${uid}:" >> /etc/group && \
    echo "valkyrie ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/valkyrie && \
    chmod 0440 /etc/sudoers.d/valkyrie && \
    chown ${uid}:${gid} -R /home/valkyrie
    
#RUN sed -i "s/allowed_users=console/allowed_users=anybody/;$ a needs_root_rights=yes" /etc/X11/Xwrapper.config

USER valkyrie
ENV HOME /home/valkyrie

#CMD [ "/usr/bin/startx", "--", "vt7" ]
