FROM ubuntu:18.04

#ENV DISPLAY=:0

RUN sed -i 's@archive.ubuntu.com@ftp.jaist.ac.jp/pub/Linux@' /etc/apt/sources.list

RUN export DEBIAN_FRONTEND=noninteractive \
    && add-apt-repository ppa:otto-kesselgulasch/gimp \
    && apt-get update \
    && apt-get install -y gimp \
                   tzdata \
                   sudo \
                   language-pack-ja-base \
                   language-pack-ja \
                   fonts-ipafont-gothic \
                   fcitx-mozc \
                   fcitx-imlist 

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
