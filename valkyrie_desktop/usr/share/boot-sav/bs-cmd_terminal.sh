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

####################### LIBRARIES THAT CAN BE CALLED BEFORE G2S ####################

################## ECHO VERSION ##################################
echo_version() {
check_package_manager
APPNAME_VERSION=$($PACKVERSION $APPNAME )
echo "$APPNAME version : $APPNAME_VERSION" # dpkg-query -W -f='${Version}' paquet
COMMON_VERSION=$($PACKVERSION boot-sav )
echo "boot-sav version : $COMMON_VERSION"
echo "boot-sav-extra version : $($PACKVERSION boot-sav-extra )"
G2S=glade2script-python3; [[ "$(type -p glade2script)" ]] && G2S=glade2script
G2S_VERSION=$($PACKVERSION $G2S )
echo "$G2S version : $G2S_VERSION"
}

#################### CHECK PACKAGE MANAGER ############################
check_package_manager() {
if [[ "$(type -p apt-get)" ]];then
	PACKMAN=apt-get
	PACKYES="-y"
	PACKINS=install
	PACKPURGE=purge
	PACKUPD="-y update"
	PACKVERSION='dpkg-query -W -f=${Version}'
elif [[ "$(type -p yum)" ]];then
	PACKMAN=yum
	PACKYES=-y
	PACKINS=install
	PACKPURGE=erase
	PACKUPD=makecache
	PACKVERSION='rpm -q --qf=%{version}'
elif [[ "$(type -p zypper)" ]];then
	PACKMAN='zypper --non-interactive'
	PACKYES=''
	PACKINS=in
	PACKPURGE=rm
	PACKUPD=ref
	PACKVERSION="zypper se -s --match-exact"
elif [[ "$(type -p pacman)" ]];then
	PACKMAN=pacman
	PACKYES='' #--noconfirm unrecognized
	PACKINS=-Sy
	PACKPURGE=-R
	PACKUPD="-Sy --noconfirm pacman; pacman-db-upgrade"
	PACKVERSION="pacman -Q"
else
	zenity --width=300 --error --text"Current distribution is not supported. Please use Boot-Repair-Disk."
	choice="exit"; echo 'EXIT@@'
fi
}


######################### CHECK EFI PARTITIONS #########################
efi_check() {
#ESP with Windows bootmgr: http://ubuntuforums.org/showthread.php?t=2090605
part="${LISTOFPARTITIONS[$i]}" #eg mapper/isw_beaibbhjji_Volume0p1
d="${DISKNB_PART[$i]}" 
while read line;do
	if [[ "$line" =~ "/dev/$part " ]];then
		[[ "$(echo "$line" | grep "dev/$part " | grep '*' | grep -i fat | grep -vi ntfs | grep -v hidden)" ]] && this_part_is_efi  #EFI working without GPT: http://forum.ubuntu-fr.org/viewtopic.php?pid=9962371#p9962371
		[[ "$(echo "$line" | grep "dev/$part " | grep 'EFI' | grep -v hidden)" ]] && this_part_is_efi #https://launchpadlibrarian.net/299779679/Boot-Repair%20bug.txt
	fi
done < <(echo "$FDISKL")
f=""
while read line;do
	if [[ "$line" =~ /dev/ ]];then
		[[ "$line" =~ "/dev/${DISK_PART[$i]}:" ]] && f=ok || f=""
	fi #eg 11:162GB:162GB:210MB:fat32::boot, hidden;
	EFIPARTNUMERO="${line%%:*}" #eg 1
	#echo "[debug] WWW $line <$EFIPARTNUMERO>${part##*[a-z]}>" #
	if [[ "$EFIPARTNUMERO" = "${part##*[a-z]}" ]] && [[ "$f" ]];then
		if [[ "$(echo "$line" | grep fat | grep boot | grep -v hidden )" ]] \
		|| [[ "$(echo "$line" | grep fat | grep esp | grep -v hidden )" ]] \
		|| [[ "$(echo "$line" | grep fat | grep ':EFI system partition:' | grep -v hidden )" ]];then
			this_part_is_efi
		elif [[ "$(echo "$line" | grep fat | grep boot )" ]] \
		|| [[ "$(echo "$line" | grep fat | grep esp )" ]] \
		|| [[ "$(echo "$line" | grep fat | grep ':EFI system partition:' )" ]];then
			this_part_maybe_efi
		fi
	fi
done < <(echo "$PARTEDLM")
}

this_part_is_efi() {
if [[ "${EFI_TYPE[$i]}" != is-correct-EFI ]];then
	[[ "${GPT_DISK[$d]}" = GPT ]] && (( NB_EFIPARTONGPT += 1 ))
	EFI_DISK[$d]=has-correctEFI
	EFI_TYPE[$i]=is-correct-EFI
	(( NB_BISEFIPART += 1 ))
fi
}

