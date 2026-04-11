# Learning Terminal — Windows PowerShell 설치 스크립트
# 사용법: irm https://raw.githubusercontent.com/lemonardo1/Learning-Terminal/main/install.ps1 | iex

$ErrorActionPreference = "Stop"

$REPO   = "lemonardo1/Learning-Terminal"
$BRANCH = "main"
$SCRIPT = "learning_terminal.py"

Write-Host ""
Write-Host "  +------------------------------------------+" -ForegroundColor Cyan
Write-Host "  |   터미널/PowerShell 학습 도우미 설치     |" -ForegroundColor Cyan
Write-Host "  |   github.com/$REPO  |" -ForegroundColor Cyan
Write-Host "  +------------------------------------------+" -ForegroundColor Cyan
Write-Host ""
Write-Host "  설치 후 'terminal' 명령어로 바로 실행할 수 있습니다." -ForegroundColor White
Write-Host ""

# ── 설치 경로 결정 ────────────────────────────────────────────────────────────
$INSTALL_DIR = "$env:USERPROFILE\.local\bin"
$CMD_NAME    = "terminal.py"
$WRAPPER     = "$env:USERPROFILE\.local\bin\terminal.ps1"

Write-Host "  설치 위치: $INSTALL_DIR\$CMD_NAME" -ForegroundColor DarkGray
Write-Host "  설정 파일: $env:APPDATA\learning-terminal\" -ForegroundColor DarkGray
Write-Host ""

$confirm = Read-Host "  설치하시겠습니까? [y/N]"
if ($confirm -notmatch "^[Yy]$") {
    Write-Host ""
    Write-Host "  설치를 취소했습니다." -ForegroundColor Yellow
    Write-Host ""
    exit 0
}
Write-Host ""

# ── Python 3 확인 ─────────────────────────────────────────────────────────────
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python 3\.(\d+)") {
            $minor = [int]$Matches[1]
            if ($minor -ge 7) {
                $pythonCmd = $cmd
                Write-Host "  v Python $($ver -replace 'Python ','') 확인" -ForegroundColor Green
                break
            }
        }
    } catch { }
}

if (-not $pythonCmd) {
    Write-Host "  x Python 3.7 이상이 필요합니다." -ForegroundColor Red
    Write-Host ""
    Write-Host "  설치 방법:" -ForegroundColor White
    Write-Host "    winget install Python.Python.3     (권장)" -ForegroundColor Cyan
    Write-Host "    또는  https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

# ── 설치 디렉터리 생성 ────────────────────────────────────────────────────────
if (-not (Test-Path $INSTALL_DIR)) {
    New-Item -ItemType Directory -Path $INSTALL_DIR -Force | Out-Null
    Write-Host "  v 디렉터리 생성: $INSTALL_DIR" -ForegroundColor Green
}

# ── 다운로드 ──────────────────────────────────────────────────────────────────
$URL  = "https://raw.githubusercontent.com/$REPO/$BRANCH/$SCRIPT"
$DEST = "$INSTALL_DIR\$CMD_NAME"

Write-Host "  ... 다운로드 중..." -ForegroundColor DarkGray
try {
    Invoke-WebRequest -Uri $URL -OutFile $DEST -UseBasicParsing
    Write-Host "  v 다운로드 완료: $DEST" -ForegroundColor Green
} catch {
    Write-Host "  x 다운로드 실패. 네트워크를 확인해주세요." -ForegroundColor Red
    Write-Host "  URL: $URL" -ForegroundColor DarkGray
    exit 1
}

# ── 래퍼 스크립트 생성 (terminal 명령어) ──────────────────────────────────────
$wrapperContent = @"
#!/usr/bin/env pwsh
& $pythonCmd "$DEST" @args
"@
Set-Content -Path $WRAPPER -Value $wrapperContent -Encoding UTF8
Write-Host "  v 래퍼 생성: $WRAPPER" -ForegroundColor Green

# ── PATH 등록 ─────────────────────────────────────────────────────────────────
$currentPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$INSTALL_DIR*") {
    [System.Environment]::SetEnvironmentVariable(
        "PATH",
        "$currentPath;$INSTALL_DIR",
        "User"
    )
    Write-Host "  v PATH 등록 완료 (사용자 환경변수)" -ForegroundColor Green
    $pathUpdated = $true
} else {
    Write-Host "  v PATH 이미 설정됨" -ForegroundColor Green
}

# ── PowerShell 프로파일에 alias 등록 ──────────────────────────────────────────
$profileDir = Split-Path $PROFILE -Parent
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}
if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
}

$aliasLine = "function terminal { & $pythonCmd `"$DEST`" @args }"
$profileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
if ($profileContent -notlike "*learning_terminal*") {
    Add-Content -Path $PROFILE -Value "`n# Learning Terminal`n$aliasLine"
    Write-Host "  v PowerShell 프로파일에 alias 등록: $PROFILE" -ForegroundColor Green
    $profileUpdated = $true
} else {
    Write-Host "  v alias 이미 프로파일에 있음" -ForegroundColor Green
}

# ── 완료 메시지 ───────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  ------------------------------------------" -ForegroundColor DarkGray
Write-Host "  설치 완료!" -ForegroundColor Green
Write-Host ""

if ($pathUpdated -or $profileUpdated) {
    Write-Host "  ! PATH/alias 적용을 위해 PowerShell을 새로 여세요." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  이후 아래 명령어로 실행하세요:" -ForegroundColor White
} else {
    Write-Host "  지금 바로 실행할 수 있습니다:" -ForegroundColor White
}

Write-Host ""
Write-Host "     terminal" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Windows에서는 PowerShell 기초 학습이 첫 번째 메뉴로 자동 설정됩니다." -ForegroundColor DarkGray
Write-Host "  ------------------------------------------" -ForegroundColor DarkGray
Write-Host ""
