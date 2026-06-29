Set-Location "C:\Users\check\PMVault"
$logFile = "C:\Users\check\PMVault\.claude\scripts\logs\nikkei-monthly-" + (Get-Date -Format 'yyyyMM') + ".log"
New-Item -ItemType Directory -Force (Split-Path $logFile) | Out-Null
("[" + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + "] nikkei-news monthly start") | Out-File -FilePath $logFile -Append -Encoding utf8
& "C:\Users\check\.local\bin\claude.exe" --dangerously-skip-permissions -p "Execute the nikkei-news skill in monthly mode" 2>&1 | Out-File -FilePath $logFile -Append -Encoding utf8
("[" + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + "] nikkei-news monthly done. exit=" + $LASTEXITCODE) | Out-File -FilePath $logFile -Append -Encoding utf8
