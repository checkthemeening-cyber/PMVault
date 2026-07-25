# 日経ニュース自動収集スクリプト
# 使用方法: pwsh -File run-nikkei.ps1 -Mode [morning|evening|monthly]
param(
    [string]$Mode = "morning"
)

$ErrorActionPreference = "Continue"
$RepoDir   = "C:\Users\check\PMVault"
$ClaudeExe = "C:\Users\check\.local\bin\claude.exe"
$LogDir    = "$RepoDir\.claude\scripts\logs"
$LogFile   = "$LogDir\nikkei-$(Get-Date -Format 'yyyyMMdd-HHmm')-$Mode.log"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Log($msg) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $msg"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
}

Log "=== nikkei-news $Mode 開始 ==="
Set-Location $RepoDir

# Claude Code CLI でスキルを実行
& $ClaudeExe --print "/nikkei-news $Mode" --dangerously-skip-permissions 2>&1 | ForEach-Object {
    Add-Content -Path $LogFile -Value $_ -Encoding UTF8
    Write-Host $_
}

# JST で現在時刻を取得
$jst = [System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId(
    [DateTime]::UtcNow, "Tokyo Standard Time"
)
$dateStr = $jst.ToString("yyyy年MM月dd日 HH:mm")

$commitMsg = switch ($Mode) {
    "morning" { "日経ニュース daily サマリ - $dateStr" }
    "evening" { "日経ニュース daily サマリ - $dateStr [evening]" }
    "monthly" { "日経ニュース monthly サマリ - $($jst.AddMonths(-1).ToString('yyyy年MM月'))" }
    default   { "日経ニュース $Mode サマリ - $dateStr" }
}

# git add -> commit -> push
git -C $RepoDir add "00_ナレッジ/nikkei-news/" 2>&1 | ForEach-Object { Log $_ }
$changes = git -C $RepoDir status --porcelain 2>&1
if ($changes) {
    git -C $RepoDir commit -m $commitMsg 2>&1 | ForEach-Object { Log $_ }
    git -C $RepoDir push origin master 2>&1   | ForEach-Object { Log $_ }
    Log "コミット完了: $commitMsg"
} else {
    Log "変更なし、コミットをスキップしました"
}

Log "=== nikkei-news $Mode 完了 ==="
