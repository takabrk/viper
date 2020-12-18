#!/bin/sh
VERSIONPOINT="5.10.1"
NOIR_VERSION="noir"
truncate noir.patch --size 0
truncate custom_config.patch --size 0

#build custom_config.patch
diff -Naur /dev/null .config | sed 1i"diff --git a/.config b/.config\nnew file mode 100644\nindex 000000000000..dcbcaa389249" > custom_config.patch

#build noir.patch
cat add_noir_version.patch \
       custom_config.patch \
       intel/0001-clearlinux-patches.patch \
       linux/patch-$VERSIONPOINT \
       UKSM/0001-UKSM-for-5.10.patch \
       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       LL/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
       LL/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       VALVE/futex-multiple-wait-v3.patch \
       other/0001-ntfs3-patches.patch \
       other/0001-zstd-dev-patches.patch \
       other/0001-btrfs-patches.patch \
       other/0003-block-set-rq_affinity-2-for-full-multithreading-I-O.patch \
       prjc/prjc_v5.10-r0.patch \
       other/0001-iosched-Add-i10-I-O-Scheduler.patch \
       zen/zen-sauce.patch \
       zen/fixes.patch \
       other/use_kyber.patch \
       other/add-acs-overrides.patch \
       ck1/0004-Create-highres-timeout-variants-of-schedule_timeout-.patch \
       ck1/0006-Convert-msleep-to-use-hrtimers-when-active.patch \
       ck1/0014-Swap-sucks.patch \
       IBM/introduce_per-task_latency_nice_for_scheduler_hints.patch \
       > noir.patch