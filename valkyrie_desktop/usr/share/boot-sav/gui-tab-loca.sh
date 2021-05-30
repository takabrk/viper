#! /bin/bash
# Copyright 2013 Yann MRN
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

osbydefault_consequences() {
echo 'SET@_button_mainapply.set_sensitive(False)' #To avoid applying before variables are changed
RETOURCOMBO_ostoboot_bydefault_OLD="$RETOURCOMBO_ostoboot_bydefault"
FORCE_PARTITION="${LISTOFPARTITIONS[$REGRUB_PART]}"
[[ "$DEBBUG" ]] && echo "[debug]osbydefault_consequences $FORCE_PARTITION"
combobox_separateusr_fillin
combobox_separateboot_fillin				#activates kernelpurge if necessary
combobox_efi_fillin							#activates grubpurge if necessary
combobox_place_grub_and_removable_fillin	#after separate_efi_show_hide & combobox_separateusr_fillin
[[ "${APTTYP[$USRPART]}" != nopakmgr ]] && echo 'SET@_checkbutton_purge_grub.show()' \
|| echo 'SET@_checkbutton_purge_grub.hide()'
activate_hide_lastgrub_if_necessary
[[ "$GRUBPACKAGE" =~ efi ]] && echo 'SET@_checkbutton_blankextraspace.set_sensitive(False)' \
|| echo 'SET@_checkbutton_blankextraspace.set_sensitive(True)'
BLANKEXTRA_ACTION=""; echo 'SET@_checkbutton_blankextraspace.set_active(False)'
UNCOMMENT_GFXMODE=""; echo 'SET@_checkbutton_uncomment_gfxmode.set_active(False)'
ATA=""; echo 'SET@_checkbutton_ata.set_active(False)'
unset_kerneloption; echo 'SET@_checkbutton_add_kernel_option.set_active(False)'
echo 'SET@_button_mainapply.set_sensitive(True)'
}

show_tab_grub_location() {
if [[ "$1" = on ]];then
	echo 'SET@_tab_grub_location.set_sensitive(True)'; echo 'SET@_vbox_grub_location.show()'
else
	echo 'SET@_tab_grub_location.set_sensitive(False)'; echo 'SET@_vbox_grub_location.hide()'
fi
}

######################## Separate boot ############################
_checkbutton_separateboot() {
if [[ "${@}" = True ]]; then
	USE_SEPARATEBOOTPART=use-separate-boot; BOOTPART="$BOOTPART_TO_USE"
	echo 'SET@_combobox_separateboot.set_sensitive(True)'
	activate_kernelpurge_if_necessary
	select_place_grub_in_on_or_all_mbr
else
	USE_SEPARATEBOOTPART=""; BOOTPART="$REGRUB_PART"
	echo 'SET@_combobox_separateboot.set_sensitive(False)'
	activate_kernelpurge_if_necessary
	select_place_grub_in_on_or_all_mbr
fi
[[ "$DEBBUG" ]] && echo "[debug]USE_SEPARATEBOOTPART becomes : $USE_SEPARATEBOOTPART"
}

