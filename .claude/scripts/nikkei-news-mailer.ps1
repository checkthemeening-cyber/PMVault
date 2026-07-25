# nikkei-news の当該回（morning/evening）の収集結果をHTML化してメール送信する。
# Claude(claude.exe)は呼ばない。収集済みMarkdownを機械的に整形して送るだけの決定的な処理。

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("morning", "evening")]
    [string]$Mode
)

$ErrorActionPreference = "Stop"

$VaultRoot = "C:\Users\check\PMVault"
Set-Location $VaultRoot

$today = Get-Date
$yyyy = $today.ToString("yyyy")
$mm = $today.ToString("MM")
$dd = $today.ToString("dd")
$dailyDir = Join-Path $VaultRoot "00_ナレッジ\nikkei-news\daily\$yyyy\$mm\$dd"

$logFile = Join-Path $VaultRoot (".claude\scripts\logs\nikkei-mailer-{0}-{1}.log" -f $today.ToString("yyyyMMdd"), $Mode)
New-Item -ItemType Directory -Force (Split-Path $logFile) | Out-Null

function Write-Log($msg) {
    ("[" + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + "] " + $msg) | Out-File -FilePath $logFile -Append -Encoding utf8
}

Write-Log "nikkei-news-mailer $Mode start"

# 収集タスク（nikkei-morning/evening）が完了する前にメーラーが起動するレース対策。
# 対応する収集ログに完了行が出るまで待つ（PCスリープ等でTask Schedulerの起動が遅延・重複するケースがあるため）。
$collectionLogFile = Join-Path $VaultRoot (".claude\scripts\logs\nikkei-{0}-{1}.log" -f $Mode, $today.ToString("yyyyMMdd"))
$doneMarker = "nikkei-news $Mode done"
$maxWaitSeconds = 900
$pollIntervalSeconds = 20
$waited = 0
while ($waited -lt $maxWaitSeconds) {
    if ((Test-Path $collectionLogFile) -and (Select-String -Path $collectionLogFile -SimpleMatch -Pattern $doneMarker -Quiet -ErrorAction SilentlyContinue)) {
        Write-Log "collection done marker found after waiting ${waited}s"
        break
    }
    Start-Sleep -Seconds $pollIntervalSeconds
    $waited += $pollIntervalSeconds
}
if ($waited -ge $maxWaitSeconds) {
    Write-Log "WARNING: gave up waiting for collection after ${maxWaitSeconds}s, proceeding with whatever is available"
}

$CategoryOrder = @("資源エネルギー", "建設・不動産", "物流・運輸", "商社・卸売り", "自動車", "素材")

function HtmlEncode($text) {
    if ($null -eq $text) { return "" }
    return [System.Web.HttpUtility]::HtmlEncode($text)
}

# 簡易Markdown→HTML変換。このスキル群が出力する定型フォーマット（見出し・**field**:value・引用・区切り線・リンク）のみ対応する。
function Convert-MarkdownToHtml([string]$md) {
    $lines = $md -split "`r?`n"
    $html = New-Object System.Text.StringBuilder
    foreach ($line in $lines) {
        $l = $line.TrimEnd()
        if ($l -match '^---\s*$') {
            [void]$html.Append("<hr>`n")
            continue
        }
        if ($l -match '^### (.+)$') {
            [void]$html.Append("<h3>" + (HtmlEncode $Matches[1]) + "</h3>`n")
            continue
        }
        if ($l -match '^## (.+)$') {
            [void]$html.Append("<h2>" + (HtmlEncode $Matches[1]) + "</h2>`n")
            continue
        }
        if ($l -match '^# (.+)$') {
            [void]$html.Append("<h1>" + (HtmlEncode $Matches[1]) + "</h1>`n")
            continue
        }
        if ($l -match '^>\s?(.*)$') {
            $quote = HtmlEncode $Matches[1]
            $quote = $quote -replace '\[([^\]]+)\]\(([^)]+)\)', '<a href="$2">$1</a>'
            [void]$html.Append("<blockquote>" + $quote + "</blockquote>`n")
            continue
        }
        if ($l -match '^\*\*(.+?)\*\*[:：]?\s*(.*)$') {
            $field = HtmlEncode $Matches[1]
            $rest = HtmlEncode $Matches[2]
            $rest = $rest -replace '\[([^\]]+)\]\(([^)]+)\)', '<a href="$2">$1</a>'
            [void]$html.Append("<p><strong>" + $field + "</strong>: " + $rest + "</p>`n")
            continue
        }
        if ($l -eq "") {
            continue
        }
        $escaped = HtmlEncode $l
        $escaped = $escaped -replace '\[([^\]]+)\]\(([^)]+)\)', '<a href="$2">$1</a>'
        [void]$html.Append("<p>" + $escaped + "</p>`n")
    }
    return $html.ToString()
}

