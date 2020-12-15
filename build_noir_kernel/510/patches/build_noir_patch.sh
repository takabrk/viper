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
       zen/0001-cpu-5.10-merge-graysky-s-patchset.patch \
       zen/0002-init-Kconfig-enable-O3-for-all-arches.patch \
       VALVE/futex_Implement_mechanism_to_wait_on_any_of_several_futexes.patch \
       VALVE/futex_Add_Proton_compatibility_code.patch \
       other/0001-block-patches.patch \
       other/0001-ntfs3-patches.patch \
       other/0001-zstd-dev-patches.patch \
       other/0001-btrfs-patches.patch \
       prjc/prjc_v5.10-r0.patch \
       > noir.patch