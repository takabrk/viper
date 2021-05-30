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

######################################### 
blkid_fdisk_and_parted_update() {
blkid -g			#Update the UUID cache
BLKID=$(blkid)
PARTEDLM="$(LANGUAGE=C LC_ALL=C parted -lms)" #ex with null -l but -lm ok http://paste.ubuntu.com/1206434
FDISKL="$(LANGUAGE=C LC_ALL=C sudo fdisk -l)"
}

######################################### blkid partitions ###############################
check_blkid_partitions() {
NBOFPARTITIONS=0; NBOFDISKS=0; LISTOFDISKS[0]=0
#Add current session partition first
if [[ "$LIVESESSION" != live ]];then
	loop_check_blkid_partitions "a$CURRENTSESSIONPARTITION" include #Put currentsession first
fi
#Add other partitions
loop_check_blkid_partitions exclude "a$CURRENTSESSIONPARTITION"
#Add additional disks, eg sdb in http://paste.ubuntu.com/1269972
part=""
while read line;do
	disk=""
	if [[ "$(echo "$line" | grep '/dev/' | grep -iv loop | grep ':' | grep ';' )" ]];then
		disk="${a%%:*}" #eg /dev/sda
		disk="${disk#*dev/}"
		add_disk exclude b
	fi
done < <(echo "$PARTEDLM")
}

