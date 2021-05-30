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


###################### ADD OR REMOVE /BOOT /USR /BOOT/EFI IN FSTAB #################################
fix_fstab() {
local bootusr CHANGEDONE TMPPART_TO_USE FSTABFIXTYPE line CORRECTLINE NEWFSTAB ADDIT temp regrubfstab="${BLKIDMNT_POINT[$REGRUB_PART]}/etc/fstab"
if [[ ! -f "$regrubfstab" ]];then
	echo "Error: no $regrubfstab"
else
	for bootusr in /boot /usr /boot/efi;do
		[[ "$bootusr" = /boot ]] &&	TMPPART_TO_USE="$BOOTPART_TO_USE" && FLINE1="0	2" && FLINE2="1	2" #1204, Fedora13 
		[[ "$bootusr" = /usr ]] && TMPPART_TO_USE="$USRPART_TO_USE" && FLINE1="0	2" && FLINE2="1	2" #1204, ?
		[[ "$bootusr" = /boot/efi ]] && TMPPART_TO_USE="$EFIPART_TO_USE" && FLINE1="0	1" && FLINE2="1	1" #1204, ?
		( [[ "$bootusr" = /boot ]] && [[ "$USE_SEPARATEBOOTPART" ]] ) \
		|| ( [[ "$bootusr" = /usr ]] && [[ "$USE_SEPARATEUSRPART" ]] ) \
		|| ( [[ "$bootusr" = /boot/efi ]] && [[ "$GRUBPACKAGE" =~ efi ]] ) \
		&& FSTABFIXTYPE=added || FSTABFIXTYPE=removed
		if [[ "$LIVESESSION" != live ]] && [[ "$bootusr" != /boot/efi ]];then
			[[ "$DEBBUG" ]] && echo "[debug] $bootusr not $FSTABFIXTYPE in installed session"
		elif [[ ! "${PART_UUID[$TMPPART_TO_USE]}" ]] && [[ "$FSTABFIXTYPE" = added ]];then
			echo "Error: no UUID to add $bootusr $TMPPART_TO_USE (${LISTOFPARTITIONS[$TMPPART_TO_USE]}, ${LISTOFPARTITIONS[$REGRUB_PART]})"
		else
			OLDFSTAB="$LOGREP/${LISTOFPARTITIONS[$REGRUB_PART]}/etc_fstab_old"
			[[ ! -f "$OLDFSTAB" ]] && cp "$regrubfstab" "$OLDFSTAB"
			NEWFSTAB="$LOGREP/${LISTOFPARTITIONS[$REGRUB_PART]}/etc_fstab_new"
			rm -f "$NEWFSTAB"
			if [[ "$FSTABFIXTYPE" = added ]];then
				temp="$(echo "$BLKID" | grep "${LISTOFPARTITIONS[$TMPPART_TO_USE]}:")"; temp=${temp#* TYPE=\"}; temp=${temp%%\"*}
				CORRECTLINE="UUID=${PART_UUID[$TMPPART_TO_USE]}	$bootusr	$temp"
				ADDIT=yes
			fi
			CHANGEDONE=""
			while read line; do
				CONTROL=ok
				if [[ "$FSTABFIXTYPE" = added ]];then
					for cta in $CORRECTLINE;do [[ ! "$line" =~ "$cta" ]] && CONTROL="";done
					[[ ! "$line" =~ "$FLINE1" ]] && [[ ! "$line" =~ "$FLINE2" ]] && CONTROL=""
					[[ ! "$line" =~ defaults ]] && [[ ! "$line" =~ relatime ]] && CONTROL="" #http://paste.ubuntu.com/1318133
				fi
				if [[ "$CONTROL" ]] && [[ ! "$line" =~ '#' ]] && [[ "$ADDIT" ]] && [[ "$FSTABFIXTYPE" = added ]];then
					echo "$line" >> "$NEWFSTAB"
					ADDIT="" #Keep only 1 correct line
				elif [[ "$line" =~ "$bootusr" ]] && [[ ! "$line" =~ "$bootusr/" ]] && [[ ! "$line" =~ "#" ]];then
					echo "#$line" >> "$NEWFSTAB"
					CHANGEDONE=yes
				else
					echo "$line" >> "$NEWFSTAB"
				fi
			done < <(cat "$regrubfstab" )
			[[ "$ADDIT" ]] && [[ "$FSTABFIXTYPE" = added ]] && CHANGEDONE=yes \
			&& echo "$CORRECTLINE	defaults	$FLINE1" >> "$NEWFSTAB"
			if [[ ! "$CHANGEDONE" ]];then
				[[ "$DEBBUG" ]] && echo "[debug]$regrubfstab unchanged for $bootusr"
			elif [[ -f "$NEWFSTAB" ]];then
				cp "$NEWFSTAB" "$regrubfstab"
				echo "$bootusr $FSTABFIXTYPE in ${LISTOFPARTITIONS[$REGRUB_PART]}/fstab"
			else
				echo "Error: no $NEWFSTAB"
			fi
		fi
	done
fi
}

fix_grub_d() {
#Fix incorrect file rights http://forum.ubuntu-fr.org/viewtopic.php?pid=9665071
local fichero direct="${BLKIDMNT_POINT[$REGRUB_PART]}/etc/grub.d/"
if [[ -d "$direct" ]];then
	for fichero in $(ls "$direct");do
		if [[ "$(grep '_' <<< $fichero )" ]] && [[ "$(ls -l "$direct" | grep "$fichero" | grep -v rwxr-xr-x )" ]];then
			chmod a+x "$direct$fichero"
			echo "Fixed file rights of $direct$fichero $PLEASECONTACT"
		fi
	done
	[[ "$DEBBUG" ]] && echo "[debug]End fix $direct" #http://paste.ubuntu.com/1095010
else
	echo "No $direct folder. $PLEASECONTACT"
fi
}


########################### REINSTALL GRUB ##############################
reinstall_grub_from_chosen_linux() {
#called by purge_end & actions_final
[[ "$UNCOMMENT_GFXMODE" ]] && uncomment_gfxmode
[[ "$ADD_KERNEL_OPTION" ]] && add_kernel_option
fix_grub_d
[[ "$FORCE_GRUB" = place-in-all-MBRs ]] && [[ ! "$GRUBPACKAGE" =~ efi ]] \
&& [[ ! "$REMOVABLEDISK" ]] && loop_install_grub_in_all_other_disks
#Reinstall in main MBR at the end to avoid core.img missing (http://paste.ubuntu.com/988941)
NOW_IN_OTHER_DISKS=""
NOFORCE_DISK="$BCKUPNOFORCE_DISK"
reinstall_grub
[[ "${UPDATEGRUB_OF_PART[$USRPART]}" != no-update-grub ]] && grub_mkconfig_main
if [[ "$KERNEL_PURGE" ]] || [[ "$GRUBPURGE_ACTION" ]];then
	restore_resolvconf_and_unchroot
else
	unchroot_linux_to_reinstall
fi
mount_all_blkid_partitions_except_df
#[[ "$DEBBUG" ]] && echo "[debug]Mount all the partitions for the logs"
}



reinstall_grub_from_non_removable() {
NOW_USING_CHOSEN_GRUB=""
NOW_IN_OTHER_DISKS=yes
BCKUPREGRUB_PART="$REGRUB_PART"
BCKUPNOFORCE_DISK="$NOFORCE_DISK"
BCKUPUSRPART="$USRPART"
if [[ ! "$GRUBPACKAGE" =~ efi ]] && [[ "$FORCE_GRUB" = place-in-all-MBRs ]] && [[ "$REMOVABLEDISK" ]];then
	local x n icrmf GRUBOS_ON_OTHERDISK=""
	echo "$NOFORCE_DISK is removable, so we reinstall GRUB of the removable media only in its disk MBR"
	REGRUB_PART=none
	for y in 1 2;do # Try to reinstall, then purge
		for ((x=1;x<=NBOFPARTITIONS;x++));do
			if ( [[ "$y" = 1 ]] && [[ "${GRUBOK_OF_PART[$x]}" ]] && [[ ! "$OSBKP" ]] ) \
			|| ( [[ "$y" = 2 ]] && [[ ! "${GRUBOK_OF_PART[$x]}" ]] && [[ "${APTTYP[$x]}" != nopakmgr ]]) \
			&& ( [[ "${ARCH_OF_PART[$x]}" = 32 ]] || [[ "$(uname -m)" = x86_64 ]] ) \
			&& [[ "$REGRUB_PART" = none ]] \
			&& [[ "${DISK_PART[$BCKUPREGRUB_PART]}" != "${DISK_PART[$x]}" ]];then
				GRUBOS_ON_OTHERDISK=yes
				if [[ "$LIVESESSION" = live ]] && [[ ! "$USE_SEPARATEBOOTPART" ]] && [[ ! "$USE_SEPARATEUSRPART" ]];then
					REGRUB_PART="$x"
					if [[ "${GRUBOK_OF_PART[$x]}" ]];then
						USRPART="$x"
						loop_install_grub_in_all_other_disks
						if [[ "$INSTALLEDINOTHERDISKS" ]];then
							[[ "${UPDATEGRUB_OF_PART[$USRPART]}" != no-update-grub ]] && grub_mkconfig_main
							unchroot_linux_to_reinstall
							mount /dev/"${LISTOFPARTITIONS[$BCKUPREGRUB_PART]}" "${BLKIDMNT_POINT[$BCKUPREGRUB_PART]}"
						fi
					else
						#PURGE_IN_OTHER_DISKS=yes
						# grub_purge
						echo "Warning: you may need to run this tool again after disconnecting the removable disk. $PLEASECONTACT"
					fi
					break
					break
				fi
			fi
		done
	done
	if [[ ! "$GRUBOS_ON_OTHERDISK" ]];then #No GRUB on other disks, so will restore MBRs
		for ((n=1;n<=NBOFDISKS;n++));do
			if [[ "${USBDISK[$n]}" != liveusb ]] && [[ "${MMCDISK[$n]}" != livemmc ]] && [[ "${DISK_WITHOS[$n]}" = has-os ]] \
			&& [[ "${GPT_DISK[$n]}" != GPT ]] && [[ "${EFI_DISK[$n]}" = has-no-EFIpart ]] && [[ "$n" != "${DISKNB_PART[$BCKUPREGRUB_PART]}" ]];then
				for ((icrmf=1;icrmf<=NB_MBR_CAN_BE_RESTORED;icrmf++));do
					MBR_TO_RESTORE="${MBR_CAN_BE_RESTORED[$icrmf]}"
					if [[ "$MBR_TO_RESTORE" =~ "${LISTOFDISKS[$n]} " ]];then
						combobox_restore_mbrof_consequences
						restore_mbr
						break
					fi
				done
			fi
		done
	elif [[ ! "$LIVESESSION" = live ]] || [[ "$USE_SEPARATEBOOTPART" ]] || [[ "$USE_SEPARATEUSRPART" ]];then
		echo "OS with GRUB found on another disk. To fix other MBRs, please use Advanced Options of Boot-Repair from live-session."
	fi
fi
REGRUB_PART="$BCKUPREGRUB_PART";USRPART="$BCKUPUSRPART"; [[ "$PLEASECONTACT" =~ '.' ]] && NOW_USING_CHOSEN_GRUB=yes
force_unmount_and_prepare_chroot
[[ "$KERNEL_PURGE" ]] && kernel_purge
}



reinstall_grub() {
FORCEPARAM=""
RECHECK=""
LSPCIV="$(${CHROOTCMD}lspci -nnk | grep -iA3 vga)"
echo "
*******lspci -nnk | grep -iA3 vga
$LSPCIV
*******
"
echo "${GRUBTYPE_OF_PART[$USRPART]} --version"
GVERSION="$($CHROOTCMD${GRUBTYPE_OF_PART[$USRPART]} --version)" #-v in old, -V in new distros
# grub-install (GNU GRUB 0.97), "grub-install (GRUB) 1.99-21ubuntu3.1", or "grub-install (GRUB) 2.00-5ubuntu3", "grub-install (GRUB) 2.02~beta2-9ubuntu1"
GSVERSION="${GVERSION%%.*}"  #grub-install (GRUB) 1 or "grub-install (GNU GRUB 0"
echo "$GVERSION,$GSVERSION."
if ( [[ "$GSVERSION" =~ 0 ]] && [[ ! "$GRUBPACKAGE" = grub ]] ) \
|| ( [[ ! "$GSVERSION" =~ 0 ]] && [[ "$GRUBPACKAGE" = grub ]] );then
	ERROR=yes
	echo "Wrong GRUB version detected. $PLEASECONTACT"
	[[ "$GSVERSION" =~ 0 ]] && GRUBPACKAGE=grub
	[[ ! "$GSVERSION" =~ 0 ]] && GRUBPACKAGE=grub-pc
fi
[[ "$GSVERSION" =~ 0 ]] && ATA=""
if [[ "$GRUBPACKAGE" =~ efi ]];then
	[[ "$GSVERSION" =~ 0 ]] || [[ "$GSVERSION" =~ 1 ]] && [[ ! "$GVERSION" =~ "1.99-21ubuntu3.10" ]] && [[ ! "$GVERSION" =~ "1.99-21ubuntu3.14" ]] && [[ "$GRUBPACKAGE" =~ signed ]] \
	&& echo "GRUB too old for SecureBoot. $PLEASECONTACT" && GRUBPACKAGE=grub-efi
	echo "
${CHROOTCMD}efibootmgr -v"
	LANGUAGE=C LC_ALL=C ${CHROOTCMD}efibootmgr -v
	echo "
${CHROOTCMD}uname -r"
	#LANGUAGE=C LC_ALL=C ${CHROOTCMD}uname -r
	RARINGK="$(LANGUAGE=C LC_ALL=C ${CHROOTCMD}uname -r)"
	BUGGYK=""
	echo "Kernel: $RARINGK"
	[[ "$RARINGK" =~ 3.8.0-[1-9][0-9] ]] || [[ "$RARINGK" =~ 3.8.[1-9] ]] || [[ "$RARINGK" =~ 3.9.[0-9] ]] && BUGGYK=is-buggy
	[[ "$BUGGYK" ]] && FUNCTION=buggy-kernel || FUNCTION=WinEFI
#	if [[ ! "$WINEFI_BKP_ACTION" ]];then
#		OPTION="$Msefi_too"
#		repbg=yes
#		update_translations
#		end_pulse
#		zenity --width=300 --question --title="$APPNAME2" --text="$FUNCTION_detected $Do_you_want_activate_OPTION $If_any_fail_try_other" || repbg=no
#		echo "$FUNCTION_detected $Do_you_want_activate_OPTION $repbg $If_any_fail_try_other"
#		start_pulse
#		[[ "$repbg" = yes ]] && WINEFI_BKP_ACTION=rename-ms-efi && CREATE_BKP_ACTION=backup-and-rename-efi-files #fixes 1173423
#	fi
	echo "
Reinstall the $GRUBPACKAGE of ${LISTOFPARTITIONS[$REGRUB_PART]}"
	GRUBSTAGEONE=""
	DEVGRUBSTAGEONE=""
	[[ "$GSVERSION" =~ 2 ]] && [[ "${ARCH_OF_PART[$USRPART]}" == 32 ]] && FORCEPARAM=" --efi-directory=/boot/efi --target=i386-efi"
	if [[ "${ARCH_OF_PART[$USRPART]}" == 64 ]];then
		[[ "$GSVERSION" =~ 2 ]] && FORCEPARAM=" --efi-directory=/boot/efi --target=x86_64-efi"
		[[ "$GRUBPACKAGE" =~ signed ]] && FORCEPARAM="$FORCEPARAM --uefi-secure-boot" || FORCEPARAM="$FORCEPARAM --no-uefi-secure-boot"
	fi
	[[ "$GVERSION" =~ "1.99-21ubuntu3.10" ]] && FORCEPARAM="$FORCEPARAM /dev/$NOFORCE_DISK"
	ATA=""
	reinstall_grubstageone
	echo "
${CHROOTCMD}efibootmgr -v"
	LANGUAGE=C LC_ALL=C ${CHROOTCMD}efibootmgr -v
elif [[ "$FORCE_GRUB" = force-in-PBR ]];then #http://paste.ubuntu.com/1063825
	GRUBSTAGEONE="$FORCE_PARTITION"
	DEVGRUBSTAGEONE="/dev/$GRUBSTAGEONE"
	FORCEPARAM=" --force"
	echo "
Reinstall the GRUB of ${LISTOFPARTITIONS[$REGRUB_PART]} into the $GRUBSTAGEONE partition"
	reinstall_grubstageone
else
	GRUBSTAGEONE="$NOFORCE_DISK"
	DEVGRUBSTAGEONE="/dev/$GRUBSTAGEONE"
	echo "
Reinstall the GRUB of ${LISTOFPARTITIONS[$REGRUB_PART]} into the MBR of $GRUBSTAGEONE"
	reinstall_grubstageone
fi
}


loop_install_grub_in_all_other_disks() {
local n
echo "
Reinstall the GRUB of ${LISTOFPARTITIONS[$REGRUB_PART]} into MBRs of all disks (except live-disks and removable disks without OS)"
INSTALLEDINOTHERDISKS=""
for ((n=1;n<=NBOFDISKS;n++)); do
	[[ "${DISK_WITHOS[$n]}" = has-os ]] || ( [[ "${USBDISK[$n]}" =~ no ]] && [[ "${MMCDISK[$n]}" =~ no ]] ) \
	&& [[ "${USBDISK[$n]}" != liveusb ]] && [[ "${MMCDISK[$n]}" != livemmc ]] && [[ "$n" != "${DISKNB_PART[$BCKUPREGRUB_PART]}" ]] \
	&& [[ "${LISTOFDISKS[$n]}" != "$BCKUPNOFORCE_DISK" ]] && INSTALLEDINOTHERDISKS=yes
done
if [[ "$INSTALLEDINOTHERDISKS" ]];then
	if [[ "$REMOVABLEDISK" ]];then
		force_unmount_and_prepare_chroot
		fix_grub_d
	fi
	for ((n=1;n<=NBOFDISKS;n++)); do
		if [[ "${DISK_WITHOS[$n]}" = has-os ]] || ( [[ "${USBDISK[$n]}" =~ no ]] && [[ "${MMCDISK[$n]}" =~ no ]] ) \
		&& [[ "${USBDISK[$n]}" != liveusb ]] && [[ "${MMCDISK[$n]}" != livemmc ]] && [[ "$n" != "${DISKNB_PART[$BCKUPREGRUB_PART]}" ]];then
			NOFORCE_DISK="${LISTOFDISKS[$n]}"
			[[ "$NOFORCE_DISK" != "$BCKUPNOFORCE_DISK" ]] && reinstall_grub
		fi
	done
fi
}

reinstall_grubstageone() {
local SETUPOUTPUT INSTALLOUTPUT cfg ztyp z r dd
repflex=yes
repoom=yes
repldm=yes
#dpkg_function
echo "SET@_label0.set_text('''$Reinstall_GRUB $GRUBSTAGEONE. $This_may_require_several_minutes''')"
grubinstall
if [[ ! "$NOW_IN_OTHER_DISKS" ]];then
	if [[ "$(cat "$CATTEE" | grep FlexNet )" ]] \
	|| [[ "$(cat "$CATTEE" | grep 't known to reserve space' )" ]] || [[ "$BLANKEXTRA_ACTION" ]];then
		if [[ ! "$BLANKEXTRA_ACTION" ]];then #http://paste.ubuntu.com/1058971 , http://paste.ubuntu.com/1060937, http://paste.ubuntu.com/1367610
			#iso9660: http://askubuntu.com/questions/158299/why-does-installing-grub2-give-an-iso9660-filesystem-destruction-warning
			[[ "$(cat "$CATTEE" | grep 't known to reserve space' )" ]] && FUNCTION=Extra-MBR-space-error || FUNCTION=FlexNet
			update_translations
			end_pulse
			zenity --width=300 --question --title="$APPNAME2" --text="$FUNCTION_detected $Please_backup_data $Do_you_want_to_continue" || repflex=no
			echo "$FUNCTION_detected $Please_backup_data $Do_you_want_to_continue $repflex"
			start_pulse
		fi
		if [[ "$repflex" = yes ]];then
			blankextraspace
			grubinstall
		else
			ERROR=yes
		fi
	fi
	if [[ "$(cat "$CATTEE" | grep recheck )" ]] || [[ "$(cat "$CATTEE" | grep 'device.map' )" ]];then
		RECHECK=" --recheck"
		grubinstall
	fi
	if [[ "$(cat "$CATTEE" | grep 'this LDM has no Embedding Partition' )" ]];then
		#Workaround for https://bugs.launchpad.net/bugs/1061255
		#Works: http://paste.ubuntu.com/1401572
		FUNCTION=LDM-blocker; update_translations
		for ((b=1;b<=NBOFDISKS;b++)); do
			[[ "${LISTOFDISKS[$b]}" = "$GRUBSTAGEONE" ]] && GRUBSTAGEONENB="$b"
		done
		SKIPP="$(cat /sys/block/"$GRUBSTAGEONE"/size)"
		(( SKIPP -= 1 ))
		if [[ "$SKIPP" -gt 10000 ]] && [[ "${BYTES_PER_SECTOR[$GRUBSTAGEONENB]}" -ge 512 ]] \
		&& [[ "${BYTES_PER_SECTOR[$GRUBSTAGEONENB]}" -le 2048 ]];then
			echo "
dd if=/dev/$GRUBSTAGEONE bs=${BYTES_PER_SECTOR[$GRUBSTAGEONENB]} count=1 skip=6 | hd"
			LANGUAGE=C LC_ALL=C dd if=/dev/"$GRUBSTAGEONE" bs="${BYTES_PER_SECTOR[$GRUBSTAGEONENB]}" count=1 skip=6 | hd
			echo "
dd if=/dev/$GRUBSTAGEONE bs=${BYTES_PER_SECTOR[$GRUBSTAGEONENB]} count=1 skip=$SKIPP | hd"
			LANGUAGE=C LC_ALL=C dd if=/dev/"$GRUBSTAGEONE" bs="${BYTES_PER_SECTOR[$GRUBSTAGEONENB]}" count=1 skip="$SKIPP" | hd
			if [[ ! "$(LANGUAGE=C LC_ALL=C dd if=/dev/"$GRUBSTAGEONE" bs="${BYTES_PER_SECTOR[$GRUBSTAGEONENB]}" count=1 skip="$SKIPP" | hd | grep PRIVHEAD )" ]] \
			&& [[ ! "$(LANGUAGE=C LC_ALL=C dd if=/dev/"$GRUBSTAGEONE" bs="${BYTES_PER_SECTOR[$GRUBSTAGEONENB]}" count=1 skip=6 | hd | grep PRIVHEAD )" ]];then
				echo "Error: no PRIVHEAD in 6th nor last sector. $PLEASECONTACT"
				ERROR=yes
			fi
			if [[ "$(LANGUAGE=C LC_ALL=C dd if=/dev/"$GRUBSTAGEONE" bs="${BYTES_PER_SECTOR[$GRUBSTAGEONENB]}" count=1 skip="$SKIPP" | hd | grep PRIVHEAD )" ]];then
				end_pulse
				zenity --width=300 --question --title="$APPNAME2" --text="$FUNCTION_detected $Please_backup_data $Do_you_want_to_continue" || repldm=no
				echo "$FUNCTION_detected $Please_backup_data $Do_you_want_to_continue $repldm"
				start_pulse
				if [[ "$repldm" = yes ]];then
					echo "dd if=/dev/zero of=/dev/$GRUBSTAGEONE bs=${BYTES_PER_SECTOR[$GRUBSTAGEONENB]} seek=$SKIPP count=1"
					LANGUAGE=C LC_ALL=C dd if=/dev/zero of=/dev/"$GRUBSTAGEONE" bs="${BYTES_PER_SECTOR[$GRUBSTAGEONENB]}" seek="$SKIPP" count=1
					grubinstall
				else
					ERROR=yes
				fi
			fi
			if [[ "$(LANGUAGE=C LC_ALL=C dd if=/dev/"$GRUBSTAGEONE" bs="${BYTES_PER_SECTOR[$GRUBSTAGEONENB]}" count=1 skip=6 | hd | grep PRIVHEAD )" ]];then
				echo "$PLEASECONTACT"
				end_pulse
				zenity --width=300 --question --title="$APPNAME2" --text="$FUNCTION_detected This will delete the 6th sector of $GRUBSTAGEONE. $Do_you_want_to_continue" || repldm=no
				echo "$FUNCTION_detected This will delete the 6th sector of $GRUBSTAGEONE. $Do_you_want_to_continue $repldm"
				start_pulse
				if [[ "$repldm" = yes ]];then
					echo "dd if=/dev/zero of=/dev/$GRUBSTAGEONE bs=${BYTES_PER_SECTOR[$GRUBSTAGEONENB]} seek=6 count=1"
					LANGUAGE=C LC_ALL=C dd if=/dev/zero of=/dev/"$GRUBSTAGEONE" bs="${BYTES_PER_SECTOR[$GRUBSTAGEONENB]}" seek=6 count=1
					grubinstall
				else
					ERROR=yes
				fi
			fi
		else
			echo "Error: bad parameters for LDM workaround. $PLEASECONTACT"
			ERROR=yes
		fi
	elif [[ "$(cat "$CATTEE" | grep 'will not proceed with blocklists' )" ]];then
		FORCEPARAM=" --force" #http://www.linuxquestions.org/questions/linux-newbie-8/problem-installing-fedora-17-in-dual-booting-with-windows-7-a-4175412439/page2.html
		grubinstall
	fi
	if [[ "$(cat "$CATTEE" | grep ': error: out of memory.' )" ]] && [[ ! "$ATA" ]];then
		FUNCTION=out-of-memory
		OPTION="$Ata_disk"
		update_translations
		end_pulse
		zenity --width=300 --question --title="$APPNAME2" --text="$FUNCTION_detected $Do_you_want_activate_OPTION" || repoom=no
		echo "$FUNCTION_detected $Do_you_want_activate_OPTION $repoom"
		start_pulse
		#http://paste.ubuntu.com/1041994 solved by ATA
		if [[ "$repoom" = yes ]];then
			ATA=" --disk-module=ata"
			grubinstall
		else
			echo "$You_may_want_to_retry_after_activating_OPTION"
			end_pulse
			zenity --width=300 --info --title="$APPNAME2" --text="$You_may_want_to_retry_after_activating_OPTION"
			start_pulse
		fi
	fi
	if [[ "$(cat "$CATTEE" | grep ': error: out of memory.' )" ]] && [[ "$ATA" ]] \
	&& [[ ! "$(cat "$CATTEE" | grep 'Installation finished. No error reported.' )" ]] \
	|| [[ "$(cat "$CATTEE" | grep 'will not proceed with blocklists' )" ]];then
		embeddingerror=yes
		FUNCTION="Embedding-error-in-$GRUBSTAGEONE"
		TYPE3=/boot
		update_translations
		OPTION="$Separate_TYPE3_partition"
		update_translations
		echo "$FUNCTION_detected $You_may_want_to_retry_after_activating_OPTION"
		end_pulse
		zenity --width=300 --warning --title="$APPNAME2" --text="$FUNCTION_detected $You_may_want_to_retry_after_activating_OPTION"
		start_pulse
	fi
	if [[ "$(cat "$CATTEE" | grep 'failed to run command' | grep grub | grep install )" ]];then
		echo "Failed to run command grub-install detected."
		${CHROOTCMD}type ${GRUBTYPE_OF_PART[$USRPART]}
		for gg in /usr/sbin/ /usr/bin/ /sbin/ /bin/ /usr/sbin/lib*/*/*/ /usr/bin/lib*/*/*/ /sbin/lib*/*/*/ /bin/lib*/*/*/;do #not sure "type" is available in all distros
			for gi in grub-install grub2-install grub-install.unsupported;do
				if [[ -f "${BLKIDMNT_POINT[$REGRUB_PART]}$gg$gi" ]];then
					ls -l "${BLKIDMNT_POINT[$REGRUB_PART]}$gg$gi"
					chmod a+x "${BLKIDMNT_POINT[$REGRUB_PART]}$gg$gi"
					ls -l "${BLKIDMNT_POINT[$REGRUB_PART]}$gg$gi"
				fi
			done
		done
		grubinstall
	fi

	GRUBCUSTOM="${BLKIDMNT_POINT[$REGRUB_PART]}"/etc/grub.d/25_custom
	[[ -f "$GRUBCUSTOM" ]] && echo "mv 25_custom" && mv "$GRUBCUSTOM" "$LOGREP/${LISTOFPARTITIONS[$REGRUB_PART]}/25_custom"

	if [[ "$GRUBPACKAGE" =~ efi ]];then
		for ((efitmmmp=1;efitmmmp<=NBOFPARTITIONS;efitmmmp++));do
			EFIDO="${BLKIDMNT_POINT[$efitmmmp]}"
			[[ -d "$EFIDO/EFI" ]] && EFIDOFI="$EFIDO/EFI/" || EFIDOFI="$EFIDO/efi/"
			REFC=refind.conf
			REFI=""
			[[ -f "$EFIDOFI/Microsoft/Boot/$REFC" ]] || [[ -f "$EFIDOFI/BOOT/$REFC" ]] || [[ -f "$EFIDOFI/refind/$REFC" ]] \
			&& REFI=y && echo "Refind detected on ${LISTOFPARTITIONS[$efitmmmp]}"
			[[ -f "$EFIDOFI/Microsoft/bootmgfw.efi" ]] && [[ "$REFI" ]] && echo "Restore /Microsoft/Boot/bootmgfw.efi" \
			&& mv "$EFIDOFI/Microsoft/bootmgfw.efi" "$EFIDOFI/Microsoft/Boot/bootmgfw.efi"
		done
		#http://paste.ubuntu.com/1070906 , http://paste.ubuntu.com/1069331, http://paste.ubuntu.com/1196571
		BEFIDO="${BLKIDMNT_POINT[$EFIPART_TO_USE]}" #eg http://paste.ubuntu.com/1227221
		NEEDMENUUPDATE=""
		LOCKEDESP=""
		#https://bugs.launchpad.net/bugs/1090829 / https://bugs.launchpad.net/ubuntu/+source/grub2/+bug/1091477
		if [[ "$(cat "$CATTEE" | grep 'Input/output')" ]] || [[ "$(cat "$CATTEE" | grep Read-only )" ]];then
			echo "
dosfsck -a /dev/${LISTOFPARTITIONS[$EFIPART_TO_USE]}"
			LANGUAGE=C LC_ALL=C dosfsck -a /dev/${LISTOFPARTITIONS[$EFIPART_TO_USE]}
			grubinstall
			if [[ "$(cat "$CATTEE" | grep 'Input/output')" ]] || [[ "$(cat "$CATTEE" | grep Read-only )" ]];then
				echo "
rm -Rf /dev/${LISTOFPARTITIONS[$EFIPART_TO_USE]}/ubuntu .. fedora"
				LANGUAGE=C LC_ALL=C rm -Rf /dev/${LISTOFPARTITIONS[$EFIPART_TO_USE]}/ubuntu
				LANGUAGE=C LC_ALL=C rm -Rf /dev/${LISTOFPARTITIONS[$EFIPART_TO_USE]}/fedora
				grubinstall
				[[ "$(cat "$CATTEE" | grep 'Input/output')" ]] || [[ "$(cat "$CATTEE" | grep Read-only )" ]] \
				&& ERROR=yes && LOCKEDESP=yes && echo "$DASH (Write-locked ESP) dmesg:
$(dmesg)


$DASH cat /var/log/syslog:
$(cat /var/log/syslog)


"
			fi
		fi
		EFIGRUBFILE=""
		for secureb in grub shim;do #Signed GRUB in priority
			if [[ "$GRUBPACKAGE" =~ sign ]] || [[ "$secureb" = grub ]];then #http://ubuntuforums.org/showthread.php?p=12376694#post12376694
				for z in "$BEFIDO/efi/"*/${secureb}*.efi "$BEFIDO/EFI/"*/${secureb}*.efi;do #http://paste.ubuntu.com/1382319
					#echo "(debug) $z"
					[[ "$(echo "$z" | grep -v '*' | grep -vi Microsoft )" ]] && EFIGRUBFILE="$z"
				done
			fi
		done
		if [[ "$EFIGRUBFILE" ]];then
			EFIGRUBFILESHORT="${EFIGRUBFILE#*$BEFIDO/}"
			EFIGRUBFILESHORT="${EFIGRUBFILESHORT#*/}" #eg ubuntu/shimx64.efi
			EFIGRUBFILEDIR="${EFIGRUBFILESHORT%/*}" #eg ubuntu
			EFIGRUBFILEDIRFULL="${EFIGRUBFILE%/*}"
			for ((efitmp=1;efitmp<=NBOFPARTITIONS;efitmp++));do #https://blueprints.launchpad.net/boot-repair/+spec/grub-on-several-efi
				EFIDO="${BLKIDMNT_POINT[$efitmp]}"
				if ( [[ "$(ls "$EFIDO"/ | grep efi)" ]] || [[ "$(ls "$EFIDO"/ | grep EFI)" ]] ) \
				&& [[ "${USBDISK[${DISKNB_PART[$efitmp]}]}" != liveusb ]] && [[ "${MMCDISK[${DISKNB_PART[$efitmp]}]}" != livemmc ]] \
				&& [[ ! -d "$EFIDO/sys" ]];then #todo paste ubuntu 6037509
					[[ "$(ls "$EFIDO"/ | grep efi)" ]] && EFIDOFI="$EFIDO/efi/" || EFIDOFI="$EFIDO/EFI/"
					#echo "(debug) beglsefi1 $EFIGRUBFILESHORT ; $EFIGRUBFILEDIR , $EFIDO ."
					[[ "$DEBBUG" ]] && ls_efi_partition #debug
					mkdir -p "$EFIDOFI$EFIGRUBFILEDIR"
					if [[ ! -f "$EFIDOFI$EFIGRUBFILESHORT" ]];then
						echo "cp $EFIGRUBFILE $EFIDOFI$EFIGRUBFILESHORT"
						cp "$EFIGRUBFILE" "$EFIDOFI$EFIGRUBFILESHORT"
						NEEDMENUUPDATE=y
						EFIFOLD="$EFIDOFI$EFIGRUBFILEDIR"
						copy_grub_along_with_shim
					fi
				fi
			done
		else
			ERROR=yes && echo "Error: no grub*.efi generated. $PLEASECONTACT
"
		fi
		#/efi/ubuntu/grubx64.efi, grubia32.efi http://forum.ubuntu-fr.org/viewtopic.php?id=207366&p=69
		MEMADDEDENTRY=""
		for tmprecov in 1 2 3 4;do
			for ((efitmp=1;efitmp<=NBOFPARTITIONS;efitmp++));do #http://forum.ubuntu-fr.org/viewtopic.php?pid=10305051#p10305051
				EFIDO="${BLKIDMNT_POINT[$efitmp]}"
				if ( [[ "$tmprecov" = 1 ]] && [[ "${RECOV[$efitmp]}" != recovery-or-hidden ]] && [[ "${DISKNB_PART[$efitmp]}" = "${DISKNB_PART[$EFIPART_TO_USE]}" ]] ) \
				|| ( [[ "$tmprecov" = 2 ]] && [[ "${RECOV[$efitmp]}" != recovery-or-hidden ]] && [[ "${DISKNB_PART[$efitmp]}" != "${DISKNB_PART[$EFIPART_TO_USE]}" ]] ) \
				|| ( [[ "$tmprecov" = 3 ]] && [[ "${RECOV[$efitmp]}" = recovery-or-hidden ]] && [[ "${DISKNB_PART[$efitmp]}" = "${DISKNB_PART[$EFIPART_TO_USE]}" ]] ) \
				|| ( [[ "$tmprecov" = 4 ]] && [[ "${RECOV[$efitmp]}" = recovery-or-hidden ]] && [[ "${DISKNB_PART[$efitmp]}" != "${DISKNB_PART[$EFIPART_TO_USE]}" ]] ) \
				&& ( [[ "$(ls "$EFIDO"/ | grep efi)" ]] || [[ "$(ls "$EFIDO"/ | grep EFI)" ]] ) \
				&& [[ "${USBDISK[${DISKNB_PART[$efitmp]}]}" != liveusb ]] && [[ "${MMCDISK[${DISKNB_PART[$efitmp]}]}" != livemmc ]];then
					[[ "$(ls "$EFIDO"/ | grep efi)" ]] && EFIDOFI="$EFIDO/efi/" || EFIDOFI="$EFIDO/EFI/"
					REFC=refind.conf
					REFI=""
					[[ -f "$EFIDOFI/Microsoft/Boot/$REFC" ]] || [[ -f "$EFIDOFI/BOOT/$REFC" ]] || [[ -f "$EFIDOFI/refind/$REFC" ]] && REFI=y
					if [[ "$REFI" ]] && [[ -f "$EFIDOFI/Microsoft/bootmgfw.efi" ]];then #fix Refind hacks
						mv -f "$EFIDOFI/Microsoft/Boot/bootmgfw.efi" "$EFIDOFI/Microsoft/Boot/bootmgfwrefind.efi"
						rm -f "$EFIDOFI/Microsoft/Boot/bootmgfw.efi"
						cp -f "$EFIDOFI/Microsoft/bootmgfw.efi" "$EFIDOFI/Microsoft/Boot/bootmgfw.efi"
					fi
					if [[ -d "$EFIDOFI/BOOT-rEFIndBackup" ]];then
						mv -f "$EFIDOFI/BOOT" "$EFIDOFI/BOOTrefind"
						rm -rf "$EFIDOFI/BOOT"
						cp -rf "$EFIDOFI/BOOT-rEFIndBackup" "$EFIDOFI/BOOT"
					fi
					if [[ "$CREATE_BKP_ACTION" ]] && [[ "$EFIGRUBFILE" ]];then #Workaround for http://askubuntu.com/questions/150174/sony-vaio-with-insyde-h2o-efi-bios-will-not-boot-into-grub-efi
						mkdir -p "${EFIDOFI}Boot"
						[[ "$WINEFI_BKP_ACTION" ]] && mkdir -p "${EFIDOFI}Microsoft/Boot"
						for chgfile in Microsoft/Boot/bootmgfw.efi Microsoft/Boot/bootx64.efi Boot/bootx64.efi;do
							if [[ "$WINEFI_BKP_ACTION" ]] || [[ ! "$chgfile" =~ Mi ]];then
								EFIFICH="$EFIDOFI$chgfile"
								EFIFOLD="${EFIFICH%/*}"
								EFIFICHEND="${chgfile##*/}"
								NEWEFIL="$EFIFOLD/bkp$EFIFICHEND"
								#Backup Win file
								#locked to /EFI/Boot/bootx64.efi: http://ubuntuforums.org/showthread.php?p=12366736#post12366736)
								#and http://forum.thinkpads.com/viewtopic.php?f=9&t=107246
								#locked to bootmgfw.efi: http://askubuntu.com/questions/150174/sony-vaio-with-insyde-h2o-efi-bios-will-not-boot-into-grub-efi
								echo "df /dev/${LISTOFPARTITIONS[$efitmp]}"
								DFX="$(df "/dev/${LISTOFPARTITIONS[$efitmp]}" )"
								if [[ "$DFX" =~ "100%" ]] || [[ "$DFX" =~ "9[0-9]%" ]];then
									echo "mv winEFI cancelled (${LISTOFPARTITIONS[$efitmp]} full)"
								elif [[ ! -f "$NEWEFIL" ]] && [[ -f "$EFIFICH" ]] && [[ ! -f "$EFIFICH.grb" ]];then
									cp "$EFIFICH" "$LOGREP/${LISTOFPARTITIONS[$efitmp]}"
									#cp "$EFIFICH" "$EFIFICH.bkp"
									echo "mv $EFIFICH $NEWEFIL"
									mv "$EFIFICH" "$NEWEFIL"
									NEEDMENUUPDATE=y
									[[ -f "$EFIFICH" ]] && echo "Error: $EFIFICH still pr. $PLEASECONTACT"
								fi
								#When no Windows EFI file
								if [[ ! -f "$EFIFICH" ]];then #Create fake Win file
									if [[ -f "$EFIFICH.grb" ]]; then
										echo "Error: still $EFIFICH.grb. $PLEASECONTACT"
									else
										if [[ ! -f "$NEWEFIL" ]];then #original has not been backed up
											echo "touch $EFIFICH.grb"
											touch "$EFIFICH.grb"
											[[ ! -f "$EFIFICH.grb" ]] && echo "Error no $EFIFICH.grb"
										fi
										if [[ -f "$NEWEFIL" ]] || [[ -f "$EFIFICH.grb" ]]; then
											echo "cp $EFIGRUBFILE $EFIFICH"
											cp "$EFIGRUBFILE" "$EFIFICH"
											copy_grub_along_with_shim
										fi
									fi
								fi
							fi
						done
						[[ "$DEBBUG" ]] && ls_efi_partition #debug
					fi

					#Workaround https://bugs.launchpad.net/ubuntu/+source/grub2/+bug/1024383
					echo "Add $EFIDO efi entries in $GRUBCUSTOM"
					for WINORMAC in Microsoft Boot MacOS Other;do #Other: http://ubuntuforums.org/showthread.php?p=12421487#post12421487
						if [[ "$WINORMAC" = MacOS ]];then
							for z in "$EFIDOFI"*/{,*/}*/*.scap;do
								[[ ! "$z" =~ '*' ]] && add_custom_efi
							done
						else
							for priorityefi in 1 2;do
								for z in "$EFIDOFI"*/{,*/}*.efi;do
									ZFOLD="${z%/*}"
									ZFICHEND="${z##*/}"
									ZNEWFIL="$ZFOLD/bkp$ZFICHEND"
									if ( [[ "$priorityefi" = 1 ]] && [[ "${ZFICHEND%%p*}" = bk ]] ) \
									|| ( [[ "$priorityefi" = 2 ]] && [[ "${ZFICHEND%%p*}" != bk ]] && [[ ! -f "$ZNEWFIL" ]] ) \
									&& [[ ! "$z" =~ '*' ]] && [[ ! -f "$z".grb ]] \
									&& [[ ! "$z" =~ memtest.efi ]] && [[ ! "$z" =~ grub ]]  && [[ ! "$z" =~ shim ]] \
									&& ( [[ "$z" =~ "$EFIDOFI$WINORMAC" ]] || [[ "$WINORMAC" = Other ]] ) \
									&& [[ ! "$z" =~ bootmgr.efi ]];then #http://ubuntuforums.org/showpost.php?p=12114780&postcount=18
										[[ "$(grep "$z,$efitmp;" <<< "$MEMADDEDENTRY")" ]] \
										&& echo "${LISTOFPARTITIONS[$efitmp]}/$ZFICHEND already added" || add_custom_efi
									fi
								done
							done
						fi
					done
				fi
			done
		done
		[[ "$NEEDMENUUPDATE" ]] && grubinstall
	fi
	if [[ ! "$(cat "$CATTEE" | grep "of ${GRUBTYPE_OF_PART[$USRPART]} $DEVGRUBSTAGEONE:0" )" ]];then
		ERROR=yes #http://paste.ubuntu.com/1011898
		echo "
---- Grub-install verbose"
		grubinstall_verbose
		echo "---- End of grub-install verbose
"
	fi
fi
}


copy_grub_along_with_shim() {
#called twice in reinstall_grubstageone()
if [[ "$EFIGRUBFILE" =~ shim ]] && [[ ! -f "$EFIFOLD"/grubx64.efi ]] && [[ ! -f "$EFIFOLD"/grubia32.efi ]];then #solves bug #1752851
	if [[ -f "$EFIGRUBFILEDIRFULL"/grubx64.efi ]];then
		echo "cp $EFIGRUBFILEDIRFULL/grubx64.efi $EFIFOLD/"
		cp $EFIGRUBFILEDIRFULL/grubx64.efi $EFIFOLD/
	elif [[ -f "$EFIGRUBFILEDIRFULL"/grubia32.efi ]];then
		echo "cp $EFIGRUBFILEDIRFULL/grubia32.efi $EFIFOLD/"
		cp $EFIGRUBFILEDIRFULL/grubia32.efi $EFIFOLD/
	else
		echo "Warning: no grub*.efi in same folder as shim. $PLEASECONTACT
"
	fi
fi		
}


force_unmount_and_prepare_chroot() {
#called by loop_install_grub_in_all_other_disks (if other GRUB) & reinstall_grub_main_mbr
[[ "$DEBBUG" ]] && echo "[debug]force_unmount_and_prepare_chroot"
[[ "$CLEANNAME" =~ r ]] && force_unmount_os_partitions_in_mnt_except_reinstall_grub #OS are not recognized if partitions are not unmounted
prepare_chroot
if [[ "$KERNEL_PURGE" ]] || [[ "$GRUBPURGE_ACTION" ]] && [[ "$NOW_USING_CHOSEN_GRUB" ]];then
	if [[ "${LISTOFPARTITIONS[$REGRUB_PART]}" != "$CURRENTSESSIONPARTITION" ]];then
		mv "${BLKIDMNT_POINT[$REGRUB_PART]}/etc/resolv.conf" "${BLKIDMNT_POINT[$REGRUB_PART]}/etc/resolv.conf.old"
		cp /etc/resolv.conf "${BLKIDMNT_POINT[$REGRUB_PART]}/etc/resolv.conf"  # Required to connect to the Internet.
	fi
	echo "SET@_label0.set_text('''Purge ${LISTOFPARTITIONS[$REGRUB_PART]} (dep). $This_may_require_several_minutes''')"
	repair_dep "$REGRUB_PART"
	update_cattee
	aptget_update_function
fi
}

add_custom_efi() {
if [[ ! -f "$GRUBCUSTOM" ]];then
	echo '#!/bin/sh' > "$GRUBCUSTOM"
	echo 'exec tail -n +3 $0' >> "$GRUBCUSTOM"
	chmod a+x "$GRUBCUSTOM"
fi
EFIFIL="${z#*$EFIDO}" #eg /EFI/Microsoft/Boot/bootmgr.efi or /efi/bootmgfw.efi, /efi/Boot/bootx64.efi, or /efi/APPLE/EXTENSIONS/Firmware.scap
[[ "$WINORMAC" = Microsoft ]] && WINORMAC2=Windows || WINORMAC2="$WINORMAC"
[[ "$(grep Windows "$GRUBCUSTOM")" ]] && [[ "$WINORMAC" = Boot ]] && WINORMAC2="Windows Boot" #http://superuser.com/questions/494601/windows-8-fails-to-load-after-boot-repair
if [[ "$WINORMAC" = Other ]];then
	EFILABEL="${EFIFIL#*/}"
else
	if [[ "$EFILABEL" =~ bootmgfw.efi ]];then #http://paste.ubuntu.com/1308398
		[[ "${RECOV[$efitmp]}" = recovery-or-hidden ]] && EFILABEL=recovery || EFILABEL=loader
	elif [[ "${RECOV[$efitmp]}" = recovery-or-hidden ]];then
		EFILABEL="recovery ${EFIFIL##*/}"
	else
		EFILABEL="${EFIFIL##*/}"
	fi
	EFILABEL="$WINORMAC2 UEFI $EFILABEL"
fi
[[ "$(grep "$EFILABEL" "$GRUBCUSTOM")" ]] && EFILABEL="$EFILABEL ${LISTOFPARTITIONS[$efitmp]}"
EFIENTRY1="
menuentry \"$EFILABEL\" {
search --fs-uuid --no-floppy --set=root ${PART_UUID[$efitmp]}
chainloader (\${root})$EFIFIL
}"
#see also http://ubuntuforums.org/showpost.php?p=12098088&postcount=9
#http://ubuntuforums.org/showpost.php?p=12114780&postcount=18
#http://www.rodsbooks.com/ubuntu-efi/index.html (/ubuntu/boot.efi)
#works: http://ubuntuforums.org/showpost.php?p=12361742&postcount=4
if [[ "$(grep "$EFILABEL" "$GRUBCUSTOM")" ]];then
	echo "Warning: $EFILABEL already in $GRUBCUSTOM. $PLEASECONTACT"
else
	echo "Adding custom $z"
	echo "$EFIENTRY1" >> "$GRUBCUSTOM"
	MEMADDEDENTRY="$z,$efitmp;$MEMADDEDENTRY"
fi
}


