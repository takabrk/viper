#!/bin/sh

#docker build \
#    -t takabrk/ubuntu \
#    --build-arg DOCKER_UID=$(id -u) \
#    --build-arg DOCKER_USER='valkyrie' \
#    --build-arg DOCKER_PASSWORD='xxxxxx' .

docker build -t takabrk/ubuntu .
