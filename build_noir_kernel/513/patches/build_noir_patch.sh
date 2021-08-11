#!/bin/sh
VERSIONPOINT="5.13.9"
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
       add_noir_version.patch \
       other/use_kyber2.patch \
       other/0003-glitched-cfs.patch \
       other/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
       other/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       aufs5/aufs5-base.patch \
       aufs5/aufs5-kbuild.patch\
       aufs5/aufs5-mmap.patch \
       aufs5/aufs5-standalone.patch \
       other/0001-cpu-patches.patch \
       other/ck1.patch \
       other/0001-bbr2-patches.patch \
       other/0001-futex-resync-from-gitlab.collabora.com.patch \
       other/0001-futex2-resync-from-gitlab.collabora.com.patch \
       other/uksm-5.13.patch \
       other/le9db-5.10.patch \
       other/LRU.patch \
       other/0001-ntfs3-patches.patch \
       other/0001-zstd-patches.patch \
       other/xanmod.patch \
       other/0001-MultiQueue-Skiplist-Scheduler-v0.210.patch \
       other/muqss_fixup.patch \
      > noir.patch
;;

pds)
cat add_noir_version.patch \
       linux/patch-$VERSIONPOINT \
       custom_config.patch \
       add_noir_version.patch \
       other/use_kyber2.patch \
       other/0003-glitched-cfs.patch \
       other/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
       other/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       aufs5/aufs5-base.patch \
       aufs5/aufs5-kbuild.patch\
       aufs5/aufs5-mmap.patch \
       aufs5/aufs5-standalone.patch \
       other/0001-cpu-patches.patch \
       other/ck1.patch \
       other/0001-bbr2-patches.patch \
       other/0001-futex-resync-from-gitlab.collabora.com.patch \
       other/0001-futex2-resync-from-gitlab.collabora.com.patch \
       other/uksm-5.13.patch \
       other/le9db-5.10.patch \
       other/LRU.patch \
       other/0001-ntfs3-patches.patch \
       other/0001-zstd-patches.patch \
       other/xanmod.patch \
       other/prjc_v5.13-r2.patch \
      > noir.patch
;;
esac