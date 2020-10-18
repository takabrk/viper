#!/bin/sh
#custom linux kernel build script
#Created by takamitsu hamada
#2020/10/15

while getopts e: OPT
do
  case $OPT in
      e) e_num=$OPTARG
         ;;\
  esac
done
VERSIONBASE="5.9"
VERSIONPOINT="5.9.1"
MUQSSPATCH="0001-MultiQueue-Skiplist-Scheduler-v0.202.patch"
PROJCPATCH="prjc_v5.9-r0"
PREEMPT_RT="patch-5.9-rc2-rt1"
#THREADS ="4"
case $e_num in
    base)
           wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-$VERSIONBASE.tar.xz
           tar -Jxvf linux-$VERSIONBASE.tar.xz
           cd linux-$VERSIONBASE
           cp -a ../other/REPORTING-BUGS ./
           cp -a ../other/config_custom.txt ./
           mv config_custom.txt .config
           #cp -a ../aufs5-standalone-aufs5.x-rcN/Documentation ./
           #cp -a ../aufs5-standalone-aufs5.x-rcN/fs ./
           #cp -a ../aufs5-standalone-aufs5.x-rcN/include ./
           #patch -p1 < ../aufs5-standalone-aufs5.x-rcN/aufs5-base.patch
           #patch -p1 < ../aufs5-standalone-aufs5.x-rcN/aufs5-kbuild.patch
           #patch -p1 < ../aufs5-standalone-aufs5.x-rcN/aufs5-mmap.patch
           #patch -p1 < ../aufs5-standalone-aufs5.x-rcN/aufs5-standalone.patch
           patch -p1 < ../other/zstd.patch
           patch -p1 < ../other/uksm/uksm-5.9.patch
           patch -p1 < ../other/FSGSBASE.patch
           patch -p1 < ../other/add-acs-overrides.patch
           patch -p1 < ../other/introduce_per-task_latency_nice_for_scheduler_hints.patch
           patch -p1 <../other/ck1/0004-Create-highres-timeout-variants-of-schedule_timeout-.patch
           patch -p1 < ../other/ck1/0006-Convert-msleep-to-use-hrtimers-when-active.patch
           rm -r ../linux-$VERSIONBASE.tar.xz
           patch -p1 < ../linux/patch-$VERSIONPOINT
           patch -p1 < ../other/zen/ZEN_Add_VHBA_driver.patch
           patch -p1 < ../other/zen/ZEN_Enable_additional_CPU_Optimizations_for_GCC_v10_1.patch
           patch -p1 < ../other/zen/ZEN_Unrestrict_CONFIG_OPTIMIZE_FOR_PERFORMANCE_O3.patch
           patch -p1 < ../other/zen/ZEN_INTERACTIVE_Base_config_item.patch
           patch -p1 < ../other/zen/ZEN_INTERACTIVE_Tune_CFS_for_interactivity.patch
           patch -p1 < ../other/LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch
           patch -p1 < ../other/LL/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch
           patch -p1 < ../other/LL/0004-mm-set-2048-for-address_space-level-file-read-ahead-.patch
           patch -p1 < ../other/0001-futex-patches.patch
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
    projc) 
           cd linux-$VERSIONPOINT-pvl
           patch -p1 < ../other/bmq/$PROJCPATCH.patch
           patch -p1 < ../other/bmq/0001-sched-alt-Fix-compilation-erro-in-pelt.c.patch
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
