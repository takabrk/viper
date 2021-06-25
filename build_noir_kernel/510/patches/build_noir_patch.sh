#!/bin/sh
VERSIONPOINT="5.10.46"
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
       linux/patch-$VERSIONPOINT \
       ck1/ck1.patch \
       zen/zen-sauce.patch \
       ck1/0001-MultiQueue-Skiplist-Scheduler-v0.205.patch \
       ck1/muqss_Fix_build_error_on_config_leak.patch \
       UKSM/0001-UKSM-for-5.10.patch \
       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       LL/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       other/0003-block-set-rq_affinity-2-for-full-multithreading-I-O.patch \
       aufs5/aufs5-base.patch \
       aufs5/aufs5-kbuild.patch\
       aufs5/aufs5-mmap.patch \
       aufs5/aufs5-standalone.patch \
       other/zstd.patch \
       other/bbr2.patch \
       VALVE/futex-multiple-wait-v3.patch \
       other/futex2.patch \
       > noir.patch
;;
pds)
cat add_noir_version.patch \
       custom_config.patch \
       linux/patch-$VERSIONPOINT \
       ck1/ck1.patch \
       zen/zen-sauce.patch \
       prjc/prjc_v5.10-r2.patch \
       UKSM/0001-UKSM-for-5.10.patch \
       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       LL/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       other/0001-iosched-Add-i10-I-O-Scheduler.patch \
       other/0003-block-set-rq_affinity-2-for-full-multithreading-I-O.patch \
       VALVE/futex-multiple-wait-v3.patch \
       other/seccomp-Implement-syscall-isolation-based-on-memory-areas.patch \
       aufs5/aufs5-base.patch \
       aufs5/aufs5-kbuild.patch\
       aufs5/aufs5-mmap.patch \
       aufs5/aufs5-standalone.patch \
       intel/0001-clearlinux-patches.patch \
      other/0001-rapl-patches.patch \
       other/0001-v4l2loopback-5.10-initial-merge.patch \
       intel/optimized-avx512.patch \
       other/reiser4-for-5.10.2.patch \
       other/NTFS-read-write-driver-GPL-implementation-by-Paragon-Software.patch \
       other/le9aa1-5.10.patch \
       other/zstd.patch \
       other/Enable-fp16-display-support-for-DCE8.patch \
       other/bbr2.patch \
       other/futex2.patch \
       other/logitech.patch \
       other/Improve-preemptive-ENOSPC-flushing.patch \
       > noir.patch
;;
esac