combobox_separateboot_fillin() {
QTY_PARTWITHOUTOS=0
if [[ "$SEP_BOOT_PARTS_PRESENCE" ]];then
	local typecsbf lup csbf fichier icsf
	[[ "$DEBBUG" ]] && echo "[debug]combobox_separateboot_fillin"
	echo "COMBO@@CLEAR@@_combobox_separateboot"
	for typecsbf in is-sepboot maybesepboot;do
		for lup in 1 2 3;do #In priority sep boot located on the same disk
			for ((csbf=1;csbf<=NBOFPARTITIONS;csbf++)); do
				if ( [[ "$lup" = 1 ]] && [[ "${DISK_PART[$REGRUB_PART]}" = "${DISK_PART[$csbf]}" ]] && [[ "$csbf" = "${BOOT_OF_PART[$REGRUB_PART]}" ]] ) \
				|| ( [[ "$lup" = 2 ]] && [[ "${DISK_PART[$REGRUB_PART]}" = "${DISK_PART[$csbf]}" ]] && [[ "$csbf" != "${BOOT_OF_PART[$REGRUB_PART]}" ]] ) \
				|| ( [[ "$lup" = 3 ]] && [[ "${DISK_PART[$REGRUB_PART]}" != "${DISK_PART[$csbf]}" ]] ) \
				&& [[ "${PART_WITH_SEPARATEBOOT[$csbf]}" = "$typecsbf" ]];then
					(( QTY_PARTWITHOUTOS += 1 ))
					LIST_PARTWITHOUTOS[$QTY_PARTWITHOUTOS]="$csbf"
				fi
			done
		done
	done
	while read fichier; do echo "COMBO@@END@@_combobox_separateboot@@${fichier}";done < <( for ((icsf=1;icsf<=QTY_PARTWITHOUTOS;icsf++)); do
		echo "${LISTOFPARTITIONS[${LIST_PARTWITHOUTOS[$icsf]}]}"
	done)
	echo 'SET@_combobox_separateboot.set_active(0)'; BOOTPART_TO_USE="${LIST_PARTWITHOUTOS[1]}"
	echo 'SET@_combobox_separateboot.set_sensitive(True)' #solves glade3 bug
	echo 'SET@_combobox_separateboot.set_sensitive(False)' #solves glade3 bug
	echo 'SET@_vbox_separateboot.show()'
else
	echo 'SET@_vbox_separateboot.hide()'
fi

#http://paste.ubuntu.com/854108
if [[ "$LIVESESSION" != live ]] && [[ "${BOOT_OF_PART[$REGRUB_PART]}" ]] \
	|| [[ "${BOOTPRESENCE_OF_PART[$REGRUB_PART]}" != with-boot ]] && [[ "$QTY_BOOTPART" != 0 ]];then
	USE_SEPARATEBOOTPART=use-separate-boot; BOOTPART="$BOOTPART_TO_USE"
	echo 'SET@_checkbutton_separateboot.set_active(True)'
	echo 'SET@_combobox_separateboot.set_sensitive(True)'
else
	USE_SEPARATEBOOTPART=""; BOOTPART="$REGRUB_PART"
	echo 'SET@_checkbutton_separateboot.set_active(False)'
	echo 'SET@_combobox_separateboot.set_sensitive(False)'
fi
if [[ "$LIVESESSION" != live ]];then
	echo 'SET@_checkbutton_separateboot.set_sensitive(False)'
	echo 'SET@_combobox_separateboot.set_sensitive(False)'
fi
activate_kernelpurge_if_necessary
activate_grubpurge_if_necessary
}

_combobox_separateboot() {
local RET_sepboot="${@}" csb
[[ "$DEBBUG" ]] && echo "[debug]RET_sepboot (BOOTPART_TO_USE) : $RET_sepboot"
for ((csb=1;csb<=NBOFPARTITIONS;csb++)); do
	if [[ "$RET_sepboot" = "${LISTOFPARTITIONS[$csb]}" ]] && [[ "$USE_SEPARATEBOOTPART" ]];then
		if [[ "$LIVESESSION" = live ]];then
			BOOTPART_TO_USE="$csb"
			BOOTPART="$BOOTPART_TO_USE"
			activate_kernelpurge_if_necessary
			activate_grubpurge_if_necessary #if menu.lst
		fi
	fi
done
}

######################## Separate /usr #################################

