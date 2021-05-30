#!/bin/sh

mogrify -path $0 -strip -format $1 -quality $2 -resize $3x\> *.*