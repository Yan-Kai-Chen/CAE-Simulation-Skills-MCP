[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)] [string]$InputUnf,
    [Parameter(Mandatory = $true)] [string]$OutputDir,
    [string]$Field = 'Temperature',
    [string]$Unit = 'C',
    [string]$Steps = '0,290,770',
    [string]$Views = 'oblique,pos_z,neg_z',
    [double]$ClimMin = 20.0,
    [double]$ClimMax = 170.0,
    [ValidateSet('alloy', 'mold', 'all')] [string]$PartMode = 'alloy',
    [ValidateRange(320, 7680)] [int]$ImageWidth = 1600,
    [ValidateRange(240, 4320)] [int]$ImageHeight = 1000,
    [ValidateRange(2, 512)] [int]$ColorLevels = 8,
    [ValidateRange(1, 100000)] [int]$AnimationIncrement = 10,
    [ValidateRange(0, 100000000)] [int]$AnimationEnd = 770,
    [string]$VEBatch = '',
    [string]$SessionScript = (Join-Path $PSScriptRoot 've_native_field_image_export.py'),
    [switch]$Elevate,
    [switch]$KeepWindowOpen
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($VEBatch)) {
    $VEBatch = $env:PROCAST_VEBATCH
}
if ([string]::IsNullOrWhiteSpace($VEBatch)) { throw 'Set -VEBatch or PROCAST_VEBATCH.' }

function Test-IsAdministrator {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Quote-Argument([string]$Value) {
    return '"' + $Value.Replace('"', '\"') + '"'
}

$inputPath = [IO.Path]::GetFullPath($InputUnf)
$outputPath = [IO.Path]::GetFullPath($OutputDir)
$outputParent = Split-Path -Parent $outputPath
if (-not (Test-Path -LiteralPath $inputPath -PathType Leaf)) { throw "Input UNF not found: $inputPath" }
if (-not (Test-Path -LiteralPath $VEBatch -PathType Leaf)) { throw "VEBatch not found: $VEBatch" }
if (-not (Test-Path -LiteralPath $SessionScript -PathType Leaf)) { throw "Session script not found: $SessionScript" }

if ($Elevate -and -not (Test-IsAdministrator)) {
    $args = @('-NoLogo')
    if ($KeepWindowOpen) { $args += '-NoExit' }
    $args += @(
        '-ExecutionPolicy', 'Bypass', '-File', (Quote-Argument $MyInvocation.MyCommand.Path),
        '-InputUnf', (Quote-Argument $inputPath), '-OutputDir', (Quote-Argument $outputPath),
        '-Field', (Quote-Argument $Field), '-Unit', (Quote-Argument $Unit),
        '-Steps', (Quote-Argument $Steps), '-Views', (Quote-Argument $Views),
        '-ClimMin', $ClimMin.ToString([Globalization.CultureInfo]::InvariantCulture),
        '-ClimMax', $ClimMax.ToString([Globalization.CultureInfo]::InvariantCulture),
        '-PartMode', $PartMode, '-ImageWidth', $ImageWidth.ToString(),
        '-ImageHeight', $ImageHeight.ToString(), '-ColorLevels', $ColorLevels.ToString(),
        '-AnimationIncrement', $AnimationIncrement.ToString(),
        '-AnimationEnd', $AnimationEnd.ToString(),
        '-VEBatch', (Quote-Argument $VEBatch),
        '-SessionScript', (Quote-Argument $SessionScript), '-Elevate'
    )
    if ($KeepWindowOpen) { $args += '-KeepWindowOpen' }
    New-Item -ItemType Directory -Force -Path $outputParent | Out-Null
    $child = Start-Process powershell.exe -Verb RunAs -ArgumentList $args `
        -WorkingDirectory $outputParent -WindowStyle Normal -PassThru
    [ordered]@{ elevated_export_started = $true; process_id = $child.Id; output_dir = $outputPath } |
        ConvertTo-Json
    return
}

New-Item -ItemType Directory -Force -Path $outputPath | Out-Null
$consoleLog = Join-Path $outputPath 've18_native_export_console.log'
$launcherManifest = Join-Path $outputPath 'native_export_launcher_manifest.json'

[ordered]@{
    schema = 'procast_native_export_launcher_v1'
    started_at = (Get-Date).ToString('o')
    elevated = Test-IsAdministrator
    input_unf = $inputPath
    output_dir = $outputPath
    field = $Field
    unit = $Unit
    steps = $Steps
    views = $Views
    clim = @($ClimMin, $ClimMax)
    part_mode = $PartMode
    image_size = @($ImageWidth, $ImageHeight)
    color_levels = $ColorLevels
    animation_increment = $AnimationIncrement
    animation_end = $AnimationEnd
    vebatch = $VEBatch
    session_script = $SessionScript
} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $launcherManifest -Encoding UTF8

$env:PROCAST_INPUT_UNF = $inputPath
$env:PROCAST_NATIVE_OUT_DIR = $outputPath
$env:PROCAST_NATIVE_FIELD = $Field
$env:PROCAST_NATIVE_UNIT = $Unit
$env:PROCAST_NATIVE_STEPS = $Steps
$env:PROCAST_NATIVE_VIEWS = $Views
$env:PROCAST_NATIVE_CLIM_MIN = $ClimMin.ToString([Globalization.CultureInfo]::InvariantCulture)
$env:PROCAST_NATIVE_CLIM_MAX = $ClimMax.ToString([Globalization.CultureInfo]::InvariantCulture)
$env:PROCAST_NATIVE_PART_MODE = $PartMode
$env:PROCAST_NATIVE_IMAGE_WIDTH = $ImageWidth.ToString()
$env:PROCAST_NATIVE_IMAGE_HEIGHT = $ImageHeight.ToString()
$env:PROCAST_NATIVE_COLOR_LEVELS = $ColorLevels.ToString()
$env:PROCAST_NATIVE_ANIMATION_INCREMENT = $AnimationIncrement.ToString()
$env:PROCAST_NATIVE_ANIMATION_END = $AnimationEnd.ToString()
if (-not $env:PROCAST_VE_COMMON_RESOURCES) { throw 'Set PROCAST_VE_COMMON_RESOURCES.' }

Write-Host '============================================================' -ForegroundColor Cyan
Write-Host ' ProCAST native field image export' -ForegroundColor Yellow
Write-Host " Field: $Field  Steps: $Steps  Views: $Views" -ForegroundColor White
Write-Host " Output: $outputPath" -ForegroundColor Green
Write-Host '============================================================' -ForegroundColor Cyan

& $VEBatch -sessionrun $SessionScript -consolelog $consoleLog -exit
$exitCode = $LASTEXITCODE
Write-Host "VE18 export exit code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { 'Green' } else { 'Red' })
exit $exitCode
