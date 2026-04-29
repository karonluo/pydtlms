[CmdletBinding()]
param(
    [switch]$Apply,
    [switch]$SkipBackupReminder,
    [switch]$SkipCompileCheck,
    [int]$TeamId,
    [int]$StudentId,
    [int]$TeamLimit,
    [int]$StudentLimit,
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
        [string[]]$CommandArgs,
        [string]$StepName
    )

    Write-Step $StepName
    & $PythonPath @CommandArgs
    if ($LASTEXITCODE -ne 0) {
        throw "步骤失败: $StepName"
    }
}

Assert-FileExists $PythonPath
Assert-FileExists (Join-Path $BackendDir '.env')
Assert-FileExists (Join-Path $BackendDir 'scripts\backfill_students_and_teams_to_relational.py')
Assert-FileExists (Join-Path $BackendDir 'sql\029_student_team_runtime_backfill.sql')

if (-not $SkipBackupReminder) {
    Write-Step '重要：执行本脚本前，请先完成 PostgreSQL 备份。'
    Write-Host '建议命令示例：' -ForegroundColor Yellow
    Write-Host 'pg_dump -h <生产库地址> -p <端口> -U <用户名> -d <数据库名> -F c -b -v -f dtlms_prod_before_student_team_fix.backup' -ForegroundColor Yellow
    if (-not $Apply) {
        Write-Step '当前未带 -Apply，仅执行只读检查。'
    }
}

if (-not $SkipCompileCheck) {
    Invoke-Python -CommandArgs @('-m', 'py_compile', 'backend/app/services/postgres_state_store.py', 'backend/app/services/management_service.py', 'backend/scripts/backfill_students_and_teams_to_relational.py') -StepName '检查后端脚本与服务文件语法'
}

$dryRunArgs = @('backend/scripts/backfill_students_and_teams_to_relational.py', '--dry-run', '--summary')
if ($PSBoundParameters.ContainsKey('TeamId')) {
    $dryRunArgs += @('--team-id', $TeamId.ToString())
}
if ($PSBoundParameters.ContainsKey('StudentId')) {
    $dryRunArgs += @('--student-id', $StudentId.ToString())
}
if ($PSBoundParameters.ContainsKey('TeamLimit')) {
    $dryRunArgs += @('--team-limit', $TeamLimit.ToString())
}
if ($PSBoundParameters.ContainsKey('StudentLimit')) {
    $dryRunArgs += @('--student-limit', $StudentLimit.ToString())
}
Invoke-Python -CommandArgs $dryRunArgs -StepName '执行学生/团队 dry-run 预检查'

if (-not $Apply) {
    Write-Step '只读检查完成。未带 -Apply，脚本不会执行任何正式补数写入。'
    exit 0
}

$applyArgs = @('backend/scripts/backfill_students_and_teams_to_relational.py', '--summary')
if ($PSBoundParameters.ContainsKey('TeamId')) {
    $applyArgs += @('--team-id', $TeamId.ToString())
}
if ($PSBoundParameters.ContainsKey('StudentId')) {
    $applyArgs += @('--student-id', $StudentId.ToString())
}
if ($PSBoundParameters.ContainsKey('TeamLimit')) {
    $applyArgs += @('--team-limit', $TeamLimit.ToString())
}
if ($PSBoundParameters.ContainsKey('StudentLimit')) {
    $applyArgs += @('--student-limit', $StudentLimit.ToString())
}
Invoke-Python -CommandArgs $applyArgs -StepName '执行学生/团队正式补数'

Write-Step '补数完成。请立即执行以下核查 SQL：'
Write-Host 'SELECT COUNT(*) AS runtime_team_count FROM dtlms_runtime_teams;' -ForegroundColor Green
Write-Host 'SELECT COUNT(*) AS relational_team_count FROM dtlms_teams WHERE is_deleted = FALSE;' -ForegroundColor Green
Write-Host 'SELECT COUNT(*) AS runtime_student_count FROM dtlms_runtime_students;' -ForegroundColor Green
Write-Host 'SELECT COUNT(*) AS relational_student_count FROM dtlms_students WHERE is_deleted = FALSE;' -ForegroundColor Green
Write-Host 'SELECT id, team_code, team_name, department_name, team_status, updated_at FROM dtlms_teams WHERE is_deleted = FALSE ORDER BY updated_at DESC, id DESC LIMIT 20;' -ForegroundColor Green
Write-Host 'SELECT id, student_no, full_name, current_status, enrollment_year, updated_at FROM dtlms_students WHERE is_deleted = FALSE ORDER BY updated_at DESC, id DESC LIMIT 20;' -ForegroundColor Green

Write-Step '脚本执行结束。该脚本未执行任何截断、删库、强覆盖或自动回滚操作。'