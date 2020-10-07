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

########################## RESTORE MBR #################################
restore_mbr() {
local temp BETWEEN_PARENTHESIS HBACKUP DBACKUP
DISK_TO_RESTORE_MBR="${MBR_TO_RESTORE%% (*}"
echo "Will restore the MBR_TO_RESTORE : $MBR_TO_RESTORE into $DISK_TO_RESTORE_MBR"
temp="${MBR_TO_RESTORE#* (}"; BETWEEN_PARENTHESIS="${temp%)*}"
echo "SET@_label0.set_text('''$Restore_MBR. $Please_wait''')"
if [[ -f $LOGREP/$DISK_TO_RESTORE_MBR/current_mbr.img ]];then	#Security
	cp $LOGREP/$DISK_TO_RESTORE_MBR/current_mbr.img $LOGREP/$DISK_TO_RESTORE_MBR/mbr_before_restoring_mbr.img
	if [[ "$MBR_TO_RESTORE" =~ xp ]];then
		install-mbr -e ${TARGET_PARTITION_FOR_MBR} /dev/${DISK_TO_RESTORE_MBR}; echo "install-mbr -e ${TARGET_PARTITION_FOR_MBR} /dev/${DISK_TO_RESTORE_MBR}"
	elif [[ "$BETWEEN_PARENTHESIS" =~ mbr ]];then
		BETWEEN_PARENTHESIS="${BETWEEN_PARENTHESIS#* }"
		[[ -f "/usr/lib/syslinux/mbr/${BETWEEN_PARENTHESIS}.bin" ]] && BETWEEN_PARENTHESIS=mbr/"$BETWEEN_PARENTHESIS"
		echo "dd if=/usr/lib/syslinux/${BETWEEN_PARENTHESIS}.bin of=/dev/${DISK_TO_RESTORE_MBR}"
		dd if=/usr/lib/syslinux/${BETWEEN_PARENTHESIS}.bin of=/dev/${DISK_TO_RESTORE_MBR} bs=446 count=1
		bootflag_action ${TARGET_PARTITION_FOR_MBR}
	else
		echo "Error : $MBR_TO_RESTORE [$BETWEEN_PARENTHESIS] could not be restored in $DISK_TO_RESTORE_MBR. $PLEASECONTACT"
		zenity --width=300 --error --text="Error : $MBR_TO_RESTORE could not be restored in $DISK_TO_RESTORE_MBR. $PLEASECONTACT"
	fi
else
	echo "Error : $LOGREP/$DISK_TO_RESTORE_MBR/current_mbr.img does not exist. $PLEASECONTACT"
	zenity --width=300 --error --text="Error : $LOGREP/$DISK_TO_RESTORE_MBR/current_mbr.img does not exist. MBR could not be restored. $PLEASECONTACT"
	ERROR=yes
fi
}


######################### RESTORE BKP EFI  #############################
restore_efi_bkp_files() {
#called by first_actions
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	EFIDO="${BLKIDMNT_POINT[$i]}/"
	for chgfile in Microsoft/Boot/bootmgfw.efi Microsoft/Boot/bootx64.efi Boot/bootx64.efi;do
		for eftmp in efi EFI;do
			EFIFICH="$EFIDO$eftmp/$chgfile"
			restore_one_efi_bkp
		done
	done
done
}

restore_one_efi_bkp() {
EFIFOLD="${EFIFICH%/*}"
EFIFICHEND="${chgfile##*/}"
NEWEFIL="$EFIFOLD/bkp$EFIFICHEND"
if [[ -f "$EFIFICH.grb" ]];then
	echo "rm $EFIFICH $EFIFICH.grb" && rm "$EFIFICH"
	[[ ! -f "$EFIFICH" ]] && rm "$EFIFICH.grb"
fi
if [[ -f "$EFIFICH.bkp" ]] || [[ -f "$NEWEFIL" ]];then
	[[ -f "$EFIFICH" ]] && echo "rm $EFIFICH" && rm "$EFIFICH"
	if [[ -f "$EFIFICH" ]];then
		echo "Error: could not rm $EFIFICH"
	else
		[[ -f "$EFIFICH.bkp" ]] && mv "$EFIFICH.bkp" "$EFIFICH"
		[[ -f "$NEWEFIL" ]] && mv "$NEWEFIL" "$EFIFICH"
	fi
fi
}

######################### UNHIDE BOOT MENUS ############################
unhide_boot_menus_xp() {
[[ "$DEBBUG" ]] && echo "[debug]Unhide boot menu ($UNHIDEBOOT_TIME seconds) if Wubi detected"
local i word MODIFDONE
if [[ "$QTY_WUBI" != 0 ]];then
	for ((i=1;i<=NBOFPARTITIONS;i++)); do
		if [[ -f "${BLKIDMNT_POINT[$i]}/boot.ini" ]];then
			echo "SET@_label0.set_text('''$Unhide_boot_menu. $This_may_require_several_minutes''')"
			cp "${BLKIDMNT_POINT[$i]}/boot.ini" "$LOGREP/${LISTOFPARTITIONS[$i]}/boot.ini_old"
			cp "${BLKIDMNT_POINT[$i]}/boot.ini" "$LOGREP/${LISTOFPARTITIONS[$i]}/boot.ini_new"
			MODIFDONE=""
			for word in $(cat "${BLKIDMNT_POINT[$i]}/boot.ini"); do #No " around cat
				if [[ "$word" =~ "timeout=" ]] && [[ "$word" != "timeout=$UNHIDEBOOT_TIME" ]];then
					sed -i "s/${word}.*/timeout=${UNHIDEBOOT_TIME}/" "$LOGREP/${LISTOFPARTITIONS[$i]}/boot.ini_new"
					MODIFDONE=yes
				fi #http://ubuntuforums.org/showthread.php?p=12394097#post12394097
			done
			if [[ -f "$LOGREP/${LISTOFPARTITIONS[$i]}/boot.ini_new" ]] && [[ "$MODIFDONE" = yes ]];then #Security
				echo "Unhide Windows XP boot menu in ${LISTOFPARTITIONS[$i]}/boot.ini"
				mv "$LOGREP/${LISTOFPARTITIONS[$i]}/boot.ini_new" "${BLKIDMNT_POINT[$i]}/boot.ini"
			elif [[ ! -f "$LOGREP/${LISTOFPARTITIONS[$i]}/boot.ini_new" ]];then
				echo "Error: could not unhide XP in ${LISTOFPARTITIONS[$i]}/boot.ini"
				zenity --width=300 --error --text="Error: could not unhide XP in ${LISTOFPARTITIONS[$i]}/boot.ini"
			else
				rm "$LOGREP/${LISTOFPARTITIONS[$i]}/boot.ini_old"
				rm "$LOGREP/${LISTOFPARTITIONS[$i]}/boot.ini_new"
			fi
		fi
	done
fi
}

