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

###################################### DEFAULT FILLING #########################################
set_easy_repair() {
echo 'SET@_button_recommendedrepair.set_sensitive(False)' #To avoid applying before variables are changed
set_easy_repair_diff #Differences between BR and OS-U
MAIN_MENU=Recommended-Repair
[[ "$DEBBUG" ]] && echo "[debug]MAIN_MENU becomes : $MAIN_MENU"
MBR_ACTION=nombraction
UNHIDEBOOT_ACTION=""
if [[ "$TOTAL_QUANTITY_OF_OS" != 0 ]] || [[ "$QUANTITY_OF_DETECTED_LINUX" != 0 ]] || [[ "$QUANTITY_OF_DETECTED_WINDOWS" != 0 ]] \
&& [[ "$NB_MBR_CAN_BE_RESTORED" != 0 ]] || [[ "$QTY_OF_PART_FOR_REINSTAL" != 0 ]];then
	UNHIDEBOOT_TIME=10
	UNHIDEBOOT_ACTION=unhide-bootmenu-10s; echo 'SET@_checkbutton_unhide_boot_menu.set_active(True)'
	if [[ "$QTY_OF_PART_FOR_REINSTAL" != 0 ]];then
		set_checkbutton_reinstall_grub
		echo 'SET@_checkbutton_reinstall_grub.set_active(True)' #Sometimes no consequence
	else
		echo 'SET@_checkbutton_reinstall_grub.hide()'
		if [[ "$QTY_WUBI" != 0 ]] || [[ "$WUBILDR" ]] && [[ ! "$CANBOOTWIN" ]];then
			zenity --width=300 --question --text="$Can_you_boot_windows" && CANBOOTWIN=yes || CANBOOTWIN=no
			echo "$Can_you_boot_windows $CANBOOTWIN"
		fi
		if [[ "$CANBOOTWIN" = no ]] || [[ ! "$CANBOOTWIN" ]];then
			set_checkbutton_restore_mbr
			echo 'SET@_checkbutton_restore_mbr.set_active(True)' #Sometimes no consequence
		fi
	fi
elif [[ "$NBOFPARTITIONS" != 0 ]];then #http://askubuntu.com/questions/215432/cant-boot-after-disk-error-12-10
	#Works: http://paste2.org/p/2481100
	echo "No OS or WinEFI system"
	unset_checkbutton_reinstall_grub
	unset_checkbutton_restore_mbr
	echo 'SET@_checkbutton_reinstall_grub.hide()'
	echo 'SET@_hbox_unhide.hide()'
else
	echo "Error: no partitions"
	if [[ "$APPNAME" =~ pa ]];then
		echo 'SET@_expander1.hide()'
		echo 'SET@_button_recommendedrepair.hide()'
	fi
fi
bootflag_update
if [[ "$QTY_WINBOOTTOREPAIR" = 0 ]];then
	WINBOOT_ACTION=""; echo 'SET@_vbox_winboot.set_sensitive(False)'
else
	WINBOOT_ACTION=fix-windows-boot; echo 'SET@_checkbutton_winboot.set_active(True)'
	echo 'SET@_vbox_winboot.set_sensitive(True)'
fi
echo 'SET@_button_recommendedrepair.set_sensitive(True)' #To avoid applying before variables are changed
}

set_easy_repair_diff_br_and_bi() {
if [[ "$QTY_OF_PART_FOR_REINSTAL" = 0 ]] && [[ "$NB_MBR_CAN_BE_RESTORED" = 0 ]] && [[ "$(grep BYT <<< "$PARTEDLM" )" ]] \
|| [[ "$ROOTDISKMISSING" ]] || [[ "$MOUNTERROR" ]];then
	FSCK_ACTION=repair-filesystems; echo 'SET@_checkbutton_repairfilesystems.set_active(True)'
else
	FSCK_ACTION=""; echo 'SET@_checkbutton_repairfilesystems.set_active(False)'
fi
if [[ "$QTY_WUBI" != 0 ]];then
	WUBI_ACTION=repair-wubi; echo 'SET@_checkbutton_wubi.set_active(True)'
	echo 'SET@_checkbutton_wubi.set_sensitive(True)'
else
	WUBI_ACTION=""; echo 'SET@_checkbutton_wubi.set_active(False)'
	echo 'SET@_checkbutton_wubi.set_sensitive(False)'
fi
PASTEBIN_ACTION=create-bootinfo; echo 'SET@_checkbutton_pastebin.set_active(True)'
UPLOAD=pastebin; echo 'SET@_checkbutton_upload.set_active(True)'
}	


