#!/bin/sh
#custom linux kernel build script
#Created by takamitsu hamada
#2020/10/8

while getopts e: OPT
do
  case $OPT in
      e) e_num=$OPTARG
         ;;\
  esac
done
VERSIONBASE="5.8"
VERSIONPOINT="5.8.14"
MUQSSPATCH="0001-MultiQueue-Skiplist-Scheduler-v0.202.patch"
BMQPATCH="prjc_v5.8-r3"
PREEMPT_RT="patch-5.9-rc2-rt1"
#THREADS ="4"
case $e_num in
    base)
           wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-$VERSIONBASE.tar.xz
           tar -Jxvf linux-$VERSIONBASE.tar.xz
           cd linux-$VERSIONBASE
           cp -a ../REPORTING-BUGS ./
           #cp -a ../aufs5-standalone-aufs5.x-rcN/Documentation ./
           #cp -a ../aufs5-standalone-aufs5.x-rcN/fs ./
           #cp -a ../aufs5-standalone-aufs5.x-rcN/include ./
           #patch -p1 < ../aufs5-standalone-aufs5.x-rcN/aufs5-base.patch
           #patch -p1 < ../aufs5-standalone-aufs5.x-rcN/aufs5-kbuild.patch
           #patch -p1 < ../aufs5-standalone-aufs5.x-rcN/aufs5-mmap.patch
           #patch -p1 < ../aufs5-standalone-aufs5.x-rcN/aufs5-standalone.patch
           patch -p1 < ../other/zstd.patch
           patch -p1 < ../uksm/uksm-5.8.patch
           patch -p1 < ../other/enable_additional_cpu_optimizations_for_gcc_v9.1+_kernel_v5.8+.patch
           #patch -p1 < ../other/Add_PVL_branding.patch
           patch -p1 < ../other/FSGSBASE.patch
           patch -p1 < ../other/add-acs-overrides.patch
           patch -p1 < ../other/introduce_per-task_latency_nice_for_scheduler_hints.patch
           patch -p1 < ../other/LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch
           patch -p1 < ../other/LL/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch
           patch -p1 < ../other/LL/0004-mm-set-2048-for-address_space-level-file-read-ahead-.patch
           patch -p1 < ../ck1/0002-Make-preemptible-kernel-default.patch
           patch -p1 <../ck1/0004-Create-highres-timeout-variants-of-schedule_timeout-.patch
           parch -p1 < ../ck1/0005-Special-case-calls-of-schedule_timeout-1-to-use-the-.patch
           patch -p1 < ../ck1/0006-Convert-msleep-to-use-hrtimers-when-active.patch
           patch -p1 < ../ck1/0014-Swap-sucks.patch
           patch -p1 < ../other/o3.patch
           rm -r ../linux-$VERSIONBASE.tar.xz
           patch -p1 < ../linux/patch-$VERSIONPOINT
           patch -p1 < ../other/zen/Base_config_item.patch
           #patch -p1 < ../other/zen/Tune_ondemand_governor_for_interactivity.patch
           #patch -p1 < ../other/zen/Increase_max_number_of_tasks_rebalanced_at_once.patch
           patch -p1 < ../other/zen/Increase_default_writeback_thresholds.patch
           patch -p1 < ../other/zen/Enable_background_reclaim_of_hugepages.patch
           patch -p1 < ../other/zen/Allow_changing_default_qdisc_to_FQ-PIE.patch
           patch -p1 < ../other/zen/Add_VHBA_driver.patch
           patch -p1 < ../other/zen/Tune_CFS_for_interactivity.patch
           patch -p1 < ../other/zen/Initialize_ata_before_graphics.patch
           patch -p1 < ../other/zen/Add_sysctl_and_CONFIG_to_disallow_unprivileged.patch
           patch -p1 < ../other/zen/Add_an_option_to_make_threadirqs_the_default.patch
           patch -p1 < ../other/0001-futex-patches.patch
           patch -p1 < ../other/anv_Implement_VK_EXT_transform_feedback_on_Gen7.patch
           #patch -p1 < ../other/i915_vgpu/v6-1-8-drm-i915-introduced-vgpu-pv-capability.patch
           #patch -p1 < ../other/i915_vgpu/v6-2-8-drm-i915-vgpu-shared-memory-setup-for-pv-optimization.patch
           #patch -p1 < ../other/i915_vgpu/v6-3-8-drm-i915-vgpu-ppgtt-update-pv-optimization.patch
           #patch -p1 < ../other/i915_vgpu/v6-4-8-drm-i915-vgpu-context-submission-pv-optimization.patch
           #patch -p1 < ../other/i915_vgpu/v6-5-8-drm-i915-gvt-GVTg-handle-pv_caps-PVINFO-register.patch
           #patch -p1 < ../other/i915_vgpu/v6-6-8-drm-i915-gvt-GVTg-handle-shared_page-setup.patch
           #patch -p1 < ../other/i915_vgpu/v6-7-8-drm-i915-gvt-GVTg-support-ppgtt-pv-optimization.patch
           #patch -p1 < ../other/i915_vgpu/v6-8-8-drm-i915-gvt-GVTg-support-context-submission-pv-optimization.patch
           cd ../
           mv linux-$VERSIONBASE linux-$VERSIONPOINT-pvl
           ;;
    core)
           cd linux-$VERSIONPOINT-pvl
           make xconfig
           sudo make-kpkg clean
           time sudo make-kpkg -j3 --initrd linux_image linux_headers
           #cd linux-$VERSIONBASE-pvl
           #sudo make modules_install -j4
           #cd ../
           #rm -r linux_modules
           #mkdir linux_modules
           #cd linux-$VERSIONPOINT-pvl
           #make INSTALL_MOD_PATH=../linux_modules modules_install -j4
           sudo make-kpkg clean
           cd ../
           zip -r linux-$VERSIONPOINT-pvl.zip linux-$VERSIONPOINT-pvl
           sudo rm -r linux-$VERSIONPOINT-pvl
           sudo dpkg -i *.deb
           sudo update-grub
           ;;
    bmq) 
           cd linux-$VERSIONPOINT-pvl
           patch -p1 -F 4 < ../bmq/$BMQPATCH.patch
           cp -a ../other/config_custom.txt ./
           mv config_custom.txt .config
           make xconfig
           sudo make-kpkg clean
           time sudo make-kpkg -j3 --initrd linux_image linux_headers
           #cd linux-$VERSIONBASE-pvl
           #sudo make modules_install -j4
           #cd ../
           #rm -r linux_modules
           #mkdir linux_modules
           #cd linux-$VERSIONPOINT-pvl
           #make INSTALL_MOD_PATH=../linux_modules modules_install -j4
           sudo make-kpkg clean
           cd ../
           zip -r linux-$VERSIONPOINT-pvl.zip linux-$VERSIONPOINT-pvl
           sudo rm -r linux-$VERSIONPOINT-pvl
           sudo dpkg -i *.deb
           sudo update-grub
           ;;
    muqss)
           cd linux-$VERSIONPOINT-pvl
           patch -p1 -F 4  < ../muqss/$MUQSSPATCH.patch
           cp -a ../other/config_custom.txt ./
           mv config_custom.txt .config
           make xconfig
           sudo make-kpkg clean
           time sudo make-kpkg -j3 --initrd linux_image linux_headers
           #sudo make modules_install
           #cd ../
           #rm -r linux_modules-$VERSIONPOINT-pvl
           #mkdir linux_modules-$VERSIONPOINT-pvl
           #make INSTALL_MOD_PATH=linux_modules-$VERSIONPOINT-pvl modules_install
           #cd linux-$VERSIONPOINT-pvl
           sudo make-kpkg clean
           cd ../
           zip -r linux-$VERSIONPOINT-pvl.zip linux-$VERSIONPOINT-pvl
           #zip -r linux_modules-$VERSIONPOINT-pvl.zip linux_modules-$VERSIONPOINT-pvl
           sudo rm -r linux-$VERSIONPOINT-pvl
           #rm -r linux_modules-$VERSIONPOINT-pvl
           sudo dpkg -i *.deb
           sudo update-grub
           ;;
    muqss_distcc)
           mv zen-kernel-$VERSIONBASE2-zen-tune linux-$VERSIONPOINT2-pvl
           cd linux-$VERSIONPOINT2-pvl
           patch  -p1 < ../muqss/$MUQSSPATCH
           patch  -p1 -F 3 < ../linux/patch-$VERSIONPOINT2
           make xconfig
           sudo make-kpkg clean
           #sudo CC="distcc gcc" CXX="distcc g++" make-kpkg -j4 --initrd linux_image linux_headers
           #sudo CONCURRENCY_LEVEL=4 MAKEFLAGS="CC=distcc\ gcc" make-kpkg -j4 --initrd linux_image linux_headers
            sudo MAKEFLAGS="CC=distcc" BUILD_TIME="/usr/bin/time" CONCURRENCY_LEVEL=$(distcc -j) make-kpkg --rootcmd fakeroot --initrd kernel_image kernel_headers
           cd ../
           sudo dpkg -i *.deb
           cd linux-$VERSIONPOINT2-pvl
           #sudo make modules_install -j4
           #cd ../
           #rm -r linux_modules
           #mkdir linux_modules
           #cd linux-$VERSIONBASE2-pvl
           #make INSTALL_MOD_PATH=../linux_modules modules_install -j4
           sudo make-kpkg clean
           cd ../
           zip -r linux-$VERSIONPOINT2-pvl.zip linux-$VERSIONPOINT2-pvl
           sudo rm -r linux-$VERSIONPOINT2-pvl
           sudo update-grub
           ;;
    rt) 
           cd linux-$VERSIONPOINT-pvl
           patch -p1 -F 4 < ../rt/$PREEMPT_RT.patch
           cp -a ../other/config_custom.txt ./
           mv config_custom.txt .config
           make xconfig
           sudo make-kpkg clean
           time sudo make-kpkg -j3 --initrd linux_image linux_headers
           #cd linux-$VERSIONBASE-pvl
           #sudo make modules_install -j4
           #cd ../
           #rm -r linux_modules
           #mkdir linux_modules
           #cd linux-$VERSIONPOINT-pvl
           #make INSTALL_MOD_PATH=../linux_modules modules_install -j4
           sudo make-kpkg clean
           cd ../
           zip -r linux-$VERSIONPOINT-pvl.zip linux-$VERSIONPOINT-pvl
           sudo rm -r linux-$VERSIONPOINT-pvl
           sudo dpkg -i *.deb
           sudo update-grub
           ;;
esac
