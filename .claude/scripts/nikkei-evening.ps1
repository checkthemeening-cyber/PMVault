Set-Location "C:\Users\check\PMVault"
$logFile = "C:\Users\check\PMVault\.claude\scripts\logs\nikkei-evening-$(Get-Date -Format 'yyyyMMdd').log"
New-Item -ItemType Directory -Force (Split-Path $logFile) | Out-Null
"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] nikkei-news evening 開始" | Tee-Object -FilePath $logFile -Append
claude --dangerously-skip-permissions -p "スキル nikkei-news を evening モードで実行してください" 2>&1 | Tee-Object -FilePath $logFile -Append
"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] nikkei-news evening 完了" | Tee-Object -FilePath $logFile -Append