############### Backup table and logs
_button_backup_table() {
echo 'SET@_mainwindow.hide()'
echo 'SET@_backupwindow.show()'
}

_button_cancelbackup() {
echo 'SET@_mainwindow.show()'
echo 'SET@_backupwindow.hide()'
}

_backup_filechooserwidget() {
CHOSENBACKUPREP="${@}"
[[ "$DEBBUG" ]] && echo "[debug]CHOSENBACKUPREP $CHOSENBACKUPREP"
}

_button_savebackup() {
local bsb FUNCTION=ZIP PACKAGELIST=zip FILETOTEST=zip temp temp2 FILE
echo 'SET@_backupwindow.hide()'
start_pulse
echo "SET@_label0.set_text('''$Backup_table. $Please_wait''')"
[[ "$DEBBUG" ]] && echo "[debug]_button_savebackup"
#for ((bsb=1;bsb<=TOTAL_QUANTITY_OF_OS;bsb++)); do
#	cp -rn ${LOG_PATH[$bsb]}* ${LOG_PATH_LINUX}
#done
installpackagelist
if [[ "$(type -p zip)" ]];then
	TMP_BKPFOLDER="$(mktemp -td ${APPNAME}-BKP-XXXXX)"
	cp -r "$LOG_PATH_LINUX"/* "$TMP_BKPFOLDER"
	cd "$TMP_BKPFOLDER"
	temp="backup_$DATE"
	temp2="${CHOSENBACKUPREP}/$temp"
	zip -r $temp2 *
	FILE="${temp2}.zip"
	update_translations
	end_pulse
	zenity --width=300 --info --text="$logs_have_been_saved_into_FILE"
	echo 'SET@_mainwindow.show()'
else
	end_pulse
	echo 'SET@_backupwindow.hide()'
fi
}

############### Unhide bootmenu
_spinbutton_unhide_boot_menu() {
UNHIDEBOOT_TIME="${@}"; UNHIDEBOOT_TIME="${UNHIDEBOOT_TIME%*.0}"
[[ "$DEBBUG" ]] && echo "[debug]UNHIDEBOOT_TIME becomes: $UNHIDEBOOT_TIME"
[[ "$UNHIDEBOOT_ACTION" ]] && UNHIDEBOOT_ACTION="unhide-bootmenu-${UNHIDEBOOT_TIME}s"
}

_checkbutton_unhide_boot_menu() {
if [[ "${@}" = True ]]; then
	UNHIDEBOOT_ACTION="unhide-bootmenu-${UNHIDEBOOT_TIME}s"; echo 'SET@_spinbutton_unhide_boot_menu.set_sensitive(True)'
else
	UNHIDEBOOT_ACTION=""; echo 'SET@_spinbutton_unhide_boot_menu.set_sensitive(False)'
fi
[[ "$DEBBUG" ]] && echo "[debug]UNHIDEBOOT_ACTION becomes : $UNHIDEBOOT_ACTION"
}


############## Reinstall GRUB
_checkbutton_reinstall_grub() {
if [[ "${@}" = True ]]; then
	set_checkbutton_reinstall_grub
else
	show_tab_grub_location off
	show_tab_grub_options off
	[[ "$MBR_ACTION" != restore ]] && MBR_ACTION=nombraction
	[[ "$DEBBUG" ]] && echo "[debug]MBR_ACTION becomes: $MBR_ACTION"
	update_bkp_boxes
fi
}

set_checkbutton_reinstall_grub() {
[[ "$DEBBUG" ]] && echo "[debug]set_checkbutton_reinstall_grub"
show_tab_grub_location on
show_tab_grub_options on
show_tab_mbr_options off
echo 'SET@_checkbutton_restore_mbr.set_active(False)'
MBR_ACTION=reinstall
REGRUB_PART="${LIST_OF_PART_FOR_REINSTAL[1]}"
update_bkp_boxes
osbydefault_consequences
echo 'SET@_combobox_ostoboot_bydefault.set_active(0)' #Sometimes no consequences
[[ "$DEBBUG" ]] && echo "[debug]MBR_ACTION is set : $MBR_ACTION (NBOFDISKS is $NBOFDISKS)"
}

update_bkp_boxes() {
if [[ "$BKPFILEPRESENCE" ]];then
	echo 'SET@_checkbutton_restore_bkp.show()'
	RESTORE_BKP_ACTION=restore-efi-backups
	echo 'SET@_checkbutton_restore_bkp.set_active(True)'
else
	echo 'SET@_checkbutton_restore_bkp.hide()'
	RESTORE_BKP_ACTION=""
fi
if [[ "$MBR_ACTION" = reinstall ]] && [[ "$GRUBPACKAGE" =~ grub-efi ]];then
	echo 'SET@_checkbutton_create_bkp.show()'
	echo 'SET@_checkbutton_winefi_bkp.show()'
	CREATE_BKP_ACTION=use-standard-efi-file
	echo 'SET@_checkbutton_create_bkp.set_active(True)'
	#http://ubuntuforums.org/showpost.php?p=12457638&postcount=9
	if [[ "$WINBKPFILEPRESENCE" ]];then
		#WINEFI_BKP_ACTION=rename-ms-efi &&	echo 'SET@_checkbutton_winefi_bkp.set_active(True)'
		echo 'SET@_checkbutton_winefi_bkp.show()'
	fi
else
	CREATE_BKP_ACTION=""
	WINEFI_BKP_ACTION=""
	echo 'SET@_checkbutton_create_bkp.hide()'
	echo 'SET@_checkbutton_winefi_bkp.hide()'
fi
}

unset_checkbutton_reinstall_grub() {
show_tab_grub_location off
show_tab_grub_options off
update_bkp_boxes
}


########################### Restore MBR
_checkbutton_restore_mbr() {
if [[ "${@}" = True ]]; then
	echo 'SET@_checkbutton_reinstall_grub.set_active(False)'
	unset_checkbutton_reinstall_grub
	MBR_ACTION=restore
	set_checkbutton_restore_mbr
else
	[[ "$MBR_ACTION" != reinstall ]] &&	MBR_ACTION=nombraction
	unset_checkbutton_restore_mbr
fi
bootflag_update
}

set_checkbutton_restore_mbr() {
MBR_ACTION=restore
show_tab_mbr_options on
update_bkp_boxes
echo 'SET@_combobox_restore_mbrof.set_active(0)'
MBR_TO_RESTORE="${MBR_CAN_BE_RESTORED[1]}"; combobox_restore_mbrof_consequences
[[ "$DEBBUG" ]] && echo "[debug]MBR_ACTION becomes : $MBR_ACTION"
}

unset_checkbutton_restore_mbr() {
show_tab_mbr_options off
update_bkp_boxes
}

############################### Bkp
_checkbutton_create_bkp() {
if [[ "${@}" = True ]]; then
	CREATE_BKP_ACTION=use-standard-efi-file
	[[ "$WINEFIFILEPRESENCE" ]] && echo 'SET@_checkbutton_winefi_bkp.show()' #|| WINEFI_BKP_ACTION=rename-ms-efi 
else
	CREATE_BKP_ACTION=""
	echo 'SET@_checkbutton_winefi_bkp.hide()'
	echo 'SET@_checkbutton_winefi_bkp.set_active(False)'
	WINEFI_BKP_ACTION=""
fi
}

_checkbutton_restore_bkp() {
if [[ "${@}" = True ]]; then
	RESTORE_BKP_ACTION=restore-efi-backups
else
	RESTORE_BKP_ACTION=""
fi
}

_checkbutton_winefi_bkp() {
[[ "${@}" = True ]] && WINEFI_BKP_ACTION=rename-ms-efi || WINEFI_BKP_ACTION=""
}

############### Action items ################

_button_mainquit() {
echo 'SET@_mainwindow.hide()'
WIOULD=would
[[ "$MAIN_MENU" =~ Recomm ]] && debug_echo_important_variables
echo "
$DASH Default settings
$IMPVAR"
unmount_all_partitions_and_quit_glade
}

_button_mainapply() {
if [[ "$MAIN_MENU" =~ fo ]];then
	justbootinfo_br_and_bi
else
	echo 'SET@_mainwindow.hide()'
	start_pulse
	TEXT=""
	ATEXT=""
	BTEXT=""
	LAB="$Applying_changes"
	echo "SET@_label0.set_text('''$LAB $This_may_require_several_minutes''')"
	check_internet_connection
	blockers_check
	if [[ "$BTEXT" ]];then
		echo "$BTEXT"
		end_pulse
		zenity --width=300 --error --title="$APPNAME2" --text="$BTEXT"
		unmount_all_partitions_and_quit_glade
	elif [[ "$ATEXT" ]];then
		echo "$DASH Repair blocked
	$ATEXT"
		end_pulse
		zenity --width=300 --warning --title="$APPNAME2" --text="$ATEXT"
		echo 'SET@_mainwindow.show()'
	elif [[ "$TEXT" ]];then
		echo "$DASH Advices
	$TEXT"
		end_pulse
		zenity --width=300 --question --title="$APPNAME2" --text="$TEXT" && mainapplypulsate || unmount_all_partitions_and_quit_glade
	else
		actions
	fi
fi
}

blockers_check() {
ERROR=""
#called by _button_mainapply and _button_justbootinfo
[[ "$GRUBPURGE_ACTION" ]] || [[ "$KERNEL_PURGE" ]] && [[ "$MBR_ACTION" = reinstall ]] && check_internet_connection
#Block and quit
if ( [[ "$TOTAL_QUANTITY_OF_OS" = 0 ]] && [[ "$QUANTITY_OF_DETECTED_LINUX" = 0 ]] \
&& [[ "$QUANTITY_OF_DETECTED_WINDOWS" = 0 ]] ) || [[ "$NBOFPARTITIONS" = 0 ]] \
|| ( [[ ! "$DISK_TO_RESTORE_MBR" ]] && [[ "$MBR_ACTION" = restore ]] ) \
&& [[ "$MBR_ACTION" != nombraction ]] && [[ "$(echo "$BLKID" | grep -i crypt | grep -vi swap )" ]];then
	BTEXT="$Encryption_detected $Please_decrypt ($Decrypt_links) $This_will_enable_this_feature"
elif [[ "$MBR_ACTION" = restore ]] && [[ ! "$DISK_TO_RESTORE_MBR" ]];then
	BTEXT="No disk to restore MBR. $PLEASECONTACT"
elif [[ "$GRUBPACKAGE" =~ grub-efi ]] && [[ "$MBR_ACTION" = reinstall ]] && [[ "$ARCHIPC" = 64 ]] && [[ ! -d /sys/firmware/efi ]];then
#[[ -d /usr/share/ubuntu-defaults-french ]] || [[ "$DISTRIB_DESCRIPTION" =~ Unknown ]] || [[ "$DISTRIB_DESCRIPTION" =~ Debian ]] || [[ "$(uname -m)" != x86_64 ]] && 
	DISK5="$DISK33";update_translations
	BTEXT="$Please_reboot_efi $This_will_enable_this_feature $Eg_use_DISK5_usb_efi"
elif [[ "${ARCH_OF_PART[$REGRUB_PART]}" = 64 ]] || [[ "${ARCH_OF_PART[$USRPART]}" = 64 ]] \
&& [[ "$(uname -m)" != x86_64 ]] && [[ "$MBR_ACTION" = reinstall ]];then
	FUNCTION=64bits; FUNCTION44=64bits; DISK44="$DISK33";update_translations
	BTEXT="$FUNCTION_detected $Please_use_in_a_64bits_session ($Please_use_DISK44_which_is_FUNCTION44_ok) $This_will_enable_this_feature"
elif [[ "$DISTRIB_DESCRIPTION" =~ Debian ]] || [[ "$DISTRIB_DESCRIPTION" =~ Unknown ]] && [[ "$FSCK_ACTION" ]];then
	FUNCTION=FSCK; FUNCTION44=FSCK; DISK44="$DISK33";update_translations
	BTEXT="$FUNCTION_detected $Please_use_DISK44_which_is_FUNCTION44_ok $This_will_enable_this_feature"
elif [[ "$MBR_ACTION" = reinstall ]] && [[ "$LIVESESSION" != live ]] \
&& [[ "${LISTOFPARTITIONS[$REGRUB_PART]}" != "$CURRENTSESSIONPARTITION" ]];then
	BTEXT="$Please_use_in_live_session $This_will_enable_this_feature"
fi
#Block and main window
if [[ "$MBR_ACTION" = restore ]] && [[ ! "$MBR_TO_RESTORE" =~ xp ]] || [[ "$BOOTFLAG_ACTION" ]] && [[ ! "$(type -p parted)" ]];then
	PACKAGELIST=parted; update_translations
	ATEXT="$please_install_PACKAGELIST $Then_try_again"
elif [[ "$MBR_ACTION" = restore ]] && [[ "$MBR_TO_RESTORE" =~ xp ]] && [[ ! "$(type -p install-mbr)" ]];then
	PACKAGELIST=mbr; update_translations
	ATEXT="$please_install_PACKAGELIST $Then_try_again"
#elif [[ "$GRUBPURGE_ACTION" ]] || [[ "$KERNEL_PURGE" ]] && [[ "$MBR_ACTION" = reinstall ]] && [[ "$INTERNET" = no-internet ]];then
#	OPTION="$Check_internet"; update_translations
#	ATEXT="$No_internet_connection_detected. $Please_connect_internet $Then_try_again $Alternatively_you_may_want_to_retry_after_deactivating_OPTION" 
elif [[ "$MBR_ACTION" = reinstall ]] && [[ "$GRUBPURGE_ACTION" = purge-grub ]] && [[ "${APTTYP[$USRPART]}" = nopakmgr ]];then
	ATEXT="No valid package manager in ${OSNAME[$REGRUB_PART]} (${LISTOFPARTITIONS[$USRPART]}). $PLEASECONTACT"
elif [[ "$MBR_ACTION" = reinstall ]] && [[ ! "$GRUBPACKAGE" =~ grub-efi ]] \
&& [[ "${BIOS_BOOT_DISK[${DISKNB_PART[$REGRUB_PART]}]}" = no-BIOS_boot ]] && [[ "$FORCE_GRUB" != force-in-PBR ]];then
	FUNCTION=GPT; TYP=BIOS-Boot; FLAGTYP=bios_grub; TOOL1=Gparted; TYPE3=/boot/efi; update_translations
	OPTION1="$Separate_TYPE3_partition";update_translations #ex: http://paste.ubuntu.com/894616 , http://paste.ubuntu.com/1051824
	ATEXT="$FUNCTION_detected $Please_create_TYP_part (>1MB, $No_filesystem, $FLAGTYP_flag). $Via_TOOL1 $Then_try_again"
	[[ "$NB_BISEFIPART" != 0 ]] && ATEXT="$ATEXT
$Alternatively_you_can_try_OPTION1"
	echo "(debug) $MBR_ACTION $GRUBPACKAGE $FORCE_GRUB ${BIOS_BOOT_DISK[${DISKNB_PART[$REGRUB_PART]}]} (${LISTOFPARTITIONS[$REGRUB_PART]})"
fi

#FYI
if [[ "$PARTEDLM" =~ "Error: Can't have a partition outside the disk!" ]] && [[ "$MBR_ACTION" != nombraction ]];then
	FUNCTION="Partition outside the disk"; update_translations
	echo "$FUNCTION_detected"
fi

#Ask confirmation
if [[ "$MBR_ACTION" = reinstall ]];then
	if [[ "$GRUBPURGE_ACTION" ]] || [[ "$KERNEL_PURGE" ]]  && [[ "$INTERNET" = no-internet ]];then
		TEXT="$TEXT$Continuing_without_internet_would_unbootable $Please_connect_internet
"
	fi
	if [[ "$FDISKL" =~ SFS ]];then #eg http://paste.ubuntu.com/1008500
		FUNCTION=SFS; TOOL1="TestDisk"; TOOL2="EASEUS-Partition-Master / MiniTool-Partition-Wizard"; update_translations
		TEXT="$TEXT$FUNCTION_detected $You_may_want_to_retry_after_converting_SFS $Via_TOOL1_or_TOOL2
"
	fi
	if [[ "$GRUBPACKAGE" =~ grub-efi ]];then #grub-efi ok even without GPT (see ReadEFIdos)
		if [[ ! -d /sys/firmware/efi ]];then
			MODE1=Legacy; MODE2=EFI; TYPE3=/boot/efi; update_translations; OPTION="$Separate_TYPE3_partition"; update_translations
			TEXT="$TEXT$Boot_is_MODE1_may_need_change_to_MODE2
"
			[[ ! "$WINEFIFILEPRESENCE" ]] && TEXT="$TEXT$Alternatively_you_may_want_to_retry_after_deactivating_OPTION
"
		elif [[ "${ARCH_OF_PART[$REGRUB_PART]}" = 32 ]] && [[ "${ARCH_OF_PART[$USRPART]}" = 32 ]] \
		&& [[ "$ARCHIPC" = 64 ]] && [[ "$GRUBPACKAGE" =~ grub-efi ]] && [[ "$MBR_ACTION" = reinstall ]];then
			PARTITION1="${LISTOFPARTITIONS[$REGRUB_PART]}"; update_translations
			BTEXT="$You_have_installed_on_PARTITION1_EFI_incompat_Linux $You_may_want_install_64os"
		elif [[ "$SECUREBOOT" = enabled ]] && [[ "$QUANTITY_OF_REAL_WINDOWS" != 0 ]];then
			OPTION5=SecureBoot; update_translations
			TEXT="$TEXT$Please_disable_OPTION5_in_BIOS $Then_try_again"
		elif [[ "${BIOS_BOOT_DISK[${DISKNB_PART[$REGRUB_PART]}]}" = BIOS_boot ]] && [[ ! "$EFIFILEPRESENCE" ]];then
			FUNCTION=BIOS-Boot; TYPE3=/boot/efi; update_translations; OPTION="$Separate_TYPE3_partition"; update_translations
			TEXT="$TEXT$FUNCTION_detected $You_may_want_to_retry_after_deactivating_OPTION
"
		elif [[ "$QUANTITY_OF_DETECTED_MACOS" != 0 ]] && [[ ! "$EFIFILEPRESENCE" ]];then
			FUNCTION=MacOS; TYPE3=/boot/efi; update_translations; OPTION="$Separate_TYPE3_partition"; update_translations
			TEXT="$TEXT$FUNCTION_detected $You_may_want_to_retry_after_deactivating_OPTION
"
		fi
	else
		[[ "$GRUBVER[$REGRUB_PART]" = grub ]] && TEXT="$TEXT$This_will_install_an_obsolete_bootloader (GRUB Legacy).
"
		if [[ -d /sys/firmware/efi ]] && [[ "$FORCE_GRUB" != force-in-PBR ]];then
			if [[ "$NB_EFIPARTONGPT" = 0 ]] \
			&& [[ "$QUANTITY_OF_REAL_WINDOWS" = 0 ]] && [[ "$QUANTITY_OF_DETECTED_MACOS" = 0 ]];then
				MODE1=EFI; MODE2=EFI; TYP=EFI; FLAGTYP=boot; update_translations
				TEXT="$TEXT$Boot_is_MODE1_but_no_MODE2_part_detected \
$You_may_want_to_retry_after_creating_TYP_part (FAT32, 100MB~250MB, $start_of_the_disk, $FLAGTYP_flag).
"
			fi #efi <500MB ubuntuforums.org/showthread.php?t=2021534
#			if [[ "$QUANTITY_OF_DETECTED_MACOS" = 0 ]];then # && [[ "${BIOS_BOOT_DISK[${DISKNB_PART[$REGRUB_PART]}]}" = BIOS_boot ]];then
#				#http://ubuntuforums.org/showthread.php?p=12031966#post12031966
#				MODE1=EFI; MODE2=BIOS-Legacy; update_translations
#				TEXT="$TEXT$Boot_is_MODE1_may_need_change_to_MODE2
#"
#			fi
			if [[ "$NB_EFIPARTONGPT" != 0 ]];then
				FUNCTION=EFI; TYPE3=/boot/efi; update_translations; OPTION="$Separate_TYPE3_partition"; update_translations
				TEXT="$TEXT$FUNCTION_detected $You_may_want_to_retry_after_activating_OPTION
"
			fi
		fi
	fi
fi

if [[ "$TOTAL_QUANTITY_OF_OS" != 0 ]] || [[ "$QUANTITY_OF_DETECTED_LINUX" != 0 ]] \
|| [[ "$QUANTITY_OF_DETECTED_WINDOWS" != 0 ]] && [[ "$NBOFPARTITIONS" != 0 ]] \
&& ( [[ "$DISK_TO_RESTORE_MBR" ]] || [[ "$MBR_ACTION" != restore ]] ) \
&& [[ "$MBR_ACTION" != nombraction ]] && [[ "$(echo "$BLKID" | grep -i crypt | grep -vi swap )" ]];then
	TEXT="$You_may_want_decrypt ($Decrypt_links)
" #apt-get install lvm2 cryptsetup; sudo modprobe dm-crypt; sudo cryptsetup luksOpen /dev/sda5 crypt1 ;sudo vgscan --mknodes; sudo vgscan --mknodes
#http://ubuntuforums.org/showthread.php?p=4530641
fi

[[ "$TEXT" ]] && TEXT="$TEXT$Do_you_want_to_continue"
}
	
mainapplypulsate() {
start_pulse
actions
}

_mainwindow() {
unmount_all_partitions_and_quit_glade
}

unmount_all_partitions_and_quit_glade() {
choice=exit
echo 'SET@_mainwindow.hide()'
zenity --width=300 --info --timeout=4 --title="$APPNAME2" --text="$Operation_aborted. $No_change_on_your_pc_See_you" | (echo "Operation_aborted"; save_log_on_disks ; unmount_all_blkid_partitions_except_df)
rm -r $TMP_FOLDER_TO_BE_CLEARED
echo 'EXIT@@'
}

resizemainwindow() {
sleep 0.1; echo 'SET@_mainwindow.resize(10,10)'
}

_expander1() {
local RETOUREXP=${@}
if [[ ${RETOUREXP} = True ]]; then
	MAIN_MENU=Recommended-Repair
	if [[ "$APPNAME" =~ boot- ]];then
		echo 'SET@_button_mainapply.hide()'
		echo 'SET@_hbox_bootrepairmenu.show()'
		set_easy_repair
	fi
else
	debug_echo_important_var_first
	MAIN_MENU=Custom-Repair
	if [[ "$APPNAME" =~ boot- ]];then
		echo 'SET@_hbox_bootrepairmenu.hide()'
		echo 'SET@_button_mainapply.show()'
	fi
fi
[[ "$APPNAME" =~ fo ]] && MAIN_MENU=Boot-Info
[[ "$DEBBUG" ]] && echo "[debug]MAIN_MENU becomes : $MAIN_MENU"
resizemainwindow
}

############## About
_button_thanks() {
zenity --width=300 --info --title="$APPNAME2" --text="THANKS TO EVERYBODY PARTICIPATING DIRECTLY OR INDIRECTLY TO MAKE THIS SOFTWARE A USEFUL TOOL FOR THE FOSS COMMUNITY:
testers,coders,translators,donators,everybody helping people on forums, or sharing their knowledge on forums-wiki...Babdu,Hizoka,oldfred,bcbc,AnsuzP,Josepe,mörgæs,Meierfra,Gert,arvidjaar,Adrian,GRUB-devs,drs305,srs5694 and many more"
}

_button_translate() {
xdg-open "https://translations.launchpad.net/boot-repair" &
}