grubinstall() {
update_cattee #eg 2 efi updates: http://paste.ubuntu.com/1547330
INSTALLOUTPUT="$(LANGUAGE=C LC_ALL=C $CHROOTCMD${GRUBTYPE_OF_PART[$USRPART]}$FORCEPARAM$RECHECK$ATA $DEVGRUBSTAGEONE ; echo "exit code of ${GRUBTYPE_OF_PART[$USRPART]} $DEVGRUBSTAGEONE:$?" )"
echo "${GRUBTYPE_OF_PART[$USRPART]}$FORCEPARAM$RECHECK$ATA $DEVGRUBSTAGEONE: $INSTALLOUTPUT"
}

grubinstall_verbose() {
update_cattee #eg 2 efi updates: http://paste.ubuntu.com/1547330
INSTALLOUTPUT="$(LANGUAGE=C LC_ALL=C ${CHROOTCMD}sh -x ${GRUBTYPE_OF_PARTZ[$USRPART]}$FORCEPARAM$RECHECK$ATA $DEVGRUBSTAGEONE ; echo "exit code of ${GRUBTYPE_OF_PART[$USRPART]} $DEVGRUBSTAGEONE:$?" )"
echo "--------"
echo "${GRUBTYPE_OF_PARTZ[$USRPART]}$FORCEPARAM$RECHECK$ATA $DEVGRUBSTAGEONE: $INSTALLOUTPUT"
}