this_part_maybe_efi() {
if [[ "${EFI_TYPE[$i]}" != is-correct-EFI ]];then
	[[ "${EFI_DISK[$d]}" != has-correctEFI ]] && EFI_DISK[$d]=has-maybe-EFI
	EFI_TYPE[$i]=is-maybe-EFI
fi
}

esp_detect() {
. /usr/share/boot-sav/bs-common.sh
blkid_fdisk_and_parted_update
check_blkid_partitions
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	efi_check
	if [[ "${EFI_TYPE[$i]}" = is-correct-EFI ]];then
		echo "${LISTOFPARTITIONS[$i]} is ESP"
	elif [[ "${EFI_TYPE[$i]}" = is-maybe-EFI ]];then
		echo "${LISTOFPARTITIONS[$i]} may be ESP"
	else
		echo "${LISTOFPARTITIONS[$i]} is not ESP"
	fi
done
}

########################## CHECK IF LIVE-SESSION #######################
check_if_live_session() {
local DR ra=/home/usr
hash lsb_release && DISTRIB_DESCRIPTION="$(lsb_release -ds)" || DISTRIB_DESCRIPTION=Unknown-name
DR="$(df / | grep /dev/ )"; DR="${DR%% *}"; DR="${DR#*v/}"
if [ "$(grep -E '(boot=casper)|(boot=live)' /proc/cmdline)" ] || [[ "$DR" =~ loop ]] || [[ "$(df -Th / | grep -E 'aufs|overlay')" ]];then #aufs bug#1281815, overlay since 19.10
	LIVESESSION=live   #if (mount | grep -E 'aufs|overlay' | grep -q 'on / type'); then live
else 
	LIVESESSION=installed
	CURRENTSESSIONNAME="$The_system_now_in_use - $DISTRIB_DESCRIPTION"
	CURRENTSESSIONPARTITION="$DR"
	if [[ "$TMP_FOLDER_TO_BE_CLEARED" ]];then
		#Add CurrentSession at the beginning of OSPROBER (so that GRUB reinstall of CurrentSession is selected by default)
		echo "/dev/${CURRENTSESSIONPARTITION}:$CURRENTSESSIONNAME CurrentSession:linux" >$TMP_FOLDER_TO_BE_CLEARED/osprober_with_currentsession
		echo "$OSPROBER" >> $TMP_FOLDER_TO_BE_CLEARED/osprober_with_currentsession
		OSPROBER=$(< $TMP_FOLDER_TO_BE_CLEARED/osprober_with_currentsession)
	fi
fi
if [[ "$GUI" ]] || [[ "$1" ]];then
	[[ -d /usr/share/ubuntu-defaults-french ]] && echo "$APPNAME est exécuté en session $LIVESESSION ($DISTRIB_DESCRIPTION, $(lsb_release -cs), $(lsb_release -is)-fr, $(uname -m))" \
	|| echo "$APPNAME is executed in $LIVESESSION-session ($DISTRIB_DESCRIPTION, $(lsb_release -cs), $(lsb_release -is), $(uname -m))"
	LANGUAGE=C LC_ALL=C lscpu | grep bit
	cat /proc/cmdline
fi
[ "$(grep -E '(boot=casper)|(boot=live)' /proc/cmdline)" ] && [[ "$(ls $ra/.config)" =~ os ]] && OSBKP=y
}

