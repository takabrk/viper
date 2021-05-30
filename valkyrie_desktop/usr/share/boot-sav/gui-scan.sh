#! /bin/bash
# Copyright 2017 Yann MRN
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


##################### Main function for GUI preparation ################
check_os_and_mount_blkid_partitions_gui() {
[[ "$GUI" ]] && delete_tmp_folder_to_be_cleared
OSPROBER=$(os-prober)
blkid_fdisk_and_parted_update
[[ "$GUI" ]] && echo "SET@_label0.set_text('''$LAB (mount). $This_may_require_several_minutes''')"
check_if_live_session $1				#After update_translation and update_osprober, and before check_os_names
check_blkid_partitions					#In order to save MBR of all disks detected by blkid
determine_bios_boot						#to avoid mounting BIOS Boot
mount_all_blkid_partitions_except_df
[[ "$GUI" ]] && remove_stage1_from_other_os_partitions	#Solve a bug of os-prober (allow to detect some OS that would be hidden)
determine_part_uuid						#After check_blkid_partitions
check_location_first_partitions			#Output: $BYTES_BEFORE_PART[$disk]
echo_osprober_and_blkid $1
check_os_names_and_partitions_and_types $1
mount_all_blkid_partitions_except_df	#To update OS_Mount_points
determine_part_with_os					#To get OSNAME (before check_recovery_or_hidden)
check_recovery_or_hidden				#After mount_all_blkid_partitions_except_df & before logs
[[ "$GUI" ]] && initialize_log_folders_in_os			#After OS_Mount_points have been updated
[[ "$GUI" ]] && put_the_current_mbr_in_tmp
check_disks_containing_mbr_backups
[[ "$GUI" ]] && echo "SET@_label0.set_text('''$LAB. $This_may_require_several_minutes''')"
check_disk_types				#before part_types (for usb and gpt and efi_check)
check_part_types $1				#After mount_all_blkid_partitions_except_df & determine_part_uuid & determine_part_with_os
check_wubi_existence $1			#After mount_all_blkid_partitions_except_df
check_efi_dmesg	$1				#After check_efi_parts
[[ "$GUI" ]] || [[ "$1" ]] && debug_echo_part_info
}

