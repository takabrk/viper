#!/bin/sh
case $1 in
        "on") sed -i -e "37 s/\#\$HOME/\$HOME/g" $HOME/.config/openbox/autostart ;;
        "off") sed -i -e "37 s/\$HOME/\#\$HOME/g" $HOME/.config/openbox/autostart ;;
esac
