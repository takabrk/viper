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

########################## REPAIR SEQUENCE DEPENDING ON USER CHOICE ##########################################
actions() {
display_action_settings_start
[[ "$MAIN_MENU" = Recommended-Repair ]] && echo "
$DASH Recommended repair"
display_action_settings_end
FSFIXED=""
[[ "$FSCK_ACTION" ]] && fsck_function	#Unmount all OS partition then remounts them
if [[ "$FSFIXED" ]];then #scan again then run the Recommended Repair
	check_os_and_mount_blkid_partitions_gui
	check_which_mbr_can_be_restored
	echo_df_and_fdisk
	save_log_on_disks
	mainwindow_filling
	WIOULD=would
	debug_echo_important_variables
	_button_mainapply
else
	first_actions
	[[ "$WUBI_ACTION" ]] && wubi_function
	[[ "$MBR_ACTION" != nombraction ]] && freed_space_function	#Requires Linux partitions to be mounted
	actions_final
fi
}

########################## UNMOUNT ALL AND SUCCESS REPAIR ##########################################
unmount_all_and_success() {
unmount_all_and_success_br_and_bi
}


########################################### REPAIR WUBI ##################################################################
wubi_function() {
local i repwubok=yes
echo "SET@_label0.set_text('''$Repair_file_systems Wubi. $This_may_require_several_minutes''')"
for ((i=1;i<=QTY_WUBI;i++)); do
	echo "mount -o loop ${BLKIDMNT_POINTWUBI[$i]}/ubuntu/disks/root.disk ${MOUNTPOINTWUBI[$i]}"
	mount -o loop ${BLKIDMNT_POINTWUBI[$i]}/ubuntu/disks/root.disk "${MOUNTPOINTWUBI[$i]}" #failed mount http://ubuntuforums.org/showthread.php?t=2083353
	WUBIHOMEMOUNTED=""	
	if [[ -f "${BLKIDMNT_POINTWUBI[$i]}/ubuntu/disks/home.disk" ]] ;then
		mkdir -p "${MOUNTPOINTWUBI[$i]}/home"
		echo "mount -o loop ${BLKIDMNT_POINTWUBI[$i]}/ubuntu/disks/home.disk ${MOUNTPOINTWUBI[$i]}/home"
		mount -o loop ${BLKIDMNT_POINTWUBI[$i]}/ubuntu/disks/home.disk "${MOUNTPOINTWUBI[$i]}/home"
		WUBIHOMEMOUNTED=yes
	fi
	xdg-open "${MOUNTPOINTWUBI[$i]}/home" &
	text="$The_browser_will_access_wubi (${MOUNTPOINTWUBI[$i]}/home) $Please_backup_data_now $Then_close_this_window"
	echo "$text"
	end_pulse
	zenity --width=300 --info --title="$(eval_gettext "$CLEANNAME")" --text="$text"
	start_pulse
	pkill pcmanfm	#To avoid it automounts
	[[ "$WUBIHOMEMOUNTED" ]] && echo "umount ${MOUNTPOINTWUBI[$i]}/home" && umount "${MOUNTPOINTWUBI[$i]}/home"
	echo "umount ${MOUNTPOINTWUBI[$i]}" #if not unmounted: http://paste.ubuntu.com/1066034
	umount "${MOUNTPOINTWUBI[$i]}"	
done
#text="$This_will_try_repair_wubi $Please_backup_data $Do_you_want_to_continue"
#zenity --width=300 --question --title="$(eval_gettext "$CLEANNAME")" --text="$text" || repwubok=no
#start_pulse
#echo "$text $repwubok"
#if [[ "$repwubok" = yes ]];then
	for ((i=1;i<=QTY_WUBI;i++)); do
		echo "SET@_label0.set_text('''$Repair_file_systems Wubi$i. $This_may_require_several_minutes''')"
		if [[ -f "${BLKIDMNT_POINTWUBI[$i]}/ubuntu/disks/home.disk" ]] ;then
			echo "fsck -f -y ${BLKIDMNT_POINTWUBI[$i]}/ubuntu/disks/home.disk"
			LANGUAGE=C LC_ALL=C fsck -f -y "${BLKIDMNT_POINTWUBI[$i]}/ubuntu/disks/home.disk"
		fi
		echo "fsck -f -y ${BLKIDMNT_POINTWUBI[$i]}/ubuntu/disks/root.disk"
		LANGUAGE=C LC_ALL=C fsck -f -y "${BLKIDMNT_POINTWUBI[$i]}/ubuntu/disks/root.disk"
	done
#fi
}

