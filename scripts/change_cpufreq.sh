#!/bin/sh
sudo cpufreq-set -r -g performance --max 3.6GHz
#echo "performance" > sudo /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
#sudo cpufreq-set -c 1 -g performance
#echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
cpufreq-info -p
#echo "high" > /sys/class/drm/card0/device/power_dpm_force_performance_level
#cat /sys/class/drm/card0/device/power_dpm_force_performance_level
#echo -n 1 > /sys/devices/system/cpu/cpufreq/performance/sampling_down_factor
#cat /sys/devices/system/cpu/cpufreq/ondemand/sampling_down_factor
exit
