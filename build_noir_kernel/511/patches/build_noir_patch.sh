#!/bin/sh
VERSIONPOINT="5.11-rc5"
NOIR_VERSION="noir"
truncate noir.patch --size 0
truncate custom_config.patch --size 0

#build custom_config.patch
diff -Naur /dev/null .config | sed 1i"diff --git a/.config b/.config\nnew file mode 100644\nindex 000000000000..dcbcaa389249" > custom_config.patch

#build noir.patch
cat add_noir_version.patch \
       custom_config.patch \
       other/add-acs-overrides.patch \
       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       LL/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
       LL/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       ck1/ck1.patch \
       other/0001-iosched-Add-i10-I-O-Scheduler.patch \
       other/enable_additional_cpu_optimizations_for_gcc_v11.0+_kernel_v5.10+.patch \
       other/gcc-O3-optimize.patch \
       VALVE/0001-futex-patches.patch \
       UKSM/0001-UKSM-for-5.11.patch \
       other/0001-v4l2loopback-patches.patch \
       intel/0001-clearlinux-patches.patch \
       other/seccomp-Implement-syscall-isolation-based-on-memory-areas.patch \
       > noir.patch