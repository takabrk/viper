#! /bin/bash
# Copyright 2020 Yann MRN
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

#Called from /usr/sbin/$APPNAME-bin
cmd_start() {
GUI=""
DEBBUG=""
[[ "$*" =~ -d ]] && DEBBUG=yes
if [[ "$1" =~ "-t" ]];then
	if [[ $EUID -ne 0 ]];then
		echo "Root privileges are required to run $APPNAME $*"
	else
		. /usr/share/boot-sav/bs-cmd_terminal.sh
		if [[ "$(echo $2 | grep "^[ [:digit:] ]*$")" ]];then
			. /usr/share/boot-sav/gui-init.sh
			lib_init
			check_os_and_mount_blkid_partitions_gui
			tail_common_logs -$2
			unmount_all_blkid_partitions_except_df
		else
			echo "-t must be followed by an integer, e.g. $APPNAME -t 30"
		fi
	fi
elif [[ "$*" =~ "-i" ]] ;then
	if [[ $EUID -ne 0 ]];then
		echo "Root privileges are required to run $APPNAME $*"
	else
		. /usr/share/boot-sav/bs-cmd_terminal.sh
		echo_version
		check_if_live_session y
		check_efi_dmesg y
		esp_detect
		full_infos
	fi
elif [[ "$*" =~ "--esp" ]];then
	. /usr/share/boot-sav/bs-cmd_terminal.sh
	[[ $EUID -ne 0 ]] && echo "Root privileges are required to run $APPNAME $*" || esp_detect
elif [[ "$*" =~ "-e" ]];then
	. /usr/share/boot-sav/bs-cmd_terminal.sh
	check_if_live_session y
	check_efi_dmesg y
elif [[ "$*" =~ "-v" ]];then
	. /usr/share/boot-sav/bs-cmd_terminal.sh
	echo_version
else
	# Ask root privileges
	if [[ $EUID -ne 0 ]];then
		if [[ "$1" ]];then
			echo "Root privileges are required to run $APPNAME $*"
			exit
		fi
		if hash xhost && ! xhost | grep -qi 'SI:localuser:root';then #workaround bug#1713313
			xhost +SI:localuser:root > /dev/null
		fi
#		if hash pkexec;then
#			pkexec $APPNAME-bin
#		elif hash gksudo;then
#			gksudo $APPNAME-bin #gksu and su dont work in Kubuntu
#		elif hash gksu;then
#			gksu $APPNAME-bin
#		elif hash kdesudo;then
#			kdesudo $APPNAME-bin
#		elif hash xdg-su;then
#			xdg-su -c $APPNAME-bin
		if hash sudo;then
			sudo $APPNAME-bin
		elif hash su;then
			su -c $APPNAME-bin
		else
			t="Root privileges are required to run $APPNAME."
			echo "$t"
			#zenity --width=300 --error --text="$t"
		fi
		#[[ "$GRANTED_XHOST_ROOT" ]] && xhost -SI:localuser:root > /dev/null
		exit 1
	fi
	# Launch the Glade window via glade2script
	G2S=glade2script-python3; [[ "$(type -p glade2script)" ]] && G2S=glade2script
	if [[ "$G2S" =~ 3 ]] && [[ ! "$DEBBUG" ]];then
		REP=yes
		zenity --width=300 --question --title="$APPNAME" --text="This will enable the Universe repository and install the 'glade2script' package, do you want to continue?" || REP=no
		if [[ "$REP" = yes ]];then
			zenity --width=300 --info --title="$APPNAME" --text="This may take several minutes depending on your internet connection, please wait." &
			sudo add-apt-repository -y universe
			sudo apt update -y
			sudo apt install -y glade2script
			$APPNAME &
		fi
	else
	$G2S $1 -g /usr/share/boot-sav/boot-sav.glade -s /usr/share/boot-sav/$APPNAME.sh \
	--combobox="@@_combobox_format_partition@@col" \
	--combobox="@@_combobox_bootflag@@col" \
	--combobox="@@_combobox_ostoboot_bydefault@@col" \
	--combobox="@@_combobox_purge_grub@@col" \
	--combobox="@@_combobox_separateboot@@col" \
	--combobox="@@_combobox_efi@@col" \
	--combobox="@@_combobox_sepusr@@col" \
	--combobox="@@_combobox_place_grub@@col" \
	--combobox="@@_combobox_add_kernel_option@@col" \
	--combobox="@@_combobox_restore_mbrof@@col" \
	--combobox="@@_combobox_partition_booted_bymbr@@col"
	fi
	if hash xhost && xhost | grep -qi 'SI:localuser:root';then
		xhost -SI:localuser:root > /dev/null
	fi
fi
exit 0
}
