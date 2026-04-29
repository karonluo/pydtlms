[CmdletBinding()]
param(
    [switch]$Apply,
    [switch]$SkipBackupReminder,
    [switch]$SkipCompileCheck,
    [int]$StudentId,
    [int]$Limit,
    [string]$PythonPath = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Split-Path -Parent $ScriptDir
$ProjectRoot = Split-Path -Parent $BackendDir

if ([string]::IsNullOrWhiteSpace($PythonPath)) {
    $PythonPath = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
}

function Write-Step {
    param([string]$Message)
    Write-Host "[DTLMS] $Message" -ForegroundColor Cyan
}

function Assert-FileExists {
    param([string]$PathValue)
    if (-not (Test-Path $PathValue)) {
        throw "未找到文件: $PathValue"
    }
}

function Invoke-Python {
    param(
        [string[]]$Args,
        [string]$StepName
    )

    Write-Step $StepName
    & $PythonPath @Args
    if ($LASTEXITCODE -ne 0) {
        throw "步骤失败: $StepName"
    }
}

Assert-FileExists $PythonPath
Assert-FileExists (Join-Path $BackendDir '.env')
Assert-FileExists (Join-Path $BackendDir 'scripts\backfill_portal_students_to_relational.py')
Assert-FileExists (Join-Path $BackendDir 'sql\027_portal_student_runtime_backfill.sql')

if (-not $SkipBackupReminder) {
    Write-Step '重要：执行本脚本前，请先完成 PostgreSQL 备份。'
    Write-Host '建议命令示例：' -ForegroundColor Yellow
    Write-Host 'pg_dump -h <生产库地址> -p <端口> -U <用户名> -d <数据库名> -F c -b -v -f dtlms_prod_before_portal_student_fix.backup' -ForegroundColor Yellow
    if (-not $Apply) {
        Write-Step '当前未带 -Apply，仅执行只读检查。'
    }
}

if (-not $SkipCompileCheck) {
    Invoke-Python -Args @('-m', 'py_compile', 'backend/app/services/postgres_state_store.py', 'backend/app/services/management_service.py', 'backend/scripts/backfill_portal_students_to_relational.py') -StepName '检查后端脚本与服务文件语法'
}

$dryRunArgs = @('backend/scripts/backfill_portal_students_to_relational.py', '--dry-run', '--summary')
if ($PSBoundParameters.ContainsKey('StudentId')) {
    $dryRunArgs += @('--student-id', $StudentId.ToString())
}
if ($PSBoundParameters.ContainsKey('Limit')) {
    $dryRunArgs += @('--limit', $Limit.ToString())
}
Invoke-Python -Args $dryRunArgs -StepName '执行 dry-run 预检查'

if (-not $Apply) {
    Write-Step '只读检查完成。未带 -Apply，脚本不会执行任何正式补数写入。'
    exit 0
}

$applyArgs = @('backend/scripts/backfill_portal_students_to_relational.py', '--summary')
if ($PSBoundParameters.ContainsKey('StudentId')) {
    $applyArgs += @('--student-id', $StudentId.ToString())
}
if ($PSBoundParameters.ContainsKey('Limit')) {
    $applyArgs += @('--limit', $Limit.ToString())
}
Invoke-Python -Args $applyArgs -StepName '执行正式补数'

Write-Step '补数完成。请立即执行以下核查 SQL：'
Write-Host 'SELECT COUNT(*) AS runtime_count FROM dtlms_runtime_portal_students;' -ForegroundColor Green
Write-Host 'SELECT COUNT(*) AS relational_count FROM dtlms_portal_students;' -ForegroundColor Green
Write-Host 'SELECT id, full_name, phone_number, email, account_status, created_at, updated_at FROM dtlms_portal_students ORDER BY created_at DESC, id DESC LIMIT 20;' -ForegroundColor Green
Write-Host 'SELECT portal_student_id, gender, birth_date, ethnic_group, native_place, political_status, updated_at FROM dtlms_portal_student_profiles ORDER BY updated_at DESC NULLS LAST, portal_student_id DESC LIMIT 20;' -ForegroundColor Green

Write-Step '脚本执行结束。该脚本未执行任何删库、截断、覆盖或回滚操作。'