delete_tmp_folder_to_be_cleared() {
update_translations
echo "SET@_label0.set_text('''$LAB (os-prober). $This_may_require_several_minutes''')"
[[ "$DEBBUG" ]] && echo "[debug]Delete the content of TMP_FOLDER_TO_BE_CLEARED and put os-prober in memory"
[[ "$TMP_FOLDER_TO_BE_CLEARED" ]] && rm -f $TMP_FOLDER_TO_BE_CLEARED/* || echo "Error: TMP_FOLDER_TBC empty. $PLEASECONTACT"
}

debug_echo_part_info() {
local i d a b x y
echo "
$DASH PARTITIONS & DISKS:"
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	echo "${LISTOFPARTITIONS[$i]}	: ${DISK_PART[$i]},	${PART_WITH_SEPARATEBOOT[$i]},	${GRUB_ENV[$i]}\
	${GRUBVER[$i]},	${DOCGRUB[$i]},	${UPDATEGRUB_OF_PART[$i]},	${ARCH_OF_PART[$i]},	${BOOTPRESENCE_OF_PART[$i]},\
	${PART_WITH_OS[$i]},	${EFI_TYPE[$i]},	${BOOT_IN_FSTAB_OF_PART[$i]},	${EFI_IN_FSTAB_OF_PART[$i]},\
	${WINNT[$i]},	${WINL[$i]},	${RECOV[$i]},	${WINMGR[$i]},	${WINBOOTPART[$i]},\
	${APTTYP[$i]},	${GRUBTYPE_OF_PART[$i]},	${USRPRESENCE_OF_PART[$i]},	${USR_IN_FSTAB_OF_PART[$i]},\
	${SEPARATE_USR_PART[$i]},	${CUSTOMIZER[$i]},	${FARBIOS[$i]},	${BIOS_BOOT[$i]}, ${BLKIDMNT_POINT[$i]}."
done
echo ""
for ((d=1;d<=NBOFDISKS;d++)); do
	echo "${LISTOFDISKS[$d]}	: ${GPT_DISK[$d]},	${BIOS_BOOT_DISK[$d]},	${EFI_DISK[$d]}, \
	${USBDISK[$d]},	${MMCDISK[$d]}, ${DISK_WITHOS[$d]},	${SECTORS_BEFORE_PART[$d]} sectors * ${BYTES_PER_SECTOR[$d]} bytes"
done
echo "

$DASH parted -lm:

$PARTEDLM

$DASH lsblk:"
#UUID et MODEL are buggy: LANGUAGE=C lsblk -o KNAME,TYPE,FSTYPE,SIZE,LABEL,MODEL,UUID
LANGUAGE=C lsblk -o KNAME,TYPE,FSTYPE,SIZE,LABEL
echo " "
LANGUAGE=C lsblk -o KNAME,ROTA,RO,RM,STATE,MOUNTPOINT
echo "

$DASH mount:
$MOUNTB

"
[[ "$GUI" ]] && echo "SET@_label0.set_text('''$Scanning_systems. $Please_wait''')"

#debug
echo "$DASH ls:"
a=/sys/block/;for x in $(ls $a);do if [[ ! "$x" =~ ram ]] && [[ ! "$x" =~ oop ]];then b="";for y in $(ls $a$x);do b="$b $y";done;echo "$a$x (filtered): $b";fi;done
a="";for x in $(ls /dev);do if [[ ! "$x" =~ ram ]] && [[ ! "$x" =~ oop ]] && [[ ! "$x" =~ tty ]] && [[ ! "$x" =~ vcs ]];then a="$a $x";fi;done;echo "/dev (filtered): $a"
if [[ "$(ls /dev | grep -ix md )" ]];then
	a="";for x in $(ls /dev/md);do a="$a $x";done;echo "ls /dev/md: $a"
fi
for y in /dev/mapper /dev/cciss; do if [ -d $y ];then a="";for x in $(ls $y);do a="$a $x";done;echo "ls $y: $a";fi;done
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	if [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep efi)" ]] && [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep EFI)" ]] ;then #	&& [[ "${PART_WITH_OS[$i]}" = no-os ]]
		efitmp="$i"
		ls_efi_partition
	fi
	if [[ "$(echo "$BLKID" | grep "/dev/${LISTOFPARTITIONS[$i]}:" | grep 'TYPE="vfat"' )" ]] \
	|| [[ "$(echo "$BLKID" | grep "/dev/${LISTOFPARTITIONS[$i]}:" | grep 'TYPE="ntfs"' )" ]];then
		echo "
$DASH hexdump -n512 -C /dev/${LISTOFPARTITIONS[$i]}"
		hexdump -n512 -C /dev/"${LISTOFPARTITIONS[$i]}"
	fi
done
if [[ ! "$BLKID" =~ /dev/ ]];then #LP1042230 &1216688
	echo "

$DASH strace blkid:
"
	strace blkid
	echo "

$DASH end of strace blkid
"
fi
}

###################### DETERMINE PARTNB FROM A PARTNAME ################
determine_partnb() {
local partnbi
#Ex of input: "sda1"
for ((partnbi=1;partnbi<=NBOFPARTITIONS;partnbi++)); do
	[[ "$1" = "${LISTOFPARTITIONS[$partnbi]}" ]] && PARTNB="$partnbi"
done
}

########################## CHECK IF WUBI ###############################
check_wubi_existence() {
local i
TOTAL_QTY_OF_OS_INCLUDING_WUBI="$TOTAL_QUANTITY_OF_OS"; QTY_WUBI=0
WUBILDR=""
ROOTDISKMISSING=""
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	if [[ -f "${BLKIDMNT_POINT[$i]}/ubuntu/disks/root.disk" ]] ;then
		[[ "$GUI" ]] || [[ "$1" ]] && echo "There is Wubi inside ${LISTOFPARTITIONS[$i]}"
		(( TOTAL_QTY_OF_OS_INCLUDING_WUBI += 1 )); (( QTY_WUBI += 1 ))
		OS_NAME[$TOTAL_QTY_OF_OS_INCLUDING_WUBI]="$Ubuntu_installed_in_Windows_via_Wubi"
		OS_PARTITION[$TOTAL_QTY_OF_OS_INCLUDING_WUBI]="${LISTOFPARTITIONS[$i]}"
		WUBI[$QTY_WUBI]="$TOTAL_QTY_OF_OS_INCLUDING_WUBI"
		WUBI_PART[$QTY_WUBI]="$i"
		BLKIDMNT_POINTWUBI[$QTY_WUBI]="${BLKIDMNT_POINT[$i]}"
		MOUNTPOINTWUBI[$QTY_WUBI]="/mnt/boot-sav/wubi$QTY_WUBI"
		mkdir -p "${MOUNTPOINTWUBI[$QTY_WUBI]}"
	fi
	[[ -f "${BLKIDMNT_POINT[$i]}/wubildr" ]] && WUBILDR=yes
done
[[ "$QUANTITY_OF_REAL_WINDOWS" != 0 ]] && [[ "$QTY_WUBI" = 0 ]] && [[ "$WUBILDR" ]] && ROOTDISKMISSING=yes
#http://ubuntu-with-wubi.blogspot.ca/2011/08/missing-rootdisk.html
}


############################ CHECK DISK TYPES ##########################
check_disk_types() {
local d e f TMPDISK
GPT_DISK_WITHOUT_BIOS_BOOT=""
MSDOSPRESENT=""
NB_EFIPARTONGPT=0; NB_BISEFIPART=0 #cant move to check_part_types
for ((d=1;d<=NBOFDISKS;d++)); do #ex: http://paste.ubuntu.com/894616 , http://paste.ubuntu.com/1199042
	TMPDISK="${LISTOFDISKS[$d]}"
	if [[ "$(LANGUAGE=C LC_ALL=C fdisk -l "/dev/$TMPDISK" | grep -i GPT )" ]] \
	&& [[ ! "$(echo "$PARTEDLM" | grep -i msdos | grep "/dev/${TMPDISK}:" )" ]] \
	&& [[ ! "$(echo "$PARTEDLM" | grep -i loop | grep "/dev/${TMPDISK}:" )" ]] \
	|| [[ "$(echo "$PARTEDLM" | grep -i gpt | grep "/dev/${TMPDISK}:" )" ]];then
		GPT_DISK[$d]=GPT
		BIOS_BOOT_DISK[$d]=no-BIOS_boot
		f=""
		for e in $PARTEDLM;do #no "" !
			if [[ "$e" =~ /dev/ ]];then
				[[ "$e" =~ "/dev/${TMPDISK}:" ]] && f=ok || f=""
			fi
			[[ "$f" ]] && [[ "$e" =~ bios_grub ]] && BIOS_BOOT_DISK[$d]=BIOS_boot #eg http://paste.ubuntu.com/961886
		done
		[[ "${BIOS_BOOT_DISK[$d]}" != BIOS_boot ]] && GPT_DISK_WITHOUT_BIOS_BOOT=yes
	else
		GPT_DISK[$d]=not-GPT #table may be loop http://paste.ubuntu.com/1159385
		BIOS_BOOT_DISK[$d]=BIOSboot-not-needed
		MSDOSPRESENT=yes #used by fillin_bootflag_combobox
	fi
	[[ "$(ls -l /dev/disk/by-id | grep " usb-" | grep "${LISTOFDISKS[$d]}")" ]] \
	&& USBDISK[$d]=usb-disk || USBDISK[$d]=not-usb

	[[ "$(grep dev/mmc <<< dev/$TMPDISK )" ]] && MMCDISK[$d]=mmc-disk || MMCDISK[$d]=not-mmc

	BOOTFLAG_NEEDED[$d]=""
	if [[ "${GPT_DISK[$d]}" != GPT ]];then #some BIOS need a flag on primary partition
		p="$(LANGUAGE=C LC_ALL=C fdisk -l /dev/$TMPDISK | grep /dev | grep '*' )"
		if [[ ! "$(echo $p  | grep "/dev/${TMPDISK}1 " )" ]] && [[ ! "$(echo $p | grep "/dev/${TMPDISK}2 " )" ]] \
		&& [[ ! "$(echo $p | grep "/dev/${TMPDISK}3 " )" ]] && [[ ! "$(echo $p | grep "/dev/${TMPDISK}4 " )" ]] \
		|| [[ "$(echo $p | grep Empty )" ]];then #http://paste.ubuntu.com/1111263
			BOOTFLAG_NEEDED[$d]=setflag
		fi
	fi
	
	EFI_DISK[$d]=has-no-EFIpart #init
done
}


############################ CHECK PART TYPES ##########################
check_part_types() {
local i temp temp2 gg gi gm a b c d e uuidp ENVFILE ENDB line word
QTY_OF_PART_WITH_GRUB=0
QTY_OF_PART_WITH_APTGET=0
QTY_OF_32BITS_PART=0
QTY_OF_64BITS_PART=0
QTY_BOOTPART=0
QTY_WINBOOTTOREPAIR=0
SEP_BOOT_PARTS_PRESENCE=""
SEP_USR_PARTS_PRESENCE=""
EFIFILEPRESENCE=""
WINEFIFILEPRESENCE=""
BKPFILEPRESENCE=""
WINBKPFILEPRESENCE=""
for ((i=1;i<=NBOFPARTITIONS;i++)); do

	tempd=""
	DOCGRUB[$i]=""
	for z in "${BLKIDMNT_POINT[$i]}"/{,usr/}share/doc/;do
		if [[ -d "$z" ]];then
			check_grubdoc_1
			if [[ -d "$z/packages" ]];then #Suse
				z="$z/packages"
				check_grubdoc_1
			fi
		fi
	done
	for z in "${BLKIDMNT_POINT[$i]}"/{,usr/}share/doc/;do
		if [[ -d "$z" ]];then
			check_grubdoc_2
			if [[ -d "$z/packages" ]];then #Suse
				z="$z/packages"
				check_grubdoc_2
			fi
		fi
	done
	[[ -f "${BLKIDMNT_POINT[$i]}/sbin/grub-crypt" ]] && [[ ! "$(grep efi <<< "${DOCGRUB[$i]}")" ]] && DOCGRUB[$i]="grub-efi ${DOCGRUB[$i]}" #TODO which distro ?
	for z in "${BLKIDMNT_POINT[$i]}"/{,usr/}share/doc/;do
		if [[ -d "$z" ]];then
			lsz="$(ls $z | grep grub)"
			[[ "$lsz" ]] && [[ ! "${DOCGRUB[$i]}" ]] && DOCGRUB[$i]="grub1 ${DOCGRUB[$i]}"
			if [[ "$(grep signed <<< "$lsz" )" ]];then
				[[ ! "$(grep sign <<< "${DOCGRUB[$i]}")" ]] && DOCGRUB[$i]="signed ${DOCGRUB[$i]}"
			else
				for zz in $lsz;do
					[[ -d "$z$zz" ]] && [[ "$(ls "$z$zz" | grep signed)" ]] && [[ ! "$(grep sign <<< "${DOCGRUB[$i]}")" ]] && DOCGRUB[$i]="${zz}-signed ${DOCGRUB[$i]}"
				done
			fi
		fi
	done
	[[ ! "${DOCGRUB[$i]}" ]] && DOCGRUB[$i]=no-docgrub

	GRUBTYPE_OF_PART[$i]=nogrubinstall
	GRUBVER[$i]=nogrub
	for gg in /usr/sbin/ /usr/bin/ /sbin/ /bin/;do #not sure "type" is available in all distros
		for gi in grub-install.unsupported grub-install grub2-install;do
			if [[ -f "${BLKIDMNT_POINT[$i]}$gg$gi" ]];then
				GRUBTYPE_OF_PART[$i]=$gi
				GRUBTYPE_OF_PARTZ[$i]=$gg$gi
				[[ -f "${BLKIDMNT_POINT[$i]}${gg}grub" ]] && GRUBVER[$i]=grub1 || GRUBVER[$i]=grub2
			fi
		done
	done
	if [[ "${GRUBVER[$i]}" = grub2 ]] && [[ -d "${BLKIDMNT_POINT[$i]}/etc/default" ]] \
	&& [[ ! -f "${BLKIDMNT_POINT[$i]}/etc/default/grub" ]] \
	|| [[ "${GRUBTYPE_OF_PART[$i]}" =~ unsup ]];then
		GRUBVER[$i]=grub1 #care of sep /usr
		[[ ! -f "${BLKIDMNT_POINT[$i]}/etc/default/grub" ]] && echo "No ${LISTOFPARTITIONS[$i]}/etc/default/grub"
	fi
	
	UPDATEGRUB_OF_PART[$i]=no-update-grub
	for gg in /usr/sbin/ /usr/bin/ /sbin/ /bin/;do
		for gm in grub-mkconfig grub2-mkconfig;do
			[[ -f "${BLKIDMNT_POINT[$i]}$gg$gm" ]] && UPDATEGRUB_OF_PART[$i]="$gm -o /boot/grub" #then complete with 2/grub.cfg or /grub.cfg
		done
	done
	for gg in /usr/sbin/ /usr/bin/ /sbin/ /bin/;do
		[[ -f "${BLKIDMNT_POINT[$i]}${gg}update-grub" ]] && UPDATEGRUB_OF_PART[$i]=update-grub #Priority against grub-mkconfig
	done

	GRUBSETUP_OF_PART[$i]=nogrubsetup
	for gg in /usr/sbin/ /usr/bin/ /sbin/ /bin/;do
		[[ -f "${BLKIDMNT_POINT[$i]}${gg}grub-setup" ]] && GRUBSETUP_OF_PART[$i]=grub-setup
	done
	
	GRUBOK_OF_PART[$i]=""
	if [[ "${GRUBVER[$i]}" = grub1 ]] || [[ "${UPDATEGRUB_OF_PART[$i]}" != no-update-grub ]] \
	&& [[ "${GRUBTYPE_OF_PART[$i]}" != nogrubinstall ]];then
		GRUBOK_OF_PART[$i]=ok
		(( QTY_OF_PART_WITH_GRUB += 1 ))
		LIST_OF_PART_WITH_GRUB[$QTY_OF_PART_WITH_GRUB]="$i"
	fi
	
	if [[ -f "${BLKIDMNT_POINT[$i]}/usr/bin/apt-get" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/usr/bin/yum" ]] \
	|| [[ -f "${BLKIDMNT_POINT[$i]}/usr/bin/zypper" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/usr/bin/pacman" ]] \
	|| [[ -f "${BLKIDMNT_POINT[$i]}/bin/apt-get" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/bin/yum" ]] \
	|| [[ -f "${BLKIDMNT_POINT[$i]}/bin/zypper" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/bin/pacman" ]];then
		(( QTY_OF_PART_WITH_APTGET += 1 ))
		LIST_OF_PART_WITH_APTGET[$QTY_OF_PART_WITH_APTGET]="$i"
		if [[ -f "${BLKIDMNT_POINT[$i]}/usr/bin/apt-get" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/bin/apt-get" ]];then
			APTTYP[$i]=apt-get #Debian
			YESTYP[$i]="-y"
			INSTALLTYP[$i]=install
			PURGETYP[$i]=purge
			POLICYTYP[$i]="apt-cache policy"
			CANDIDATETYP[$i]="grep Candidate"
			CANDIDATETYP2[$i]="grep -v none"
			UPDATETYP[$i]="-y update"
		elif [[ -f "${BLKIDMNT_POINT[$i]}/usr/bin/yum" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/bin/yum" ]];then
			APTTYP[$i]=yum #fedora
			YESTYP[$i]=-y
			INSTALLTYP[$i]=install
			PURGETYP[$i]=erase
			POLICYTYP[$i]="yum info name"
			CANDIDATETYP[$i]="grep Available"
			UPDATETYP[$i]=makecache
		elif [[ -f "${BLKIDMNT_POINT[$i]}/usr/bin/zypper" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/bin/zypper" ]];then
			APTTYP[$i]='zypper --non-interactive' #opensuse
			YESTYP[$i]=''
			INSTALLTYP[$i]=in
			PURGETYP[$i]=rm
			POLICYTYP[$i]="zypper info"
			CANDIDATETYP[$i]="grep Installed"
			UPDATETYP[$i]=refresh
		elif [[ -f "${BLKIDMNT_POINT[$i]}/usr/bin/pacman" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/bin/pacman" ]];then
			APTTYP[$i]=pacman #arch
			YESTYP[$i]=''
			INSTALLTYP[$i]=-Sy
			PURGETYP[$i]=-R
			POLICYTYP[$i]="pacman -Syw --noconfirm"
			CANDIDATETYP[$i]="grep download"
			UPDATETYP[$i]="-Sy --noconfirm pacman"
			UPDATETYP2[$i]=pacman-db-upgrade
		#elif [[ -f "${BLKIDMNT_POINT[$i]}/usr/bin/urpmi" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/bin/urpmi" ]];then
		#	APTTYP[$i]=urpmi #http://wiki.mandriva.com/fr/Installer_et_supprimer_des_logiciels
		#	YESTYP[$i]=""
		#	INSTALLTYP[$i]=urpmi
		#	PURGETYP[$i]=urpme
		#	POLICYTYP[$i]=
		#	CANDIDATETYP[$i]="grep Installed"
		#	UPDATETYP[$i]="urpmi.update -a"
		#elif [[ -f "${BLKIDMNT_POINT[$i]}/usr/bin/emerge" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/bin/emerge" ]];then
		#	APTTYP[$i]=emerge #http://en.gentoo-wiki.com/wiki/Emerge
		#	YESTYP[$i]=
		#	INSTALLTYP[$i]=""
		#	PURGETYP[$i]=--unmerge
		#	POLICYTYP[$i]="emerge --search" #http://www.gentoo.org/doc/en/handbook/handbook-amd64.xml?part=2&chap=1
		#	CANDIDATETYP[$i]="grep installed"
		#	CANDIDATETYP2[$i]="grep -v 'Not Installed'"
		#	UPDATETYP[$i]="--sync"
		fi
	else
		APTTYP[$i]=nopakmgr
	fi

	temp="${BLKIDMNT_POINT[$i]}/etc/grub.d/"
	CUSTOMIZER[$i]=standard
	if [[ -d "$temp" ]];then
		if [[ "$GUI" ]] || [[ "$1" ]];then
			echo "
$DASH ${temp#*boot-sav/} :"
			ls -l "${BLKIDMNT_POINT[$i]}/etc" | grep grub.d #http://forum.ubuntu-fr.org/viewtopic.php?pid=9698751#p9698751
			ls -l "$temp"
			echo "
"
		fi
		[[ "$(ls "$temp" | grep prox)" ]] || [[ -d "${temp}bin" ]] || [[ ! "$(ls /usr/share/boot-sav | grep 'x-')" ]] && CUSTOMIZER[$i]=customized
		temp="${temp}40_custom"
		if [[ -f "$temp" ]];then
			temp2="$(cat "$temp" | grep -v "# " | grep -v '#!' | grep -v "exec tail")"
			if [[ "$temp2" ]];then
				[[ "$GUI" ]] || [[ "$1" ]] && echo "$DASH ${temp#*boot-sav/} :
$temp2

"
			fi
		fi
	fi

	DISABLE_OS[$i]=""
	temp="${BLKIDMNT_POINT[$i]}/etc/default/grub"
	if [[ -f "$temp" ]];then
		if [[ "$GUI" ]] || [[ "$1" ]];then
			echo "

$DASH ${temp#*boot-sav/} :
		"
			cat "$temp"
			echo "

"
		fi
		[[ "$(cat "$temp" | grep GRUB_DISABLE_OS | grep -v '#GRUB_DISABLE_OS' )" ]] && DISABLE_OS[$i]=yes
	fi

	LIB64=""
	for z in "${BLKIDMNT_POINT[$i]}"/{,usr/}lib64;do
		if [[ -d "$z" ]];then #http://paste.ubuntu.com/1072493 , http://forum.ubuntu-fr.org/viewtopic.php?pid=10355311#p10355311
			[[ "$(ls "$z" | grep -vi libfakeroot | grep -vi gnomenu | grep -vi elilo )" ]] && LIB64=yes
		fi
	done
	if [[ "${CURRENTSESSIONPARTITION}" = "${LISTOFPARTITIONS[$i]}" ]] && [[ "$(uname -m)" = i686 ]] \
	|| [[ ! "$LIB64" ]] || [[ "$ARCHIPC" = 32 ]];then
		ARCH_OF_PART[$i]=32
		(( QTY_OF_32BITS_PART += 1 ))
		for z in "${BLKIDMNT_POINT[$i]}"/{,usr/}lib64;do
			if [[ -d "$z" ]];then #debug, eg http://paste.ubuntu.com/1195587
				if [[ "$(ls "$z" | grep -vi libfakeroot | grep -vi gnomenu | grep -vi elilo )" ]];then
					b=""; for a in $(ls "$z");do b="$a $b";done;echo "$PLEASECONTACT : $z: $b"
				fi
			fi
		done
	else
		ARCH_OF_PART[$i]=64
		(( QTY_OF_64BITS_PART += 1 ))
	fi

	BOOTPRESENCE_OF_PART[$i]=no-boot
	tmp="${BLKIDMNT_POINT[$i]}/boot"
	if [[ -d "$tmp" ]] && [[ ! "$(grep -i /boot/efi <<< "${BLKIDMNT_POINT[$i]}/" )" ]];then #http://paste.ubuntu.com/1375034
		if [[ "$(ls "$tmp" )" ]] && [[ ! "$(ls "$tmp" | grep -ix bcd )" ]];then
			if [[ "$(ls "$tmp" | grep vmlinuz )" ]] && [[ "$(ls "$tmp" | grep initr )" ]];then #initramfs and vmlinuz-linux for Arch
				BOOTPRESENCE_OF_PART[$i]=with-boot
			else #if [[ ! "$(ls "$tmp" | grep '.efi' )" ]];then
				BOOTPRESENCE_OF_PART[$i]=no-kernel
				[[ "$GUI" ]] || [[ "$1" ]] && echo "$DASH No kernel in $tmp:
$(ls "$tmp")

"
			fi
		fi
	fi

	if [[ ! -d "${BLKIDMNT_POINT[$i]}/usr" ]];then
		USRPRESENCE_OF_PART[$i]=no---usr # REINSTALL_POSSIBLE will be Yes only if a separate /usr exists
	elif [[ ! "$(ls "${BLKIDMNT_POINT[$i]}/usr")" ]];then
		USRPRESENCE_OF_PART[$i]=emptyusr
	else # REINSTALL_POSSIBLE will be Yes
		USRPRESENCE_OF_PART[$i]=with--usr
	fi

	if [[ "${APTTYP[$i]}" != nopakmgr ]] || [[ "${GRUBOK_OF_PART[$i]}" ]] \
	&& [[ "${USRPRESENCE_OF_PART[$i]}" != with--usr ]] && [[ "${PART_WITH_OS[$i]}" != is-os ]];then
		SEPARATE_USR_PART[$i]=is-sep-usr
		SEP_USR_PARTS_PRESENCE=yes
	else
		SEPARATE_USR_PART[$i]=not-sep-usr
	fi
	

	if [[ -f "${BLKIDMNT_POINT[$i]}/etc/fstab" ]];then
		if [[ "$(cat "${BLKIDMNT_POINT[$i]}/etc/fstab" | grep /boot/efi | grep -v '#' )" ]];then
			EFI_IN_FSTAB_OF_PART[$i]=fstab-has-bad-efi
			EFI_OF_PART[$i]=""
			b=""
			while read line;do
				a="$(echo "$line" | grep /boot/efi | grep -v '#' )" #eg. UUID=0EC9-AA63  /boot/efi       vfat    defaults        0       1
				if [[ "$a" ]];then
					b="${a%%/boot/efi*}"	#eg. "UUID=0EC9-AA63	" , or "/dev/sda1	"
					break
				fi
			done < <(cat "${BLKIDMNT_POINT[$i]}/etc/fstab" )
			if [[ "$b" =~ UUID ]];then
				UUID_OF_EFIPART="${b##*=}"
				for ((uuidp=1;uuidp<=NBOFPARTITIONS;uuidp++)); do
					if [[ "$UUID_OF_EFIPART" =~ "${PART_UUID[$uuidp]}" ]];then
						EFI_OF_PART[$i]="$uuidp"
						EFI_IN_FSTAB_OF_PART[$i]=fstab-has-goodEFI
					fi
				done
			elif [[ "$b" =~ dev/ ]];then
				PARTOF_EFIPART="${b##*dev/}"
				for ((uuidp=1;uuidp<=NBOFPARTITIONS;uuidp++)); do
					if [[ "$PARTOF_EFIPART" =~ "${LISTOFPARTITIONS[$uuidp]}" ]];then
						EFI_OF_PART[$i]="$uuidp"
						EFI_IN_FSTAB_OF_PART[$i]=fstab-has-goodEFI
					fi
				done
			fi
			[[ "$GUI" ]] || [[ "$1" ]] && echo "/boot/efi detected in the fstab of ${LISTOFPARTITIONS[$i]}: $b (${LISTOFPARTITIONS[${EFI_OF_PART[$i]}]})"
		else
			EFI_IN_FSTAB_OF_PART[$i]=fstab-without-efi
		fi
		if [[ "$(cat "${BLKIDMNT_POINT[$i]}/etc/fstab" | grep /boot | grep -v /boot/ | grep -v '#' )" ]];then
			BOOT_IN_FSTAB_OF_PART[$i]=fstab-has-bad-boot
			BOOT_OF_PART[$i]=""
			b=""
			while read line;do
				a="$(echo "$line" | grep /boot | grep -v /boot/ | grep -v '#' )" #eg. UUID=0EC9-AA63  /boot       vfat    defaults        0       1
				if [[ "$a" ]];then
					b="${a%%/boot*}"	#eg. UUID=0EC9-AA63 , or /dev/sda1
					break
				fi
			done < <(cat "${BLKIDMNT_POINT[$i]}/etc/fstab" )
			if [[ "$b" =~ UUID ]];then
				UUID_OF_BOOTPART="${b##*=}"
				for ((uuidp=1;uuidp<=NBOFPARTITIONS;uuidp++)); do
					if [[ "$UUID_OF_BOOTPART" =~ "${PART_UUID[$uuidp]}" ]] && [[ "${PART_WITH_OS[$uuidp]}" = no-os ]];then
						BOOT_OF_PART[$i]="$uuidp"
						BOOT_IN_FSTAB_OF_PART[$i]=fstab-has-goodBOOT
					fi
				done
			elif [[ "$b" =~ dev/ ]];then
				PARTOF_BOOTPART="${b##*dev/}"
				for ((uuidp=1;uuidp<=NBOFPARTITIONS;uuidp++)); do
					if [[ "$PARTOF_BOOTPART" =~ "${LISTOFPARTITIONS[$uuidp]}" ]] && [[ "${PART_WITH_OS[$uuidp]}" = no-os ]];then
						BOOT_OF_PART[$i]="$uuidp"
						BOOT_IN_FSTAB_OF_PART[$i]=fstab-has-goodBOOT
					fi
				done
			fi
			[[ "$GUI" ]] || [[ "$1" ]] && echo "/boot detected in the fstab of ${LISTOFPARTITIONS[$i]}: $b (${LISTOFPARTITIONS[${BOOT_OF_PART[$i]}]})"
		else
			BOOT_IN_FSTAB_OF_PART[$i]=fstab-without-boot
		fi
		if [[ "$(cat "${BLKIDMNT_POINT[$i]}/etc/fstab" | grep /usr | grep -v /usr/ | grep -v '#' | grep -v swap)" ]];then
			USR_IN_FSTAB_OF_PART[$i]=fstab-has-bad-usr #http://paste.ubuntu.com/1099854
			USR_OF_PART[$i]=""
			b=""
			while read line;do
				a="$(echo "$line" | grep /usr | grep -v '#' )" #eg. UUID=0EC9-AA63  /usr       ext4    defaults        0       2
				if [[ "$a" ]];then
					b="${a%%/usr*}"	#eg. UUID=0EC9-AA63 , or /dev/sda1
					break
				fi
			done < <(cat "${BLKIDMNT_POINT[$i]}/etc/fstab" )
			if [[ "$b" =~ UUID ]];then
				UUID_OF_USRPART="${b##*=}"
				for ((uuidp=1;uuidp<=NBOFPARTITIONS;uuidp++)); do
					if [[ "$UUID_OF_USRPART" =~ "${PART_UUID[$uuidp]}" ]] && [[ "${PART_WITH_OS[$uuidp]}" = no-os ]];then
						USR_OF_PART[$i]="$uuidp"
						USR_IN_FSTAB_OF_PART[$i]=fstab-has-goodUSR
					fi
				done
			elif [[ "$b" =~ dev/ ]];then
				PARTOF_USRPART="${b##*dev/}"
				for ((uuidp=1;uuidp<=NBOFPARTITIONS;uuidp++)); do
					if [[ "$PARTOF_USRPART" =~ "${LISTOFPARTITIONS[$uuidp]}" ]] && [[ "${PART_WITH_OS[$uuidp]}" = no-os ]];then
						USR_OF_PART[$i]="$uuidp"
						USR_IN_FSTAB_OF_PART[$i]=fstab-has-goodUSR
					fi
				done
			fi
			[[ "$GUI" ]] || [[ "$1" ]] && echo "/usr detected in the fstab of ${LISTOFPARTITIONS[$i]}: $b (${LISTOFPARTITIONS[${USR_OF_PART[$i]}]})"
		else
			USR_IN_FSTAB_OF_PART[$i]=fstab-without-usr
		fi
	else
		EFI_IN_FSTAB_OF_PART[$i]=part-has-no-fstab
		BOOT_IN_FSTAB_OF_PART[$i]=part-has-no-fstab
		USR_IN_FSTAB_OF_PART[$i]=part-has-no-fstab
	fi
	
	PART_WITH_SEPARATEBOOT[$i]=not-sepboot
	if [[ "${PART_WITH_OS[$i]}" != no-os ]];then
		PART_WITH_SEPARATEBOOT[$i]=not-sepboot
	elif [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep vmlinuz )" ]] && [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep initr )" ]];then
		[[ "$DEBBUG" ]] && echo "[debug] ${LISTOFPARTITIONS[$i]} contains a kernel, so it is probably a /boot partition."
		(( QTY_BOOTPART += 1 ))
		PART_WITH_SEPARATEBOOT[$i]=is-sepboot
		SEP_BOOT_PARTS_PRESENCE=yes
	elif [[ ! "$(echo "$BLKID" | grep "/dev/${LISTOFPARTITIONS[$i]}:" | grep 'TYPE="vfat"' )" ]] \
	&& [[ ! "$(echo "$BLKID" | grep "/dev/${LISTOFPARTITIONS[$i]}:" | grep 'TYPE="ntfs"' )" ]];then
		PART_WITH_SEPARATEBOOT[$i]=maybesepboot
		SEP_BOOT_PARTS_PRESENCE=yes
	fi

	[[ "${PART_WITH_OS[$i]}" = no-os ]] && temp="" || temp=/boot


	GRUB_ENV[$i]=no-grubenv
	if [[ -f "${BLKIDMNT_POINT[$i]}${temp}/grub/grubenv" ]];then
		GRUB_ENV[$i]=grubenv-ok
		ENVFILE="$LOGREP/${LISTOFPARTITIONS[$i]}/grubenv"
		cp "${BLKIDMNT_POINT[$i]}${temp}/grub/grubenv" "$ENVFILE"
		sed -i "/^#/ d" "$ENVFILE"
		sed -i "/^\/var\/log\/boot-sav/ d" "$ENVFILE"
		temp="$(cat "$ENVFILE")"
		if [[ "$temp" ]];then
			GRUB_ENV[$i]=grubenv-ng
			[[ "$GUI" ]] || [[ "$1" ]] && echo "
$DASH ${LISTOFPARTITIONS[$i]}${temp}/grub/grubenv :
$temp


"
		fi
	fi


	PART_GRUBLEGACY[$i]=no-legacy-files
	for z in "${BLKIDMNT_POINT[$i]}"/{,boot/}grub/menu.lst;do
		[[ -f "$z" ]] && PART_GRUBLEGACY[$i]=has-legacyfiles && echo "$z detected"
	done

	WINXPTOREPAIR[$i]=""
	WINSETOREPAIR[$i]="" #after xp
	if [[ "${RECOV[$i]}" != recovery-or-hidden ]] && [[ "${WINXP[$i]}" ]];then
	#&& [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep -ix 'Program Files' )" ]] http://paste.ubuntu.com/1032766
		(( QTY_WINBOOTTOREPAIR += 1 ))
		WINXPTOREPAIR[$i]=yes
	elif [[ "${WINMGR[$i]}" = no-bmgr ]] || [[ "${WINBCD[$i]}" = no-b-bcd ]] || [[ "${WINL[$i]}" = no-winload ]] \
	&& [[ "${RECOV[$i]}" != recovery-or-hidden ]] && [[ "${WINSE[$i]}" ]];then
		(( QTY_WINBOOTTOREPAIR += 1 ))
		WINSETOREPAIR[$i]=yes
	fi

	FARBIOS[$i]=not-far
	part="${LISTOFPARTITIONS[$i]}" #eg mapper/isw_beaibbhjji_Volume0p1

	### TODO les grep/cut ne fonctionne probablement plus avec fdisk
	while read temp;do
		if [[ "$temp" =~ "/dev/$part " ]] && [[ ! "$temp" =~ GPT ]];then #eg: /dev/sda3   *    81922048   163842047    40960000    7  HPFS
			[[ "$temp" =~ '*' ]] && temp="${temp#* \*}" || temp="${temp#* }" #eg:  81922048   163842047    40960000    7  HPFS
			a=0
			for b in $temp; do
				(( a += 1 ))
				if [[ "$a" = 2 ]];then
					e="${BYTES_PER_SECTOR[${DISKNB_PART[$i]}]}"
					if [[ "$b" =~ [0-9][0-9][0-9] ]];then
						c="$(( e * b ))"
						ENDB="$(( c / 1000000000 ))"
						[[ "$ENDB" ]] && check_farbios
					fi
					break
				fi
			done
		fi
	done < <(echo "$FDISKL")
	#workaround fdisk bug: http://ubuntuforums.org/showthread.php?t=2085733
	f=""
	while read line;do #eg 1:1049kB:21.0GB:21.0GB:ext4::;
		if [[ "$line" =~ /dev/ ]];then
			[[ "$line" =~ "/dev/${DISK_PART[$i]}:" ]] && f=ok || f=""
		fi
		if [[ "$f" ]] && [[ "${line%%:*}" = "${part##*[a-z]}" ]];then
			ENDB="${line#*B:}" #eg 21.0GB:21.0GB:ext4::;
			ENDB="${ENDB%%B:*}" #eg 21.0G
			if [[ "$ENDB" =~ G ]];then
				ENDB="${ENDB%%G*}" #eg 21.0
				[[ "$ENDB" =~ '.' ]] && ENDB="${ENDB%%.*}" #eg 21
				[[ "$ENDB" ]] && check_farbios
			fi
		fi
	done < <(echo "$PARTEDLM")
	
	if [[ -f "${BLKIDMNT_POINT[$i]}/etc/mdadm/mdadm.conf" ]];then
		[[ "$GUI" ]] || [[ "$1" ]] && echo "
$DASH ${LISTOFPARTITIONS[$i]}/etc/mdadm/mdadm.conf :
$(cat "${BLKIDMNT_POINT[$i]}"/etc/mdadm/mdadm.conf)


"
		if [[ -f "${BLKIDMNT_POINT[$i]}/proc/mdstat" ]];then
			[[ "$GUI" ]] || [[ "$1" ]] && echo "
$DASH ${LISTOFPARTITIONS[$i]}/proc/mdstat :
$(cat "${BLKIDMNT_POINT[$i]}"/proc/mdstat)


"
		fi
	fi

	ddd="${DISKNB_PART[$i]}"
	if [[ -d "${BLKIDMNT_POINT[$i]}/casper" ]] || [[ -d "${BLKIDMNT_POINT[$i]}/preseed" ]] \
	|| [[ -f "${BLKIDMNT_POINT[$i]}/autorun.inf" ]] || [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep '.sys' )" ]] \
	&& [[ "${USBDISK[${DISKNB_PART[$i]}]}" = usb-disk ]] || [[ -f "${BLKIDMNT_POINT[$i]}/ldlinux.sys" ]];then
		#eg http://ubuntuforums.org/showpost.php?p=12264795&postcount=574
		#ex with usb not detected: http://paste.ubuntu.com/1370752
		USBDISK[$ddd]=liveusb		
	fi
	if [[ -d "${BLKIDMNT_POINT[$i]}/casper" ]] || [[ -d "${BLKIDMNT_POINT[$i]}/preseed" ]] \
	|| [[ -f "${BLKIDMNT_POINT[$i]}/autorun.inf" ]] || [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep '.sys' )" ]] \
	&& [[ "${MMCDISK[${DISKNB_PART[$i]}]}" = mmc-disk ]] || [[ -f "${BLKIDMNT_POINT[$i]}/ldlinux.sys" ]];then
		MMCDISK[$ddd]=livemmc		
	fi
	
	WINEFI[$i]=""
	BOOTEFI[$i]=""
	MACEFI[$i]=""
	EFI_TYPE[$i]=not--efi--part #init
	tmp="${DISKNB_PART[$i]}"
	if [[ -d "${BLKIDMNT_POINT[$i]}/efi" ]] || [[ -d "${BLKIDMNT_POINT[$i]}/EFI" ]] \
	&& [[ "${USBDISK[$tmp]}" != liveusb ]] && [[ "${MMCDISK[$tmp]}" != livemmc ]];then #exclude liveUSB , eg http://paste.ubuntu.com/1195690
		d="${DISKNB_PART[$i]}"
		this_part_maybe_efi
		[[ -d "${BLKIDMNT_POINT[$i]}/EFI" ]] && efidoss="${BLKIDMNT_POINT[$i]}/EFI" || efidoss="${BLKIDMNT_POINT[$i]}/efi"
		for z in $efidoss/Microsoft/{,*/}*.efi;do #eg /EFI/Microsoft/Boot/bootmgfw.efi or bootx64.efi
			if [[ ! "$z" =~ '*' ]] && [[ ! "$z" =~ bootmgr.efi ]] \
			&& [[ ! "$z" =~ memtest.efi ]];then #http://ubuntuforums.org/showpost.php?p=12114780&postcount=18
				echo "Presence of EFI/Microsoft file detected: $z"
				EFIFILEPRESENCE=yes #tab-main
				( [[ -f "$efidoss"/Microsoft/Boot/bootmgfw.efi ]] && [[ ! -f "$efidoss"/Microsoft/Boot/bootmgfw.efi.grb ]] ) \
				|| ( [[ -f "$efidoss"/Microsoft/Boot/bootx64.efi ]] && [[ ! -f "$efidoss"/Microsoft/Boot/bootx64.efi.grb ]] ) \
				&& WINEFIFILEPRESENCE=yes && WINEFI[$i]=y #efi-fillin
			fi
		done
		for z in $efidoss/Boot/{,*/}*.efi;do
			if [[ ! "$z" =~ '*' ]];then
				echo "Presence of EFI/Boot file detected: $z"
				EFIFILEPRESENCE=yes #tab-main
				#[[ "$z" =~ Boot/bootx64.efi ]] && WINEFIFILEPRESENCE=yes
				#BOOTEFI[$i]="${z#*${BLKIDMNT_POINT[$i]}}" #eg /efi/Boot/bootx64.efi
			fi
		done
		for z in $efidoss/{,*/}*/*.scap;do
			if [[ ! "$z" =~ '*' ]];then
				echo "Presence of MacEFI file detected: $z" #File but no OS: http://ubuntuforums.org/showthread.php?t=2077532
				EFIFILEPRESENCE=yes #tab-main
				MACEFIFILEPRESENCE=yes #tab-loca
				#http://forum.ubuntu-fr.org/viewtopic.php?id=983441
				#MACEFI[$i]="${z#*${BLKIDMNT_POINT[$i]}}" #eg /efi/APPLE/EXTENSIONS/Firmware.scap
			fi
		done
		for z in $efidoss/{,*/}*/*.bkp $efidoss/{,*/}*/bkp*.efi;do
			if [[ ! "$z" =~ '*' ]];then
				BKPFILEPRESENCE=yes
				if [[ "$z" =~ icros ]];then
					[[ "$GUI" ]] || [[ "$1" ]] && echo "Presence of winbkp file detected: $z"
					WINBKPFILEPRESENCE=yes
				else
					[[ "$GUI" ]] || [[ "$1" ]] && echo "Presence of bkp file detected: $z"
				fi
			fi
		done
	fi
	efi_check