grub_mkconfig_main() {
[[ "$GRUBPACKAGE" = grub ]] && UPDATEYES=" -y" || UPDATEYES=""
grub_mkconfig
if [[ "$(cat "$CATTEE" | grep 'Unrecognized option' )" ]] && [[ "$UPDATEYES" = " -y" ]];then #in case grub2 detected as grub1
	UPDATEYES=""
	grub_mkconfig
fi
if [[ "$(cat "$CATTEE" | grep 'error:' )" ]];then #eg http://paste.ubuntu.com/1097173 http://paste.ubuntu.com/1306993
	ERROR=yes
fi
for z in grub grub2;do #Set Windows as default OS
	if [[ -f "${BLKIDMNT_POINT[$REGRUB_PART]}"/boot/$z/grub.cfg ]] && [[ "$CHANGEDEFAULTOS" ]];then
		r="$(cat "${BLKIDMNT_POINT[$REGRUB_PART]}/boot/$z/grub.cfg" | grep -i windows | grep menuentry | grep -v '#' )"
		if [[ "$r" ]];then
			if [[ "$(grep "Boot-Repair" <<< "$r" )" ]];then
				r="$(grep "Boot-Repair" <<< "$r" )"
			elif [[ "$(grep -i loader <<< "$r" )" ]];then
				r="$(grep -i loader <<< "$r" )"
			elif [[ "$(grep -vi recovery <<< "$r" )" ]];then
				r="$(grep -vi recovery <<< "$r" )"
			fi
			r="${r#*\"}"; r="${r%%\"*}" #eg Windows 7 (loader) (on /dev/sda11)
			dd="${BLKIDMNT_POINT[$REGRUB_PART]}/etc/default/grub"
			if [[ -f "$dd" ]];then
				sed -i "s|GRUB_DEFAULT=.*|GRUB_DEFAULT=\"${r}\"|" "$dd"
				echo "
Set $r as default entry"
				grub_mkconfig
			fi
		else
			echo "Warning: no Windows in ${BLKIDMNT_POINT[$REGRUB_PART]}/boot/$z/grub.cfg"
		fi
	fi
done
}

