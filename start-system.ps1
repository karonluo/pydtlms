[CmdletBinding()]
param(
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 5173,
    [string]$BackendHost = '0.0.0.0',
    [string]$FrontendHost = '0.0.0.0',
    [string]$AccessHost = '',
    [switch]$InstallDependencies
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
$FrontendDir = Join-Path $ProjectRoot 'frontend'
$BackendDir = Join-Path $ProjectRoot 'backend'
$FrontendNodeModules = Join-Path $FrontendDir 'node_modules'

$PreferredShell = Get-Command pwsh -ErrorAction SilentlyContinue
if ($PreferredShell) {
    $TerminalExe = $PreferredShell.Source
}
else {
    $TerminalExe = (Get-Command powershell -ErrorAction Stop).Source
}

function Write-Step {
    param([string]$Message)

    Write-Host "[DTLMS] $Message" -ForegroundColor Cyan
}

function Test-CommandExists {
    param([string]$CommandName)

    return $null -ne (Get-Command $CommandName -ErrorAction SilentlyContinue)
}

function Get-PreferredAccessHost {
    param([string]$RequestedHost)

    if ($RequestedHost) {
        return $RequestedHost
    }

    $candidate = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
        Where-Object {
            $_.IPAddress -and
            $_.IPAddress -notin @('127.0.0.1', '0.0.0.0') -and
            $_.PrefixOrigin -ne 'WellKnown' -and
            $_.IPAddress -like '192.168.*'
        } |
        Select-Object -First 1 -ExpandProperty IPAddress

    if (-not $candidate) {
        $candidate = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
            Where-Object {
                $_.IPAddress -and
                $_.IPAddress -notin @('127.0.0.1', '0.0.0.0') -and
                $_.PrefixOrigin -ne 'WellKnown'
            } |
            Select-Object -First 1 -ExpandProperty IPAddress
    }

    if (-not $candidate) {
        $candidate = '127.0.0.1'
    }

    return $candidate
}

function Resolve-ProbeHost {
    param([string]$BindHost)

    if ([string]::IsNullOrWhiteSpace($BindHost) -or $BindHost -eq '0.0.0.0' -or $BindHost -eq '::') {
        return '127.0.0.1'
    }

    return $BindHost
}

function Resolve-ApiHost {
    param(
        [string]$BindHost,
        [string]$PreferredHost
    )

    if ([string]::IsNullOrWhiteSpace($BindHost) -or $BindHost -eq '0.0.0.0' -or $BindHost -eq '::') {
        return $PreferredHost
    }

    return $BindHost
}

function Get-AllowedOriginsValue {
    param(
        [string[]]$Origins
    )

    return (($Origins | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique) -join ',')
}

function Assert-Prerequisites {
    if (-not (Test-Path $PythonExe)) {
        throw "未找到 Python 虚拟环境: $PythonExe"
    }

    if (-not (Test-Path $BackendDir)) {
        throw "未找到 backend 目录: $BackendDir"
    }

    if (-not (Test-Path $FrontendDir)) {
        throw "未找到 frontend 目录: $FrontendDir"
    }

    if (-not (Test-CommandExists 'npm')) {
        throw '未检测到 npm，请先安装 Node.js。'
    }
}

function Ensure-Dependencies {
    if ($InstallDependencies) {
        Write-Step '开始安装后端依赖...'
        & $PythonExe -m pip install -r (Join-Path $BackendDir 'requirements.txt')

        Write-Step '开始安装前端依赖...'
        Push-Location $FrontendDir
        try {
            npm install
        }
        finally {
            Pop-Location
        }

        return
    }

    try {
        & $PythonExe -c "import fastapi, uvicorn" | Out-Null
    }
    catch {
        throw '后端依赖未就绪，请先执行 .\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt，或使用 -InstallDependencies 运行本脚本。'
    }

    if (-not (Test-Path $FrontendNodeModules)) {
        throw '未检测到 frontend/node_modules，请先执行 npm install，或使用 -InstallDependencies 运行本脚本。'
    }
}

function Get-PortProcesses {
    param([int]$Port)

    $connections = @(Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue)
    if (-not $connections) {
        return @()
    }

    $owningProcesses = $connections |
        Select-Object -ExpandProperty OwningProcess -Unique |
        Where-Object { $_ -and $_ -gt 0 }

    $processes = foreach ($processId in $owningProcesses) {
        try {
            Get-Process -Id $processId -ErrorAction Stop
        }
        catch {
            continue
        }
    }

    return @($processes)
}

function Test-PortListening {
    param(
        [string]$TargetHost,
        [int]$Port
    )

    $client = [System.Net.Sockets.TcpClient]::new()
    try {
        $asyncResult = $client.BeginConnect($TargetHost, $Port, $null, $null)
        $waitHandle = $asyncResult.AsyncWaitHandle
        try {
            if (-not $waitHandle.WaitOne(1000, $false)) {
                return $false
            }
            $client.EndConnect($asyncResult)
            return $true
        }
        finally {
            $waitHandle.Close()
        }
    }
    catch {
        return $false
    }
    finally {
        $client.Dispose()
    }
}

function Wait-PortState {
    param(
        [string]$TargetHost,
        [int]$Port,
        [ValidateSet('Free', 'Listening')]
        [string]$DesiredState,
        [int]$TimeoutSeconds = 30
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $listening = Test-PortListening -TargetHost $TargetHost -Port $Port
        if ($DesiredState -eq 'Listening' -and $listening) {
            return $true
        }

        if ($DesiredState -eq 'Free' -and -not $listening) {
            return $true
        }

        Start-Sleep -Milliseconds 500
    }

    return $false
}

function Stop-PortProcesses {
    param([int]$Port)

    $deadline = (Get-Date).AddSeconds(20)
    $handledProcessIds = @{}

    while ((Get-Date) -lt $deadline) {
        $processes = Get-PortProcesses -Port $Port
        if (-not $processes) {
            Write-Step "端口 $Port 已释放。"
            return
        }

        foreach ($process in $processes) {
            if ($handledProcessIds.ContainsKey($process.Id)) {
                continue
            }

            Write-Step "端口 $Port 被进程 $($process.ProcessName) ($($process.Id)) 占用，正在终止。"
            Stop-Process -Id $process.Id -Force
            $handledProcessIds[$process.Id] = $true
        }

        Start-Sleep -Milliseconds 800
    }

    if (-not (Wait-PortState -TargetHost '127.0.0.1' -Port $Port -DesiredState Free -TimeoutSeconds 5)) {
        throw "端口 $Port 在终止进程后仍未释放。"
    }
}

function Start-Backend {
    $command = "& { Set-Location '$ProjectRoot'; `n`$host.UI.RawUI.WindowTitle = 'DTLMS Backend'; `n`$env:ALLOWED_ORIGINS = '$AllowedOriginsValue'; `n& '$PythonExe' -m uvicorn app.main:app --app-dir backend --host $BackendHost --port $BackendPort --reload }"
    return Start-Process -FilePath $TerminalExe -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $command) -PassThru
}

