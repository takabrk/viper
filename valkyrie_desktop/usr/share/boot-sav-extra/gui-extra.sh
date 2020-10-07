#! /bin/bash
# Copyright 2010-2017 Yann MRN
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

first_translations_extra() {
RECENTUB=artful;RECENTREP=Ubuntu-17.10   ##see also: open_sources_editor in actions-purge
#/// Please do not translate ${RECENTREP}
Warning_lastgrub=$(eval_gettext $'Warning: this will install necessary packages from ${RECENTREP} repositories.')
Use_last_grub=$(eval_gettext $'Upgrade GRUB to its most recent version')
}

lastgrub_extra() {
zenity --warning --title="$APPNAME2" --text="$Warning_lastgrub $Please_backup_data"
set_checkbutton_lastgrub
}

grub_purge_extra() {
if [[ "$LASTGRUB_ACTION" ]];then
	TMPDEP="${BLKIDMNT_POINT[$REGRUB_PART]}"
	CHECKRECUB="$(cat "$TMPDEP$slist" | grep " $RECENTUB " | grep main | grep -v '#' | grep -v extra )"
	if [[ ! "$CHECKRECUB" ]] && [[ "$DISABLE_TEMPORARY_CHANGE_THE_SOURCESLIST_OF_A_BROKEN_OS" != yes ]] \
	&& [[ -f "$TMPDEP$slist" ]];then
		echo "Install last GRUB version in $TMPDEP$slist"
		echo "deb http://archive.ubuntu.com/ubuntu/ $RECENTUB main" >> $TMPDEP$slist
		cp $TMPDEP$slist $LOGREP/sources.list_after_grubpurge #debug
		update_cattee
		aptget_update_function
	fi
fi
}

activate_hide_lastgrub_if_necessary() {
TMPDEP="${BLKIDMNT_POINT[$REGRUB_PART]}"
unset_checkbutton_lastgrub
if [[ "$(lsb_release -is)" = Ubuntu ]] || [[ "$DISTRIB_DESCRIPTION" =~ Boot-Repair-Disk ]] \
&& [[ "${APTTYP[$USRPART]}" = apt-get ]] && [[ "$DISABLE_TEMPORARY_CHANGE_THE_SOURCESLIST_OF_A_BROKEN_OS" != yes ]] \
&& [[ ! "$(cat "$TMPDEP$slist" | grep $RECENTUB | grep main | grep -v '#')" ]];then
	echo 'SET@_checkbutton_lastgrub.show()'
#	if [[ "$(cat "$TMPDEP$slist" | grep saucy | grep main | grep -v '#')" ]] \
#	|| [[ "$(cat "$TMPDEP$slist" | grep raring | grep main | grep -v '#')" ]] \
#	|| [[ "$(cat "$TMPDEP$slist" | grep quantal | grep main | grep -v '#')" ]] \
#	|| [[ "$(cat "$TMPDEP$slist" | grep precise | grep main | grep -v '#')" ]] || [[ "$GRUBPACKAGE" = grub ]];then
#		unset_checkbutton_lastgrub; echo 'SET@_checkbutton_lastgrub.set_active(False)'
#		echo 'SET@_checkbutton_lastgrub.set_sensitive(False)'
#	elif [[ "$GRUBPACKAGE" =~ efi ]];then
#		set_checkbutton_lastgrub; echo 'SET@_checkbutton_lastgrub.set_active(True)'
#		if [[ "$(cat "$TMPDEP$slist" | grep main | grep oneiric | grep -v '#')" ]] \
#		|| [[ "$(cat "$TMPDEP$slist" | grep main | grep lucid | grep -v '#')" ]];then
#			echo 'SET@_checkbutton_lastgrub.set_sensitive(False)'
#		else
#			echo 'SET@_checkbutton_lastgrub.set_sensitive(True)'
#		fi
#	else
		echo 'SET@_checkbutton_lastgrub.set_active(False)'
		echo 'SET@_checkbutton_lastgrub.set_sensitive(True)'
#	fi
else
	echo 'SET@_checkbutton_lastgrub.hide()'
fi
echo "[debug]LASTGRUB_ACTION becomes: $LASTGRUB_ACTION"
}


repair_boot_ini_nonfree() {
if [[ "$(type -p tar)" ]];then
	[[ "$file" =~ l ]] && tmp=2 || tmp=1
	tar -Jxf /usr/share/boot-sav-extra/bin$tmp -C "${BLKIDMNT_POINT[$i]}"
	echo "Fixed ${BLKIDMNT_POINT[$i]}/$file"
fi
}

installpackagelist_extra() {
if [[ "$INTERNET" = connected ]] && [[ "$MISSINGPACKAGE" ]];then
	repair_dep;	temp="$($UPDCOM)"; temp2="$($INSCOM)"; restore_dep
fi
check_missing_packages
}

################## Repair repositories
repair_dep() {
local PARTI="$1" line TEMPUV tempuniv
TMPDEP=""
if [[ "$PARTI" ]];then TMPDEP="${BLKIDMNT_POINT[$PARTI]}";fi #cant minimize
if [[ "$DISABLE_TEMPORARY_CHANGE_THE_SOURCESLIST_OF_A_BROKEN_OS" != yes ]] && [[ -f "${TMPDEP}/usr/bin/apt-get" ]];then
	echo "[debug]Repair repositories in $TMPDEP$slist"
	if [[ -f "$TMPDEP$slist" ]];then
		if [[ ! -f "${LOGREP}/sources.list$PARTI" ]];then
			mv $TMPDEP$slist $LOGREP/sources.list$PARTI #will be restored later
			if [[ -f "$LOGREP/sources.list$PARTI" ]];then #security
				#Avoids useless warnings
				while read line; do
					if [[ "$(echo "$line" | grep cdrom | grep -v '#' )" ]];then
						echo "# $line" >> $TMPDEP$slist
					else
						echo "$line" >> $TMPDEP$slist
					fi
				done < <(echo "$(< $LOGREP/sources.list$PARTI )" )
				#Allows pastebinit install on old Ubuntu versions
				#if [[ ! "$TMPDEP" ]] && [[ "$(lsb_release -is)" = Ubuntu ]] \
				#&& [[ "$PACKAGELIST" =~ pastebin ]];then
				#	UV=$(lsb_release -cs)
				#	for TEMPUV in precise;do #Pastebinit in Main since 12.10
				#		tempuniv="deb http://archive.ubuntu.com/ubuntu/ $UV universe"
				#		[[ ! "$(cat $slist | grep universe | grep -v '#' )" ]] \
				#		&& [[ "$UV" = "$TEMPUV" ]] && echo "$tempuniv" >> $slist
				#	done
				#fi
			fi
		fi
	fi
fi
}

restore_dep() {
#called by force_unmount_and_prepare_chroot & installpackagelist_extra
local PARTI="$1"
TMPDEP=""
if [[ "$PARTI" ]];then TMPDEP="${BLKIDMNT_POINT[$PARTI]}";fi #cant minimize
if [[ "$DISABLE_TEMPORARY_CHANGE_THE_SOURCESLIST_OF_A_BROKEN_OS" != yes ]] && [[ -f "${TMPDEP}/usr/bin/apt-get" ]];then
	#[[ ! -f "$LOGREP/sources_$PARTI" ]] && cp "$LOGREP/sources.list" "$PARTI $LOGREP/sources_$PARTI"
	[[ ! -f "$LOGREP/sources.list$PARTI" ]] && echo "Error: no $LOGREP/sources.list$PARTI" \
	|| mv "$LOGREP/sources.list$PARTI" "${TMPDEP}/etc/apt/sources.list"
fi
}