grub_mkconfig() {
update_cattee
if [[ "${UPDATEGRUB_OF_PART[$USRPART]}" = update-grub ]];then
	echo "SET@_label0.set_text('''Grub-update. $This_may_require_several_minutes''')"
	echo "
$CHROOTCMD${UPDATEGRUB_OF_PART[$USRPART]}$UPDATEYES"
	LANGUAGE=C LC_ALL=C $CHROOTCMD${UPDATEGRUB_OF_PART[$USRPART]}$UPDATEYES
elif [[ "${UPDATEGRUB_OF_PART[$USRPART]}" =~ mkconfig ]];then
	echo "SET@_label0.set_text('''Grub-mkconfig. $This_may_require_several_minutes''')"
	for cfg in "/" "2/";do
		if [[ -d "${BLKIDMNT_POINT[$REGRUB_PART]}/boot/grub$cfg" ]];then
			echo "
$CHROOTCMD${UPDATEGRUB_OF_PART[$USRPART]}${cfg}grub.cfg"
			LANGUAGE=C LC_ALL=C $CHROOTCMD${UPDATEGRUB_OF_PART[$USRPART]}${cfg}grub.cfg
		fi
	done
fi
}

#####Used by repair, uninstaller (for GRUB reinstall, and purge)
force_unmount_os_partitions_in_mnt_except_reinstall_grub() {
[[ "$DEBBUG" ]] && echo "[debug]Unmount all OS partitions except / and partition where we reinstall GRUB (${LISTOFPARTITIONS[$REGRUB_PART]})"
local fuopimerg
echo "SET@_label0.set_text('''Unmount all except ${LISTOFPARTITIONS[$REGRUB_PART]}. $This_may_require_several_minutes''')"
pkill pcmanfm	#To avoid it automounts
if [[ ! "$FEDORA_DETECTED" ]] || [[ "$NOTFEDORA_DETECTED" ]];then
	for ((fuopimerg=1;fuopimerg<=NBOFPARTITIONS;fuopimerg++)); do
		if [[ "${PART_WITH_OS[$fuopimerg]}" = is-os ]] && [[ "${BLKIDMNT_POINT[$fuopimerg]}" ]] \
		&& [[ "${BLKIDMNT_POINT[$fuopimerg]}" != /boot ]] && [[ "${BLKIDMNT_POINT[$fuopimerg]}" != /usr ]] \
		&& [[ ! "${OSNAME[$fuopimerg]}" =~ Fedora ]] && [[ ! "${OSNAME[$fuopimerg]}" =~ Arch ]] \
		&& [[ "$fuopimerg" != "$REGRUB_PART" ]] && [[ "${EFI_TYPE[$fuopimerg]}" = not--efi--part ]];then
			umount "${BLKIDMNT_POINT[$fuopimerg]}"
		fi #http://forum.ubuntu-fr.org/viewtopic.php?id=957301 , http://forums.linuxmint.com/viewtopic.php?f=46&t=108870&p=612288&hilit=grub#p612288
	done
fi
}

