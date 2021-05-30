#!/bin/sh
#proton_set.sh
#Use winetricks and winecfg on Valve's Proton
#Created by takamitsu hamada
#website:https://vsrx.work
#Updated 2020/11/27

echo "$HOME/.steam/steamapps/compatdata/$3/pfx"
while getopts e: OPT
do
  case $OPT in
      e) e_n=$OPTARG
         ;;
  esac
done
case $e_n in
    tricks)
        WINEPREFIX=$HOME/.steam/steamapps/compatdata/$3/pfx winetricks
    ;;
    cfg)
        WINEPREFIX=$HOME/.steam/steamapps/compatdata/$3/pfx winecfg
    ;;
    tricks32)
        WINEARCH=win32 WINEPREFIX=$HOME/.steam/steamapps/compatdata/$3/pfx winetricks
    ;;
    cfg32)
        WINEARCH=win32 WINEPREFIX=$HOME/.steam/steamapps/compatdata/$3/pfx winecfg
    ;;
    esac