combobox_separateusr_fillin() {
QTY_SEP_USR_PARTS=0
if [[ "$SEP_USR_PARTS_PRESENCE" ]];then
	local lup fichier icsf csbf
	[[ "$DEBBUG" ]] && echo "[debug]combobox_sepusr_fillin"
	echo "COMBO@@CLEAR@@_combobox_sepusr"
	for lup in 1 2 3;do #In priority sep usr located on the same disk
		for ((csbf=1;csbf<=NBOFPARTITIONS;csbf++)); do
			if ( [[ "$lup" = 1 ]] && [[ "${DISK_PART[$REGRUB_PART]}" = "${DISK_PART[$csbf]}" ]] && [[ "$csbf" = "${USR_OF_PART[$REGRUB_PART]}" ]] ) \
			|| ( [[ "$lup" = 2 ]] && [[ "${DISK_PART[$REGRUB_PART]}" = "${DISK_PART[$csbf]}" ]] && [[ "$csbf" != "${USR_OF_PART[$REGRUB_PART]}" ]] ) \
			|| ( [[ "$lup" = 3 ]] && [[ "${DISK_PART[$REGRUB_PART]}" != "${DISK_PART[$csbf]}" ]] ) \
			&& [[ "${SEPARATE_USR_PART[$csbf]}" = is-sep-usr ]];then
				(( QTY_SEP_USR_PARTS += 1 ))
				LIST_SEP_USR_PARTS[$QTY_SEP_USR_PARTS]="$csbf"
			fi
		done
	done
	while read fichier; do echo "COMBO@@END@@_combobox_sepusr@@${fichier}";done < <( for ((icsf=1;icsf<=QTY_SEP_USR_PARTS;icsf++)); do
		echo "${LISTOFPARTITIONS[${LIST_SEP_USR_PARTS[$icsf]}]}"
	done)
	echo 'SET@_combobox_sepusr.set_active(0)'; USRPART_TO_USE="${LIST_SEP_USR_PARTS[1]}"
	echo 'SET@_vbox_sepusr.show()'
else
	echo 'SET@_vbox_sepusr.hide()'
fi

if [[ "$LIVESESSION" != live ]] && [[ "${USR_OF_PART[$REGRUB_PART]}" ]] \
|| [[ "${USRPRESENCE_OF_PART[$REGRUB_PART]}" != with--usr ]] && [[ "$QTY_SEP_USR_PARTS" != 0 ]];then #http://paste.ubuntu.com/1080968
	USE_SEPARATEUSRPART=use-separate-usr
	USRPART="$USRPART_TO_USE"
	echo 'SET@_combobox_sepusr.set_sensitive(True)' #solves glade3 bug
	echo 'SET@_label_sepusr.set_sensitive(True)'
	echo 'SET@_checkbutton_sepusr.set_active(True)'
else
	USE_SEPARATEUSRPART=""
	USRPART="$REGRUB_PART"
	echo 'SET@_combobox_sepusr.set_sensitive(False)' #solves glade3 bug
	echo 'SET@_label_sepusr.set_sensitive(False)'
	echo 'SET@_checkbutton_sepusr.set_active(False)'
fi
if [[ "$LIVESESSION" != live ]];then
	echo 'SET@_checkbutton_sepusr.set_sensitive(False)'
	echo 'SET@_combobox_sepusr.set_sensitive(False)'
fi
}

_combobox_sepusr() {
local RETOURCOMBO_separateusr="${@}" csb
[[ "$DEBBUG" ]] && echo "[debug]RETOURCOMBO_sepusr (USRPART_TO_USE) : $RETOURCOMBO_sepusr"
for ((csb=1;csb<=NBOFPARTITIONS;csb++)); do
	[[ "$RETOURCOMBO_sepusr" = "${LISTOFPARTITIONS[$csb]}" ]] && USRPART_TO_USE="$csb"
done
[[ "$USE_SEPARATEUSRPART" ]] && USRPART="$USRPART_TO_USE" && activate_grubpurge_if_necessary
}

############################## EFI #####################################
_checkbutton_efi() {
if [[ "${@}" = True ]];then
	set_efi
else
	unset_efi
fi
[[ "$DEBBUG" ]] && echo "[debug]GRUBPACKAGE becomes: $GRUBPACKAGE"
activate_grubpurge_if_necessary
}

set_efi() {
GRUBPACKAGE=grub-efi
echo 'SET@_checkbutton_signed.show()'
#if [[ "$SECUREBOOT" = enabled ]];then 
	set_signed
	echo 'SET@_checkbutton_signed.set_active(True)'
#else #disabled or maybe enabled
#	unset_signed #works: http://ubuntuforums.org/showthread.php?t=2098914
#	echo 'SET@_checkbutton_signed.set_active(False)'
#fi
echo 'SET@_combobox_efi.set_sensitive(True)'
echo 'SET@_vbox_place_or_force.hide()'
echo 'SET@_checkbutton_legacy.hide()'
activate_hide_lastgrub_if_necessary
update_bkp_boxes
}
		
unset_efi() {
GRUBPACKAGE=grub2
echo 'SET@_checkbutton_signed.hide()'
echo 'SET@_combobox_efi.set_sensitive(False)'
echo 'SET@_vbox_place_or_force.show()'
echo 'SET@_checkbutton_legacy.show()'
activate_hide_lastgrub_if_necessary
update_bkp_boxes
}

_combobox_efi() {
local RETOURCOMBO_efi="${@}" i
[[ "$DEBBUG" ]] && echo "[debug]RETOURCOMBO_efi (EFIPART_TO_USE) : $RETOURCOMBO_efi"
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	[[ "$RETOURCOMBO_efi" = "${LISTOFPARTITIONS[$i]}" ]] && EFIPART_TO_USE="$i"
done
[[ "$DEBBUG" ]] && echo "[debug]EFIPART_TO_USE becomes : $EFIPART_TO_USE"
}

