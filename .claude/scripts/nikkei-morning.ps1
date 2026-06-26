Set-Location "C:\Users\check\PMVault"
$logFile = "C:\Users\check\PMVault\.claude\scripts\logs\nikkei-morning-$(Get-Date -Format 'yyyyMMdd').log"
New-Item -ItemType Directory -Force (Split-Path $logFile) | Out-Null
"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] nikkei-news morning 開始" | Tee-Object -FilePath $logFile -Append
claude --dangerously-skip-permissions -p "スキル nikkei-news を morning モードで実行してください" 2>&1 | Tee-Object -FilePath $logFile -Append
"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] nikkei-news morning 完了" | Tee-Object -FilePath $logFile -Append
