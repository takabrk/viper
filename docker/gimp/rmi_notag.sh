#!/bin/sh

docker rmi `docker images -f "dangling=true" -q`
