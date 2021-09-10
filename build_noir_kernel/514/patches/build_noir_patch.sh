#!/bin/sh
VERSIONPOINT="5.14.2"
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
pds)
cat add_noir_version.patch \
      other/use_kyber2.patch \
      other/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
      other/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
      other/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
      other/0001-UKSM-for-5.14.patch \
      other/ck1.patch \
      other/prjc_v5.14-r0.patch \
      other/0001-bbr2-5.14-introduce-BBRv2.patch \
      other/0001-cpu-patches.patch \
      other/0001-ntfs3-patches.patch \
      other/0001-zstd-patches.patch \
      > noir.patch
;;

cacule)
cat add_noir_version.patch \
      linux/patch-$VERSIONPOINT \
      other/use_kyber2.patch \
      other/cacule-5.14-full.patch \
      other/0001-cpu-patches.patch \
      other/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
      other/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
      other/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
      other/ck1.patch \
      other/0001-UKSM-for-5.14.patch \
      other/0001-bbr2-5.14-introduce-BBRv2.patch \
      other/0001-ntfs3-patches.patch \
      other/0001-zstd-patches.patch \
      other/le9ec-5.14.patch \
      other/0001-aufs-20210906.patch \
      other/0001-clearlinux-patches.patch \
      other/0001-futex2-resync-from-gitlab.collabora.com.patch \
      other/0007-v5.14-winesync.patch \
      other/acso.patch \
      other/OpenRGB.patch \
      other/VHBA.patch \
      other/0006-x86-ACPI-State-Optimize-C3-entry-on-AMD-CPUs.patch \
      other/0001-v4l2loopback-5.14-merge-v0.12.5.patch \
      other/0001-zen-Allow-MSR-writes-by-default.patch \
      other/0002-PCI-Add-Intel-remapped-NVMe-device-support.patch \
      other/0001-bcachefs-5.14-introduce-bcachefs-patchset.patch \
      other/0001-sched-autogroup-Add-kernel-parameter-and-config-opti.patch \
      other/0001-spadfs-5.13-merge-v1.0.14.patch \
      other/0003-block-set-rq_affinity-2-for-full-multithreading-I-O.patch \
      other/prjc_v5.14-r1.patch \
      other/slub_preempt_rt.patch \
      other/locking_core_preempt_rt.patch \
      > noir.patch
;;

esac