################################### CHECK EFI DMSG #####################
check_efi_dmesg() {
#http://forum.ubuntu-fr.org/viewtopic.php?id=742721
local ue="$(dmesg | grep EFI | grep -v Variables )"
SECUREBOOT='maybe enabled'
if [[ -d /sys/firmware/efi ]];then #http://paste.ubuntu.com/1176988
	EFIDMESG="BIOS is EFI-compatible, and is setup in EFI-mode for this $LIVESESSION-session."
	[[ "$(uname -m)" != x86_64 ]] || [[ -d /usr/share/ubuntu-defaults-french ]] \
	&& EFIDMESG="$EFIDMESG
Unusual EFI: $PLEASECONTACT"
	[[ ! "$ue" ]] && EFIDMESG="$EFIDMESG
No EFI in dmseg."
	#SecureBoot http://launchpadlibrarian.net/119223180/ubiquity_2.12.8_2.12.9.diff.gz
	local efi_vars sb_var
	efi_vars=/sys/firmware/efi/vars
	sb_var="$efi_vars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c/data"
	sb_var2="$efi_vars/SecureBoot-a8be4df61-93ca-11d2-aa0d-00e098032b8c/data"
	if [[ ! -d $efi_vars ]];then
		SECUREBOOT=disabled
	elif [[ -e "$sb_var" ]];then
		[[ "$(printf %x \'"$(cat "$sb_var")")" = 1 ]] && SECUREBOOT=enabled || SECUREBOOT=disabled
	elif [[ -e "$sb_var2" ]];then #http://paste.ubuntu.com/1643471
		[[ "$(printf %x \'"$(cat "$sb_var2")")" = 1 ]] && SECUREBOOT=enabled || SECUREBOOT=disabled
	else
		[[ -f "$sb_var" ]] || [[ -f "$sb_var2" ]] && echo "Warning: sbvar. $PLEASECONTACT"
		tst="$(ls $efi_vars | grep SecureBoot )"
		if [[ "$tst" ]];then
			if [ -e "$efi_vars/$tst/data" ];then
				[ "$(printf %x \'"$(cat "$efi_vars/$tst/data")")" = 1 ] && SECUREBOOT=enabled || SECUREBOOT=disabled
			elif [[ -f "$efi_vars/$tst/data" ]];then
				echo "Warning: $tst/data . $PLEASECONTACT"
			fi
		fi
		a=""; for b in $(ls $efi_vars);do a="$b,$a";done
		echo "ls $efi_vars : $a
$PLEASECONTACT" #eg http://paste.ubuntu.com/1398454 , http://paste.ubuntu.com/1460548
	fi
	if [[ "$SECUREBOOT" = 'maybe enabled' ]] && [[ "$(grep signed /proc/cmdline)" ]];then
		SECUREBOOT=enabled
		a=""; for b in $(ls $efi_vars);do a="$b,$a";done
		echo "ls $efi_vars : $a
Special SecureBoot. $PLEASECONTACT"
	fi
	if [[ "$(type -p efibootmgr)" ]];then
		echo "
$DASH efibootmgr -v"
		LANGUAGE=C LC_ALL=C sudo efibootmgr -v
	else
		echo "Please install package efibootmgr and retry."
	fi
else
	[[ "$LIVESESSION" = installed ]] && SECUREBOOT=disabled
	if [[ "$EFIFILEPRESENCE" ]];then
		EFIDMESG="BIOS is EFI-compatible, but it is not setup in EFI-mode for this $LIVESESSION-session."
		#ex of efi win with no efi dmsg: http://paste.ubuntu.com/1079434 , http://paste.ubuntu.com/1088771
	elif [[ "$(uname -m)" != x86_64 ]] || [[ "$(lsb_release -is)" = Debian ]] || [[ "$(lsb_release -cs)" = lucid ]];then
		EFIDMESG="This $LIVESESSION-session is not EFI-compatible."
	elif [[ -d /usr/share/ubuntu-defaults-french ]] && [[ "$LIVESESSION" = live ]];then
		EFIDMESG="Le disque Ubuntu Edition Francophone ne peut pas être démarré en mode EFI."
	else # http://paste.ubuntu.com/1001831 , http://paste.ubuntu.com/966239 , http://paste.ubuntu.com/934497
		EFIDMESG="This $LIVESESSION-session is not in EFI-mode."
	fi
	[[ "$ue" ]] && EFIDMESG="$EFIDMESG
EFI in dmesg.
$ue" #ex: http://paste.ubuntu.com/1354258
fi
EFIDMESG="$EFIDMESG
SecureBoot $SECUREBOOT."
#Not sure if SecureBoot disabled
[[ -d /sys/firmware/efi ]] && [[ -d $efi_vars ]] && [[ "$SECUREBOOT" != enabled ]] \
&& EFIDMESG="$EFIDMESG (maybe sec-boot, $PLEASECONTACT)"
[[ "$GUI" ]] || [[ "$1" ]] && echo "
$DASH UEFI/Legacy mode:
$EFIDMESG
"
}

################################### TAIL COMMON LOGS #####################
tail_common_logs() {
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	for j in syslog kern.log Xorg.0.log dpkg.log;do
		if [[ -f "${BLKIDMNT_POINT[$i]}/var/log/$j" ]];then
			echo "$DASH tail $1 ${LISTOFPARTITIONS[$i]}/var/log/$j"
			tail $1 "${BLKIDMNT_POINT[$i]}/var/log/$j"
			echo ""
		fi
	done
done
}

full_infos() {
. /usr/share/boot-sav/gui-init.sh
lib_init
check_os_and_mount_blkid_partitions_gui y
check_which_mbr_can_be_restored
echo_df_and_fdisk
tail_common_logs
unmount_all_blkid_partitions_except_df
}