unhide_boot_menus_etc_default_grub() {
local i MODIFDONE word
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	if [[ -f "${BLKIDMNT_POINT[$i]}/etc/default/grub" ]];then
		echo "SET@_label0.set_text('''$Unhide_boot_menu. $This_may_require_several_minutes''')"
		cp "${BLKIDMNT_POINT[$i]}/etc/default/grub" "$LOGREP/${LISTOFPARTITIONS[$i]}/etc_default_grub_old"
		cp "${BLKIDMNT_POINT[$i]}/etc/default/grub" "$LOGREP/${LISTOFPARTITIONS[$i]}/etc_default_grub_new"
		MODIFDONE=""
		for word in $(cat "${BLKIDMNT_POINT[$i]}/etc/default/grub"); do
			if [[ "$word" =~ "GRUB_TIMEOUT=" ]] && [[ "$word" != "GRUB_TIMEOUT=${UNHIDEBOOT_TIME}" ]];then
				sed -i "s/${word}.*/GRUB_TIMEOUT=${UNHIDEBOOT_TIME}/" "$LOGREP/${LISTOFPARTITIONS[$i]}/etc_default_grub_new"
				MODIFDONE=yes #Set timout to UNHIDEBOOT_TIME seconds
			elif [[ "$word" =~ "GRUB_HIDDEN_TIMEOUT=" ]] && [[ ! "$word" =~ "#GRUB_HIDDEN_TIMEOUT=" ]];then
				sed -i "s/${word}.*/#${word}/" "$LOGREP/${LISTOFPARTITIONS[$i]}/etc_default_grub_new"
				MODIFDONE=yes #Comment GRUB_HIDDEN_TIMEOUT
			elif [[ "$word" =~ "GRUB_DISABLE_RECOVERY=" ]] && [[ ! "$word" =~ "#GRUB_DISABLE_RECOVERY=" ]];then
				sed -i "s/${word}.*/#${word}/" "$LOGREP/${LISTOFPARTITIONS[$i]}/etc_default_grub_new"
				MODIFDONE=yes #Comment GRUB_DISABLE_RECOVERY
			fi
		done
		if [[ -f "$LOGREP/${LISTOFPARTITIONS[$i]}/etc_default_grub_new" ]] && [[ "$MODIFDONE" = yes ]];then #Security
			echo "Unhide GRUB boot menu in ${LISTOFPARTITIONS[$i]}/etc/default/grub"
			mv "$LOGREP/${LISTOFPARTITIONS[$i]}/etc_default_grub_new" "${BLKIDMNT_POINT[$i]}/etc/default/grub"
		elif [[ ! -f "$LOGREP/${LISTOFPARTITIONS[$i]}/etc_default_grub_new" ]];then
			echo "Error: could not unhide GRUB menu in ${LISTOFPARTITIONS[$i]}/etc/default/grub"
			zenity --width=300 --error --text="Error: could not unhide GRUB menu in ${LISTOFPARTITIONS[$i]}/etc/default/grub"
		else
			rm "$LOGREP/${LISTOFPARTITIONS[$i]}/etc_default_grub_old"
			rm "$LOGREP/${LISTOFPARTITIONS[$i]}/etc_default_grub_new"
		fi
	fi
done
comment_disable_os
}

comment_disable_os() {
[[ "${DISABLE_OS[$REGRUB_PART]}" ]] && sed -i "s/GRUB_DISABLE_OS/#GRUB_DISABLE_OS/" "${BLKIDMNT_POINT[$REGRUB_PART]}/etc/default/grub"
}

unhide_boot_menus_grubcfg() {
local i FLD MODIFDONE word
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	for FLD in grub grub2;do
		if [[ -f "${BLKIDMNT_POINT[$i]}/boot/$FLD/grub.cfg" ]];then
			echo "SET@_label0.set_text('''$Unhide_boot_menu. $This_may_require_several_minutes''')"
			cp "${BLKIDMNT_POINT[$i]}/boot/$FLD/grub.cfg" "$LOGREP/${LISTOFPARTITIONS[$i]}/grub.cfg_old"
			cp "${BLKIDMNT_POINT[$i]}/boot/$FLD/grub.cfg" "$LOGREP/${LISTOFPARTITIONS[$i]}/grub.cfg_new"
			MODIFDONE=""
			for word in $(cat "${BLKIDMNT_POINT[$i]}/boot/$FLD/grub.cfg"); do
				if [[ "$word" =~ "timeout=" ]] && [[ "$word" != "timeout=$UNHIDEBOOT_TIME" ]];then
					sed -i "s/$word.*/timeout=$UNHIDEBOOT_TIME/" "$LOGREP/${LISTOFPARTITIONS[$i]}/grub.cfg_new"
					MODIFDONE=yes #Set timout to UNHIDEBOOT_TIME seconds
				fi
			done
			if [[ -f "$LOGREP/${LISTOFPARTITIONS[$i]}/grub.cfg_new" ]] && [[ "$MODIFDONE" = yes ]];then #Security
				echo "Unhide GRUB boot menu in ${LISTOFPARTITIONS[$i]}/boot/$FLD/grub.cfg"
				mv "$LOGREP/${LISTOFPARTITIONS[$i]}/grub.cfg_new" "${BLKIDMNT_POINT[$i]}/boot/$FLD/grub.cfg"
				[[ "$i" = "$REGRUB_PART" ]] && rm "$LOGREP/${LISTOFPARTITIONS[$i]}/grub.cfg_old" #Not needed
			elif [[ ! -f "$LOGREP/${LISTOFPARTITIONS[$i]}/grub.cfg_new" ]];then
				echo "Error: could not unhide GRUB menu in ${LISTOFPARTITIONS[$i]}/boot/$FLD/grub.cfg"
				zenity --width=300 --error --text="Error: could not unhide GRUB menu in ${LISTOFPARTITIONS[$i]}/boot/$FLD/grub.cfg"
			else
				rm "$LOGREP/${LISTOFPARTITIONS[$i]}/grub.cfg_old"
				rm "$LOGREP/${LISTOFPARTITIONS[$i]}/grub.cfg_new"
			fi
		fi
	done
done
}