done
QTY_OF_OTHER_LINUX="$QTY_OF_PART_WITH_GRUB"
}


check_grubdoc_1() {
lsz="$(ls $z | grep grub)"
for zz in $lsz;do
	if [[ "$(grep efi <<< "$zz" )" ]] || ( [[ -d "$z$zz" ]] && [[ "$(ls "$z$zz" | grep efi )" ]] );then
		[[ ! "$(grep efi <<< "${DOCGRUB[$i]}")" ]] && DOCGRUB[$i]="grub-efi ${DOCGRUB[$i]}"
	elif [[ "$(grep pc <<< "$zz" )" ]] || ( [[ -d "$z$zz" ]] && [[ "$(ls "$z$zz" | grep pc )" ]] );then
		[[ ! "$(grep pc <<< "${DOCGRUB[$i]}")" ]] && DOCGRUB[$i]="grub-pc ${DOCGRUB[$i]}"
	elif [[ "$(grep legacy <<< "$zz" )" ]] || ( [[ -d "$z$zz" ]] && [[ "$(ls "$z$zz" | grep legacy )" ]] );then
		[[ ! "$(grep grub1 <<< "${DOCGRUB[$i]}")" ]] && DOCGRUB[$i]="grub1 ${DOCGRUB[$i]}"
	fi
done
}

