[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RunRoot,

    [string]$Prefix = '132',
    [switch]$AsJson
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$runPath = [IO.Path]::GetFullPath($RunRoot)
if (-not (Test-Path -LiteralPath $runPath -PathType Container)) {
    throw "Run root not found: $runPath"
}

$launchPath = Join-Path $runPath 'launch_manifest.json'
$launch = $null
$startedAt = $null
if (Test-Path -LiteralPath $launchPath -PathType Leaf) {
    $launch = Get-Content -LiteralPath $launchPath -Raw | ConvertFrom-Json
    if ($launch.started_at) { $startedAt = [datetime]$launch.started_at }
}

$all = Get-CimInstance Win32_Process
$runProcesses = @($all | Where-Object {
    $_.Name -match '^(esi_procast|procastDMP|datacast).*\.exe$' -and
    ($null -eq $startedAt -or [datetime]$_.CreationDate -ge $startedAt.AddSeconds(-5))
})
$ranks = @($runProcesses | Where-Object { $_.Name -match '^(esi_procast|procastDMP)' })
$datacast = @($runProcesses | Where-Object { $_.Name -match '^datacast' })

$pout = Join-Path $runPath ($Prefix + 'p.out')
$dout = Join-Path $runPath ($Prefix + 'd.out')
$text = ''
if (Test-Path -LiteralPath $pout -PathType Leaf) {
    $text = Get-Content -LiteralPath $pout -Raw
}

function Last-MatchValue([string]$Pattern, [int]$Group = 1) {
    $matches = [regex]::Matches($text, $Pattern)
    if ($matches.Count -eq 0) { return $null }
    return $matches[$matches.Count - 1].Groups[$Group].Value.Trim()
}

$version = Last-MatchValue 'ProCAST Version\s+([0-9.]+)'
$mode = Last-MatchValue 'ProCAST Version\s+[0-9.]+,\s*([^*\r\n]+)'
$reportedCores = Last-MatchValue '(?im)^\s*Number of [Pp]rocessors:\s*(?:=\s*)?(\d+)'
$nstep = Last-MatchValue '(?im)NSTEP\s*=\s*(\d+)'
$lastStep = Last-MatchValue '(?im)^\s*STEP NO\.\s+(\d+)'
$lastTime = Last-MatchValue '(?im)^\s*STEP NO\.\s+\d+\s+TIME\s*=\s*([^\s]+)'
$lastWallClock = Last-MatchValue '(?im)^\s*WALL CLOCK TIME\s*=\s*([0-9.]+)'
$normalTermination = [regex]::IsMatch(
    $text, '(?i)normal termination|calculation completed|\bTFINAL[ \t]+reached\b'
)
$errorMatches = [regex]::Matches($text, '(?im)^.*(?:FATAL|ABORT|LICENSE.*FAIL|ERROR:).*$')
$errors = @($errorMatches | ForEach-Object { $_.Value.Trim() } | Select-Object -Unique)

$state = 'prepared'
if ($datacast.Count -gt 0) { $state = 'preprocessing' }
if ($ranks.Count -gt 0) { $state = 'running' }
if ($errors.Count -gt 0 -and $ranks.Count -eq 0) { $state = 'failed' }
if ($normalTermination -and $ranks.Count -eq 0 -and $errors.Count -eq 0) { $state = 'completed' }
if ($null -ne $lastStep -and $ranks.Count -eq 0 -and -not $normalTermination -and
    $errors.Count -eq 0) { $state = 'stopped_after_progress' }

$files = @(Get-ChildItem -LiteralPath $runPath -File)
$status = [ordered]@{
    schema = 'procast_solver_status_v1'
    checked_at = (Get-Date).ToString('o')
    run_root = $runPath
    prefix = $Prefix
    state = $state
    launch_manifest_present = Test-Path -LiteralPath $launchPath
    requested_cores = if ($null -ne $launch) { $launch.requested_cores } else { $null }
    procast_version = $version
    mode = $mode
    reported_cores = if ($null -ne $reportedCores) { [int]$reportedCores } else { $null }
    requested_steps = if ($null -ne $nstep) { [int]$nstep } else { $null }
    last_step = if ($null -ne $lastStep) { [int]$lastStep } else { $null }
    last_simulation_time = $lastTime
    last_wall_clock_seconds = if ($null -ne $lastWallClock) { [double]$lastWallClock } else { $null }
    active_rank_count = $ranks.Count
    active_rank_pids = @($ranks | ForEach-Object { $_.ProcessId })
    active_datacast_count = $datacast.Count
    error_count = $errors.Count
    errors = $errors
    p_out_present = Test-Path -LiteralPath $pout
    d_out_present = Test-Path -LiteralPath $dout
    file_count = $files.Count
    run_root_bytes = ($files | Measure-Object Length -Sum).Sum
}

if ($AsJson) {
    $status | ConvertTo-Json -Depth 6
} else {
    [pscustomobject]$status
}