combobox_efi_fillin() {
local lup1 lup mef icef temp tempdisq fichier
[[ "$DEBBUG" ]] && echo "[debug]combobox_efi_fillin ${LISTOFPARTITIONS[$REGRUB_PART]} , ${GPTTYPE[$REGRUB_PART]}"
QTY_EFIPART=0
QTY_SUREEFIPART=0
for mef in is-correct-EFI is-maybe-EFI;do #not hidden
	for lup in 1 2 3 4 5 6;do #same disk > not live-usb > live-usb 
		for wup in 1 2;do #avoid win files
			for mmcc in 1 2;do #avoid usb and mmc
				for egpt in GPT not-GPT;do
					for ((icef=1;icef<=NBOFPARTITIONS;icef++));do
						temp=""
						tempdisq="${DISKNB_PART[$icef]}"
						if ( [[ "$wup" = 1 ]] && [[ ! "${WINEFI[$icef]}" ]] ) || ( [[ "$wup" = 2 ]] && [[ "${WINEFI[$icef]}" ]] ) && [[ ! "$OSBKP" ]] \
						&& ( ( [[ "${USBDISK[$tempdisq]}" = not-usb ]] && [[ "${MMCDISK[$tempdisq]}" = not-mmc ]] && [[ "$mmcc" = 1 ]] ) \
						|| ( [[ "${USBDISK[$tempdisq]}" != not-usb ]] || [[ "${MMCDISK[$tempdisq]}" != not-mmc ]] && [[ "$mmcc" = 2 ]] ) ) \
						&& [[ "${EFI_TYPE[$icef]}" = "$mef" ]] && [[ "${GPT_DISK[$tempdisq]}" = "$egpt" ]];then
							if [[ "$tempdisq" = "${DISKNB_PART[$REGRUB_PART]}" ]];then
								[[ "$lup" = 1 ]] && [[ "${EFI_OF_PART[$REGRUB_PART]}" ]] && temp=ok \
								&& echo "[debug] ${LISTOFPARTITIONS[$icef]} EFI part (detected by BIS and in fstab) in same disk"
								[[ "$lup" = 2 ]] && [[ ! "${EFI_OF_PART[$REGRUB_PART]}" ]] && temp=ok \
								&& echo "[debug] ${LISTOFPARTITIONS[$icef]} EFI part (detected by BIS but not in fstab) in same disk"
							elif [[ "${USBDISK[$tempdisq]}" != liveusb ]] && [[ "${MMCDISK[$tempdisq]}" != livemmc ]];then
								[[ "$lup" = 3 ]] && [[ "${EFI_OF_PART[$REGRUB_PART]}" ]] && temp=ok \
								&& echo "[debug] ${LISTOFPARTITIONS[$icef]} EFI part (detected by BIS and in fstab) in another disk"
								[[ "$lup" = 4 ]] && [[ ! "${EFI_OF_PART[$REGRUB_PART]}" ]] && temp=ok \
								&& echo "[debug] ${LISTOFPARTITIONS[$icef]} EFI part (detected by BIS but not in fstab) in another disk"
							else
								[[ "$lup" = 5 ]] && [[ "${EFI_OF_PART[$REGRUB_PART]}" ]] && temp=ok \
								&& echo "[debug] ${LISTOFPARTITIONS[$icef]} EFI part (detected by BIS and in fstab) in a live disk"
								[[ "$lup" = 6 ]] && [[ ! "${EFI_OF_PART[$REGRUB_PART]}" ]] && temp=ok \
								&& echo "[debug] ${LISTOFPARTITIONS[$icef]} EFI part (detected by BIS but not in fstab) in a live disk"
							fi
							if [[ "$temp" = ok ]];then
								(( QTY_EFIPART += 1 ))
								LIST_EFIPART[$QTY_EFIPART]="$icef"
								[[ "$mef" = is-correct-EFI ]] && [[ "$lup" != 5 ]] && [[ "$lup" != 6 ]] && (( QTY_SUREEFIPART += 1 ))
							fi
						fi
					done
				done
			done
		done
	done
done
echo "COMBO@@CLEAR@@_combobox_efi"
while read fichier; do echo "COMBO@@END@@_combobox_efi@@${fichier}";done < <( for ((icef=1;icef<=QTY_EFIPART;icef++)); do
	echo "${LISTOFPARTITIONS[${LIST_EFIPART[$icef]}]}"
done)
echo 'SET@_combobox_efi.set_active(0)'; EFIPART_TO_USE="${LIST_EFIPART[1]}"
echo 'SET@_combobox_efi.set_sensitive(True)' #solves glade3 bug
NOTEFIREASON=""
[[ "$DEBBUG" ]] && echo "[debug]EFIFILEPRESENCE $EFIFILEPRESENCE, QTY_SUREEFIPART $QTY_SUREEFIPART"
if [[ "$LIVESESSION" = live ]] || [[ -d /sys/firmware/efi ]] \
&& [[ "$QTY_SUREEFIPART" != 0 ]] && [[ "$QUANTITY_OF_REAL_WINDOWS" = 0 ]] \
|| [[ "$WINEFIFILEPRESENCE" ]] \
&& [[ "$QTY_EFIPART" != 0 ]];then #forum.ubuntu-fr.org/viewtopic.php?id=1091731
	#&& [[ "$QUANTITY_OF_DETECTED_MACOS" = 0 ]] && [[ ! "$MACEFIFILEPRESENCE" ]] bug#1250611
	#[[ "${BIOS_BOOT_DISK[${DISKNB_PART[$EFIPART_TO_USE]}]}" != BIOS_boot ]]
	#ex with no efi dmsg: http://paste.ubuntu.com/1079434
	set_efi
	echo 'SET@_checkbutton_efi.set_active(True)'
else
	unset_efi
	echo 'SET@_checkbutton_efi.set_active(False)'
	if [[ "$QTY_EFIPART" = 0 ]];then
		echo 'SET@_vbox_efi.hide()'
	else
		temp=""
		tempdisq="${DISKNB_PART[$EFIPART_TO_USE]}"
		#[[ "$QUANTITY_OF_DETECTED_MACOS" != 0 ]] || [[ "$MACEFIFILEPRESENCE" ]] && temp="mac-os $temp"
		if [[ ! "$WINEFIFILEPRESENCE" ]];then
			temp="no-win-efi $temp"
		else
			[[ "$QUANTITY_OF_REAL_WINDOWS" != 0 ]] && temp="legacy-win $temp"
			[[ "$QTY_SUREEFIPART" = 0 ]] && temp="no-sure-esp $temp"
			[[ ! -d /sys/firmware/efi ]] && temp="legacy-session $temp"
			[[ "$LIVESESSION" != live ]] && temp="not-live $temp"
		fi
		[[ "$temp" ]] && NOTEFIREASON="$temp" || NOTEFIREASON="other-reason - $PLEASECONTACT"
	fi
fi
activate_grubpurge_if_necessary
}