loop_check_blkid_partitions() {
local lvline line temp part disk raidset temp2
while read line; do
	if [[ "$line" =~ '/dev/' ]] && [[ "$line" =~ ':' ]];then
		temp=${line%%:*} 
		part=${temp#*dev/} 	#e.g. "sda12" or "mapper/isw_decghhaeb_Volume0p2" or "/mapper/isw_bcbggbcebj_ARRAY4" or "/dev/mapper/vg_adamant-lv_root"
		disk=""
		#echo "[debug]part : $part"	#Add "squashfs" ?   #sr1 : http://paste.ubuntu.com/996225
		if [[ "$part" ]] && [[ ! "$line" =~ /dev/loop ]] && [[ ! "$(df "/dev/$part")" =~ /cdrom ]] \
		&& [[ ! "$(df "/dev/$part")" =~ /live/ ]] && [[ ! "$line" =~ "TYPE=\"iso" ]] && [[ ! "$line" =~ "TYPE=\"udf" ]] \
		&& [[ ! "$line" =~ "Microsoft reserved partition" ]];then
			if [[ "$line" =~ LVM2_member ]];then # http://www.linux-sxs.org/storage/fedora2ubuntu.html
				[[ "$DEBBUG" ]] && echo "[debug] $part is LVM2_member"
			elif [[ "$line" =~ raid_member ]];then #http://paste.ubuntu.com/852777 , http://paste.ubuntu.com/1056793
				[[ "$DEBBUG" ]] && echo "[debug] $part is RAID_member" #http://paste.ubuntu.com/1074972 (md0 on sdb & sdc)
				determine_disk_from_part
				add_disk $1 $2
			elif [[ "$part" =~ nvme ]] && [[ ! "$(grep "p[0-9]" <<< $part )" ]];then
				disk="$part" #eg nvme0n1
				add_disk $1 $2
			elif [[ "$part" = sd[a-z] ]] || [[ "$part" = hd[a-z] ]] || [[ "$part" = sd[a-z][a-z] ]];then
				echo "$part may have broken partition table." #sda http://paste.ubuntu.com/1059957
			elif [[ "$line" =~ swap ]] || [[ "$(grep swap <<< "$line" )" ]];then
				[[ ! "$line" =~ swap ]] && echo "Swap not detected by =~. $PLEASECONTACT" #http://paste.ubuntu.com/1004461
			elif [[ "$line" =~ "dev/md/" ]];then
				echo "$part avoided" #http://paste.ubuntu.com/785087
			else
				determine_disk_from_part
				add_disk $1 $2 add_part_too
			fi
		fi
	fi
done < <(echo "$BLKID")
}

determine_disk_from_part() {
#called by loop_check_blkid_partitions and check_os_names_and_partitions_and_types
if [[ "$part" =~ mapper ]] || [[ "$(grep mapper <<< $part )" ]];then
	#e.g. "mapper/nvidia_dgicebef12" or "mapper/isw_bcbggbcebj_ARRAY3" (FakeRAID)
	[[ ! "$part" =~ mapper ]] && echo "$part not detected by =~mapper. $PLEASECONTACT"
	if [[ "$(type -p dmraid)" ]];then
		if [[ "$(dmraid -sa -c)" ]] && [[ "$(dmraid -sa -c)" != "no raid disk" ]];then
			for raidset in $(dmraid -sa -c); do #Be careful: http://paste.ubuntu.com/1042248
				echo "[dmraid -sa -c] $raidset"  #http://ubuntuforums.org/showthread.php?t=1559762&page=2
				[[ "$(grep "$raidset" <<< "$part" )" ]] && disk="mapper/$raidset"
			done
		fi
	fi
	#if [[ "$(type -p mdadm)" ]];then #This may be wrong (software raid so mdX should correspond to hardware disk)
	#	if [[ "$(mdadm --detail --scan)" ]] && [[ ! "$disk" ]];then
	#		for raidset in $(mdadm --detail --scan); do
	#			echo "[mdadm --detail --scan] $raidset"
	#			[[ "$(grep "$raidset" <<< "$part" )" ]] && disk="mapper/$raidset"
	#		done
	#	fi
	#fi
	#temp2="${part%p*}"; temp2="${temp2#mapper/*}"
	#[[ "${temp2}" ]] && [[ "$(ls /dev/mapper | grep "${temp2}" )" ]] && [[ ! "$disk" ]] \
	#&& disk="mapper/${temp2}" #eg isw_ccdei_ARRAY0
	[[ ! "$disk" ]] && set_default_disk
elif [[ "$(grep "md[0-9]" <<< $part )" ]];then #Software array
	#http://www.howtoforge.com/how-to-set-up-software-raid1-on-a-running-system-incl-grub2-configuration-ubuntu-10.04-p2
	#https://wiki.archlinux.org/index.php/Convert_a_single_drive_system_to_RAID
	#Worked with disk as sda: http://paste.ubuntu.com/785087
	#http://ubuntuforums.org/showthread.php?t=1551087
	#disk of md1 is md1, but better leaving sda: http://paste.ubuntu.com/1035388
	#be careful with md1 -> sda (http://paste.ubuntu.com/1048368)
	set_default_disk
elif [[ "$part" =~ cciss/ ]] || [[ "$part" =~ nvme ]] || [[ "$part" =~ mmcblk ]] && [[ "$(grep "p[0-9]" <<< $part )" ]];then
	disk="${part%p[0-9]*}" #nvme0n1p1, cciss/c1d1p1 -> cciss/c1d1 , https://blueprints.launchpad.net/boot-repair/+spec/check-cciss-support
elif [[ "$(grep "hd[a-z][0-9]" <<< $part )" ]] || [[ "$(grep "hd[a-z][a-z][0-9]" <<< $part )" ]] \
|| [[ "$(grep "sd[a-z][0-9]" <<< $part )" ]] || [[ "$(grep "sd[a-z][a-z][0-9]" <<< $part )" ]] && [[ $(ls /dev/${part%[0-9]*}) ]];then
	disk="${part%%[0-9]*}"		#e.g. "sda"   ##Add sr[0-9] (memcard)?
elif [[ "$line" =~ raid_member ]] && [[ $(ls /dev/$part ) ]];then
	disk="$part" #eg: http://paste.ubuntu.com/1072789
elif [[ "$(grep "p[0-9]" <<< $part )" ]] && [[ "$(ls /dev/${part%%p[0-9]*})" ]];then
	disk="${part%%p[0-9]*}" # SDcard: dev/mmcblk0p1 -> mmcblk0, also works for /dev/nvme0n1p1
else
	set_default_disk
fi
}

set_default_disk() {
#called by loop_check_blkid_partitions and determine_disk_from_part
# TODO les grep ne fonctionnent probablement plus avec PARTED et FDISK
if [[ "$(echo "$PARTEDLM" | grep /dev/sda | grep -vi error )" ]] || [[ "$(echo "$FDISKL" | grep /dev/sda )" ]];then
	disk=sda #eg paste.ubuntu.com/1045002
elif [[ "$(echo "$PARTEDLM" | grep /dev/sdb | grep -vi error )" ]] || [[ "$(echo "$FDISKL" | grep /dev/sdb )" ]];then
	disk=sdb
elif [[ "$(echo "$PARTEDLM" | grep /dev/hda | grep -vi error )" ]] || [[ "$(echo "$FDISKL" | grep /dev/hda )" ]];then
	disk=hda
elif [[ "$NBOFDISKS" != 0 ]];then
	disk="${LISTOFDISKS[1]}"
else
	disk="$part" #eg sdd -> sdd (http://paste.ubuntu.com/1049962
fi
if [[ "$part" =~ md ]] || [[ "$part" =~ mapper ]] || [[ "$line" =~ raid_member ]];then
	echo "Set $disk as corresponding disk of $part"
else
	echo "$part ($disk) has unknown type. $PLEASECONTACT"
fi
}

add_disk() {
if [[ "a${part}" = "$1" ]] || [[ "$1" = exclude ]] && [[ "a$part" != "$2" ]] && [[ "$disk" ]] && [[ ! "$(df "/dev/$disk")" =~ /cdrom ]];then
	local ADD_DISK=yes ADD_PART="$3" b
	for ((b=1;b<=NBOFDISKS;b++)); do
		[[ "${LISTOFDISKS[$b]}" = "$disk" ]] && ADD_DISK=""
	done
	if [[ "$ADD_DISK" ]] && [[ "$disk" ]];then
		(( NBOFDISKS += 1 ))
		LISTOFDISKS[$NBOFDISKS]="$disk"
		#echo "[debug]Disk $NBOFDISKS is $disk"
		mkdir -p "$LOGREP/$disk"
	fi
	for ((b=1;b<=NBOFPARTITIONS;b++)); do
		[[ "${LISTOFPARTITIONS[$b]}" = "$part" ]] && ADD_PART=""
	done
	if [[ "$ADD_PART" ]] && [[ "$part" ]];then
		if [[ ! "$part" =~ nvme ]] || [[ "$(grep "p[0-9]" <<< $part )" ]];then #blkid can contain /dev/nvme0n1 which is not partition https://forum.ubuntu-fr.org/viewtopic.php?pid=21827617#p21827617
			(( NBOFPARTITIONS += 1 ))
			LISTOFPARTITIONS[$NBOFPARTITIONS]="$part" #sda1
			DISK_PART[$NBOFPARTITIONS]="$disk" #sda
			for ((b=1;b<=NBOFDISKS;b++)); do
				[[ "${LISTOFDISKS[$b]}" = "$disk" ]] && DISKNB_PART[$NBOFPARTITIONS]="$b"
			done
			#echo "[debug]Partition $NBOFPARTITIONS is $part ($disk)"
			mkdir -p "$LOGREP/$part"
		fi
	fi
fi
}


####################### determine_part_uuid ############################
determine_part_uuid() {
local i temp
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	temp="$(echo "$BLKID" | grep "${LISTOFPARTITIONS[$i]}:")"; temp=${temp#*UUID=\"}; temp=${temp%%\"*}
	PART_UUID[$i]="$temp"		#e.g. "b3f9b3f2-a0c7-49c1-ae50-f849a02fd52e"
	[[ "$DEBBUG" ]] && echo "[debug]PART_UUID of ${LISTOFPARTITIONS[$i]} is ${PART_UUID[$i]}"
done
}

############################# CHECK BIOS Boot #######################
determine_bios_boot() {
#avoid mounting BIOS_Boot (bug #1720591)
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	BIOS_BOOT[$i]=notbiosboot
	[[ "$(echo "$FDISKL" | grep "dev/${LISTOFPARTITIONS[$i]}" | grep -i BIOS | grep -i Boot )" ]] && BIOS_BOOT[$i]=is-biosboot
	[[ "$DEBBUG" ]] && echo "[debug]BIOSBOOT of ${LISTOFPARTITIONS[$i]} is ${BIOS_BOOT[$i]}"
done
}

############################# CHECK PART WITH OS #######################
determine_part_with_os() {
local i j n
#used by check_recovery_or_hidden & check_separate_boot_partitions & check_part_types
FEDORA_DETECTED=""
NOTFEDORA_DETECTED=""
QUANTITY_OF_REAL_WINDOWS=0
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	PART_WITH_OS[$i]=no-os
	for ((j=1;j<=TOTAL_QUANTITY_OF_OS;j++)); do
		if [[ "${LISTOFPARTITIONS[$i]}" = "${OS_PARTITION[$j]}" ]];then
			PART_WITH_OS[$i]=is-os
			OSNAME[$i]="${OS_NAME[$j]}"
			[[ "${OSNAME[$i]}" =~ Fedora ]] || [[ "${OSNAME[$i]}" =~ Arch ]] && FEDORA_DETECTED=yes || NOTFEDORA_DETECTED=yes
		fi
	done
	scan_windows_parts
	if [[ "${PART_WITH_OS[$i]}" = no-os ]];then
		if [[ -d "${BLKIDMNT_POINT[$i]}/selinux" ]] || [[ -d "${BLKIDMNT_POINT[$i]}/srv" ]];then
			PART_WITH_OS[$i]=is-os
			(( QUANTITY_OF_DETECTED_LINUX += 1 ))
			OSNAME[$i]=Linux
			echo "Linux not detected by os-prober on ${LISTOFPARTITIONS[$i]}. $PLEASECONTACT"
		elif [[ "${WINXP[$i]}" ]];then
			PART_WITH_OS[$i]=is-os
			(( QUANTITY_OF_DETECTED_WINDOWS += 1 ))
			OSNAME[$i]="Windows XP"
			echo "XP not detected by os-prober on ${LISTOFPARTITIONS[$i]}. $PLEASECONTACT"
		elif [[ "${WINSE[$i]}" ]];then
			PART_WITH_OS[$i]=is-os
			(( QUANTITY_OF_DETECTED_WINDOWS += 1 ))
			OSNAME[$i]=Windows
			echo "Windows not detected by os-prober on ${LISTOFPARTITIONS[$i]}."
		fi
	fi
	[[ "$DEBBUG" ]] && echo "[debug]PART_WITH_OS of ${LISTOFPARTITIONS[$i]} : ${PART_WITH_OS[$i]}"
done
for ((n=1;n<=NBOFDISKS;n++)); do
	DISK_WITHOS[$n]=no-os
	for ((i=1;i<=NBOFPARTITIONS;i++)); do
		if [[ "${PART_WITH_OS[$i]}" = is-os ]] && [[ "${DISKNB_PART[$i]}" = "$n" ]];then
			[[ "$DEBBUG" ]] && echo "[debug]${LISTOFDISKS[$n]} contains minimum one OS"
			DISK_WITHOS[$n]=has-os
			break
		fi
	done
done
}


scan_windows_parts() {
#called by determine_part_with_os and repair_bootmgr
#Vista+
WINBCD[$i]=no-b-bcd
WINBOOT[$i]=""
if [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep -xi boot )" ]];then #may be boot or Boot
	for temp in $(ls "${BLKIDMNT_POINT[$i]}/" | grep -xi boot );do
		WINBOOT[$i]="$temp"
		if [[ "$(ls "${BLKIDMNT_POINT[$i]}/$temp/" | grep -xi bcd )" ]];then #may be bcd or BCD
			for temp2 in $(ls "${BLKIDMNT_POINT[$i]}/$temp/" | grep -xi bcd );do
				WINBCD[$i]="$temp/$temp2"
				break
			done
			break
		fi
	done
fi
[[ -f "${BLKIDMNT_POINT[$i]}/Windows/System32/winload.exe" ]] && WINL[$i]=haswinload || WINL[$i]=no-winload #ex http://paste.ubuntu.com/894852
[[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep -xi bootmgr )" ]] \
&& WINMGR[$i]="$(ls "${BLKIDMNT_POINT[$i]}/" | grep -xi bootmgr )" || WINMGR[$i]=no-bmgr
[[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep -xi grldr )" ]] \
&& WINGRL[$i]="$(ls "${BLKIDMNT_POINT[$i]}/" | grep -xi grldr )" || WINGRL[$i]=no-grldr
[[ "${WINBCD[$i]}" != no-b-bcd ]] && [[ "${WINMGR[$i]}" != no-bmgr ]] \
&& WINBOOTPART[$i]=is-winboot || WINBOOTPART[$i]=notwinboot

#xp
[[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep -xi ntldr )" ]] \
&& WINNT[$i]="$(ls "${BLKIDMNT_POINT[$i]}/" | grep -xi ntldr )" || WINNT[$i]=no-nt

#all
[[ "${WINBCD[$i]}" != no-b-bcd ]] || [[ "${WINNT[$i]}" != no-nt ]] && WINBN[$i]=bcd-or-nt || WINBN[$i]=""
[[ "${WINBCD[$i]}" != no-b-bcd ]] && [[ "${WINNT[$i]}" != no-nt ]] && WINBN[$i]=bcd-and-nt #XP upgraded to Seven http://ubuntuforums.org/showthread.php?t=2042955&page=3

WINXP[$i]=""
WINSE[$i]=""
if ( [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep -ix 'Documents and Settings' )" ]] \
&& [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep -ix 'System Volume Information' )" ]] ) \
|| [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep -ix boot.ini )" ]] \
&& [[ "${WINL[$i]}" = no-winload ]] && [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep -ix WINDOWS )" ]];then
#&& [[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep -ix 'Program Files' )" ]] http://paste.ubuntu.com/1032766
	WINXP[$i]=yes #Win2000 has no WINDOWS folder: http://paste.ubuntu.com/1073016
	(( QUANTITY_OF_REAL_WINDOWS += 1 ))
elif [[ -d "${BLKIDMNT_POINT[$i]}/Windows/System32" ]];then
	WINSE[$i]=yes
	(( QUANTITY_OF_REAL_WINDOWS += 1 ))
fi
[[ "${WINXP[$i]}" ]] || [[ "${WINSE[$i]}" ]] && REALWIN[$i]=yes || REALWIN[$i]=""
#Attention: Win7 +XP: http://paste.ubuntu.com/1062506
}


################# CHECK RECOVERY OR HIDDEN PARTS #######################
check_recovery_or_hidden() {
local i part f
for ((i=1;i<=NBOFPARTITIONS;i++)); do #ex http://paste.ubuntu.com/895327
	part="${LISTOFPARTITIONS[$i]}" #eg mapper/isw_beaibbhjji_Volume0p1
	f=""
	RECOV[$i]=no-recov-nor-hid
	while read line;do #eg 1:1049kB:21.0GB:21.0GB:ext4::;
		if [[ "$line" =~ /dev/ ]];then
			[[ "$line" =~ "/dev/${DISK_PART[$i]}:" ]] && f=ok || f=""
		fi
		[[ "$line" =~ diag ]] || [[ "$line" =~ hidden ]] && [[ "$f" ]] && [[ "${line%%:*}" = "${part##*[a-z]}" ]] \
		&& RECOV[$i]=recovery-or-hidden #Hidden ESP: paste.ubuntu.com/1306470 , ex diag: paste.ubuntu.com/9643853
	done < <(echo "$PARTEDLM")
	
	while read line;do #eg 1:1049kB:21.0GB:21.0GB:ext4::;
		if [[ "$line" =~ "${LISTOFPARTITIONS[$i]} " ]];then
			[[ "$line" =~ diag ]] || [[ "$line" =~ hidden ]] && RECOV[$i]=recovery-or-hidden
		fi
	done < <(echo "$FDISKL")
	
	[[ "$(echo "$BLKID" | grep "${LISTOFPARTITIONS[$i]} " | grep -i recovery )" ]] \
	|| [[ "$(grep -i recovery <<< "${OSNAME[$i]}" )" ]] && RECOV[$i]=recovery-or-hidden
	#ex of Vista Recovery: http://paste.ubuntu.com/1053651
	[[ "$(ls "${BLKIDMNT_POINT[$i]}/" | grep -xi bootmgr )" ]] && [[ ! -d "${BLKIDMNT_POINT[$i]}/Windows/System32" ]] \
	&& SEPWINBOOT[$i]=yes || SEPWINBOOT[$i]=""
	[[ "${SEPWINBOOT[$i]}" ]] && OSNAME[$i]="${OSNAME[$i]} (boot)"
done
for ((i=1;i<=TOTAL_QUANTITY_OF_OS;i++)); do
	for ((f=1;f<=NBOFPARTITIONS;f++)); do
		if [[ "${LISTOFPARTITIONS[$f]}" = "${OS_PARTITION[$i]}" ]];then
			[[ "${RECOV[$f]}" = recovery-or-hidden ]] && RECOVORHID[$i]=yes || RECOVORHID[$i]=""
			SEPWINBOOTOS[$i]="${SEPWINBOOT[$f]}"
			[[ "${SEPWINBOOTOS[$i]}" ]] && OS_NAME[$i]="${OS_NAME[$i]} (boot)"
		fi
	done
done
}

######################################### Check location first partition ###############################
check_location_first_partitions() {
local i partition a
for ((i=1;i<=NBOFDISKS;i++)); do
	SECTORS_BEFORE_PART[$i]=0; rm -f $TMP_FOLDER_TO_BE_CLEARED/sort
	for partition in $(ls "/sys/block/${LISTOFDISKS[$i]}/" | grep "${LISTOFDISKS[$i]}");do
		echo "$(cat "/sys/block/${LISTOFDISKS[$i]}/$partition/start" )" >> $TMP_FOLDER_TO_BE_CLEARED/sort
	done
	echo 2048 >> $TMP_FOLDER_TO_BE_CLEARED/sort # Save maximum 2048 sectors (in case the first partition is far)
	a=$(cat "$TMP_FOLDER_TO_BE_CLEARED/sort" | sort -g -r | tail -1 )  #sort the file in the increasing order
	[[ "$(grep "^[0-9]\+$" <<< $a )" ]] && SECTORS_BEFORE_PART[$i]="$a" || SECTORS_BEFORE_PART[$i]="1" # Save minimum 1 sector (the MBR)
	rm -f $TMP_FOLDER_TO_BE_CLEARED/sort
	# a=$(LANGUAGE=C LC_ALL=C fdisk -l /dev/$disk | grep "sectors of"); b=${a##*= }; c=${b% *}; 
	# echo "$c" > $TMP_FOLDER_TO_BE_CLEARED/sort   #Other way to calculate
	echo "$(stat -c %B /dev/${LISTOFDISKS[$i]})" > ${TMP_FOLDER_TO_BE_CLEARED}/sort
	echo 512 >> $TMP_FOLDER_TO_BE_CLEARED/sort # Save minimum 512 bytes/sector (in case there is a problem with stat)
	BYTES_PER_SECTOR[$i]=$(cat "$TMP_FOLDER_TO_BE_CLEARED/sort" | sort -g | tail -1 ) 
	rm -f $TMP_FOLDER_TO_BE_CLEARED/sort
	BYTES_BEFORE_PART[$i]=$((${SECTORS_BEFORE_PART[$i]}*${BYTES_PER_SECTOR[$i]}))
	[[ "$DEBBUG" ]] && echo "[debug] BYTES_BEFORE_PART[$i] (${LISTOFDISKS[$i]}) = ${SECTORS_BEFORE_PART[$i]} sectors * ${BYTES_PER_SECTOR[$i]} bytes = ${BYTES_BEFORE_PART[$i]} bytes."
done
}

######################################### Mount / Unmount functions ###############################
mount_all_blkid_partitions_except_df() {
local i j temp MOUNTCODE
[[ "$DEBBUG" ]] && echo "[debug]Mount all blkid partitions except the ones already mounted and BIOS_Boot"
MOUNTB="$(mount)"
MOUNTERROR=""
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	if [[ ! "${BIOS_BOOT[$i]}" =~ is ]];then
		if [[ "$MOUNTB" =~ "/dev/${LISTOFPARTITIONS[$i]} on" ]];then
			if [[ "${LISTOFPARTITIONS[$i]}" != "$CURRENTSESSIONPARTITION" ]];then
				[[ "$DEBBUG" ]] && echo "[debug]DF$(df /dev/${LISTOFPARTITIONS[$i]} | grep "/dev/${LISTOFPARTITIONS[$i]}" )"	#debug
				temp="$(grep "/dev/${LISTOFPARTITIONS[$i]} on" <<< "$MOUNTB" )"
				temp="${temp#*on }"
				BLKIDMNT_POINT[$i]="${temp%% type*}"
				if [[ "${BLKIDMNT_POINT[$i]}/" =~ " " ]];then
					echo "Unmount ${LISTOFPARTITIONS[$i]} from ${BLKIDMNT_POINT[$i]}/ to avoid space incompatibilities"
					umount "${BLKIDMNT_POINT[$i]}"
					MOUNTB="$(mount)"
				fi
			else
				BLKIDMNT_POINT[$i]=""
			fi
		fi
		if [[ ! "$MOUNTB" =~ "/dev/${LISTOFPARTITIONS[$i]} on" ]];then
			BLKIDMNT_POINT[$i]="/mnt/boot-sav/${LISTOFPARTITIONS[$i]}"
			mkdir -p "${BLKIDMNT_POINT[$i]}/"
			if [[ "$(echo "$BLKID" | grep btrfs | grep "${LISTOFPARTITIONS[$i]}:" )" ]];then
				mount /dev/${LISTOFPARTITIONS[$i]} "${BLKIDMNT_POINT[$i]}/"
				echo "$DASH BTRFS detected on ${LISTOFPARTITIONS[$i]}
ls:
$(ls ${BLKIDMNT_POINT[$i]})

os-prober:
$(os-prober)

"
				if [[ -d "${BLKIDMNT_POINT[$i]}/@" ]];then
					echo "Mount ${LISTOFPARTITIONS[$i]} with @ subvol"
					umount "${BLKIDMNT_POINT[$i]}"
					mount -t btrfs -o subvol=@ /dev/${LISTOFPARTITIONS[$i]} "${BLKIDMNT_POINT[$i]}/"
					OSPROBER=$(os-prober)
					echo "os-prober after @ subvol mount:
$(os-prober)"
				fi
			else
				mount /dev/${LISTOFPARTITIONS[$i]} "${BLKIDMNT_POINT[$i]}/"
			fi
			MOUNTCODE="$?"
			if [[ "$MOUNTCODE" = 14 ]];then #https://bugs.launchpad.net/ubuntu/+source/util-linux/+bug/1064928
				#http://ubuntuforums.org/showthread.php?t=2067828
				echo "mount -t ntfs-3g -o remove_hiberfile /dev/${LISTOFPARTITIONS[$i]} ${BLKIDMNT_POINT[$i]}"
				mount -t ntfs-3g -o remove_hiberfile /dev/${LISTOFPARTITIONS[$i]} "${BLKIDMNT_POINT[$i]}"
				MOUNTCODE="$?"
			fi
			if [[ "$MOUNTCODE" != 0 ]];then
				echo "mount /dev/${LISTOFPARTITIONS[$i]} : Error code $MOUNTCODE
mount -r /dev/${LISTOFPARTITIONS[$i]} ${BLKIDMNT_POINT[$i]}"
				mount -r /dev/${LISTOFPARTITIONS[$i]} "${BLKIDMNT_POINT[$i]}"
				MOUNTCODE="$?"
				if [[ "$MOUNTCODE" != 0 ]];then
					echo "mount -r /dev/${LISTOFPARTITIONS[$i]} : Error code $MOUNTCODE"
					if [[ "$(echo "$BLKID" | grep ext | grep "${LISTOFPARTITIONS[$i]}:" )" ]];then
						MOUNTERROR="$MOUNTCODE" #http://ubuntuforums.org/showthread.php?t=2068280
					fi
				fi
			fi
		fi
		[[ "$DEBBUG" ]] && echo "[debug]BLKID Mount point of ${LISTOFPARTITIONS[$i]} is: ${BLKIDMNT_POINT[$i]}"
		for ((j=1;j<=TOTAL_QUANTITY_OF_OS;j++)); do #Correspondency with OS_PARTITION
			if [[ "${LISTOFPARTITIONS[$i]}" = "${OS_PARTITION[$j]}" ]];then
				MNT_PATH[$j]="${BLKIDMNT_POINT[$i]}"
				[[ "$DEBBUG" ]] && echo "[debug]Mount path of ${OS_PARTITION[$j]} is: ${MNT_PATH[$j]}"
			fi
		done
	fi
done
update_log_path
}

#start_kill_nautilus() {
#avoid popups when mounting partitions, used in pastebinaction
#local i
#while true; do pkill nautilus; pkill caja; sleep 0.15; done &
#pid_kill_nautilus=$!
#}

#end_kill_nautilus() {
#kill ${pid_kill_nautilus}
#}

#Used by : repair, uninstaller, before, after
unmount_all_blkid_partitions_except_df() {
local i
[[ "$DEBBUG" ]] && echo "[debug]Unmount all blkid partitions except df ones"
pkill pcmanfm	#To avoid it automounts
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	[[ "$DEBBUG" ]] && echo "[debug]BLKID Mount point of ${LISTOFPARTITIONS[$i]} is: ${BLKIDMNT_POINT[$i]}"
	[[ "${BLKIDMNT_POINT[$i]}/" =~ "/mnt/boot-sav" ]] \
	&& [[ ! "$(mount | grep "${LISTOFPARTITIONS[$i]} " | grep "subvol=" | grep -v 'subvol=/)' | grep -v 'subvol=/,' )" ]] \
	&& umount "${BLKIDMNT_POINT[$i]}"
done
}


################################### SAVE / UPDATE THE LOG ON DISKS ##############################################
save_log_on_disks() {
local i
if [[ "$TOTAL_QUANTITY_OF_OS" != 0 ]];then
	TMP_LOGFOLDER="$(mktemp -td ${APPNAME}-LOG-XXXXX)"
	cp -r $LOGREP/* $TMP_LOGFOLDER
	for i in $(ls $TMP_LOGFOLDER);do
		[[ -d "$TMP_LOGFOLDER/$i" ]] &&	rm -f "$TMP_LOGFOLDER/$i/current_mbr.img" #does not save MBRs on disks
	done
fi
for ((i=1;i<=TOTAL_QUANTITY_OF_OS;i++)); do  
	if [[ "${OS_PARTITION[$i]}" != "$OS_TO_DELETE_PARTITION" ]] \
	&& [[ "${LOG_PATH[$i]}/$DATE$SECOND" != "$LOGREP" ]] \
	&& [[ ! "${RECOVORHID[$i]}" ]] && [[ ! "${SEPWINBOOTOS[$i]}" ]] && [[ ! "${READONLY[$i]}" ]]; then
		if [[ -d "${LOG_PATH[$i]}/$DATE$SECOND" ]];then
			cp -r $TMP_LOGFOLDER/* "${LOG_PATH[$i]}/$DATE$SECOND"
			[[ "$DEBBUG" ]] && echo "[debug]Logs saved into ${LOG_PATH[$i]}/$DATE$SECOND"
		fi
	fi
done
}

echo_df_and_fdisk() {
#blkid_fdisk_and_parted_update
[[ "$GUI" ]] || [[ "$1" ]] && echo "
$DASH df -Th:

$(LANGUAGE=C LC_ALL=C df -Th)

$DASH fdisk -l:
$(LANGUAGE=C LC_ALL=C fdisk -l)

"
}

echo_osprober_and_blkid() {
[[ "$GUI" ]] || [[ "$1" ]] && echo "
$DASH os-prober:
$OSPROBER

$DASH blkid:
$BLKID
"
}

########################### CHECKS THE OS NAMES AND PARTITIONS AND TYPES, AND MOUNTS THEM ##################################
check_os_names_and_partitions_and_types() {
local ligne temp part disk tempp ADDISK m i
TOTAL_QUANTITY_OF_OS=0; QUANTITY_OF_DISKS=0
QUANTITY_OF_DETECTED_LINUX=0; QUANTITY_OF_DETECTED_WINDOWS=0; QUANTITY_OF_DETECTED_MACOS=0; QUANTITY_OF_UNKNOWN_OS=0
if [[ "$OSPROBER" ]];then
	while read ligne; do
		if [[ "$ligne" =~ '/dev/' ]] && [[ "$ligne" =~ ':' ]];then
			(( TOTAL_QUANTITY_OF_OS += 1 ))
			temp=${ligne##*/dev/}
			part=${temp%%:*}
			part=${part%%@*} #/dev/sda2@/efi/Microsoft/Boot/bootmgfw.efi:Windows Boot Manager:Windows:efi , or /dev/nvme0n1p1@/efi/Microsoft/Boot/bootmgfw.efi:Windows Boot Manager:Windows:efi
			OS_PARTITION[$TOTAL_QUANTITY_OF_OS]=$part			#e.g. "sda1" or "sdc10"
			determine_disk_from_part
			OS_DISK[$TOTAL_QUANTITY_OF_OS]=$disk				#e.g. "sda" or "sdc"
			tempp=${ligne#*:}
			OS_COMPLETE_NAME[$TOTAL_QUANTITY_OF_OS]=$tempp		#e.g. "Ubuntu 10.04.1 LTS (10.04):Ubuntu:linux"
			temp=${tempp%%:*}									#e.g. "Ubuntu 10.04.1 LTS (10.04)"
			if [[ "$temp" ]];then
				OS_NAME[$TOTAL_QUANTITY_OF_OS]=${temp% *}		#e.g. "Ubuntu 10.04.1 LTS"
			else
				OS_NAME[$TOTAL_QUANTITY_OF_OS]=${tempp#*:}		#e.g. "Arch:linux"
			fi
			OS_MINI_NAME[$TOTAL_QUANTITY_OF_OS]=${OS_NAME[$TOTAL_QUANTITY_OF_OS]%% *}			#e.g. "Ubuntu"
			ADDISK=yes
			for ((m=1;m<=QUANTITY_OF_DISKS;m++)); do
				[[ "${DISK[$m]}" = "${OS_DISK[$TOTAL_QUANTITY_OF_OS]}" ]] && ADDISK=""
			done
			if [[ "$ADDISK" ]];then
				(( QUANTITY_OF_DISKS += 1 ))
				DISK[$QUANTITY_OF_DISKS]=${OS_DISK[$TOTAL_QUANTITY_OF_OS]}		#List of disks with OS  (e.g. "sdb")
			fi
		fi
	done < <(echo "$OSPROBER")

	##CHECK THE TYPE OF EACH OS
	for ((i=1;i<=TOTAL_QUANTITY_OF_OS;i++)); do
		if [[ "$(grep -i linux <<< ${OS_COMPLETE_NAME[$i]} )" ]]; then 
			(( QUANTITY_OF_DETECTED_LINUX += 1 ))
			TYPE[$i]=linux
		elif [[ "$(grep -i windows <<< ${OS_COMPLETE_NAME[$i]} )" ]];then
			(( QUANTITY_OF_DETECTED_WINDOWS += 1 ))
			TYPE[$i]=windows
		elif [[ "$(grep -i mac <<< ${OS_COMPLETE_NAME[$i]} )" ]];then
			(( QUANTITY_OF_DETECTED_MACOS += 1 ))
			TYPE[$i]=macos
		else
			(( QUANTITY_OF_UNKNOWN_OS += 1 ))
			TYPE[$i]=else
		fi
		[[ "$DEBBUG" ]] && echo "[debug]${OS_PARTITION[$i]} contains ${OS_NAME[$i]} (${TYPE[$i]})"
	done
	[[ "$GUI" ]] || [[ "$1" ]] && echo "
$QUANTITY_OF_DISKS disks with OS, $TOTAL_QUANTITY_OF_OS OS : $QUANTITY_OF_DETECTED_LINUX Linux, $QUANTITY_OF_DETECTED_MACOS MacOS, $QUANTITY_OF_DETECTED_WINDOWS Windows, $QUANTITY_OF_UNKNOWN_OS unknown type OS.
	"
fi
}


########################### CREATE LOG FOLDERS INSIDE OS ##################################
initialize_log_folders_in_os() {
local i
for ((i=1;i<=TOTAL_QUANTITY_OF_OS;i++)); do
	if [[ ! "${RECOVORHID[$i]}" ]] && [[ ! "${SEPWINBOOTOS[$i]}" ]];then
		mkdir -p "${LOG_PATH[$i]}/$DATE$SECOND"
		if [[ -d "${LOG_PATH[$i]}/$DATE$SECOND" ]];then
			READONLY[$i]=""
		else
			echo "${OS_PARTITION[$i]} is Read-only or full"
			READONLY[$i]=yes
		fi
	fi
done
}

########################### update_log_path ##################################
update_log_path() {
local i
for ((i=1;i<=TOTAL_QUANTITY_OF_OS;i++)); do
	if [[ "${TYPE[$i]}" = linux ]];then
		LOG_PATH[$i]="${MNT_PATH[$i]}$LOG_PATH_LINUX"	#Folder to store logs
	else
		LOG_PATH[$i]="${MNT_PATH[$i]}$LOG_PATH_OTHER"
	fi
done
}

######################## DETECTS THE PREVIOUS MBR BACKUPS ##################################################
check_disks_containing_mbr_backups() {
local m i loop k temp
[[ "$DEBBUG" ]] && echo "[debug]CREATES A LIST OF DISKS CONTAINING BACKUP"
QTY_OF_DISKS_WITH_BACKUP=0
for ((m=1;m<=QUANTITY_OF_DISKS;m++)); do
	QTY_OF_OS_ON_DISK[$m]=0; NB_OF_BACKUPS_IN_DISK[$m]=0
	for ((i=1;i<=TOTAL_QUANTITY_OF_OS;i++)); do
		if [[ "${OS_DISK[$i]}" = "${DISK[$m]}" ]];then
			(( QTY_OF_OS_ON_DISK[$m] += 1 ))
			OS_PARTITION_ON_DISK[${QTY_OF_OS_ON_DISK[$m]}]="${OS_PARTITION[$i]}"
			TYPE_ON_DISK[${QTY_OF_OS_ON_DISK[$m]}]="${TYPE[$i]}" 
			LOG_PATH_ON_DISK[${QTY_OF_OS_ON_DISK[$m]}]="${LOG_PATH[$i]}"
		fi
	done
	[[ "$DEBBUG" ]] && echo "[debug] Total of ${QTY_OF_OS_ON_DISK[$m]} OS detected on ${DISK[$m]} disk."
done
}


################################ PUT THE CURRENT MBRs IN TMP ##################################################
put_the_current_mbr_in_tmp() {
local i
for ((i=1;i<=NBOFDISKS;i++)); do
	if [[ ! -f $LOGREP/${LISTOFDISKS[$i]}/current_mbr.img ]]; then
		dd if=/dev/${LISTOFDISKS[$i]} of=$LOGREP/${LISTOFDISKS[$i]}/current_mbr.img bs=${BYTES_BEFORE_PART[$i]} count=1
		[[ ! -f $LOGREP/${LISTOFDISKS[$i]}/current_mbr.img ]] && echo "Warning: $LOGREP/${LISTOFDISKS[$i]}/current_mbr.img could not be created. $PLEASECONTACT"
	fi
	if [[ ! -f $LOGREP/${LISTOFDISKS[$i]}/partition_table.dmp ]] && [[ "$(type -p sfdisk)" ]]; then
		sfdisk -d /dev/${LISTOFDISKS[$i]} > $LOGREP/${LISTOFDISKS[$i]}/partition_table.dmp
		[[ "$DEBBUG" ]] && echo "[debug]$LOGREP/${LISTOFDISKS[$i]}/partition_table.dmp created"
	fi
done
}


############################# CHECKS IF TMP/MBR IS GRUB TYPE OR NOT #############################################
check_if_tmp_mbr_is_grub_type() {
if [[ -f $1 ]];then
	[[ "$(dd if=$1 bs=446 count=1 | hexdump -e \"%_p\" | grep -i GRUB )" ]] && MBRCONTAINSGRUB=true || MBRCONTAINSGRUB=false
else
	MBRCONTAINSGRUB=error; echo "Error : $1 does not exist, so we cannot check type."
fi
}

########################################### REMOVE STAGE1 FROM UNWANTED PARTITIONS #############################################
remove_stage1_from_other_os_partitions() {
[[ "$DEBBUG" ]] && echo "[debug]Remove_mislocated_stage1"
local i temp j
for ((i=1;i<=NBOFPARTITIONS;i++)); do
	if [[ -d "${BLKIDMNT_POINT[$i]}/Boot" ]] || [[ -d "${BLKIDMNT_POINT[$i]}/BOOT" ]] && [[ -d "${BLKIDMNT_POINT[$i]}/boot" ]];then
		temp=0
		for j in $(ls "${BLKIDMNT_POINT[$i]}/"); do #For fat (case insensitive)
			[[ "$j" = Boot ]] || [[ "$j" = BOOT ]] || [[ "$j" = boot ]] && (( temp += 1 ))
		done
		if [[ "$temp" != 1 ]];then
			echo "$temp /boot folders exist in ${BLKIDMNT_POINT[$i]}/ and may disturb os-prober, we rename boot into oldbooot"
			mv "${BLKIDMNT_POINT[$i]}/boot" "${BLKIDMNT_POINT[$i]}/oldbooot"
		fi
	fi
	if [[ -f "${BLKIDMNT_POINT[$i]}/boot.ini" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/ntldr" ]] \
	|| [[ -f "${BLKIDMNT_POINT[$i]}/bootmgr" ]] || [[ -f "${BLKIDMNT_POINT[$i]}/Windows/System32/winload.exe" ]] \
	&& [[ ! -d "${BLKIDMNT_POINT[$i]}/selinux" ]];then
		if [[ -d "${BLKIDMNT_POINT[$i]}/boot/grub" ]];then
			echo "GRUB detected inside Windows partition. Rename ${BLKIDMNT_POINT[$i]}/boot/grub into boot/grub_old"
			mv "${BLKIDMNT_POINT[$i]}/boot/grub" "${BLKIDMNT_POINT[$i]}/boot/grub_old"
		fi
		if [[ -d "${BLKIDMNT_POINT[$i]}/grub" ]];then
			echo "GRUB detected inside Windows partition. Rename ${BLKIDMNT_POINT[$i]}/grub into grub_old"
			mv "${BLKIDMNT_POINT[$i]}/grub" "${BLKIDMNT_POINT[$i]}/grub_old"
		fi
	elif [[ -d "${BLKIDMNT_POINT[$i]}/selinux" ]] && [[ -d "${BLKIDMNT_POINT[$i]}/grub" ]];then #eg http://paste.ubuntu.com/978825
		echo "/grub detected inside a Linux partition. Rename ${BLKIDMNT_POINT[$i]}/grub into grub_old"
		mv "${BLKIDMNT_POINT[$i]}/grub" "${BLKIDMNT_POINT[$i]}/grub_old"
	fi
done
}
