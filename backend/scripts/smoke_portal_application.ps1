param(
    [string]$BaseUrl = 'http://127.0.0.1:8000/api/v1',
    [string]$Password = 'Portal@123456'
)

$ErrorActionPreference = 'Stop'
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

function Invoke-CurlJson {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Uri,

        [Parameter(Mandatory = $true)]
        [string]$Method,

        [string]$Json,

        [hashtable]$Headers
    )

    $Method = $Method.ToUpperInvariant()
    $arguments = @('--noproxy', '*', '-sS', '-X', $Method, $Uri)
    if ($null -ne $Headers) {
        foreach ($entry in $Headers.GetEnumerator()) {
            $arguments += '-H'
            $arguments += ("{0}: {1}" -f $entry.Key, $entry.Value)
        }
    }

    $payloadFile = $null
    if ($PSBoundParameters.ContainsKey('Json')) {
        $payloadFile = Join-Path $env:TEMP ('portal-json-' + [guid]::NewGuid().ToString('N') + '.json')
        [System.IO.File]::WriteAllText($payloadFile, $Json, [System.Text.UTF8Encoding]::new($false))
        $arguments += '-H'
        $arguments += 'Content-Type: application/json; charset=utf-8'
        $arguments += '--data-binary'
        $arguments += ('@' + $payloadFile)
    }

    $arguments += '-w'
    $arguments += "`n%{http_code}"

    try {
        $raw = & curl.exe @arguments
    }
    finally {
        if ($null -ne $payloadFile -and (Test-Path $payloadFile)) {
            Remove-Item $payloadFile -Force
        }
    }

    $parts = ($raw -split "`r?`n")
    $statusCode = [int]$parts[-1]
    $body = ($parts[0..($parts.Length - 2)] -join "`n")
    if ($statusCode -ge 400) {
        throw "HTTP ${statusCode}: $body"
    }
    return $body | ConvertFrom-Json
}

$phone = '13' + (Get-Random -Minimum 1000000000 -Maximum 9999999999)
$email = 'portal.' + (Get-Random -Minimum 100000000 -Maximum 999999999) + '@example.com'
$idNumber = '3200001999' + (Get-Random -Minimum 1000000 -Maximum 9999999)

$registerBody = @{
    phone_number = $phone
    email = $email
    full_name = '门户联调考生'
    id_number = $idNumber
    password = $Password
} | ConvertTo-Json

$null = Invoke-CurlJson -Uri "$BaseUrl/portal/register" -Method Post -Json $registerBody
Write-Host 'REGISTER_OK' $phone

$loginBody = @{ account = $phone; password = $Password } | ConvertTo-Json
$login = Invoke-CurlJson -Uri "$BaseUrl/portal/login" -Method Post -Json $loginBody
$headers = @{ Authorization = "Bearer $($login.access_token)" }
Write-Host 'LOGIN_OK'

$plans = Invoke-CurlJson -Uri "$BaseUrl/portal/plans" -Method Get -Headers $headers
$teams = Invoke-CurlJson -Uri "$BaseUrl/portal/teams" -Method Get -Headers $headers
if (-not $plans.items -or -not $teams.items) {
    throw 'Missing plans or teams for smoke test'
}

$plan = $plans.items[0]
$team = $teams.items[0]
Write-Host 'PLAN_OK' $plan.id
Write-Host 'TEAM_OK' $team.team_name

$tempResume = Join-Path $env:TEMP ('portal-resume-' + (Get-Random -Minimum 10000000 -Maximum 99999999) + '.pdf')
Set-Content -Path $tempResume -Value 'mock resume content' -Encoding utf8
$uploadRaw = curl.exe --noproxy "*" -s -X POST "$BaseUrl/portal/attachments/upload" -H "Authorization: Bearer $($login.access_token)" -F "category=resume" -F "file=@$tempResume;type=application/octet-stream"
$upload = $uploadRaw | ConvertFrom-Json
if (-not $upload.url) {
    throw "Upload failed: $uploadRaw"
}
Write-Host 'UPLOAD_OK' $upload.url

$submitBody = @{
    plan_id = $plan.id
    profile = @{
        gender = '男'
        birth_date = '1999-01-01'
        native_place = '江苏无锡'
        political_status = '中共党员'
    }
    source_channel = '实验室官网'
    preferences = @(
        @{
            preference_order = 1
            research_center_name = $team.team_name
            advisor_name = $team.lead_advisor_name
            is_optional = $false
        }
    )
    education_experiences = @(
        @{
            sort_order = 1
            education_stage = '硕士'
            school_name = '江南大学'
        }
    )
    family_members = @(
        @{ member_name = '张父'; relation_type = '父亲' },
        @{ member_name = '张母'; relation_type = '母亲' }
    )
    personal_statement = @{
        personal_statement_text = '门户联调提交'
        resume_attachment_url = $upload.url
    }
    declaration = @{
        has_read_declaration = $true
        declaration_text = '本人承诺以上填写内容真实、准确。'
    }
} | ConvertTo-Json -Depth 8

$submit = Invoke-CurlJson -Uri "$BaseUrl/portal/applications" -Method Post -Headers $headers -Json $submitBody
Write-Host 'SUBMIT_OK' $submit.application_business_key $submit.application_status

$me = Invoke-CurlJson -Uri "$BaseUrl/portal/me" -Method Get -Headers $headers
Write-Host 'ME_OK' $me.selected_plan_id $me.selected_team_name
Write-Host 'RESUME_OK' $me.application_draft.personal_statement.resume_attachment_url

[PSCustomObject]@{
    phone = $phone
    plan_id = $plan.id
    team_name = $team.team_name
    upload_url = $upload.url
    business_key = $submit.application_business_key
    application_status = $submit.application_status
    selected_plan_id = $me.selected_plan_id
    selected_team_name = $me.selected_team_name
    resume_url = $me.application_draft.personal_statement.resume_attachment_url
} | ConvertTo-Json -Depth 4