check_grubdoc_2() {
lsz="$(ls $z | grep grub)"
for zz in $lsz;do
	if [[ ! "$(grep efi <<< "${DOCGRUB[$i]}")" ]] && [[ ! "$(grep pc <<< "${DOCGRUB[$i]}")" ]];then
		if [[ "$(grep grub2 <<< "$zz" )" ]] || ( [[ -d "$z$zz" ]] && [[ "$(ls "$z$zz" | grep grub2 )" ]] );then
			DOCGRUB[$i]="grub-pc ${DOCGRUB[$i]}"
		fi
	fi
done
}

check_farbios() {
d="$(( ENDB / 100 ))"
[[ "$d" != 0 ]] && FARBIOS[$i]=farbios
[[ "$DEBBUG" ]] && echo "[debug] ${LISTOFPARTITIONS[$i]} ends at ${c}GB. ${FARBIOS[$i]}"
}


################## WARNINGS BEFORE DISPLAYING MAIN MENU ################
check_options_warning() {
local FUNCTION
#if [[ "$NB_EFIPARTONGPT" -ge 1 ]] && [[ ! "$MACEFIFILEPRESENCE" ]];then
#	FUNCTION=EFI
#	update_translations
#	zenity --width=300 --info --title="$APPNAME2" --text="$FUNCTION_detected $Please_check_options"
#	echo "$FUNCTION_detected $Please_check_options"
#fi
if [[ "$QTY_BOOTPART" -ge 1 ]] && [[ "$LIVESESSION" = live ]];then
	FUNCTION=/boot
	update_translations
	zenity --width=300 --info --title="$APPNAME2" --text="$FUNCTION_detected $Please_check_options"
	echo "$FUNCTION_detected $Please_check_options"
fi
if [[ "$QTY_SEP_USR_PARTS" -ge 1 ]] && [[ "$LIVESESSION" = live ]];then
	FUNCTION=/usr
	update_translations
	zenity --width=300 --info --title="$APPNAME2" --text="$FUNCTION_detected $Please_check_options"
	echo "$FUNCTION_detected $Please_check_options"
fi
}