######################### OS to boot by default ########################
_combobox_ostoboot_bydefault() {
local cotbbd
RETOURCOMBO_ostoboot_bydefault="${@}"
[[ "$DEBBUG" ]] && echo "[debug]RETOURCOMBO_ostoboot_bydefault : ${RETOURCOMBO_ostoboot_bydefault}"
if [[ "$RETOURCOMBO_ostoboot_bydefault" = "$RETOURCOMBO_ostoboot_bydefault_OLD" ]];then
	[[ "$DEBBUG" ]] && echo "[debug]Warning: Duplicate _combobox_ostoboot_bydefault"
elif [[ "$RETOURCOMBO_ostoboot_bydefault" =~ Windows ]];then
	REGRUB_PART="${LIST_OF_PART_FOR_REINSTAL[1]}"
	CHANGEDEFAULTOS=set-windows-as-default
	osbydefault_consequences
else
	for ((cotbbd=1;cotbbd<=NBOFPARTITIONS;cotbbd++)); do 
		[[ "$DEBBUG" ]] && echo "[debug]${LABEL_PART_FOR_REINSTAL[$cotbbd]}"
		if [[ "$RETOURCOMBO_ostoboot_bydefault" =~ "${LISTOFPARTITIONS[$cotbbd]} " ]];then
			if [[ "$REGRUB_PART" = "$cotbbd" ]];then
				[[ "$DEBBUG" ]] && echo "[debug]Warning: Duplicate _combobox_ostoboot_bydefault ${LISTOFPARTITIONS[$i]}."
			elif [[ "$LIVESESSION" != live ]] && [[ "$cotbbd" != 1 ]];then
				zenity --width=300 --info --timeout=3 --title="$APPNAME2" --text="$Please_use_in_live_session $This_will_enable_this_feature"
				echo 'SET@_combobox_ostoboot_bydefault.set_active(0)'
			elif [[ "${ARCH_OF_PART[$cotbbd]}" = 64 ]] && [[ "$(uname -m)" != x86_64 ]] && [[ ! "$OSBKP" ]] && [[ "$cotbbd" != 1 ]];then
				zenity --width=300 --info --timeout=3 --title="$APPNAME2" --text="$Please_use_in_a_64bits_session $This_will_enable_this_feature"
				echo 'SET@_combobox_ostoboot_bydefault.set_active(0)'
			else
				REGRUB_PART="$cotbbd"
				CHANGEDEFAULTOS=""
				osbydefault_consequences
			fi
		fi
	done
fi
}