####################### STATS FOR IMPROVING THE TOOLS ##################
stats() {
local i URLST CODO WGETST
NEWUSER=no
echo "SET@_label0.set_text('''$LAB (net-check). $This_may_require_several_minutes''')"
WGETTIM=8
check_internet_connection
if [[ "$INTERNET" = connected ]];then
	echo "SET@_label0.set_text('''$LAB (net-ok). $This_may_require_several_minutes''')"
	URLST="http://sourceforge.net/projects/$APPNAME/files/statistics/$APPNAME"
	URLSTBI="http://sourceforge.net/projects/boot-info/files/statistics/boot-info"
	CODO="counter/download"
	WGETST="wget -T $WGETTIM -o /dev/null -O"
	for ((i=1;i<=TOTAL_QUANTITY_OF_OS;i++)); do
		[[ ! -d "${LOG_PATH[$i]}" ]] && [[ ! -f "${LOG_PATH[$i]}/log/$APPNAME" ]] && NEWUSER=""
		[[ ! -d "${LOG_PATH[$i]}" ]] && mkdir -p "${LOG_PATH[$i]}"
	done
	[[ "$MAIN_MENU" =~ mm ]] && [[ "$NEWUSER" ]] && $WGETST ${TMP_FOLDER_TO_BE_CLEARED}/nu $URLST.user.$CODO
	[[ "$MAIN_MENU" =~ fo ]] && [[ "$NEWUSER" ]] && $WGETST ${TMP_FOLDER_TO_BE_CLEARED}/nubi $URLSTBI.user.$CODO
	[[ "$MAIN_MENU" =~ fo ]] && $WGETST ${TMP_FOLDER_TO_BE_CLEARED}/biug $URLSTBI.usage.$CODO
	if [[ "$MAIN_MENU" = Custom-Repair ]];then
		echo "SET@_label0.set_text('''$LAB (cus). $This_may_require_several_minutes''')"
		[[ "$NEWUSER" ]] && [[ "$MAIN_MENU" = Custom-Repair ]] && $WGETST ${TMP_FOLDER_TO_BE_CLEARED}/uh $URLST.customrepairbynewuser.$CODO \
		|| $WGETST ${TMP_FOLDER_TO_BE_CLEARED}/uh $URLST.customrepair.$CODO
	fi
	stats_diff
fi
echo "SET@_label0.set_text('''$LAB. $Please_wait''')"
}

############################# BOOTFLAG #################################
bootflag_action() {
#called by first_actions & restore_mbr
local PARTTOBEFLAGGED=$1 temp PRIMARYNUM DISKTOFLAG r
temp=${LISTOFPARTITIONS[$PARTTOBEFLAGGED]}	#sdXY
PRIMARYNUM="${temp##*[a-z]}"				#Y (1~4) of sdXY
DISKTOFLAG="${DISK_PART[$PARTTOBEFLAGGED]}" #sdX
[[ ! "$(echo "$FDISKL" | grep '*' | grep "/$temp " )" ]] \
&& echo "parted /dev/$DISKTOFLAG set $PRIMARYNUM boot on" && parted /dev/$DISKTOFLAG set $PRIMARYNUM boot on
#FDISKL="$(LANGUAGE=C LC_ALL=C sudo fdisk -l)"
for r in 1 2 3 4;do #http://paste.ubuntu.com/1111263
	[[ "$(echo "$FDISKL" | grep '*' | grep "/$DISKTOFLAG$r " )" ]] && [[ "$r" != "$PRIMARYNUM" ]] \
	&& echo "parted /dev/$DISKTOFLAG set $r boot off" && parted /dev/$DISKTOFLAG set $r boot off
done #Don't work if "Can't have a partition outside the disk!" http://ubuntuforums.org/showpost.php?p=12179704&postcount=23
}

##################### REPAIR WINDOWS ################################
repair_boot_ini() {
SYSTEM1=Windows
update_translations
echo "SET@_label0.set_text('''$Repair_SYSTEM1_bootfiles. $This_may_require_several_minutes''')"
local i j part disk temp num tempnum templetter tempdisk letter tempfld
[[ "$DEBBUG" ]] && echo "[debug]repair_boot_ini (solves bug#923374)"
echo "Quantity of real Windows: $QUANTITY_OF_REAL_WINDOWS"
for ((i=1;i<=NBOFPARTITIONS;i++)); do #http://ubuntuforums.org/showthread.php?p=12210940#post12210940
	if [[ "${WINXPTOREPAIR[$i]}" ]] && [[ "$QUANTITY_OF_REAL_WINDOWS" = 1 ]];then #eg http://paste.ubuntu.com/999367
		part=${LISTOFPARTITIONS[$i]}	#sdXY
		disk="${DISK_PART[$i]}" 		#sdX
		num="${part##*[a-z]}"			#Y of sdXY
		tempnum=$num
		fdiskk="$(LANGUAGE=C LC_ALL=C fdisk -l /dev/$disk)"
		for ((j=1;j<num;j++)); do #Skip empty&extended http://ubuntuforums.org/showthread.php?t=813628
			temp="$(grep /dev/${disk}$j <<< "$fdiskk" )"
			[[ ! "$temp" ]] || [[ "$(grep -i Extended <<< "$temp" )" ]] && [[ "$fdiskk" ]] && ((tempnum -= 1 ))
		done
		templetter=$(cut -c3 <<< ${DISK_PART[$i]} )	#X of sdXY
		tempdisk=0
		for letter in a b c d e f g h i j k;do
			[[ "$templetter" = "$letter" ]] && break || ((tempdisk += 1 ))
		done
		BOOTPINI="$(ls ${BLKIDMNT_POINT[$i]}/ | grep -ix boot.ini )"
		if [[ ! "$BOOTPINI" ]];then #may be BOOT.INI or Boot.ini
			tempfld="${BLKIDMNT_POINT[$i]}/boot.ini"
			echo "[boot loader]
timeout=$UNHIDEBOOT_TIME
default=multi(0)disk(0)rdisk($tempdisk)partition($tempnum)\WINDOWS
[operating systems]
multi(0)disk(0)rdisk($tempdisk)partition($tempnum)\WINDOWS=\"Windows\" /noexecute=optin /fastdetect" > "$tempfld"
			echo "Fixed $tempfld"
		else
			BOOTPINI="${BLKIDMNT_POINT[$i]}/$BOOTPINI"
			if [[ ! "$(cat "$BOOTPINI" | grep "on($tempnum)" | grep -v default )" ]] \
			|| [[ ! "$(cat "$BOOTPINI" | grep "on($tempnum)" | grep default )" ]] \
			&& [[ "$(cat "$BOOTPINI" | grep multi | grep disk | grep rdisk | grep partition )" ]];then
				sed -i.bak "s|on([0-9])|on(${tempnum})|g" "$BOOTPINI"
				echo "Repaired $BOOTPINI"
			elif [[ -f "$BOOTPINI.bak" ]];then
				echo "Detected $BOOTPINI.bak"
			fi
		fi
		for file in ntldr NTDETECT.COM;do #http://paste.ubuntu.com/997227
			if [[ ! "$(ls ${BLKIDMNT_POINT[$i]}/ | grep -ix $file )" ]] \
			&& [[ "$QUANTITY_OF_REAL_WINDOWS" = 1 ]];then #http://paste.ubuntu.com/996163
				for ((j=1;j<=NBOFPARTITIONS;j++)); do
					if [[ "$(ls ${BLKIDMNT_POINT[$j]}/ | grep -ix $file )" ]];then
						filetocopy="$(ls ${BLKIDMNT_POINT[$j]} | grep -ix $file )"
						cp "${BLKIDMNT_POINT[$j]}/$filetocopy" "${BLKIDMNT_POINT[$i]}/$filetocopy"
						echo "Copied $filetocopy from ${LISTOFPARTITIONS[$j]} to ${LISTOFPARTITIONS[$i]}"			
						break
					fi
				done
				[[ ! "$(ls ${BLKIDMNT_POINT[$i]}/ | grep -ix $file )" ]] && repair_boot_ini_nonfree
				[[ ! "$(ls ${BLKIDMNT_POINT[$i]}/ | grep -ix $file )" ]] && ERROR=yes
			fi
		done
	fi
done
}