Add-Type -AssemblyName System.Web

$sections = New-Object System.Collections.Generic.List[string]
$anyContent = $false

if (-not (Test-Path $dailyDir)) {
    Write-Log "daily dir not found: $dailyDir"
    $sections.Add("<p>本日（$($today.ToString('yyyy年MM月dd日'))）の nikkei-news $Mode 収集データが見つかりませんでした。収集タスク自体が失敗している可能性があります。</p>")
}
else {
    foreach ($cat in $CategoryOrder) {
        $file = Join-Path $dailyDir ("$cat.md")
        if (-not (Test-Path $file)) {
            continue
        }
        $content = Get-Content -Path $file -Raw -Encoding UTF8

        if ($Mode -eq "evening") {
            $idx = $content.IndexOf("## 夕刊更新")
            if ($idx -lt 0) {
                continue
            }
            $content = $content.Substring($idx)
        }

        $anyContent = $true
        $bodyHtml = Convert-MarkdownToHtml $content
        $sections.Add("<section style=`"margin-bottom:32px;`"><h2 style=`"border-bottom:2px solid #333;padding-bottom:4px;`">$cat</h2>$bodyHtml</section>")
    }

    if (-not $anyContent) {
        if ($Mode -eq "evening") {
            $sections.Add("<p>本日の夕刊更新（新着差分）はありませんでした。</p>")
        }
        else {
            $sections.Add("<p>本日分のカテゴリファイルが見つかりませんでした。</p>")
        }
    }
}

$modeLabel = if ($Mode -eq "morning") { "朝刊" } else { "夕刊" }
$subject = "[nikkei-news $modeLabel] " + $today.ToString("yyyy年MM月dd日")

$htmlBody = @"
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: 'Meiryo', sans-serif; line-height:1.6; color:#222;">
<h1>$subject</h1>
$([string]::Join("`n", $sections))
<hr>
<p style="color:#888; font-size:12px;">このメールは nikkei-news-mailer スキルにより自動送信されました。</p>
</body>
</html>
"@

Write-Log "sections built: $($sections.Count), anyContent=$anyContent"

# --- 送信 ---
$fromAddress = "matsuo.and.consultants@gmail.com"
$toAddress = "matsuo.and.consultants@gmail.com"
$secretFile = Join-Path $VaultRoot ".claude\scripts\secrets\gmail-app-password.secure.txt"

if (-not (Test-Path $secretFile)) {
    Write-Log "ERROR: secret file not found: $secretFile"
    throw "Gmail app password secret file not found"
}

$secure = Get-Content $secretFile | ConvertTo-SecureString
$cred = New-Object System.Management.Automation.PSCredential($fromAddress, $secure)

try {
    $smtp = New-Object System.Net.Mail.SmtpClient("smtp.gmail.com", 587)
    $smtp.EnableSsl = $true
    $smtp.Credentials = New-Object System.Net.NetworkCredential($fromAddress, $cred.GetNetworkCredential().Password)

    $mail = New-Object System.Net.Mail.MailMessage
    $mail.From = $fromAddress
    $mail.To.Add($toAddress)
    $mail.Subject = $subject
    $mail.SubjectEncoding = [System.Text.Encoding]::UTF8
    $mail.Body = $htmlBody
    $mail.BodyEncoding = [System.Text.Encoding]::UTF8
    $mail.IsBodyHtml = $true

    $smtp.Send($mail)
    Write-Log "mail sent to $toAddress"
    $mail.Dispose()
}
catch {
    $ex = $_.Exception
    $detail = $ex.Message
    while ($ex.InnerException) {
        $ex = $ex.InnerException
        $detail += " <- " + $ex.Message
    }
    Write-Log ("ERROR sending mail: " + $detail)
    throw
}

Write-Log "nikkei-news-mailer $Mode done"

# SIG # Begin signature block
# MIIFpAYJKoZIhvcNAQcCoIIFlTCCBZECAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQH8w7YFlLCE63JNLG
# KX7zUQIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCClfz6rJQ949ClH
# zkL5dSvb20y9T/SRCrPxfwqDkGtBiaCCAxQwggMQMIIB+KADAgECAhAZJRYA597D
# lUpVWTyk/jn3MA0GCSqGSIb3DQEBCwUAMCAxHjAcBgNVBAMMFVBNVmF1bHQgTG9j
# YWwgU2NyaXB0czAeFw0yNjA3MjQwMDEyNTRaFw0zMTA3MjQwMDIyNTRaMCAxHjAc
# BgNVBAMMFVBNVmF1bHQgTG9jYWwgU2NyaXB0czCCASIwDQYJKoZIhvcNAQEBBQAD
# ggEPADCCAQoCggEBANOsGWEVqSxhSUo3Yv4xGOXgDZZEebdymXrNhOBFQ5CvYoLx
# YUn+wR1Px0hoGPrpkDn00Y7GnJEf3Eet2riKnw5HozBQsEtJBh2xWemIkFxJRyDg
# 8DPmPtlaP8afisOyh+xlBbpesx3211nAZyYQcLabdo9JVO6X928/RQardmW2Z3bu
# M206n5ivO/10InsE4DWfvVV+v+akrddp6m7KeTDgMqvmgJloqPLkuGVNYr8in60Z
# pDqkh7JdQvkZt6e57nCp0Wfzth4sKblcmfk0z+1hs2PPFI6xn6phv4/yb/GljSuq
# 6Dz+Pj/jRR1aEy/zevHoYplKEbltdSuBE8lzq4UCAwEAAaNGMEQwDgYDVR0PAQH/
# BAQDAgeAMBMGA1UdJQQMMAoGCCsGAQUFBwMDMB0GA1UdDgQWBBShSWdyeewpGMlk
# MK7EmC8ESdCIYTANBgkqhkiG9w0BAQsFAAOCAQEAzS3MNsfLAnXxO60lPLYUAPZi
# mpFNutUI5EMXlFb2m8+VAoDuIvOwBn8/L2k3BPfDGbA8Pwh0axvzxhjwCvmof1Th
# L2eJ0WaOCBYETcaNS2deWKQs7m/KugyshAZrlacXU/LgbCYI4v9sRS4Qd5Vp8LWu
# MUBbGftMat7pTffx6nMN1GD0zAsVAGSNFUoUzF3ePTiT7scjo/iM/ycsduzFAoJb
# Ki5MhwAcARQqcFLc+b+voH6Shi++EUtyPUXlDnPKTob30SUP+M/wbShZcZEoXCHm
# yxYCsCFoiTK+UzeY38qwDf96wCsK90+WFe6yT0HHDCYBmzQZUUZlEPBNiJ2Y6zGC
# AeYwggHiAgEBMDQwIDEeMBwGA1UEAwwVUE1WYXVsdCBMb2NhbCBTY3JpcHRzAhAZ
# JRYA597DlUpVWTyk/jn3MA0GCWCGSAFlAwQCAQUAoIGEMBgGCisGAQQBgjcCAQwx
# CjAIoAKAAKECgAAwGQYJKoZIhvcNAQkDMQwGCisGAQQBgjcCAQQwHAYKKwYBBAGC
# NwIBCzEOMAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEIIjOxeSRiNoDyGE6
# dZpaAOJT4FQXkg/LOxhQWQ19gA7JMA0GCSqGSIb3DQEBAQUABIIBAHsdH8vzujJc
# Yy772MD/MKonKDisAJJe+Y9gFQhaZdQncg+fcx0uo71Q4Hghye4ORMVXuV2T0HFY
# F2uUzRecddjuaoW80kcuP0y92HfsDTpD8fcdqNwqa52OR8l1dHDSqY6F8eiFDbr/
# P8Ly/RZtLZXI7RBMV0dTz+b8ArTjljgfqFPCZpbIPadqgMh/MNyqXEEwcVm/ReQj
# uuDSvjA/frIh4nl2+3dwFr/8U4aoYK5h7NZ4+5T5Kabvt3yWJgaULgHoxWqXbqCU
# BzlHROAD9N0XeGQOR/qedeAEbJGiw3U56y89txyxRBBMYdFgmgd4kNpI/qanB2mo
# V6xS8Tt1MdM=
# SIG # End signature block