combobox_ostoboot_bydefault_fillin() {
local cotbdf cotbdfb fichier parttmpp
[[ "$DEBBUG" ]] && echo "[debug]combobox_ostoboot_bydefault_fillin"
QTY_OF_PART_FOR_REINSTAL=0
if [[ "$QTY_OF_PART_WITH_GRUB" != 0 ]] || [[ "$QTY_OF_PART_WITH_APTGET" != 0 ]];then
	if [[ "$(uname -m)" != x86_64 ]];then
		[[ "$DEBBUG" ]] && echo "[debug]Order Linux according to their arch type"
		loop_ostoboot_bydefault_fillin 64
		loop_ostoboot_bydefault_fillin 32
	else
		loop_ostoboot_bydefault_fillin noorder
	fi
	if [[ "$QTY_OF_PART_FOR_REINSTAL" != 0 ]];then
		if [[ "$QUANTITY_OF_DETECTED_WINDOWS" != 0 ]] && [[ ! "$(grep -i windows <<< "$OS_TO_DELETE_NAME" )" ]];then
			for ((cotbdf=1;cotbdf<=NBOFPARTITIONS;cotbdf++)); do
				if [[ "$(grep -i windows <<< "${OSNAME[$cotbdf]}" )" ]];then
					(( QTY_OF_PART_FOR_REINSTAL += 1 ))
					LIST_OF_PART_FOR_REINSTAL[$QTY_OF_PART_FOR_REINSTAL]="$cotbdf"
					LABEL_PART_FOR_REINSTAL[$QTY_OF_PART_FOR_REINSTAL]="Windows \(via ${LISTOFPARTITIONS[${LIST_OF_PART_FOR_REINSTAL[1]}]} menu\)"
					break
				fi
			done
		fi
	fi
	while read fichier; do echo "COMBO@@END@@_combobox_ostoboot_bydefault@@${fichier}";done < <( for ((cotbdf=1;cotbdf<=QTY_OF_PART_FOR_REINSTAL;cotbdf++)); do
		echo "${LABEL_PART_FOR_REINSTAL[$cotbdf]}"
	done)
	echo 'SET@_combobox_ostoboot_bydefault.set_sensitive(True)' #solves glade3 bug
fi
}


loop_ostoboot_bydefault_fillin() {
local tmparch=$1 ilobf grubtmp looop bootyp
if [[ "$LIVESESSION" != live ]];then
	for ((ilobf=1;ilobf<=NBOFPARTITIONS;ilobf++)); do
		[[ "${GRUBOK_OF_PART[$ilobf]}" ]] || [[ "${APTTYP[$ilobf]}" != nopakmgr ]] \
		|| ( [[ "${USR_IN_FSTAB_OF_PART[$ilobf]}" != part-has-no-fstab ]] && [[ "$SEP_USR_PARTS_PRESENCE" ]] ) \
		&& subloop_ostobootbydefault_fillin
	done
else
	[[ "$DEBBUG" ]] && echo "[debug]Order Linux $tmparch bits"
	for looop in 1 2 3 4;do #Reinstall, then purge, then sep /usr
		for grubtmp in grub2 grub1 nogrub;do #put GRUB2 Linux in priority	
			for bootyp in with-boot no-kernel no-boot;do
				for ((ilobf=1;ilobf<=NBOFPARTITIONS;ilobf++)); do
					if [[ "${GRUBVER[$ilobf]}" = "$grubtmp" ]] && [[ "${BOOTPRESENCE_OF_PART[$ilobf]}" = "$bootyp" ]];then
						if [[ "$looop" = 1 ]] && [[ "${GRUBOK_OF_PART[$ilobf]}" ]] && [[ "${APTTYP[$ilobf]}" != nopakmgr ]];then
							subloop_ostobootbydefault_fillin
						elif [[ "$looop" = 2 ]] && [[ "${GRUBOK_OF_PART[$ilobf]}" ]] && [[ "${APTTYP[$ilobf]}" = nopakmgr ]];then
							subloop_ostobootbydefault_fillin
						elif [[ "$looop" = 3 ]] && [[ "${APTTYP[$ilobf]}" != nopakmgr ]] \
						&& [[ ! "${GRUBOK_OF_PART[$ilobf]}" ]];then
							subloop_ostobootbydefault_fillin
						elif [[ "$looop" = 4 ]] && [[ "${APTTYP[$ilobf]}" = nopakmgr ]] \
						&& [[ ! "${GRUBOK_OF_PART[$ilobf]}" ]] && [[ "$SEP_USR_PARTS_PRESENCE" ]] \
						&& [[ "${USR_IN_FSTAB_OF_PART[$ilobf]}" != part-has-no-fstab ]];then
							subloop_ostobootbydefault_fillin	
						fi
					fi
				done
			done
		done
	done
fi
}

