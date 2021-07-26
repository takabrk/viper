#!/bin/sh
VERSIONPOINT="5.13.5"
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
       zen/v5.13.1-zen1.patch \
       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       other/0001-MultiQueue-Skiplist-Scheduler-v0.210.patch \
       other/uksm-5.13.patch \
       aufs5/aufs5-base.patch \
       aufs5/aufs5-kbuild.patch\
       aufs5/aufs5-mmap.patch \
       aufs5/aufs5-standalone.patch \
      > noir.patch
;;

pds)
cat add_noir_version.patch \
       linux/patch-$VERSIONPOINT \
       other/prjc_v5.13-r1.patch \
       custom_config.patch \
       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       LL/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
       LL/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       other/uksm-5.13.patch \
       aufs5/aufs5-base.patch \
       aufs5/aufs5-kbuild.patch\
       aufs5/aufs5-mmap.patch \
       aufs5/aufs5-standalone.patch \
       other/0001-bbr2-patches.patch \
       other/0001-cpu-patches.patch \
       other/0001-futex2-resync-from-gitlab.collabora.com.patch \
       le9db-5.13-rc2-mg-LRU-v3.patch \
      > noir.patch
;;
bmq)
cat add_noir_version.patch \
       linux/patch-$VERSIONPOINT \
       other/prjc_v5.13-r1.patch \
       custom_config.patch \
       add_noir_version.patch \
       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       LL/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
       LL/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       other/uksm-5.13.patch \
       aufs5/aufs5-base.patch \
       aufs5/aufs5-kbuild.patch\
       aufs5/aufs5-mmap.patch \
       aufs5/aufs5-standalone.patch \
       other/0001-bbr2-patches.patch \
       other/0001-cpu-patches.patch \
       other/0001-futex2-resync-from-gitlab.collabora.com.patch \
       other/use_kyber2.patch \
       ck1/ck1.patch \
       other/le9db-5.10.patch \
       other/LRU.patch \
      > noir.patch
;;
esac