########################################### REPAIR PARTITIONS (FSCK) ##################################################################
fsck_function() {
#works: http://paste.ubuntu.com/1385756 then http://paste.ubuntu.com/1387291
update_cattee
local i FUNCTION=NTFSFIX PACKAGELIST=ntfsprogs FILETOTEST=ntfsfix
force_unmount_blkid_partitions
#fsck -fyM  # repair partitions detected in the /etc/fstab except those mounted
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	echo "SET@_label0.set_text('''$Repair_file_systems ${LISTOFPARTITIONS[$i]}. $This_may_require_several_minutes''')"
	if [[ "$(echo "$BLKID" | grep ntfs | grep "${LISTOFPARTITIONS[$i]}:" )" ]];then
		[[ ! "$(type -p $FILETOTEST)" ]] && installpackagelist
		[[ "$(type -p $FILETOTEST)" ]] && echo "
ntfsfix /dev/${LISTOFPARTITIONS[$i]}" \
		&& LANGUAGE=C LC_ALL=C ntfsfix /dev/${LISTOFPARTITIONS[$i]}	#Repair NTFS partitions
	else
		echo "
fsck -fyM /dev/${LISTOFPARTITIONS[$i]}"
		LANGUAGE=C LC_ALL=C fsck -fyM /dev/${LISTOFPARTITIONS[$i]}	#Repair other partitions (except if mounted = security)
	fi
done
[[ "$(cat "$CATTEE" | grep 'FILE SYSTEM WAS MODIFIED' )" ]] && FSFIXED=yes
mount_all_blkid_partitions_except_df
}

#Called by fsck_function
force_unmount_blkid_partitions() {
local i
end_pulse
zenity --width=300 --info --title="$(eval_gettext "$CLEANNAME")" --text="$Filesystem_repair_need_unmount_parts $Please_close_all_programs $Then_close_this_window"
start_pulse
echo "Force Unmount all blkid partitions (for fsck) except / /boot /cdrom /dev /etc /home /opt /pas /proc /rofs /sys /tmp /usr /var "
pkill pcmanfm	#To avoid it automounts
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	[[ "${BLKIDMNT_POINT[$i]}" ]] \
	&& [[ "$(echo "${BLKIDMNT_POINT[$i]}" | grep -v /boot | grep -v /cdrom | grep -v /dev | grep -v /etc| grep -v /home | grep -v /opt | grep -v /pas | grep -v /proc | grep -v /rofs | grep -v /sys | grep -v /tmp | grep -v /usr | grep -v /var )" ]] \
	&& umount "${BLKIDMNT_POINT[$i]}"
done
}