function Start-Frontend {
    $command = "& { Set-Location '$FrontendDir'; `n`$host.UI.RawUI.WindowTitle = 'DTLMS Frontend'; `n`$env:VITE_API_BASE_URL = '/api/v1'; `n`$env:VITE_API_PROXY_TARGET = 'http://$BackendAccessHost`:$BackendPort'; `nnpm run dev -- --host $FrontendHost --port $FrontendPort }"
    return Start-Process -FilePath $TerminalExe -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $command) -PassThru
}

Assert-Prerequisites
Ensure-Dependencies

$ResolvedAccessHost = Get-PreferredAccessHost -RequestedHost $AccessHost
$BackendProbeHost = Resolve-ProbeHost -BindHost $BackendHost
$FrontendProbeHost = Resolve-ProbeHost -BindHost $FrontendHost
$BackendAccessHost = Resolve-ApiHost -BindHost $BackendHost -PreferredHost $ResolvedAccessHost
$FrontendAccessHost = Resolve-ApiHost -BindHost $FrontendHost -PreferredHost $ResolvedAccessHost
$FrontendApiBaseUrl = "http://$BackendAccessHost`:$BackendPort/api/v1"
$AllowedOriginsValue = Get-AllowedOriginsValue -Origins @(
    "http://127.0.0.1:$FrontendPort",
    "http://localhost:$FrontendPort",
    "http://$FrontendAccessHost`:$FrontendPort"
)

Write-Step '检查并清理端口占用。'
Stop-PortProcesses -Port $BackendPort
Stop-PortProcesses -Port $FrontendPort

Write-Step '启动后端服务。'
$backendProcess = Start-Backend

if (Wait-PortState -TargetHost $BackendProbeHost -Port $BackendPort -DesiredState Listening -TimeoutSeconds 30) {
    Write-Step "后端已启动: http://127.0.0.1`:$BackendPort/docs"
}
else {
    Write-Warning "后端启动超时，请查看新打开的后端终端窗口。进程 ID: $($backendProcess.Id)"
}

Write-Step '启动前端服务。'
$frontendProcess = Start-Frontend

if (Wait-PortState -TargetHost $FrontendProbeHost -Port $FrontendPort -DesiredState Listening -TimeoutSeconds 30) {
    Write-Step "前端已启动: http://127.0.0.1`:$FrontendPort"
}
else {
    Write-Warning "前端启动超时，请查看新打开的前端终端窗口。进程 ID: $($frontendProcess.Id)"
}

Write-Host ''
Write-Host '启动完成。' -ForegroundColor Green
Write-Host "前端地址(本机): http://127.0.0.1`:$FrontendPort" -ForegroundColor Green
Write-Host "前端地址(局域网): http://$FrontendAccessHost`:$FrontendPort" -ForegroundColor Green
Write-Host "后端地址(本机): http://127.0.0.1`:$BackendPort/docs" -ForegroundColor Green
Write-Host "后端地址(局域网): http://$BackendAccessHost`:$BackendPort/docs" -ForegroundColor Green
Write-Host "前端 API 基地址: /api/v1 (通过 Vite 代理到 http://$BackendAccessHost`:$BackendPort)" -ForegroundColor Green
Write-Host "后端允许的前端源: $AllowedOriginsValue" -ForegroundColor Green
