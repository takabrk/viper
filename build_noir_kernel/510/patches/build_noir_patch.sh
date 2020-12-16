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
       VALVE/futex_Implement_mechanism_to_wait_on_any_of_several_futexes.patch \
       VALVE/futex_Add_Proton_compatibility_code.patch \
       other/0001-cpu-5.10-merge-graysky-s-patchset.patch \
       other/0002-init-Kconfig-enable-O3-for-all-arches.patch \
       other/0001-ntfs3-patches.patch \
       other/0001-zstd-dev-patches.patch \
       other/0001-btrfs-patches.patch \
       other/0003-block-set-rq_affinity-2-for-full-multithreading-I-O.patch \
       prjc/prjc_v5.10-r0.patch \
       other/0001-iosched-Add-i10-I-O-Scheduler.patch \
       zen/ZEN-INTERACTIVE-Base-config-item.patch \
       zen/ZEN-INTERACTIVE-Tune-CFS-for-interactivity.patch \
       zen/ZEN-INTERACTIVE-Add-help-text-for-the-MuQSS-tweaks.patch \
       zen/ZEN-Add-CONFIG-to-rename-the-mq-deadline-scheduler.patch \
       zen/ZEN-INTERACTIVE-Increase-default-writeback-thresholds.patch \
       zen/ZEN-INTERACTIVE-Tune-ondemand-governor-for-interactivity.patch \
       zen/ZEN-INTERACTIVE-Enable-background-reclaim-of-hugepages.patch \
       zen/ZEN-Add-VHBA-driver.patch \
       zen/ZEN-Add-OpenRGB-patches.patch \
       zen/ZEN-Add-an-option-to-make-threadirqs-the-default.patch \
       other/use_kyber.patch \
       other/add-acs-overrides.patch \
       ck1/0004-Create-highres-timeout-variants-of-schedule_timeout-.patch \
       ck1/0006-Convert-msleep-to-use-hrtimers-when-active.patch \
       ck1/0014-Swap-sucks.patch \
       > noir.patch