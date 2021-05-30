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


######################### CHECK INTERNET CONNECTION ####################
check_internet_connection() {
[[ "$DISABLEWEBCHECK" ]] || [[ "$(ping -c1 google.com)" ]] && INTERNET=connected || INTERNET=no-internet
#[[ "$(wget -T $WGETTIM -q -O - checkip.dyndns.org)" =~ "Current IP Address:" ]]
[[ "$DEBBUG" ]] && echo "[debug]internet: $INTERNET"
}

ask_internet_connection() {
if [[ "$INTERNET" != connected ]];then
	echo "$Please_connect_internet $Then_close_this_window"
	end_pulse
	zenity --width=300 --info --title="$APPNAME2" --text="$Please_connect_internet $Then_close_this_window"
	start_pulse
	check_internet_connection
fi
}

exit_as_packagelist_is_missing() {
end_pulse
update_translations
echo "$please_install_PACKAGELIST"
choice=exit; echo 'EXIT@@'
}

################################# CRYPT ##################################
#propose_decrypt() {
#BLKID=$(blkid)
#FUNCTION=LUKS PACKAGELIST=ecryptfs-utils FILETOTEST=ecryptfsd
#if [[ "$(echo "$BLKID" | grep -i crypt | grep -vi swap )" ]];then
#	update_translations
#	text="$Encryption_detected $You_may_want_to_retry_after_installing_PACKAGELIST"
#	echo "$text"
#	end_pulse
#	zenity --width=300 --info --title="$APPNAME2" --text="$text"
#	[[ ! "$(type -p $FILETOTEST)" ]] && installpackagelist
#	start_pulse
#	text="$You_may_want_decrypt ($Decrypt_links)"
#fi
	
#apt-get install lvm2 cryptsetup; sudo modprobe dm-crypt; sudo cryptsetup luksOpen /dev/sda5 crypt1 ;sudo vgscan --mknodes; sudo vgscan --mknodes
#http://ubuntuforums.org/showthread.php?p=4530641



################################# LVM ##################################
activate_lvm_if_needed() {
#works: http://paste.ubuntu.com/1004461
local FUNCTION=LVM PACKAGELIST=lvm2 FILETOTEST=vgchange
BLKID=$(blkid)
BEFLVMBLKID=""
AFTLVMBLKID=""
if [[ "$DISTRIB_DESCRIPTION" =~ Unknown ]] || [[ "$(lsb_release -cs)" =~ squeeze ]] && [[ "$BLKID" =~ LVM ]];then
	FUNCTION=LVM; FUNCTION44=LVM; DISK44="Boot-Repair-Disk (www.sourceforge.net/p/boot-repair-cd/home)"; update_translations
	end_pulse
	zenity --width=300 --info --title="$APPNAME2" --text="$FUNCTION_detected $Please_use_DISK44_which_is_FUNCTION44_ok"
	choice=exit
elif [[ "$BLKID" =~ LVM ]];then
	BEFLVMBLKID="$BLKID"
	[[ ! "$(type -p $FILETOTEST)" ]] && installpackagelist
	[[ ! "$(type -p $FILETOTEST)" ]] && choice=exit || scan_and_activate_lvm #dont invert!
fi
}

scan_and_activate_lvm() {
echo "BLKID BEFORE LVM ACTIVATION:
$BLKID"
echo "MODPROBE"
modprobe dm-mod		# Not sure it is necessary
echo "VGSCAN"
vgscan --mknodes	# Not sure it is necessary
echo "VGCHANGE"
vgchange -ay		# Activate volumes
LVSCAN="$(LANGUAGE=C LC_ALL=C lvscan)"
echo "LVSCAN:
$LVSCAN"
[[ "$LVSCAN" =~ inactive ]] && echo "Warning: inactive LVM"
blkid -g #Update the UUID cache
BLKID=$(blkid)
AFTLVMBLKID="$BLKID"
[[ "$BEFLVMBLKID" != "$BLKID" ]] && echo "Successfully activated LVM."
}