repair_bootmgr() {
[[ "$DEBBUG" ]] && echo "[debug]repair_bootmgr"
local i j folder
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	if [[ "${WINSETOREPAIR[$i]}" ]] && [[ "$QUANTITY_OF_REAL_WINDOWS" = 1 ]] && [[ "$QTY_SUREEFIPART" = 0 ]];then
		echo "WinSE in ${LISTOFPARTITIONS[$i]}"
		for looop in 1 2;do #First not recovery
			for loop in 1 2;do #then first same disk
				scan_windows_parts
				if [[ "${WINMGR[$i]}" = no-bmgr ]] || [[ "${WINBCD[$i]}" = no-b-bcd ]];then
					for ((j=1;j<=NBOFPARTITIONS;j++)); do
						if ( ( [[ "$looop" = 1 ]] && [[ "${RECOV[$j]}" != recovery-or-hidden ]] ) \
						|| ( [[ "$looop" = 2 ]] && [[ "${RECOV[$j]}" = recovery-or-hidden ]] ) ) \
						&& ( ( [[ "$loop" = 1 ]] && [[ "${DISKNB_PART[$i]}" = "${DISKNB_PART[$j]}" ]] ) \
						|| ( [[ "$loop" = 2 ]] && [[ "${DISKNB_PART[$i]}" != "${DISKNB_PART[$j]}" ]] ) ) \
						&& [[ "${WINMGR[$j]}" != no-bmgr ]] && [[ "${WINBCD[$j]}" != no-b-bcd ]];then
							[[ ! "${WINBOOT[$i]}" ]] && mkdir "${BLKIDMNT_POINT[$i]}/${WINBOOT[$j]}" && WINBOOT[$i]="${WINBOOT[$j]}"
							cp -r ${BLKIDMNT_POINT[$j]}/${WINBOOT[$j]}/* "${BLKIDMNT_POINT[$i]}/${WINBOOT[$i]}/"
							cp "${BLKIDMNT_POINT[$j]}/${WINMGR[$j]}" "${BLKIDMNT_POINT[$i]}/${WINMGR[$j]}"
							echo "Copied Win boot files from ${LISTOFPARTITIONS[$j]} to ${LISTOFPARTITIONS[$i]}"
							if [[ "${WINGRL[$j]}" != no-grldr ]];then
								[[ ! -f "${BLKIDMNT_POINT[$j]}/grldr" ]] && echo "Strange -f /grldr. $PLEASECONTACT"
								if [[ "${WINGRL[$i]}" = no-grldr ]];then
									if [[ ! "$(ls ${BLKIDMNT_POINT[$i]}/${WINGRL[$j]} )" ]];then
										cp "${BLKIDMNT_POINT[$j]}/${WINGRL[$j]}" "${BLKIDMNT_POINT[$i]}/"
										echo "Copied /${WINGRL[$j]} file from ${LISTOFPARTITIONS[$j]} to ${LISTOFPARTITIONS[$i]}"
									fi
								fi
							fi
						fi
					done
				fi
			done
		done
		scan_windows_parts
		if [[ "${WINL[$i]}" = no-winload ]] || [[ "${WINMGR[$i]}" = no-bmgr ]] || [[ "${WINBCD[$i]}" = no-b-bcd ]];then
			#http://askubuntu.com/questions/155492/why-cannot-ubuntu-12-04-detect-windows-7-dual-boot
			[[ "${WINBCD[$i]}" = no-b-bcd ]] && echo "${BLKIDMNT_POINT[$i]}/${WINBOOT[$i]} may need repair."
			[[ "${WINL[$i]}" = no-winload ]] &&	echo "${BLKIDMNT_POINT[$i]}/Windows/System32/winload.exe may need repair."
			[[ "${WINMGR[$i]}" = no-bmgr ]] && echo "${BLKIDMNT_POINT[$i]}/bootmgr may need repair."
		fi
	fi
done
}


####################### OPEN etc/default/grub ##########################
_button_open_etc_default_grub() {
if [[ -f "${BLKIDMNT_POINT[$REGRUB_PART]}/etc/default/grub" ]];then
	xdg-open "${BLKIDMNT_POINT[$REGRUB_PART]}/etc/default/grub" &
else
	echo "User tried to open ${BLKIDMNT_POINT[$REGRUB_PART]}/etc/default/grub but it does not exist."
	zenity --width=300 --info --title="$APPNAME2" --text="${BLKIDMNT_POINT[$REGRUB_PART]}/etc/default/grub does not exist. Please choose the [Purge and reinstall] option."
fi
}

################################ ADD KERNEL ############################
add_kernel_option() {
echo "add_kernel_option CHOSEN_KERNEL_OPTION is : $CHOSEN_KERNEL_OPTION"
local line
echo "SET@_label0.set_text('''$Add_a_kernel_option $CHOSEN_KERNEL_OPTION. $This_may_require_several_minutes''')"
if [[ -f "${BLKIDMNT_POINT[$REGRUB_PART]}/etc/default/grub" ]];then
	rm -f $TMP_FOLDER_TO_BE_CLEARED/grub_new
	while read line; do
		if [[ "$line" =~ "GRUB_CMDLINE_LINUX_DEFAULT=" ]];then
			echo "${line%\"*} ${CHOSEN_KERNEL_OPTION}\"" >> $TMP_FOLDER_TO_BE_CLEARED/grub_new
		else
			echo "$line" >> $TMP_FOLDER_TO_BE_CLEARED/grub_new
		fi
	done < <(cat "${BLKIDMNT_POINT[$REGRUB_PART]}/etc/default/grub" )
	cp -f $TMP_FOLDER_TO_BE_CLEARED/grub_new "${BLKIDMNT_POINT[$REGRUB_PART]}/etc/default/grub"
	echo "Added kernel options in ${LISTOFPARTITIONS[$REGRUB_PART]}/etc/default/grub"
fi
}

########################### FlexNet ####################################
blankextraspace() {
if [[ ! -f "$LOGREP/$GRUBSTAGEONE/before_wiping.img" ]];then #works: http://paste.ubuntu.com/1172629
	local partition a SECTORS_TO_WIPE BYTES_PER_SECTOR cmd
	rm -f $TMP_FOLDER_TO_BE_CLEARED/sort
	for partition in $(ls "/sys/block/$GRUBSTAGEONE/" | grep "$GRUBSTAGEONE");do
		echo "$(cat "/sys/block/$GRUBSTAGEONE/$partition/start" )" >> $TMP_FOLDER_TO_BE_CLEARED/sort
	done
	echo 2048 >> $TMP_FOLDER_TO_BE_CLEARED/sort # Blank max 2048 sectors (in case the first partition is far)
	#http://askubuntu.com/questions/158299/why-does-installing-grub2-give-an-iso9660-filesystem-destruction-warning
	a=$(cat "$TMP_FOLDER_TO_BE_CLEARED/sort" | sort -g -r | tail -1 )  #sort the file in the increasing order
	[[ "$(grep "^[0-9]\+$" <<< $a )" ]] && SECTORS_TO_WIPE=$(($a-1)) || SECTORS_TO_WIPE="-1"
	rm -f $TMP_FOLDER_TO_BE_CLEARED/sort
	#  a=$(LANGUAGE=C LC_ALL=C fdisk -lu /dev/$disk | grep "sectors of"); b=${a##*= }; c=${b% *}; echo "$c" > /tmp/boot-sav_sort   #Other way to calculate
	BYTES_PER_SECTOR="$(stat -c %B /dev/$GRUBSTAGEONE)"
	cmd="dd if=/dev/$GRUBSTAGEONE of=$LOGREP/$GRUBSTAGEONE/before_wiping.img bs=$BYTES_PER_SECTOR count=$SECTORS_TO_WIPE seek=1"
	echo "$cmd"
	$cmd
	if [[ ! -f "$LOGREP/$GRUBSTAGEONE/before_wiping.img" ]] \
	|| [[ ! "$(ls "/sys/block/$GRUBSTAGEONE/" | grep "$GRUBSTAGEONE")" ]];then
		echo "Could not backup, wipe cancelled."
		ERROR=yes
	else	
		echo "WIPE $GRUBSTAGEONE : $SECTORS_TO_WIPE sectors * $BYTES_PER_SECTOR bytes"
		if [[ "$SECTORS_TO_WIPE" -gt 0 ]] && [[ "$SECTORS_TO_WIPE" -le 2048 ]] && [[ "$BYTES_PER_SECTOR" -ge 512 ]] \
		&& [[ "$BYTES_PER_SECTOR" -le 1024 ]];then
			cmd="dd if=/dev/zero of=/dev/$GRUBSTAGEONE bs=$BYTES_PER_SECTOR count=$SECTORS_TO_WIPE seek=1"
			#seek=1, so MBR (icl. partition table) is not wiped
			echo "$cmd"
			$cmd
		else
			MSSG="By security, $GRUBSTAGEONE sectors were not wiped. \
			(one of these values is incorrect: SECTORS_TO_WIPE=$SECTORS_TO_WIPE , BYTES_PER_SECTOR=$BYTES_PER_SECTOR )"
			echo "$MSSG"
			end_pulse
			zenity --width=300 --warning --title="$APPNAME2" --text="$MSSG"
			start_pulse
			ERROR=yes
		fi
	fi
fi
}

######################### UNCOMMENT GFXMODE ############################
uncomment_gfxmode() {
local line
echo "SET@_label0.set_text('''$Uncomment_GRUB_GFXMODE. $This_may_require_several_minutes''')"
sed -i 's/#GRUB_GFXMODE/GRUB_GFXMODE/' "${BLKIDMNT_POINT[$REGRUB_PART]}/etc/default/grub" \
&& sed -i 's/# GRUB_GFXMODE/GRUB_GFXMODE/' "${BLKIDMNT_POINT[$REGRUB_PART]}/etc/default/grub" \
&& echo "Uncommented GRUB_GFXMODE in ${LISTOFPARTITIONS[$REGRUB_PART]}/etc/default/grub"
}

########################## Final sequence ##############################

display_action_settings_start() {
if [[ "$MAIN_MENU" != Recommended-Repair ]];then
	[[ "$MAIN_MENU" =~ fo ]] && THISSET="Suggested repair" || THISSET="Default settings of $CLEANNAME"
	echo "

$DASH $THISSET
$IMPVARUN"
	[[ "$BTEXTUN" ]] || [[ "$ATEXTUN" ]] && echo "

$DASH Blockers in case of suggested repair
$BTEXTUN $ATEXTUN"
	[[ "$TEXTUN" ]] && echo "

$DASH Advice in case of suggested repair
$TEXTUN"
	[[ "$TEXTENDUN" ]] && echo "

$DASH Final advice in case of suggested repair
$TEXTENDUN"
	echo "

$DASH User settings"
fi
WIOULD=will
debug_echo_important_variables
}

display_action_settings_end() {
echo "$IMPVAR

"
TEECOUNTER=0
}

first_actions() {
#action before removal (if os-un)
[[ "$MBR_ACTION" != reinstall ]] || [[ ! "$GRUBPACKAGE" =~ efi ]] \
&& [[ "$BOOTFLAG_ACTION" ]] && [[ "$BOOTFLAG_TO_USE" ]] && bootflag_action $BOOTFLAG_TO_USE
[[ "$MBR_ACTION" = reinstall ]] && fix_fstab
[[ "$RESTORE_BKP_ACTION" ]] || [[ "$CREATE_BKP_ACTION" ]] && restore_efi_bkp_files
if [[ "$WINBOOT_ACTION" ]];then
	repair_boot_ini
	repair_bootmgr
fi
}

actions_final() {
#action after removal (if os-un)
[[ "$MBR_ACTION" = reinstall ]] && reinstall_grub_from_non_removable
if [[ "$GRUBPURGE_ACTION" ]] && [[ "$MBR_ACTION" = reinstall ]];then
	grub_purge
else
	[[ "$UNHIDEBOOT_ACTION" ]] && unhide_boot_menus_etc_default_grub #Requires all OS partitions to be mounted
	if [[ "$MBR_ACTION" = reinstall ]];then
		reinstall_grub_from_chosen_linux
	elif [[ "$MBR_ACTION" = restore ]];then
		restore_mbr
	fi
	unmount_all_and_success
fi
}

unhideboot_and_textprepare() {
BSERROR=""
if [[ "$UNHIDEBOOT_ACTION" ]];then
	unhide_boot_menus_xp
	unhide_boot_menus_grubcfg	#To replace the "-1"
fi
TEXTBEG=""
TEXTEND=""
if [[ "$MBR_ACTION" != nombraction ]] || [[ "$UNHIDEBOOT_ACTION" ]] || [[ "$FSCK_ACTION" ]] \
|| [[ "$BOOTFLAG_ACTION" ]] || [[ "$WINBOOT_ACTION" ]];then
	if [[ "$ERROR" ]];then
		TEXTBEG="$An_error_occurred_during

"
	else
		TEXTBEG="$Successfully_processed

"
	fi
	if [[ "$LOCKEDESP" ]];then
		FUNCTION=Locked-ESP; TYP=/boot/efi; TOOL1=gParted; TYPE3=/boot/efi; update_translations
		FLAGTYP=boot; OPTION2="$Separate_TYPE3_partition"; update_translations
		TEXTEND="$FUNCTION_detected $You_may_want_to_retry_after_creating_TYP_part (FAT32, 100MB~250MB, $start_of_the_disk, $FLAGTYP_flag). $Via_TOOL1 \
$Then_select_this_part_via_OPTION2_of_TOOL3"
	else
		TEXTEND="$You_can_now_reboot
"
		textprepare
	fi
#elif [[ ! "$MAIN_MENU" =~ nf ]];then
#	TEXTEND="$No_change_on_your_pc"
fi
echo "
$TEXTBEG$TEXTMID$TEXTEND"
}

textprepare() {
#called by _button_justbootinfo & unhideboot_and_textprepare
if [[ "$MBR_ACTION" = reinstall ]];then
	if [[ "$FORCE_GRUB" = force-in-PBR ]] || [[ "$ADVISE_BOOTLOADER_UPDATE" = yes ]];then
		TEXTEND="$TEXTEND$Please_update_main_bootloader"
	elif [[ "$GRUBPACKAGE" =~ efi ]];then #[[ ! -d /sys/firmware/efi ]] || [[ ! "$CREATE_BKP_ACTION" ]] && [[ "$EFIGRUBFILE" ]]
			FILE1="${LISTOFPARTITIONS[$EFIPART_TO_USE]}${EFIGRUBFILE#*/boot/efi}"
			BIOS1=BIOS; update_translations
			TEXTEND="$TEXTEND$Please_setup_BIOS1_on_FILE1"
	elif [[ "$NBOFDISKS" != 1 ]];then
		if [[ "$REMOVABLEDISK" ]];then
			TEXTEND="$TEXTEND$Please_setup_bios_on_removable_disk"
		else
			a="$(echo "$PARTEDLM" | grep "/dev/$NOFORCE_DISK:" )"; a="${a%:*}"; a="${a##*:}"
			[[ "$a" ]] && DISK1="$NOFORCE_DISK ($a)" || DISK1="$NOFORCE_DISK"
			update_translations
			TEXTEND="$TEXTEND$Please_setup_bios_on_DISK1"
		fi
	fi
	if [[ "$SECUREBOOT" = enabled ]] && [[ "$QUANTITY_OF_REAL_WINDOWS" != 0 ]] && [[ ! "$GRUBPACKAGE" =~ sign ]];then
		OPTION5=SecureBoot; update_translations
		TEXTEND="$TEXTEND $Please_disable_OPTION5_in_BIOS"
	fi
	if [[ "$QUANTITY_OF_DETECTED_MACOS" != 0 ]] || [[ "$MACEFIFILEPRESENCE" ]];then
		TEXTEND="$TEXTEND