warnings_and_show_mainwindow() {
WIOULD=would
end_pulse
[[ ! "$CLEANNAME" =~ nf ]] && check_options_warning
echo 'SET@_mainwindow.show()'
}

debug_echo_important_variables() {
[[ "$DEBBUG" ]] && echo "[debug] debug_echo_important_variables"
if [[ "$WIOULD" =~ ld ]] || [[ "$MAIN_MENU" =~ Recomm ]];then
	[[ "$APPNAME" =~ os ]] &&  THISSET="The default settings of $CLEANNAME" || THISSET="The default repair of the Boot-Repair utility"
else
	THISSET="The settings chosen by the user"
fi
IMPVAR="$THISSET $WIOULD"
[[ "$APPNAME" =~ os ]] && IMPVAR="$IMPVAR $FORMAT_OS ($FORMAT_TYPE) wubi($WUBI_TO_DELETE), then"
if [[ "$MBR_ACTION" = restore ]];then
	IMPVAR="$IMPVAR restore the [${MBR_TO_RESTORE#* }] MBR in $DISK_TO_RESTORE_MBR, and make it boot on ${LISTOFPARTITIONS[$TARGET_PARTITION_FOR_MBR]}."
elif [[ "$BOOTFLAG_ACTION" ]] || [[ "$UNHIDEBOOT_ACTION" ]] || [[ "$FSCK_ACTION" ]] || [[ "$WUBI_ACTION" ]] || [[ "$WINBOOT_ACTION" ]] \
|| [[ "$CREATE_BKP_ACTION" ]] || [[ "$RESTORE_BKP_ACTION" ]] && [[ "$MBR_ACTION" = nombraction ]];then
	IMPVAR="$IMPVAR not act on the MBR."
elif [[ "$MBR_ACTION" = nombraction ]];then
	IMPVAR="$IMPVAR not act on the boot."
else
	[[ "$GRUBPURGE_ACTION" ]] && IMPVAR="$IMPVAR purge ($PURGREASON) and"
	IMPVAR="$IMPVAR reinstall the $GRUBPACKAGE of ${LISTOFPARTITIONS[$REGRUB_PART]}"
	if [[ ! "$GRUBPACKAGE" =~ efi ]];then
		[[ "$FORCE_GRUB" = place-in-MBR ]] || [[ "$REMOVABLEDISK" ]] && IMPVAR="$IMPVAR into the MBR of $NOFORCE_DISK"
		[[ "$FORCE_GRUB" = force-in-PBR ]] && IMPVAR="$IMPVAR into the PBR of $FORCE_PARTITION"
		[[ ! "$REMOVABLEDISK" ]] && [[ "$FORCE_GRUB" = place-in-all-MBRs ]] && IMPVAR="$IMPVAR into the MBRs of all disks (except live-disks and removable disks without OS)"
	fi
	[[ "$LASTGRUB_ACTION" ]] || [[ "$BLANKEXTRA_ACTION" ]] || [[ "$UNCOMMENT_GFXMODE" ]] || [[ "$ATA" ]] \
	|| [[ "$KERNEL_PURGE" ]] || [[ "$USE_SEPARATEBOOTPART" ]] || [[ "$USE_SEPARATEUSRPART" ]] \
	|| [[ "$ADD_KERNEL_OPTION" ]] || [[ "$GRUBPACKAGE" =~ efi ]] || [[ "$DISABLEWEBCHECK" ]] || [[ "$CHANGEDEFAULTOS" ]] \
	&& IMPVAR="$IMPVAR, using the following options: $LASTGRUB_ACTION $BLANKEXTRA_ACTION $UNCOMMENT_GFXMODE $ATA $KERNEL_PURGE $DISABLEWEBCHECK $CHANGEDEFAULTOS" \
	|| IMPVAR="$IMPVAR."
	[[ "$USE_SEPARATEBOOTPART" ]] && IMPVAR="$IMPVAR ${LISTOFPARTITIONS[$BOOTPART_TO_USE]}/boot,"
	[[ "$USE_SEPARATEUSRPART" ]] && IMPVAR="$IMPVAR ${LISTOFPARTITIONS[$USRPART_TO_USE]}/usr,"
	[[ "$GRUBPACKAGE" =~ efi ]] && IMPVAR="$IMPVAR ${LISTOFPARTITIONS[$EFIPART_TO_USE]}/boot/efi,"
	[[ "$ADD_KERNEL_OPTION" ]] && IMPVAR="$IMPVAR $ADD_KERNEL_OPTION ($CHOSEN_KERNEL_OPTION),"
	[[ "$REMOVABLEDISK" ]] && [[ "$FORCE_GRUB" = place-in-all-MBRs ]] && IMPVAR="$IMPVAR
It $WIOULD also fix access to other systems (other MBRs) for the situations when the removable media is disconnected."
	[[ "$NOTEFIREASON" ]] && IMPVAR="$IMPVAR
Grub-efi $WIOULD not be selected by default because: $NOTEFIREASON"
fi
[[ "$BOOTFLAG_ACTION" ]] && IMPVAR="$IMPVAR
The boot flag $WIOULD be placed on ${LISTOFPARTITIONS[$BOOTFLAG_TO_USE]}."
[[ "$UNHIDEBOOT_ACTION" ]] || [[ "$FSCK_ACTION" ]] || [[ "$WUBI_ACTION" ]] || [[ "$WINBOOT_ACTION" ]] \
|| [[ "$CREATE_BKP_ACTION" ]] || [[ "$RESTORE_BKP_ACTION" ]] && IMPVAR="$IMPVAR
Additional repair $WIOULD be performed: $UNHIDEBOOT_ACTION $FSCK_ACTION $WUBI_ACTION $WINBOOT_ACTION $CREATE_BKP_ACTION $WINEFI_BKP_ACTION $RESTORE_BKP_ACTION"
}