################################# RAID #################################
activate_raid_if_needed() {
BEFRAIDBLKID=""
raiduser=no
if [[ "$DISTRIB_DESCRIPTION" =~ Unknown ]] || [[ "$(lsb_release -cs)" =~ squeeze ]] && [[ "$BLKID" =~ raid ]];then #|| [[ "$DISTRIB_DESCRIPTION" =~ Boot-Repair-Disk ]]
	FUNCTION=RAID; FUNCTION44=RAID; DISK44="Boot-Repair-Disk (www.sourceforge.net/p/boot-repair-cd/home)"; update_translations
	end_pulse
	zenity --width=300 --info --title="$APPNAME2" --text="$FUNCTION_detected $Please_use_DISK44_which_is_FUNCTION44_ok"
	choice=exit
elif [[ "$BLKID" =~ raid ]] || [[ "$(echo "$BLKID" | grep /dev/mapper/ | grep -v swap  | grep -vi LVM)" ]];then
	raiduser=yes
	if [[ ! "$BLKID" =~ raid ]];then
		end_pulse
		zenity --width=300 --question --title="$APPNAME2" --text="$Is_there_RAID_on_this_pc" || raiduser=no
		echo "$Is_there_RAID_on_this_pc $raiduser"
		[[ "$raiduser" = yes ]] && echo "Unusual RAID (no raid in blkid)." #zenity --width=300 --warning --title="$APPNAME2" --text="Unusual RAID. $PLEASECONTACT"
		start_pulse
	fi
	if [[ "$raiduser" = yes ]];then
		local FUNCTION=RAID PACKAGELIST FILETOTEST removedmraid=yes
		DMRAID=""
		MD_ARRAY=""
		BEFRAIDBLKID="$BLKID"
		echo "
		BLKID BEFORE RAID ACTIVATION:
		$BLKID"
		[[ "$(type -p dmraid)" ]] && INIT_DMR=y || INIT_DMR=""
		if [[ "$INIT_DMR" ]];then
			assemble_dmraid
			[[ ! "$DMRAID" ]] && propose_remove_dmraid #mdadm & dmraid interfere: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=534274
		fi
		if [[ ! "$(type -p mdadm)" ]];then
			PACKAGELIST=mdadm
			FILETOTEST=mdadm
			installpackagelist
		fi
		assemble_mdadm #software raid
		if [[ ! "$INIT_DMR" ]] && [[ ! "$MD_ARRAY" ]];then
			FUNCTION=RAID
			[[ "$(type -p mdadm)" ]] && PACKAGELIST=dmraid || PACKAGELIST="dmraid/mdadm"
			update_translations
			text="$FUNCTION_detected $You_may_want_to_retry_after_installing_PACKAGELIST"
			echo "$text"
			end_pulse
			zenity --width=300 --info --title="$APPNAME2" --text="$text"
			start_pulse
		fi
		[[ ! "$INIT_DMR" ]] && assemble_dmraid
		
		[[ "$DEBBUG" ]] && echo "[debug]$(type -p dmraid) , MDADM $(type -p mdadm)"
		[[ "$BLKID" =~ raid ]] || [[ ! "$BLKID" =~ LVM ]] && [[ ! "$(type -p dmraid)" ]] && [[ ! "$(type -p mdadm)" ]] && choice=exit
		if [[ ! "$DMRAID" ]] && [[ ! "$MD_ARRAY" ]] && [[ "$choice" != exit ]];then
			echo "Warning: no DMRAID nor MD_ARRAY."
			[[ ! "$BLKID" =~ LVM ]] && zenity --width=300 --warning --text="No active RAID."
		fi
		BLKID=$(blkid)
		[[ "$BEFRAIDBLKID" != "$BLKID" ]] && echo "Successfully activated RAID."
	fi
fi
}

propose_remove_dmraid() {
if [[ "$(type -p dmraid)" ]] && [[ "$APPNAME" =~ re ]];then	#http://ubuntuforums.org/showthread.php?t=1551087
	end_pulse
	zenity --width=300 --question --title="$APPNAME2" --text="$dmraid_may_interfere_MDraid_remove" || removedmraid=no
	start_pulse
	echo "$dmraid_may_interfere_MDraid_remove $removedmraid"
	if [[ "$removedmraid" = no ]];then
		echo "User chose to keep dmraid. It may interfere with mdadm."
	else
		echo "$PACKMAN remove $PACKYES dmraid"
		$PACKMAN remove $PACKYES dmraid
		if [[ "$(type -p mdadm)" ]];then
			text="It is now recommended to reinstall mdadm. Please continue when done."
			echo "$text"
			end_pulse
			zenity --width=300 --info --title="$APPNAME2" --text="$text"
			start_pulse
		fi
	fi
fi
}

assemble_dmraid() {
if [[ "$(type -p dmraid)" ]];then
	#end_pulse
	#zenity --width=300 --question --title="$APPNAME2" --text="${FUNCTION_detected} ${activate_dmraid} (dmraid -ay; dmraid -sa -c)" || dmraidenable="no"
	#start_pulse
	#if [[ ! "$dmraidenable" ]]; then
		DMRAID="$(dmraid -si -c)"
		echo "dmraid -si -c: $DMRAID"
		if [[ "$DMRAID" =~ "no raid disk" ]];then
			DMRAID=""
			echo "No DMRAID disk."
		else
			echo "dmraid -ay:"
			dmraid -ay	#Activate RAID
			DMRAID="$(dmraid -sa -c)"
			echo "dmraid -sa -c: $DMRAID"	#e.g. isw_bcbggbcebj_ARRAY (http://paste.ubuntu.com/1055404)
		fi
	#fi
fi
}	

assemble_mdadm() {
if [[ "$(type -p mdadm)" ]];then
	echo "Scanning MDraid Partitions"
	mdadm --assemble --scan 	# Assemble all arrays
	# All arrays.
	MD_ARRAY=$(mdadm --detail --scan) #TODO  | ${AWK} '{ print $2 }')
	echo "mdadm --detail --scan: $MD_ARRAY"
	#for MD in ${MD_ARRAY}; do
	#	MD_SIZE=$(fdisks ${MD})     # size in blocks
	#	MD_SIZE=$((2*${MD_SIZE}))   # size in sectors
	#	MDNAME=${MD:5}
	#	MDMOUNTNAME="MDRaid/${name}"
	#	echo "MD${MD}: ${MDNAME}, ${MDMOUNTNAME}, ${MD_SIZE}"
	#done
fi
}