mount_separate_boot_if_required() {
[[ "$DEBBUG" ]] && echo "[debug] mount_separate_boot_if_required $NOW_IN_OTHER_DISKS , $USE_SEPARATEBOOTPART, $GRUBPACKAGE ,$USE_SEPARATEUSRPART"
if [[ "$NOW_USING_CHOSEN_GRUB" ]];then
	if [[ "$USE_SEPARATEBOOTPART" ]];then
		pkill pcmanfm	#To avoid it automounts
		if [[ ! -d "${BLKIDMNT_POINT[$REGRUB_PART]}/boot" ]];then
			mkdir -p "${BLKIDMNT_POINT[$REGRUB_PART]}/boot"
			echo "Created ${LISTOFPARTITIONS[$REGRUB_PART]}/boot"
		elif [[ "$(ls "${BLKIDMNT_POINT[$REGRUB_PART]}/boot" )" ]] && [[ "$KERNEL_PURGE" ]];then
			echo "Rename ${LISTOFPARTITIONS[$BOOTPART_TO_USE]}/boot to boot_bak"
			cp -r "${BLKIDMNT_POINT[$REGRUB_PART]}/boot" "${BLKIDMNT_POINT[$REGRUB_PART]}/boot_bak"
			mkdir -p "${BLKIDMNT_POINT[$REGRUB_PART]}/boot"
		fi
		if [[ "$LIVESESSION" = live ]] || [[ "${BLKIDMNT_POINT[$BOOTPART_TO_USE]}" != /boot ]];then
			umount "${BLKIDMNT_POINT[$BOOTPART_TO_USE]}"
			BLKIDMNT_POINT[$BOOTPART_TO_USE]="${BLKIDMNT_POINT[$REGRUB_PART]}/boot"
			echo "Mount ${LISTOFPARTITIONS[$BOOTPART_TO_USE]} on ${BLKIDMNT_POINT[$BOOTPART_TO_USE]}"
			mount "/dev/${LISTOFPARTITIONS[$BOOTPART_TO_USE]}" "${BLKIDMNT_POINT[$BOOTPART_TO_USE]}"
		fi
	fi
	[[ -d "${BLKIDMNT_POINT[$BOOTPART_TO_USE]}/boot" ]] && [[ ! -d "${BLKIDMNT_POINT[$BOOTPART_TO_USE]}/dev" ]] \
	&& mv "${BLKIDMNT_POINT[$BOOTPART_TO_USE]}/boot" "${BLKIDMNT_POINT[$BOOTPART_TO_USE]}/boot_rm" #http://paste.ubuntu.com/1313675
	if [[ "$GRUBPACKAGE" =~ efi ]];then
		pkill pcmanfm	#To avoid it automounts
		if [[ ! -d "${BLKIDMNT_POINT[$REGRUB_PART]}/boot/efi" ]];then
			mkdir -p "${BLKIDMNT_POINT[$REGRUB_PART]}/boot/efi"
			echo "Created ${LISTOFPARTITIONS[$REGRUB_PART]}/boot/efi"
		elif [[ "$(ls "${BLKIDMNT_POINT[$REGRUB_PART]}/boot/efi" )" ]];then
			echo "${LISTOFPARTITIONS[$REGRUB_PART]}/boot/efi not empty"	
		fi
		if [[ "$LIVESESSION" = live ]] || [[ "${BLKIDMNT_POINT[$EFIPART_TO_USE]}" != /boot/efi ]];then
			umount "${BLKIDMNT_POINT[$EFIPART_TO_USE]}"
			BLKIDMNT_POINT[$EFIPART_TO_USE]="${BLKIDMNT_POINT[$REGRUB_PART]}/boot/efi"
			echo "Mount ${LISTOFPARTITIONS[$EFIPART_TO_USE]} on ${BLKIDMNT_POINT[$EFIPART_TO_USE]}"
			mount "/dev/${LISTOFPARTITIONS[$EFIPART_TO_USE]}" "${BLKIDMNT_POINT[$EFIPART_TO_USE]}"
			efitmp="$EFIPART_TO_USE"; ls_efi_partition
			aa="$(ls "${BLKIDMNT_POINT[$REGRUB_PART]}/boot/efi/efi")"
			[[ ! "$aa" =~ ubuntu ]] && [[ ! "$aa" =~ mint ]] && echo "No ${LISTOFPARTITIONS[$REGRUB_PART]}/boot/efi/efi/ ubuntu/mint folder"
		fi
	fi
	if [[ "$USE_SEPARATEUSRPART" ]] && [[ "$LIVESESSION" = live ]];then
		pkill pcmanfm	#To avoid it automounts
		umount "${BLKIDMNT_POINT[$USRPART_TO_USE]}"
		if [[ ! -d "${BLKIDMNT_POINT[$REGRUB_PART]}/usr" ]];then
			mkdir -p "${BLKIDMNT_POINT[$REGRUB_PART]}/usr"
			echo "Created ${LISTOFPARTITIONS[$REGRUB_PART]}/usr"
		elif [[ "$(ls "${BLKIDMNT_POINT[$REGRUB_PART]}/usr" )" ]];then
			echo "Warning: ${LISTOFPARTITIONS[$REGRUB_PART]}/usr not empty. $PLEASECONTACT"
			ls "${BLKIDMNT_POINT[$REGRUB_PART]}/usr"
			echo ""
		fi
		BLKIDMNT_POINT[$USRPART_TO_USE]="${BLKIDMNT_POINT[$REGRUB_PART]}/usr"
		echo "Mount ${LISTOFPARTITIONS[$USRPART_TO_USE]} on ${BLKIDMNT_POINT[$USRPART_TO_USE]}"
		mount "/dev/${LISTOFPARTITIONS[$USRPART_TO_USE]}" "${BLKIDMNT_POINT[$USRPART_TO_USE]}"
	fi
fi
}


