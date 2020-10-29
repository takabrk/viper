#!/bin/sh
truncate noir.patch --size 0
VERSIONPOINT="5.9.1"
cat ../linux/patch-$VERSIONPOINT \
       patch-5.9.1-rt20.patch \
       uksm-5.9.patch \
       add-acs-overrides.patch \
       zen/ZEN_INTERACTIVE_Base_config_item.patch \
       zen/ZEN_INTERACTIVE_Tune_CFS_for_interactivity.patch \
       zen/ZEN_INTERACTIVE_Add_help_text_for_the_MuQSS_tweaks.patch \
       zen/Add_help_text_for_the_BFQ_tweaks.patch \
       zen/ZEN_INTERACTIVE_Increase_default_writeback_thresholds.patch \
       zen/ZEN_INTERACTIVE_Tune_ondemand_governor_for_interactivity.patch \
       zen/ZEN_INTERACTIVE_Enable_background_reclaim_of_hugepages.patch \
       zen/ZEN_Add_VHBA_driver.patch \
       zen/ZEN_Enable_additional_CPU_Optimizations_for_GCC_v10_1.patch \
       zen/ZEN_Unrestrict_CONFIG_OPTIMIZE_FOR_PERFORMANCE_O3.patch \
       LL/0001-LL-kconfig-add-750Hz-timer-interrupt-kernel-config-o.patch \
       LL/0003kai-sched-core-nr_migrate-256-increases-number-of-tasks-.patch \
       LL/0004-mm-set-2048-for-address_space-level-file-read-ahead-.patch \
       ck1/0004-Create-highres-timeout-variants-of-schedule_timeout-.patch \
       ck1/0006-Convert-msleep-to-use-hrtimers-when-active.patch \
       ck1/0014-Swap-sucks.patch \
       introduce_per-task_latency_nice_for_scheduler_hints.patch \
       custom_config.patch \
       > noir.patch