$You_may_also_want_to_install_PROGRAM6 (https://help.ubuntu.com/community/ubuntupreciseon2011imac)"
	fi
	if [[ "${FARBIOS[$BOOTPART]}" = farbios ]] && [[ "$FORCE_GRUB" != force-in-PBR ]] \
	&& [[ ! "$GRUBPACKAGE" =~ efi ]] && [[ "${GPT_DISK[${DISKNB_PART[$REGRUB_PART]}]}" != GPT ]];then  # && [[ "$LIVESESSION" != live ]] 
		SYSTEM2="${OSNAME[$REGRUB_PART]}"; TYP=/boot; TOOL1=gParted; TYPE3=/boot; update_translations
		OPTION2="$Separate_TYPE3_partition"; update_translations
		TEXTEND="$TEXTEND

$Boot_files_of_SYSTEM2_are_far \
$You_may_want_to_retry_after_creating_TYP_part (EXT4, >200MB, $start_of_the_disk). $Via_TOOL1 \
$Then_select_this_part_via_OPTION2_of_TOOL3 ($BootPartitionDoc)"
	fi
	if [[ "${FARBIOS[$EFIPART_TO_USE]}" = farbios ]] && [[ "$GRUBPACKAGE" =~ grub-efi ]] \
	&& [[ "$LIVESESSION" != live ]] && [[ "$FORCE_GRUB" != force-in-PBR ]];then
		SYSTEM2="${OSNAME[$REGRUB_PART]}"; TYP=/boot/efi; TOOL1=gParted; TYPE3=/boot/efi; update_translations
		FLAGTYP=boot; OPTION2="$Separate_TYPE3_partition"; update_translations
		TEXTEND="$TEXTEND

$Boot_files_of_SYSTEM2_are_far \
$You_may_want_to_retry_after_creating_TYP_part (FAT32, 100MB~250MB, $start_of_the_disk, $FLAGTYP_flag). $Via_TOOL1 \
$Then_select_this_part_via_OPTION2_of_TOOL3"
	fi
	if [[ "$WINEFIFILEPRESENCE" ]] && [[ "$GRUBPACKAGE" =~ efi ]];then
		OPTION="$Msefi_too"
		BIOS1=BIOS
		update_translations
		if [[ "$WINEFI_BKP_ACTION" ]];then
			TEXTEND="$TEXTEND

$You_may_want_to_retry_after_deactivating_OPTION"
		else
			temp=""
			if [[ "$EFIGRUBFILE" ]];then
				temp="${EFIGRUBFILE#*/boot/efi}"
				temp="${temp#*EFI/}"
				temp="${temp#*efi/}"
				temp="$Via_command_in_win
bcdedit /set {bootmgr} path \\\\EFI\\\\${temp////\\\\}"
			fi
			TEXTEND="$TEXTEND

$If_boot_win_try_change_BIOS1_order
$If_BIOS1_blocked_change_win_order
$temp"
#$You_may_want_to_retry_after_activating_OPTION"		
		fi
	fi
	if [[ ! -d /sys/firmware/efi ]] && [[ "$GRUBPACKAGE" =~ efi ]];then
		MODE1=Legacy; Mode2=UEFI; update_translations
		TEXTEND="$TEXTEND

$Boot_is_MODE1_may_need_change_to_MODE2"
	fi
fi
if [[ "$ROOTDISKMISSING" ]];then
	TEXTEND="$TEXTEND

$Broken_wubi_detected
$Missingrootdiskurl"
fi
}


stats_savelogs_unmount_endpulse() {
[[ "$SENDSTATS" != nostats ]] && stats
save_log_on_disks
unmount_all_blkid_partitions_except_df
end_pulse
}

finalzenity_and_exitapp() {
zenity --width=300 --info --title="$APPNAME2" --text="$TEXTBEG$TEXTMID$TEXTEND"
rm -r $TMP_FOLDER_TO_BE_CLEARED
echo "End of unmount_all_and_success (SHOULD NOT SEE THIS ON LOGS ON DISKS)"
echo 'EXIT@@'
}


########################## PASTEBIN ACTION ##########################################
pastebinaction() {
local temp line PACKAGELIST="" FUNCTION=BootInfo FILETOTEST
LAB="$Create_a_BootInfo_report"
echo "SET@_label0.set_text('''$LAB. $This_may_require_several_minutes''')"
for temp in pastebinit gawk;do
	[[ "$UPLOAD" ]] || [[ "$temp" = gawk ]] && [[ ! "$(type -p $temp)" ]] && PACKAGELIST="$temp $PACKAGELIST"
done
FILETOTEST="pastebinit gawk"
if [[ ! "$(type -p xz)" ]] && [[ ! "$(type -p lzma)" ]];then
	PACKAGELIST="$temp xz-utils"
	FILETOTEST="$FILETOTEST xz"
fi
[[ "$PACKAGELIST" ]] && installpackagelist
cp "$TMP_LOG" "${TMP_LOG}t"
sed -i "/^SET@/ d" "${TMP_LOG}t"
sed -i "/^DEBUG=>/ d" "${TMP_LOG}t"
sed -i "/^\[debug\]/ d" "${TMP_LOG}t"
sed -i "/^COMBO@@/ d" "${TMP_LOG}t"
sed -i "/^done/ d" "${TMP_LOG}t"
sed -i "/^1+0/ d" "${TMP_LOG}t"
sed -i "/^gpg:/ d" "${TMP_LOG}t"
sed -i "/^sh: 0: getc/ d" "${TMP_LOG}t"
sed -i "/^Executing: gpg/ d" "${TMP_LOG}t"
sed -i "/^Reading/ d" "${TMP_LOG}t"
sed -i "/^Building dependency/ d" "${TMP_LOG}t"
sed -i "/^Need to get/ d" "${TMP_LOG}t"
sed -i "/^After this operation/ d" "${TMP_LOG}t"
sed -i "/^Get:/ d" "${TMP_LOG}t"
sed -i "/^Download complete/ d" "${TMP_LOG}t"
sed -i "/^sh: getcwd/ d" "${TMP_LOG}t"
sed -i "/^E: Package 'pastebinit' has no installation candidate/ d" "${TMP_LOG}t"
while read line; do
	[[ ! "$line" ]] || [[ "$(echo "$line" | grep -v B/s | grep -v 'while true' | grep -v 'sleep 0' )" ]] \
	&& echo "$line" >> "${TMP_LOG}b"
done < <(cat ${TMP_LOG}t )
rm "${TMP_LOG}t"
unmount_all_blkid_partitions_except_df # necessary ?
echo "SET@_label0.set_text('''$LAB (bis). $This_may_require_several_minutes''')"
BISR="$TMP_FOLDER_TO_BE_CLEARED/RESULTS.txt"
#thanks to Meierfra & Gert Hulselmans
#start_kill_nautilus
LANGUAGE=C LC_ALL=C bash /usr/share/boot-sav/b-i-s.sh $BISR
#end_kill_nautilus
check_if_grub_in_bootsector
echo "ADDITIONAL INFORMATION :" >> "$BISR"
cat "${TMP_LOG}b" >> "$BISR"
rm "${TMP_LOG}b"
cp "$BISR" "$LOGREP/"
repup=yes
if [[ "$UPLOAD" ]] && [[ "$APPNAME" =~ re ]];then
	text="$Upload_report ?"
	end_pulse
	zenity --width=300 --question --title="$(eval_gettext "Boot-Info")" --text="$text" || repup=no
	echo "$text $repup"
	start_pulse
fi
if [[ "$UPLOAD" ]] && [[ "$repup" = yes ]];then
	echo "SET@_label0.set_text('''$LAB (net-check). $This_may_require_several_minutes''')"
	check_internet_connection
	ask_internet_connection
	echo "SET@_label0.set_text('''$LAB (url). $This_may_require_several_minutes''')"
	if [[ "$(type -p pastebinit)" ]] && [[ "$(type -p gawk)" ]];then #[[ "$INTERNET" = connected ]] && 
		if [[ "$(lsb_release -is)" = Debian ]] && [[ ! "$(lsb_release -ds)" =~ Boot-Repair-Disk ]];then
			PASTEB="paste.debian.net"
		elif [[ "$(lsb_release -is)" = Ubuntu ]];then
			PASTEB="paste.ubuntu.com"
		else
			PASTEB="paste2.org"
		fi
		PASTEBIN_URL=$(cat "$BISR" | pastebinit -a boot-repair -f bash -b $PASTEB)
		pastebin_retry
		pastebin_retry
	fi
fi
#start_kill_nautilus
mount_all_blkid_partitions_except_df #For logs
#sleep 2;end_kill_nautilus
}

pastebin_retry() {
if [[ "$PASTEBIN_URL" = "http://$PASTEB/" ]] || [[ ! "$PASTEBIN_URL" ]] || [[ "$PASTEBIN_URL" =~ new-paste ]];then
	[[ "$PASTEBIN_URL" =~ host ]] && echo "No internet for $PASTEB ($PASTEBIN_URL)." >> "$BISR"
	if [[ "$PASTEB" =~ ubuntu ]];then
		echo "$PASTEB ko ($PASTEBIN_URL)" >> "$BISR"
		PASTEB="paste.debian.net"
	elif [[ "$PASTEB" =~ debian ]];then
		echo "$PASTEB ko ($PASTEBIN_URL)" >> "$BISR"
		PASTEB="paste2.org"
	else
		echo "$PASTEB ko ($PASTEBIN_URL)" >> "$BISR"
		PASTEB="paste.ubuntu.com"
	fi
	PASTEBIN_URL=$(cat "$BISR" | pastebinit -a boot-repair -f bash -b $PASTEB)
fi
}

check_if_grub_in_bootsector() {
local GRUBINBS="" PARTBS="" line
if [[ -f "$BISR" ]];then
	echo "SET@_label0.set_text('''$LAB (bs-check). $This_may_require_several_minutes''')"
	while read line;do
		[[ "$(grep ': __' <<< "$line")" ]] && GRUBINBS="" && PARTBS="${line%:*}"
		[[ "$PARTBS" ]] && [[ "$(echo "$line" | grep "is installed in the boot sector" | grep -i grub )" ]] && GRUBINBS=ok
		[[ "$PARTBS" ]] && [[ "$GRUBINBS" ]] && [[ "$(echo "$line" | grep "Operating System" | grep -i windows )" ]] && ERROR=yes && BSERROR="$PARTBS"
		[[ "$(grep '== Drive/Partition Info: ==' <<< "$line")" ]] && break
	done < <(cat "$BISR")
else
	echo "Error: BIS produced no RESULT.txt . $PLEASECONTACT"
fi
}

unmount_all_and_success_br_and_bi() {
TEXTMID=""
unhideboot_and_textprepare
[[ "$PASTEBIN_ACTION" ]] && pastebinaction
stats_savelogs_unmount_endpulse
if [[ "$PASTEBIN_ACTION" ]];then
	[[ "$ERROR" ]] && or_to_your_favorite_support_forum=""
	if [[ "$PASTEBIN_URL" ]] && [[ "$PASTEBIN_URL" != "http://paste.debian.net/" ]] \
	&& [[ "$PASTEBIN_URL" != "http://paste.ubuntu.com/" ]] && [[ ! "$PASTEBIN_URL" =~ host ]];then
		TEXTMID="$Please_write_url_on_paper
$PASTEBIN_URL

"
		[[ ! "$MAIN_MENU" =~ nf ]] && TEXTMID="$TEXTMID
$Indicate_it_in_case_still_pb
boot.repair@gmail.com $or_to_your_favorite_support_forum

" || TEXTMID="$TEXTMID
$Indicate_url_if_pb $On_forums_eg

"
	elif [[ -f "$LOGREP/RESULTS.txt" ]];then
		FILENAME="$LOGREP/Boot-Info_$DATE.txt" #can't include the ~/
		mv "$LOGREP/RESULTS.txt" "$FILENAME"
		if [[ "$(type -p leafpad)" ]];then	#to avoid opening in term
			leafpad "$FILENAME" &
		else
			xdg-open "$FILENAME" &
		fi
		sleep 1.5
		update_translations
		TEXTMID="$FILENAME_has_been_created

"
		[[ ! "$MAIN_MENU" =~ nf ]] && TEXTMID="$TEXTMID
$Indicate_its_content_in_case_still_pb
boot.repair@gmail.com $or_to_your_favorite_support_forum

" || TEXTMID="$TEXTMID
$Indicate_content_if_pb $On_forums_eg

"
	else
		TEXTMID="(Could not create BootInfo. $PLEASECONTACT )"
	fi
	if [[ "$BSERROR" ]];then
		PARTBS="$BSERROR"; TOOL1=TestDisk; update_translations
		TEXTMID="$TEXTMID
$Please_fix_bs_of_PARTBS $Via_TOOL1
(https://help.ubuntu.com/community/BootSectorFix)


"
	fi
elif [[ "$ERROR" ]];then
	TEXTMID="$PLEASECONTACT
"
fi
finalzenity_and_exitapp
}


############WHEN CLICKING BOOTINFO BUTTON
justbootinfo_br_and_bi() {
echo 'SET@_mainwindow.hide()'
start_pulse
debug_echo_important_var_first
MAIN_MENU=Boot-Info
MBR_ACTION=nombraction ; UNHIDEBOOT_ACTION="" ; FSCK_ACTION="" ; WUBI_ACTION=""
GRUBPURGE_ACTION="" ; BLANKEXTRA_ACTION="" ; UNCOMMENT_GFXMODE="" ; KERNEL_PURGE=""
BOOTFLAG_ACTION="" ; WINBOOT_ACTION="" ; PASTEBIN_ACTION=create-bootinfo
RESTORE_BKP_ACTION=""; CREATE_BKP_ACTION=""; WINEFI_BKP_ACTION=""
[[ "$DEBBUG" ]] && echo "[debug]MAIN_MENU becomes : $MAIN_MENU"
LAB="$Create_a_BootInfo_report"
echo "SET@_label0.set_text('''$LAB. $This_may_require_several_minutes''')"
actions
}

debug_echo_important_var_first() {
if [[ ! "$IMPVARUN" ]];then
	debug_echo_important_variables
	IMPVARUN="$IMPVAR"
	blockers_check
	EFIGRUBFILE="/efi/.../grub*.efi"
	textprepare
	BTEXTUN="$BTEXT"
	ATEXTUN="$ATEXT"
	TEXTUN="$TEXT"
	TEXTENDUN="$TEXTEND"
fi
}
