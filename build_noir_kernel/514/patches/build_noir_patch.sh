#!/bin/sh
VERSIONPOINT="5.14"
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
       custom_config.patch \
       add_noir_version.patch \
       other/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       other/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       other/use_kyber2.patch \
       aufs5/aufs5-base.patch \
       aufs5/aufs5-kbuild.patch\
       aufs5/aufs5-mmap.patch \
       aufs5/aufs5-standalone.patch \
       other/uksm-5.13.patch \
       other/0001-zstd-patches.patch \
       other/xanmod.patch \
       other/v5.13.13-zen1.patch \
      > noir.patch
;;

pds)
cat add_noir_version.patch \
      other/use_kyber2.patch \
      other/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
      other/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
      other/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
      other/0001-UKSM-for-5.14.patch \
      other/ck1.patch \
      other/prjc_v5.14-r0.patch \
      > noir.patch
;;
esac

#       linux/patch-$VERSIONPOINT \