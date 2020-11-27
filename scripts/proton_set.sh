#!/bin/sh
#proton_set.sh
#Use winetricks and winecfg on Valve's Proton
#Created by takamitsu hamada
#website:https://vsrx.work
#Updated 2020/11/27

while getopts e: OPT
do
  case $OPT in
      e) e_n=$OPTARG
         ;;
  esac
done
case $e_n in
    tricks)
        WINEPREFIX=$HOME/.steam/steamapps/compatdata/$1/pfx winetricks
    ;;
    cfg)
        WINEPREFIX=$HOME/.steam/steamapps/compatdata/$1/pfx winecfg
    ;;
    esac