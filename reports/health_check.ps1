# System Health Check Script
# Outputs JSON for the monitoring watchdog

$timestamp = (Get-Date -Format "o")

# GPU info via nvidia-smi
$gpuCsv = nvidia-smi --query-gpu=temperature.gpu,power.draw,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits 2>$null
if ($gpuCsv) {
    $parts = $gpuCsv.Split(',').Trim()
    $gpuTemp = [int]$parts[0]
    $gpuPower = [math]::Round([double]$parts[1])
    $gpuUtil = [int]$parts[2]
    $gpuVram = [int]$parts[3]
} else {
    $gpuTemp = -1; $gpuPower = -1; $gpuUtil = -1; $gpuVram = -1
}

# CPU load
$cpuLoad = (Get-CimInstance Win32_Processor).LoadPercentage

# Free RAM in GB
$freeRamGB = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 2)

# Top processes by memory
$topProcs = Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 Name, @{N='MB';E={[math]::Round($_.WorkingSet64/1MB)}}
$topProcsStr = ($topProcs | ForEach-Object { "$($_.Name):$($_.MB)" }) -join ","

# Disk space
$disks = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
    "$($_.DeviceID)=$([math]::Round($_.FreeSpace/1GB,1))/$([math]::Round($_.Size/1GB,1))GB"
}
$diskStr = $disks -join ","

# Process counts
$pythonCount = @(Get-Process python* -ErrorAction SilentlyContinue).Count
$nodeCount = @(Get-Process node* -ErrorAction SilentlyContinue).Count

# Determine status
$status = "ok"
$warnings = @()

if ($gpuTemp -gt 82) { $status = "critical"; $warnings += "GPU_TEMP_CRITICAL:${gpuTemp}C" }
elseif ($gpuTemp -gt 75) { $status = "warning"; $warnings += "GPU_TEMP_HIGH:${gpuTemp}C" }

if ($gpuPower -gt 250) { if ($status -ne "critical") { $status = "warning" }; $warnings += "GPU_POWER_HIGH:${gpuPower}W" }
if ($gpuVram -gt 10000) { if ($status -ne "critical") { $status = "warning" }; $warnings += "GPU_VRAM_HIGH:${gpuVram}MB" }
if ($freeRamGB -lt 1) { $status = "critical"; $warnings += "RAM_CRITICAL:${freeRamGB}GB" }
elseif ($freeRamGB -lt 2) { if ($status -ne "critical") { $status = "warning" }; $warnings += "RAM_LOW:${freeRamGB}GB" }

$warningStr = if ($warnings.Count -gt 0) { $warnings -join "," } else { "none" }

# Output JSON line
$json = @{
    timestamp = $timestamp
    gpu_temp_c = $gpuTemp
    gpu_power_w = $gpuPower
    gpu_util_pct = $gpuUtil
    gpu_vram_used_mb = $gpuVram
    cpu_load_pct = $cpuLoad
    free_ram_gb = $freeRamGB
    top_procs = $topProcsStr
    disk = $diskStr
    python_procs = $pythonCount
    node_procs = $nodeCount
    status = $status
    warnings = $warningStr
} | ConvertTo-Json -Compress

Write-Output $json
