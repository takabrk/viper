#!/bin/sh
VERSIONPOINT="5.10.3"
NOIR_VERSION="noir"
truncate noir.patch --size 0
truncate custom_config.patch --size 0

#build custom_config.patch
diff -Naur /dev/null .config | sed 1i"diff --git a/.config b/.config\nnew file mode 100644\nindex 000000000000..dcbcaa389249" > custom_config.patch

#build noir.patch
cat add_noir_version.patch \
       custom_config.patch \
       linux/patch-$VERSIONPOINT \
       other/add-acs-overrides.patch \
       ck1/ck1.patch \
       other/enable_additional_cpu_optimizations_for_gcc_v11.0+_kernel_v5.10+.patch \
       UKSM/0001-UKSM-for-5.10.patch \
       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       LL/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
       LL/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       VALVE/futex-multiple-wait-v3.patch \
       other/0001-btrfs-patches.patch \
       other/0003-block-set-rq_affinity-2-for-full-multithreading-I-O.patch \
       prjc/prjc_v5.10-r1.patch \
       other/0001-iosched-Add-i10-I-O-Scheduler.patch \
       zen/zen-sauce.patch \
       zen/fixes.patch \
       other/use_i10.patch \
       IBM/introduce_per-task_latency_nice_for_scheduler_hints.patch \
       other/seccomp-Implement-syscall-isolation-based-on-memory-areas.patch \
       aufs5/aufs5-base.patch \
       aufs5/aufs5-kbuild.patch\
       aufs5/aufs5-mmap.patch \
       aufs5/aufs5-standalone.patch \
       aufs5/k510.patch \
       other/0001-init-Kconfig-set-default-value-of-SCHED_PDS.patch \
       other/0002-init-Kconfig-Restore-original-PDS-description.patch \
       other/0001-rapl-patches.patch \
       other/0001-v4l2loopback-5.10-initial-merge.patch \
       intel/optimized-avx512.patch \
       other/reiser4-for-5.10.2.patch \
       other/Improve-preemptive-ENOSPC-flushing.patch \
       other/NTFS-read-write-driver-GPL-implementation-by-Paragon-Software.patch \
       intel/0001-clearlinux-patches.patch \
       other/le9aa1-5.10.patch \
       other/zstd.patch \
       other/Enable-fp16-display-support-for-DCE8.patch \
       > noir.patch