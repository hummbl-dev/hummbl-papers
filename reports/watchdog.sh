#!/bin/bash
# System Health Watchdog - runs every 60 seconds
# Logs to system_health_log.jsonl and creates alert files on critical conditions

LOGFILE="C:/Users/Owner/autoresearch-reports/system_health_log.jsonl"
REPORTDIR="C:/Users/Owner/autoresearch-reports"
HIGH_CPU_COUNT=0
ITERATION=0

while true; do
    ITERATION=$((ITERATION + 1))

    # Run the health check script
    RESULT=$(powershell.exe -ExecutionPolicy Bypass -File "C:/Users/Owner/autoresearch-reports/health_check.ps1" 2>/dev/null)

    if [ -z "$RESULT" ]; then
        echo "{\"timestamp\":\"$(date -Iseconds)\",\"error\":\"health_check_failed\",\"status\":\"warning\"}" >> "$LOGFILE"
        sleep 60
        continue
    fi

    # Log the result
    echo "$RESULT" >> "$LOGFILE"

    # Parse key values
    GPU_TEMP=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['gpu_temp_c'])" 2>/dev/null || echo "-1")
    GPU_POWER=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['gpu_power_w'])" 2>/dev/null || echo "-1")
    FREE_RAM=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['free_ram_gb'])" 2>/dev/null || echo "99")
    CPU_LOAD=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['cpu_load_pct'])" 2>/dev/null || echo "0")
    STATUS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])" 2>/dev/null || echo "unknown")

    NOW=$(date '+%Y-%m-%d %H:%M:%S')

    # Track sustained CPU load
    if [ "$CPU_LOAD" -gt 90 ] 2>/dev/null; then
        HIGH_CPU_COUNT=$((HIGH_CPU_COUNT + 1))
    else
        HIGH_CPU_COUNT=0
    fi

    # CRITICAL: GPU temp > 82C
    if [ "$GPU_TEMP" -gt 82 ] 2>/dev/null; then
        cat > "$REPORTDIR/THERMAL_ALERT.md" << ALERT
# THERMAL ALERT - CRITICAL

**Time:** $NOW
**GPU Temperature:** ${GPU_TEMP}C (CRITICAL - limit 85C)
**GPU Power:** ${GPU_POWER}W

## IMMEDIATE ACTION REQUIRED
The GPU temperature has exceeded 82C. Thermal shutdown risk is imminent.

### Recommended Actions:
1. Kill GPU-intensive processes (training jobs)
2. Set power limit: \`nvidia-smi -pl 200\`
3. Check case fans and airflow
4. Allow cooldown before restarting workloads

### Recent readings logged to system_health_log.jsonl
ALERT
        echo "[$NOW] CRITICAL: GPU temp ${GPU_TEMP}C - wrote THERMAL_ALERT.md"
    fi

    # CRITICAL: Free RAM < 1 GB
    FREE_RAM_INT=$(printf "%.0f" "$FREE_RAM" 2>/dev/null || echo "99")
    if [ "$FREE_RAM_INT" -lt 1 ] 2>/dev/null; then
        cat > "$REPORTDIR/MEMORY_ALERT.md" << ALERT
# MEMORY ALERT - CRITICAL

**Time:** $NOW
**Free RAM:** ${FREE_RAM} GB (CRITICAL - under 1 GB)

## IMMEDIATE ACTION REQUIRED
System is running out of physical memory. Swap thrashing and potential crash imminent.

### Recommended Actions:
1. Kill non-essential processes (browsers, Loom, Signal, Teams)
2. Check for memory leaks in research processes
3. Restart Ollama if it has grown too large

### Top processes at alert time:
$(powershell.exe -Command "Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 15 Name, @{N='MB';E={[math]::Round(\$_.WorkingSet64/1MB)}} | Format-Table" 2>/dev/null)
ALERT
        echo "[$NOW] CRITICAL: Free RAM ${FREE_RAM}GB - wrote MEMORY_ALERT.md"
    fi

    # Sustained CPU warning
    if [ "$HIGH_CPU_COUNT" -ge 3 ]; then
        echo "[$NOW] WARNING: CPU load >90% for $HIGH_CPU_COUNT consecutive readings"
    fi

    # Every 10 iterations, print a summary to stdout
    if [ $((ITERATION % 10)) -eq 0 ]; then
        echo "[$NOW] Watchdog iteration $ITERATION: GPU=${GPU_TEMP}C/${GPU_POWER}W, CPU=${CPU_LOAD}%, RAM_free=${FREE_RAM}GB, Status=$STATUS"
    fi

    sleep 60
done
