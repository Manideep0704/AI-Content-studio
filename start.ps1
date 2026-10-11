# Root launcher forwarding to image-ai/start.ps1
param(
    [int]$Port = 8000,
    [string]$HostAddress = "127.0.0.1",
    [switch]$NoBrowser,
    [switch]$RebuildFrontend
)

$targetScript = Join-Path $PSScriptRoot "image-ai\start.ps1"
if (Test-Path $targetScript) {
    & $targetScript @PSBoundParameters
} else {
    Write-Error "Could not find image-ai\start.ps1"
}
