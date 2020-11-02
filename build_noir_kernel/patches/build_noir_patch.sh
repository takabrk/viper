#!/bin/sh
truncate noir.patch --size 0
VERSIONPOINT="5.9.3"
cat linux/patch-$VERSIONPOINT \
       custom_config.patch \
       UKSM/uksm-5.9.patch \
       other/add-acs-overrides.patch \
       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       LL/0003kai2-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
       LL/0004-mm-set-8-megabytes-for-address_space-level-file-read.patch \
       zen/ZEN_INTERACTIVE_Base_config_item.patch \
       zen/ZEN_INTERACTIVE_Tune_CFS_for_interactivity.patch \
       zen/ZEN_INTERACTIVE_Add_help_text_for_the_MuQSS_tweaks.patch \
       zen/Add_help_text_for_the_BFQ_tweaks.patch \
       zen/ZEN_INTERACTIVE_Increase_default_writeback_thresholds.patch \
       zen/ZEN_INTERACTIVE_Tune_ondemand_governor_for_interactivity.patch \
       zen/ZEN_INTERACTIVE_Enable_background_reclaim_of_hugepages.patch \
       zen/ZEN_INTERACTIVE_Increase_max_number_of_tasks_rebalanced_at_once_kai.patch \
       zen/ZEN_Add_VHBA_driver.patch \
       zen/ZEN_Enable_additional_CPU_Optimizations_for_GCC_v10_1.patch \
       zen/ZEN_Unrestrict_CONFIG_OPTIMIZE_FOR_PERFORMANCE_O3.patch \
       zen/ZEN_Add_OpenRGB_patches.patch \
       ck1/0004-Create-highres-timeout-variants-of-schedule_timeout-.patch \
       ck1/0005-Special-case-calls-of-schedule_timeout-1-to-use-the-.patch \
       ck1/0006-Convert-msleep-to-use-hrtimers-when-active.patch \
       ck1/0007-Replace-all-schedule-timeout-1-with-schedule_min_hrt.patch \
       ck1/0008-Replace-all-calls-to-schedule_timeout_interruptible-.patch \
       ck1/0009-Replace-all-calls-to-schedule_timeout_uninterruptibl.patch \
       ck1/0010-Don-t-use-hrtimer-overlay-when-pm_freezing-since-som.patch \
       ck1/0012-Make-threaded-IRQs-optionally-the-default-which-can-.patch \
       ck1/0014-Swap-sucks.patch \
       IBM/introduce_per-task_latency_nice_for_scheduler_hints.patch \
       xanmod/0001-sched-autogroup-Add-kernel-parameter-and-config-opti.patch \
       VALVE/futex_Implement_mechanism_to_wait_on_any_of_several_futexes.patch \
       VALVE/futex_Add_Proton_compatibility_code.patch \
       other/0001-block-patches.patch \
       intel/0001-clearlinux-patches.patch \
       > noir.patch

