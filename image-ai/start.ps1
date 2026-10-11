<#
.SYNOPSIS
    Starts the Image AI & Marketing Studio platform with automated environment verification.
.DESCRIPTION
    Verifies virtual environments, dependencies, configuration, builds the frontend if needed,
    handles port collision, launches the server, and opens the application in your default browser.
#>

param(
    [int]$Port = 8000,
    [string]$HostAddress = "127.0.0.1",
    [switch]$NoBrowser,
    [switch]$RebuildFrontend
)

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

# ANSI Color Helpers
function Write-Header {
    Clear-Host
    Write-Host ""
    Write-Host "  ================================================================" -ForegroundColor Cyan
    Write-Host "    ___ __  __    _    ____ _____       _    ___ " -ForegroundColor Cyan
    Write-Host "   |_ _|  \/  |  / \  / ___| ____|     / \  |_ _|  " -ForegroundColor Cyan
    Write-Host "    | || |\/| | / _ \| |  _|  _|      / _ \  | |   " -ForegroundColor Cyan
    Write-Host "    | || |  | |/ ___ \ |_| | |___    / ___ \ | |   " -ForegroundColor Cyan
    Write-Host "   |___|_|  |_/_/   \_\____|_____|  /_/   \_\___|  " -ForegroundColor Cyan
    Write-Host ""
    Write-Host "        AI MARKETING & IMAGE GENERATION STUDIO" -ForegroundColor White
    Write-Host "  ================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Message)
    Write-Host " [..] $Message" -ForegroundColor DarkGray -NoNewline
}

function Write-StepDone {
    param([string]$Message)
    Write-Host "`r [OK] $Message" -ForegroundColor Green
}

function Write-StepWarn {
    param([string]$Message)
    Write-Host "`r [WARN] $Message" -ForegroundColor Yellow
}

function Write-StepFail {
    param([string]$Message)
    Write-Host "`r [FAIL] $Message" -ForegroundColor Red
}

try {
    Write-Header

    # 1. Check Python Virtual Environment
    Write-Step "Checking Python virtual environment..."
    $venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-StepWarn "Virtual environment missing. Initializing .venv..."
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create Python virtual environment. Ensure Python is on PATH."
        }
        Write-Step "Installing backend dependencies from lockfile..."
        & $venvPython -m pip install -r backend/requirements.lock.txt
        if ($LASTEXITCODE -ne 0) {
            throw "Backend dependency installation failed."
        }
    }
    Write-StepDone "Python environment ready (.venv)"

    # 2. Check Security / Configuration
    Write-Step "Checking environment configuration..."
    $envPath = Join-Path $PSScriptRoot "backend\.env"
    if (-not (Test-Path $envPath)) {
        & $venvPython -c "import secrets; from pathlib import Path; Path('backend/.env').write_text('SECRET_KEY=' + secrets.token_urlsafe(48) + '\n')"
        Write-StepDone "Generated secure application secret in backend/.env"
    } else {
        Write-StepDone "Configuration loaded (backend/.env)"
    }

    # 3. Check Frontend Build
    $distIndex = Join-Path $PSScriptRoot "frontend\dist\index.html"
    if ($RebuildFrontend -or (-not (Test-Path $distIndex))) {
        Write-Step "Building production frontend bundle..."
        Push-Location frontend
        try {
            if (-not (Test-Path "node_modules")) {
                npm ci
                if ($LASTEXITCODE -ne 0) { throw "npm ci failed." }
            }
            npm run build
            if ($LASTEXITCODE -ne 0) { throw "Frontend build failed." }
        } finally {
            Pop-Location
        }
        Write-StepDone "Production frontend compiled successfully"
    } else {
        Write-StepDone "Frontend build verified (frontend/dist)"
    }

    # 4. Port Conflict Check & Resolution
    Write-Step "Checking network availability on port $Port..."
    $activeConn = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
    if ($activeConn) {
        $ownerPid = $activeConn.OwningProcess | Select-Object -First 1
        $proc = Get-Process -Id $ownerPid -ErrorAction SilentlyContinue
        Write-StepWarn "Port $Port is currently occupied by PID $ownerPid ($($proc.ProcessName))."
        
        # Test if it is already our app
        try {
            $health = Invoke-RestMethod -Uri "http://$HostAddress`:$Port/api/health" -Method Get -TimeoutSec 2 -ErrorAction Stop
            if ($health.status -eq 'ok') {
                Write-Host ""
                Write-Host "  ------------------------------------------------------------" -ForegroundColor Yellow
                Write-Host "   A running instance is already serving on http://$HostAddress`:$Port" -ForegroundColor Yellow
                Write-Host "  ------------------------------------------------------------" -ForegroundColor Yellow
                Write-Host ""
                $choice = Read-Host "  Would you like to restart it? (Y/n)"
                if ($choice -match '^[nN]') {
                    Write-Host "`n  Reusing existing running instance." -ForegroundColor Green
                    if (-not $NoBrowser) {
                        Start-Process "http://$HostAddress`:$Port"
                    }
                    exit 0
                }
            }
        } catch { }

        Write-Host "  Stopping process $ownerPid to free port $Port..." -ForegroundColor Yellow
        Stop-Process -Id $ownerPid -Force -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 800
    }
    Write-StepDone "Network socket available on $HostAddress`:$Port"

    # 5. Launch Service Info Card
    $appUrl = "http://$HostAddress`:$Port"
    Write-Host ""
    Write-Host "  +--------------------------------------------------------------+" -ForegroundColor Cyan
    Write-Host "  |                    STUDIO SERVICE IS READY                   |" -ForegroundColor Cyan
    Write-Host "  +--------------------------------------------------------------+" -ForegroundColor Cyan
    Write-Host "  |                                                              |" -ForegroundColor Cyan
    Write-Host "  |   Web Studio:   $appUrl".PadRight(65) + "|" -ForegroundColor White
    Write-Host "  |   API Docs:     $appUrl/docs".PadRight(65) + "|" -ForegroundColor DarkGray
    Write-Host "  |   Health Check: $appUrl/api/health".PadRight(65) + "|" -ForegroundColor DarkGray
    Write-Host "  |                                                              |" -ForegroundColor Cyan
    Write-Host "  |   Press [Ctrl + C] in this window to stop the server         |" -ForegroundColor DarkYellow
    Write-Host "  +--------------------------------------------------------------+" -ForegroundColor Cyan
    Write-Host ""

    # Open Browser automatically if requested
    if (-not $NoBrowser) {
        Start-Job -ScriptBlock {
            param($url)
            Start-Sleep -Seconds 1
            Start-Process $url
        } -ArgumentList $appUrl | Out-Null
    }

    # Execute Uvicorn server
    & $venvPython -m uvicorn backend.app.main:app --host $HostAddress --port $Port

} catch {
    Write-Host ""
    Write-StepFail "Startup error: $_"
    Write-Host ""
    Write-Host "  Troubleshooting Tips:" -ForegroundColor Yellow
    Write-Host "  1. If port $Port is blocked, pass a different port: .\start.ps1 -Port 8001" -ForegroundColor Gray
    Write-Host "  2. Ensure dependencies are intact by running: .\.venv\Scripts\python.exe -m pip check" -ForegroundColor Gray
    Write-Host "  3. To force rebuild frontend: .\start.ps1 -RebuildFrontend" -ForegroundColor Gray
    Write-Host ""
    exit 1
}
