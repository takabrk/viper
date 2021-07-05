#!/bin/sh
VERSIONPOINT="5.13"
NOIR_VERSION="noir"
truncate noir.patch --size 0
truncate custom_config.patch --size 0

#build custom_config.patch
diff -Naur /dev/null .config | sed 1i"diff --git a/.config b/.config\nnew file mode 100644\nindex 000000000000..dcbcaa389249" > custom_config.patch

while getopts e: OPT
do
  case $OPT in
      e) e_num=$OPTARG
         ;;
  esac
done

#build noir.patch
case $e_num in
muqss)
cat add_noir_version.patch \
       linux/patch-$VERSIONPOINT \
       custom_config.patch \
       zen/zen-sauce.patch \
       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       LL/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       other/0001-MultiQueue-Skiplist-Scheduler-v0.210.patch \
       other/uksm-5.13.patch \
       aufs5/aufs5-base.patch \
       aufs5/aufs5-kbuild.patch\
       aufs5/aufs5-mmap.patch \
       aufs5/aufs5-standalone.patch \
      > noir.patch
;;
esac

#      custom_config.patch \
#       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
#       LL/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
#       zen/zen-sauce.patch \
#       other/0001-MultiQueue-Skiplist-Scheduler-v0.210.patch \
#       other/0001-iosched-Add-i10-I-O-Scheduler.patch \
#       other/uksm-5.12.patch \
#       aufs5/aufs5-base.patch \
#       aufs5/aufs5-kbuild.patch\
#       aufs5/aufs5-mmap.patch \
#       aufs5/aufs5-standalone.patch \