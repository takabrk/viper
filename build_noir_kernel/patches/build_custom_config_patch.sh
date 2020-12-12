#!/bin/sh
truncate custom_config.patch --size 0

diff -Naur /dev/null .config  > custom_config.patch