subloop_ostobootbydefault_fillin() {
if [[ "${LISTOFPARTITIONS[$ilobf]}" != "$OS_TO_DELETE_PARTITION" ]] && [[ "${PART_WITH_OS[$ilobf]}" = is-os ]] \
&& [[ "${ARCH_OF_PART[$ilobf]}" != "$tmparch" ]] && [[ "${ARCH_OF_PART[$ilobf]}" ]];then
	(( QTY_OF_PART_FOR_REINSTAL += 1 ))
	LIST_OF_PART_FOR_REINSTAL[$QTY_OF_PART_FOR_REINSTAL]="$ilobf"
	[[ "${OSNAME[$ilobf]}" ]] \
	&& LABEL_PART_FOR_REINSTAL[$QTY_OF_PART_FOR_REINSTAL]="${LISTOFPARTITIONS[$ilobf]} \(${OSNAME[$ilobf]}\)" \
	|| LABEL_PART_FOR_REINSTAL[$QTY_OF_PART_FOR_REINSTAL]="${LISTOFPARTITIONS[$ilobf]}"
	[[ "$DEBBUG" ]] && echo "[debug]LABEL_PART_FOR_REINSTAL[$QTY_OF_PART_FOR_REINSTAL] ${LABEL_PART_FOR_REINSTAL[$QTY_OF_PART_FOR_REINSTAL]}"
fi
}

##################### Removable disk
_checkbutton_is_removable_disk() {
[[ "${@}" = True ]] && REMOVABLEDISK=is-removable-disk || REMOVABLEDISK=""
[[ "$DEBBUG" ]] && echo "[debug]REMOVABLEDISK becomes : $REMOVABLEDISK"
}

##################### Place all disks
_radiobutton_place_alldisks() {
[[ "${@}" = True ]] && set_radiobutton_place_alldisks || echo 'SET@_vbox_is_removable_disk.hide()'
}

set_radiobutton_place_alldisks() {
local srpad
[[ "$DEBBUG" ]] && echo "[debug]set_radiobutton_place_alldisks"
FORCE_GRUB=place-in-all-MBRs
for ((srpad=1;srpad<=QTY_OF_PART_WITH_GRUB;srpad++)); do
	[[ "${DISK_PART[$REGRUB_PART]}" != "${DISK_PART[${LIST_OF_PART_WITH_GRUB[$srpad]}]}" ]] && echo 'SET@_vbox_is_removable_disk.show()'
done
}

#################### Place GRUB
_radiobutton_place_grub() {
[[ "${@}" = True ]] && set_radiobutton_place_grub || echo 'SET@_combobox_place_grub.set_sensitive(False)'
}

set_radiobutton_place_grub() {
[[ "$DEBBUG" ]] && echo "[debug]set_radiobutton_place_grub"
echo 'SET@_combobox_place_grub.set_sensitive(True)'; FORCE_GRUB=place-in-MBR
}

_combobox_place_grub() {
NOFORCE_DISK="${@}"
[[ "$DEBBUG" ]] && echo "[debug]RETOURCOMBO_place_grub (NOFORCE_DISK) : $NOFORCE_DISK"
}

