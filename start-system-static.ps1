[CmdletBinding()]
param(
    [int]$Port = 8000,
    [string]$AppHost = '127.0.0.1',
    [switch]$InstallDependencies,
    [switch]$SkipFrontendBuild
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
    }

    if (-not (Wait-PortState -TargetHost '127.0.0.1' -Port $Port -DesiredState Free -TimeoutSeconds 5)) {
        throw "端口 $Port 在终止进程后仍未释放。"
    }
}

function Build-FrontendDist {
    if ($SkipFrontendBuild) {
        Write-Step '已跳过前端 build。'
        return
    }

    Write-Step '开始构建前端 dist...'
    Push-Location $FrontendDir
    try {
        npm run build
    }
    finally {
        Pop-Location
    }
}

function Start-BackendWithStatic {
    $command = "& { Set-Location '$ProjectRoot'; `n`$host.UI.RawUI.WindowTitle = 'DTLMS Static App'; `n& '$PythonExe' -m uvicorn app.main_static:app --app-dir backend --host $AppHost --port $Port }"
    return Start-Process -FilePath $TerminalExe -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $command) -PassThru
}

Assert-Prerequisites
Ensure-Dependencies
Build-FrontendDist

Write-Step '检查并清理端口占用。'
Stop-PortProcesses -Port $Port

Write-Step '启动后端静态托管服务。'
$appProcess = Start-BackendWithStatic

if (Wait-PortState -TargetHost $AppHost -Port $Port -DesiredState Listening -TimeoutSeconds 30) {
    Write-Step "静态应用已启动: http://$AppHost`:$Port"
    Write-Step "OpenAPI 仍可通过 http://$AppHost`:$Port/docs 访问"
}
else {
    Write-Warning "静态应用启动超时，请查看新打开的终端窗口。进程 ID: $($appProcess.Id)"
}

Write-Host ''
Write-Host '启动完成。' -ForegroundColor Green
Write-Host "应用地址: http://$AppHost`:$Port" -ForegroundColor Green
Write-Host "OpenAPI 地址: http://$AppHost`:$Port/docs" -ForegroundColor Green
