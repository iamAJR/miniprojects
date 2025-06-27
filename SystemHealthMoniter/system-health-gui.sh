#!/bin/bash

# Paths
LOGFILE="/var/log/system-health-$(date +%F).log"
HEALTH_SCRIPT="/opt/system-health.sh"

# Run health check script (make sure it uses sudo if needed)
sudo "$HEALTH_SCRIPT"

# Extract key data
hostname=$(hostname)
uptime=$(uptime -p)
disk=$(df -h / | awk 'NR==2 {print $5 " used on " $6}')
cpu=$(uptime | awk -F'load average:' '{print $2}')
memory=$(free -h | awk '/Mem:/ {print $3 "/" $2 " used"}')

FAILED=$(systemctl --failed --no-legend)
if [ -z "$FAILED" ]; then
    failed_services="No failed services"
else
    failed_services="$(echo "$FAILED" | wc -l) failed services"
fi

# Zenity GUI with Yes/No (Yes = view full report)
zenity --question \
--title="🩺 System Health Summary for $hostname" \
--width=400 \
--height=300 \
--ok-label="View Full Report" \
--cancel-label="Close" \
--text="📅 $(date)
🖥️  Uptime: $uptime
💾 Disk: $disk
🧠 Memory: $memory
🔥 CPU Load:$cpu
❌ $failed_services

Click 'View Full Report' to see detailed log.
"

# If user clicks "View Full Report"
if [ $? -eq 0 ]; then
    xdg-open "$LOGFILE"
fi

