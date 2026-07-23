[CmdletBinding()]
param(
    [string]$ConfigPath = '',
    [switch]$SetProcessEnvironment,
    [switch]$RequireAll,
    [switch]$AsJson
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Full-Path([string]$Value) {
    if ([string]::IsNullOrWhiteSpace($Value)) { return $null }
    return [IO.Path]::GetFullPath([Environment]::ExpandEnvironmentVariables($Value))
}

if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
    $ConfigPath = Join-Path $PSScriptRoot '..\..\..\13_ProCAST_Export\config\procast_environment.json'
}
$configFile = Full-Path $ConfigPath
if (-not (Test-Path -LiteralPath $configFile -PathType Leaf)) {
    throw "ProCAST environment config not found: $configFile"
}

$config = Get-Content -LiteralPath $configFile -Raw | ConvertFrom-Json
if ($config.schema -ne 'procast_environment_v1') {
    throw "Unsupported ProCAST environment schema: $($config.schema)"
}

$projectRoot = Full-Path ([string]$config.project_root)
$exportRoot = Full-Path ([string]$config.export_root)
$procastRoot = Full-Path ([string]$config.procast.root)
$procastLauncher = Full-Path ([string]$config.procast.launcher)
$veRoot = Full-Path ([string]$config.visual_environment.root)
$veBatch = Full-Path ([string]$config.visual_environment.batch)
$veCommon = Full-Path ([string]$config.visual_environment.common_resources)
$python = Full-Path ([string]$config.tools.python)
$ffmpeg = Full-Path ([string]$config.tools.ffmpeg)
$caseRoots = @($config.case_roots | ForEach-Object { Full-Path ([string]$_) })
$activeCaseRoot = @($caseRoots | Where-Object { Test-Path -LiteralPath $_ -PathType Container } | Select-Object -First 1)
$activeCaseRoot = if ($activeCaseRoot.Count -gt 0) { $activeCaseRoot[0] } else { $null }

$checks = [ordered]@{
    config = Test-Path -LiteralPath $configFile -PathType Leaf
    project_root = Test-Path -LiteralPath $projectRoot -PathType Container
    export_root = Test-Path -LiteralPath $exportRoot -PathType Container
    procast_root = Test-Path -LiteralPath $procastRoot -PathType Container
    procast_launcher = Test-Path -LiteralPath $procastLauncher -PathType Leaf
    ve_root = Test-Path -LiteralPath $veRoot -PathType Container
    ve_batch = Test-Path -LiteralPath $veBatch -PathType Leaf
    ve_common_resources = Test-Path -LiteralPath $veCommon -PathType Container
    active_case_root = $null -ne $activeCaseRoot
    python = Test-Path -LiteralPath $python -PathType Leaf
    ffmpeg = Test-Path -LiteralPath $ffmpeg -PathType Leaf
}
$missing = @($checks.GetEnumerator() | Where-Object { -not $_.Value } | ForEach-Object { $_.Key })

$resolved = [ordered]@{
    schema = 'procast_environment_resolved_v1'
    resolved_at = (Get-Date).ToString('o')
    config_path = $configFile
    name = [string]$config.name
    project_root = $projectRoot
    export_root = $exportRoot
    procast_version = [string]$config.procast.version
    procast_root = $procastRoot
    procast_launcher = $procastLauncher
    ve_version = [string]$config.visual_environment.version
    ve_root = $veRoot
    ve_batch = $veBatch
    ve_common_resources = $veCommon
    case_roots = $caseRoots
    active_case_root = $activeCaseRoot
    python = $python
    ffmpeg = $ffmpeg
    ve_requires_admin = [bool]$config.machine.ve_requires_admin
    solver_requires_admin = [bool]$config.machine.solver_requires_admin
    checks = $checks
    missing = $missing
    ready = $missing.Count -eq 0
}

if ($SetProcessEnvironment) {
    $env:PROCAST_ENV_CONFIG = $configFile
    $env:PROCAST_PROJECT_ROOT = $projectRoot
    $env:PROCAST_EXPORT_ROOT = $exportRoot
    $env:PROCAST_ROOT = $procastRoot
    $env:PROCAST_LAUNCHER = $procastLauncher
    $env:PROCAST_VE_ROOT = $veRoot
    $env:PROCAST_VEBATCH = $veBatch
    $env:PROCAST_VE_COMMON_RESOURCES = $veCommon
    if ($null -ne $activeCaseRoot) { $env:PROCAST_CASE_ROOT = $activeCaseRoot }
    $env:PROCAST_PYTHON = $python
    $env:PROCAST_FFMPEG = $ffmpeg
    $env:PROCAST_VE_REQUIRES_ADMIN = if ($resolved.ve_requires_admin) { '1' } else { '0' }
    $env:PROCAST_SOLVER_REQUIRES_ADMIN = if ($resolved.solver_requires_admin) { '1' } else { '0' }
}

if ($RequireAll -and -not $resolved.ready) {
    throw "ProCAST environment is incomplete: $($missing -join ', ')"
}

if ($AsJson) {
    $resolved | ConvertTo-Json -Depth 6
} else {
    [pscustomobject]$resolved
}
