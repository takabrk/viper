#!/bin/sh
truncate pvl.patch --size 0
VERSIONPOINT="5.9.1"
cat other/zen/ZEN_INTERACTIVE_Base_config_item.patch \
       other/zen/ZEN_INTERACTIVE_Tune_CFS_for_interactivity.patch \
       other/zen/ZEN_INTERACTIVE_Add_help_text_for_the_MuQSS_tweaks.patch \
       other/zen/Add_help_text_for_the_BFQ_tweaks.patch \
       other/zen/ZEN_INTERACTIVE_Increase_default_writeback_thresholds.patch \
       other/zen/ZEN_INTERACTIVE_Tune_ondemand_governor_for_interactivity.patch \
       other/zen/ZEN_INTERACTIVE_Enable_background_reclaim_of_hugepages.patch \
       other/zen/ZEN_Add_VHBA_driver.patch \
       other/zen/ZEN_Enable_additional_CPU_Optimizations_for_GCC_v10_1.patch \
       other/zen/ZEN_Unrestrict_CONFIG_OPTIMIZE_FOR_PERFORMANCE_O3.patch \
       other/LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       other/LL/0003-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
       other/LL/0004-mm-set-2048-for-address_space-level-file-read-ahead-.patch \
       other/ck1/0004-Create-highres-timeout-variants-of-schedule_timeout-.patch \
       other/ck1/0006-Convert-msleep-to-use-hrtimers-when-active.patch \
       other/ck1/0014-Swap-sucks.patch \
       other/uksm-5.9.patch \
       other/add-acs-overrides.patch \
       other/introduce_per-task_latency_nice_for_scheduler_hints.patch \
       other/0001-futex-patches.patch \
       linux/patch-$VERSIONPOINT \
       > pvl.patch