#Used by reinstall_grub_main_mbr, loop_install_grub_in_all_other_disks (reinstal), restore_resolvconf_and_unchroot (purge)
unchroot_linux_to_reinstall() {
echo "SET@_label0.set_text('''Unchroot. $Please_wait''')"
local w
if [[ "$LIVESESSION" = live ]];then
	pkill pcmanfm	#avoids automounts
	[[ "$GRUBPACKAGE" =~ efi ]] && umount "${BLKIDMNT_POINT[$REGRUB_PART]}/boot/efi"
	[[ "$USE_SEPARATEBOOTPART" ]] && umount "${BLKIDMNT_POINT[$REGRUB_PART]}/boot"
	[[ "$USE_SEPARATEUSRPART" ]] && umount "${BLKIDMNT_POINT[$REGRUB_PART]}/usr"
	for w in run sys proc dev/pts dev; do umount "${BLKIDMNT_POINT[$REGRUB_PART]}/$w" ; done
fi
}

ls_efi_partition() {
#Used by mount_separate_boot_if_required & reinstall_grubstageone & debug_echo_part_info
EFIDIRE="${BLKIDMNT_POINT[$efitmp]}"
EFIDDD="${LISTOFPARTITIONS[$efitmp]}"
for xia in efi bkp;do
	a=""; for x in "$EFIDIRE"/efi/{,*/}*/*.$xia;do
		[[ ! "$x" =~ '*' ]] && a="${x#*$EFIDIRE/efi} $a"
	done
	[[ "$a" ]] && echo "$xia files in $EFIDDD/efi: $a"
done
#if [[ "$(ls "$EFIDIRE/" | grep -vi efi | grep -vi sys | grep -vi windows | grep -v BOOTSECT.BAK  | grep -v kernel | grep -v initr | grep -vi .bin | grep -vi .sim | grep -vi sources | grep -vi boot)" ]];then
#	a=""; for x in "$(ls "$EFIDIRE/")";do a="$x $a";done
#	echo "[debug] ls $EFIDDD: $a . $PLEASECONTACT"
#fi
#if [[ "$LIVESESSION" != live ]] && [[ "$EFIDIRE" != /boot/efi ]];then
#	a=""; for x in "$(ls /boot/efi/efi)";do
#		for y in "$x";do a="$y $a";done
#	done
#	echo "[debug] ls /boot/efi/efi : $a
#[debug] Error efitmp. $PLEASECONTACT"
#fi
}

prepare_chroot() {
#called by force_unmount_and_prepare_chroot (GRUB reinstall), and prepare_chroot_and_internet (purge)
[[ "$DEBBUG" ]] && echo "[debug]prepare_chroot"
if [[ "$LIVESESSION" = live ]];then
	echo "SET@_label0.set_text('''$LAB (chroot). $This_may_require_several_minutes''')"
	local w
	[[ ! -d "${BLKIDMNT_POINT[$REGRUB_PART]}/dev" ]] && mount /dev/${LISTOFPARTITIONS[$REGRUB_PART]} "${BLKIDMNT_POINT[$REGRUB_PART]}" \
	&& echo "Mounted /dev/${LISTOFPARTITIONS[$REGRUB_PART]} on ${BLKIDMNT_POINT[$REGRUB_PART]}" \
	|| echo "[debug] Already mounted /dev/${LISTOFPARTITIONS[$REGRUB_PART]} on ${BLKIDMNT_POINT[$REGRUB_PART]}" #debug error 127
	for w in dev dev/pts proc run sys; do
		mkdir -p "${BLKIDMNT_POINT[$REGRUB_PART]}/$w"
		mount -B /$w "${BLKIDMNT_POINT[$REGRUB_PART]}/$w"
	done  #ubuntuforums.org/showthread.php?t=1965163
	CHROOTCMD="chroot ${BLKIDMNT_POINT[$REGRUB_PART]} "
	CHROOTUSR="chroot \"${BLKIDMNT_POINT[$REGRUB_PART]}\" "
	#CHROOTCMD='chroot "${BLKIDMNT_POINT[$REGRUB_PART]}" '
	#CHROOTUSR='chroot \"${BLKIDMNT_POINT[$REGRUB_PART]}\" '
else
	CHROOTCMD=""
	CHROOTUSR=""
fi
mount_separate_boot_if_required
}

update_cattee() {
(( TEECOUNTER += 1 ))
CATTEE="$TMP_FOLDER_TO_BE_CLEARED/$TEECOUNTER.tee"
exec >& >(tee "$CATTEE")
}