combobox_place_grub_and_removable_fillin() {
local fichier cpgarf DISKA a DISK1
#Place GRUB into #########
NOFORCE_DISK="${DISK_PART[$REGRUB_PART]}"
echo "COMBO@@CLEAR@@_combobox_place_grub"
while read fichier; do
	echo "COMBO@@END@@_combobox_place_grub@@${fichier}";
done < <( echo "${NOFORCE_DISK}";
for ((cpgarf=1;cpgarf<=NBOFDISKS;cpgarf++)); do
	[[ "${LISTOFDISKS[$cpgarf]}" != "${NOFORCE_DISK}" ]] && echo "${LISTOFDISKS[$cpgarf]}" #Propose by default the disk of PART_TO_REINSTALL_GRUB
done)
echo 'SET@_combobox_place_grub.set_active(0)'

#Place GRUB in all MBR , and removable disk ####
select_place_grub_in_on_or_all_mbr

#Force GRUB into #########
FORCE_PARTITION="${LISTOFPARTITIONS[$REGRUB_PART]}"
echo "SET@_label_force_grub.set_text('''$Force_GRUB_into $FORCE_PARTITION ($for_chainloader)''')"
}

select_place_grub_in_on_or_all_mbr() {
#called by combobox_place_grub_and_removable_fillin & _checkbutton_separateboot
REMOVABLEDISK=""
SHOW_REMOVABLEDISK=no
if [[ "$QUANTITY_OF_DETECTED_MACOS" != 0 ]] || [[ "$MACEFIFILEPRESENCE" ]];then
	echo 'SET@_radiobutton_force_grub.show()'
#	if [[ "$FORCE_GRUB" != force-in-PBR ]];then
#		echo 'SET@_radiobutton_force_grub.set_active(True)'; FORCE_GRUB=force-in-PBR
#	fi
# ( [[ ! "$USE_SEPARATEBOOTPART" ]] && [[ ! "$USE_SEPARATEUSRPART" ]] ||
#RAID is broken if install GRUB in sdX
#Mac: forum.ubuntu-fr.org/viewtopic.php?id=1091731
elif [[ "/${LISTOFPARTITIONS[$REGRUB_PART]}" =~ "/md" ]] || [[ ! "${LISTOFPARTITIONS[$REGRUB_PART]}" =~ "mapper/" ]] \
&& [[ "$NBOFDISKS" != 1 ]] && [[ ! "$GRUBPACKAGE" =~ efi ]];then
	echo 'SET@_radiobutton_place_alldisks.show()'
	echo 'SET@_radiobutton_place_alldisks.set_active(True)'; set_radiobutton_place_alldisks
	DISKA="${DISK_PART[$REGRUB_PART]}"
	for ((cpgarf=1;cpgarf<=TOTAL_QUANTITY_OF_OS;cpgarf++));do
		if [[ "${OS_DISK[$cpgarf]}" != "$DISKA" ]];then
			[[ "$DEBBUG" ]] && echo "[debug]It exists another disk with OS"
			echo 'SET@_vbox_is_removable_disk.show()'
			a="$(grep "/dev/${DISKA}:" <<< "$PARTEDLM" )"; a="${a%:*}"; a="${a##*:}"
			[[ "$a" ]] && DISK5="$DISKA ($a)" || DISK5="$DISKA"
			DISK1="$DISK5"
			update_translations
			echo "SET@_label_is_removable_disk.set_text('''$DISK5_is_a_removable_disk''')"
			SHOW_REMOVABLEDISK=yes
			if [[ ! "${REMOVABLE[$DISKA]}" ]];then
				#end_pulse
				zenity --width=300 --question --text="$Is_DISK1_removable" && REMOVABLE[$DISKA]=yes \
				|| REMOVABLE[$DISKA]=no
				echo "User choice: $Is_DISK1_removable ${REMOVABLE[$DISKA]}
				
"
			fi
			if [[ "${REMOVABLE[$DISKA]}" = yes ]];then
				REMOVABLEDISK=is-removable-disk; echo 'SET@_checkbutton_is_removable_disk.set_active(True)'
			elif [[ "${REMOVABLE[$DISKA]}" = no ]];then
				REMOVABLEDISK=""; echo 'SET@_checkbutton_is_removable_disk.set_active(False)'
			else
				echo "Error: REMOVABLE is empty. $PLEASECONTACT"
				zenity --width=300 --error --text="Error: REMOVABLE is empty. $PLEASECONTACT"
			fi			
			break
		fi
	done
else
	echo 'SET@_radiobutton_place_grub.set_active(True)'; set_radiobutton_place_grub
fi
}

######################## Force GRUB
_radiobutton_force_grub() {
[[ "${@}" = True ]] && FORCE_GRUB=force-in-PBR
[[ "$DEBBUG" ]] && echo "[debug]FORCE_GRUB becomes : $FORCE_GRUB"
}