########################################### FREED SPACE ACTION ##################################################################
freed_space_function() {
local i USEDPERCENT THISPARTITION temp
#Workaround for https://bugs.launchpad.net/bugs/610358
[[ "$DEBBUG" ]] && echo "[debug]Freed space function"
echo "SET@_label0.set_text('''Checking full partitions. $This_may_require_several_minutes''')"
for ((i=1;i<=TOTAL_QUANTITY_OF_OS;i++)); do
	if [[ ! "${RECOVORHID[$i]}" ]] && [[ ! "${SEPWINBOOTOS[$i]}" ]] && [[ ! "${READONLY[$i]}" ]];then
		determine_usedpercent
		if [[ "$USEDPERCENT" != [0-9][0-9] ]] && [[ "$USEDPERCENT" != [0-9] ]] && [[ "$USEDPERCENT" != 100 ]];then
			echo "Could not detect USEDPERCENT of ${OS_PARTITION[$i]} ($USEDPERCENT)."
			df /dev/${OS_PARTITION[$i]} | grep /
			echo ""
		elif [[ "$USEDPERCENT" -ge 97 ]];then
			temp="$(echo "$BLKID" | grep "${OS_PARTITION[$i]}:")"; temp=${temp#*TYPE=\"}; temp=${temp%%\"*}
			if [[ ! "${READONLY[$i]}" ]] || [[ "$temp" != ntfs ]];then #http://paste.ubuntu.com/989382
				echo "${OS_PARTITION[$i]} is $USEDPERCENT % full"
				end_pulse
				if [[ -d "${MNT_PATH[$i]}/home" ]];then
					xdg-open "${MNT_PATH[$i]}/home" &
				elif [[ -d "${MNT_PATH[$i]}/Documents and Settings" ]];then
					xdg-open "${MNT_PATH[$i]}/Documents and Settings" &
				elif [[ "${OS_PARTITION[$i]}" = "$CURRENTSESSIONPARTITION" ]];then
					xdg-open "/" &
				elif [[ "${MNT_PATH[$i]}" =~ "/mnt/boot-sav" ]];then #To avoid https://bugs.launchpad.net/ubuntu/+source/xdg-utils/+bug/821284
					xdg-open "/mnt/boot-sav" &
				else
					xdg-open "/" &
				fi
				THISPARTITION="${OS_PARTITION[$i]} \(${OS_NAME[$i]}\)" #TODO: integrate variables into mo for arabic translation
				update_translations
				zenity --width=300 --warning --title="$(eval_gettext "$CLEANNAME")" --text="$THISPARTITION_is_nearly_full $This_can_prevent_to_start_it. $Please_use_the_file_browser $Close_this_window_when_finished"
				determine_usedpercent
				if [[ "$USEDPERCENT" -ge 98 ]];then
					textt="$THISPARTITION_is_still_full $This_can_prevent_to_start_it ($Power_manager_error)."
					echo "$textt"
					zenity --width=300 --warning --title="$(eval_gettext "$CLEANNAME")" --text="$textt"
				fi
				start_pulse
			fi
		fi
	fi
done
}

determine_usedpercent() {
#care: http://paste.ubuntu.com/1053287
USEDPERCENT="$(df /dev/${OS_PARTITION[$i]} | grep / | grep % )"
USEDPERCENT=${USEDPERCENT%%\%*}; USEDPERCENT=${USEDPERCENT##* }
}


######################### STATS FOR IMPROVING BOOT-REPAIR##################
stats_diff() {
echo "SET@_label0.set_text('''$LAB (20). $This_may_require_several_minutes''')"
[[ "$DISABLEWEBCHECK" ]] && $WGETST ${TMP_FOLDER_TO_BE_CLEARED}/nock $URLST.nointernetchk.$CODO
echo "SET@_label0.set_text('''$LAB (19). $This_may_require_several_minutes''')"
[[ ! "$PASTEBIN_ACTION" ]] && $WGETST ${TMP_FOLDER_TO_BE_CLEARED}/nop $URLST.noreport.$CODO	
echo "SET@_label0.set_text('''$LAB (18). $This_may_require_several_minutes''')"
[[ "$PASTEBIN_ACTION" ]] && [[ ! "$UPLOAD" ]] && $WGETST ${TMP_FOLDER_TO_BE_CLEARED}/loc $URLST.local.$CODO	
if [[ "$MAIN_MENU" = Boot-Info ]];then
	echo "SET@_label0.set_text('''$LAB (17). $This_may_require_several_minutes''')"
	$WGETST $TMP_FOLDER_TO_BE_CLEARED/bi $URLST.bootinfo.$CODO
else
	[[ "$GRUBPACKAGE" =~ sign ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/sig $URLST.secureboot.$CODO
	echo "SET@_label0.set_text('''$LAB (16). $This_may_require_several_minutes''')"
	[[ "$MAIN_MENU" = Recommended-Repair ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/rr $URLST.recommendedrepair.$CODO
	echo "SET@_label0.set_text('''$LAB (15). $This_may_require_several_minutes''')"
	$WGETST $TMP_FOLDER_TO_BE_CLEARED/re $URLST.repair.$CODO
	[[ "$GRUBPURGE_ACTION" ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/pu $URLST.purge.$CODO
	echo "SET@_label0.set_text('''$LAB (14). $This_may_require_several_minutes''')"
	[[ "$MBR_ACTION" != reinstall ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/ma $URLST.$MBR_ACTION.$CODO
	echo "SET@_label0.set_text('''$LAB (13). $This_may_require_several_minutes''')"
	[[ "$FSCK_ACTION" ]] &&	$WGETST $TMP_FOLDER_TO_BE_CLEARED/fsck $URLST.fsck.$CODO
	echo "SET@_label0.set_text('''$LAB (12). $This_may_require_several_minutes''')"
	[[ "$UNCOMMENT_GFXMODE" ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/gf $URLST.gfx.$CODO
	echo "SET@_label0.set_text('''$LAB (11). $This_may_require_several_minutes''')"
	[[ "$ADD_KERNEL_OPTION" ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/ke $URLST.kernel.$CODO
	echo "SET@_label0.set_text('''$LAB (10). $This_may_require_several_minutes''')"
	[[ "$ATA" ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/at $URLST.ata.$CODO
	echo "SET@_label0.set_text('''$LAB (9). $This_may_require_several_minutes''')"
	[[ "$KERNEL_PURGE" ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/gf $URLST.kernelpurge.$CODO
	echo "SET@_label0.set_text('''$LAB (8). $This_may_require_several_minutes''')"
	[[ "$GRUBPACKAGE" =~ grub-efi ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/efi $URLST.efi.$CODO
	echo "SET@_label0.set_text('''$LAB (7). $This_may_require_several_minutes''')"
	if [[ "$(lsb_release -ds)" =~ Linux-Secure ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/ub $URLST.linux-secure.$CODO
	elif [[ "$(lsb_release -ds)" =~ Ubuntu-Secure ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/ub $URLST.ubuntu-secure.$CODO
	elif [[ "$(lsb_release -is)" =~ Debian ]] && [[ -f /etc/skel/.config/autostart/boot-repair.desktop ]] \
	|| [[ "$(lsb_release -ds)" =~ Boot-Repair-Disk ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/de $URLST.boot-repair-disk.$CODO
	elif [[ "$(lsb_release -is)" =~ Mint ]];then #Mint13 --> LinuxMint
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/gf $URLST.mint.$CODO
	elif [[ "$(lsb_release -ds)" =~ Hybryde ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/hy $URLST.hybryde.$CODO
	elif [[ "$(lsb_release -is)" =~ Ubuntu ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/de $URLST.ubuntu.$CODO
	elif [[ "$(lsb_release -is)" =~ Debian ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/de $URLST.debian.$CODO
	else
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/oh $URLST.otherhost.$CODO
	fi
	echo "SET@_label0.set_text('''$LAB (6). $This_may_require_several_minutes''')"
	if [[ "$QUANTITY_OF_DETECTED_LINUX" != 0 ]] && [[ "$QUANTITY_OF_DETECTED_WINDOWS" = 0 ]] && [[ "$QUANTITY_OF_DETECTED_MACOS" = 0 ]] \
	&& [[ "$QUANTITY_OF_UNKNOWN_OS" = 0 ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/lo $URLST.linuxonly.$CODO
	elif [[ "$QUANTITY_OF_DETECTED_LINUX" = 0 ]] && [[ "$QUANTITY_OF_DETECTED_WINDOWS" != 0 ]] && [[ "$QUANTITY_OF_DETECTED_MACOS" = 0 ]] \
	&& [[ "$QUANTITY_OF_UNKNOWN_OS" = 0 ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/wo $URLST.winonly.$CODO
	elif [[ "$QUANTITY_OF_DETECTED_LINUX" = 0 ]] && [[ "$QUANTITY_OF_DETECTED_WINDOWS" = 0 ]] && [[ "$QUANTITY_OF_DETECTED_MACOS" != 0 ]] \
	&& [[ "$QUANTITY_OF_UNKNOWN_OS" = 0 ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/mo $URLST.maconly.$CODO
	fi
	echo "SET@_label0.set_text('''$LAB (5). $This_may_require_several_minutes''')"
	[[ "$QUANTITY_OF_UNKNOWN_OS" != 0 ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/uo $URLST.unknownos.$CODO
	echo "SET@_label0.set_text('''$LAB (4). $This_may_require_several_minutes''')"
	if [[ "$TOTAL_QUANTITY_OF_OS" = 0 ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/0o $URLST.0os.$CODO
	elif [[ "$TOTAL_QUANTITY_OF_OS" = 1 ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/1o $URLST.1os.$CODO
	elif [[ "$TOTAL_QUANTITY_OF_OS" = 2 ]];then
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/2o $URLST.2os.$CODO
	else
		$WGETST $TMP_FOLDER_TO_BE_CLEARED/3o $URLST.3osormore.$CODO
	fi
	echo "SET@_label0.set_text('''$LAB (3). $This_may_require_several_minutes''')"
	[[ "$BLKID" =~ LVM2_member ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/lv $URLST.lvm.$CODO
	echo "SET@_label0.set_text('''$LAB (2). $This_may_require_several_minutes''')"
	[[ "$DMRAID" ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/dm $URLST.dmraid.$CODO
	[[ "$MD_ARRAY" ]] && $WGETST $TMP_FOLDER_TO_BE_CLEARED/dm $URLST.mdadm.$CODO
	echo "SET@_label0.set_text('''$LAB (1). $This_may_require_several_minutes''')"
fi
}

